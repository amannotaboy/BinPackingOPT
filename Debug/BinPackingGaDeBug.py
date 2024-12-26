import random
import time

class GeneticAlgorithm:
    def __init__(self, orders, vehicles, population_size, generations, mutation_rate, time_limit):
        self.orders = orders
        self.vehicles = vehicles
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.num_orders = len(orders)
        self.num_vehicles = len(vehicles)
        self.time_limit = time_limit

    def initialize_population(self):
        population = []
        for _ in range(self.population_size):
            individual = [-1] * self.num_orders 
            
            orders_sorted = sorted(range(self.num_orders), key=lambda i: self.orders[i][0], reverse=True) 
            vehicle_loads = [0] * self.num_vehicles 
            
            for order_index in orders_sorted:
                for vehicle_index in range(self.num_vehicles):
                    if vehicle_loads[vehicle_index] + self.orders[order_index][0] <= self.vehicles[vehicle_index][1]:
                        individual[order_index] = vehicle_index
                        vehicle_loads[vehicle_index] += self.orders[order_index][0]
                        break
            
            if self.is_feasible(individual):  # Kiểm tra tính khả thi của cá thể
                population.append(individual)
            else:
                continue  # Nếu không khả thi, tạo lại cá thể mới
        return population


    def fitness(self, individual):
        total_cost = 0
        penalty = 0
        for k in range(self.num_vehicles):
            vehicle_orders = [i for i, v in enumerate(individual) if v == k]
            load = sum(self.orders[i][0] for i in vehicle_orders)
            if self.vehicles[k][0] <= load <= self.vehicles[k][1]:
                total_cost += sum(self.orders[i][1] for i in vehicle_orders)
            else:
                penalty += abs(load - self.vehicles[k][0]) if load < self.vehicles[k][0] else abs(load - self.vehicles[k][1])
        return total_cost - penalty

    def select_parents(self, population, fitness_scores):
        total_fitness = sum(fitness_scores)
        probabilities = [f / total_fitness for f in fitness_scores]
        parent1 = random.choices(population, probabilities)[0]
        parent2 = random.choices(population, probabilities)[0]
        return parent1, parent2

    def crossover(self, parent1, parent2):
        point = random.randint(1, self.num_orders - 1)
        child1 = parent1[:point] + parent2[point:]
        child2 = parent2[:point] + parent1[point:]
        return child1, child2

    def mutate(self, individual):
        for i in range(self.num_orders):
            if random.random() < self.mutation_rate:
                individual[i] = random.choice(range(self.num_vehicles))
        return individual

    def is_feasible(self, individual):
        for k in range(self.num_vehicles):
            vehicle_orders = [i for i, v in enumerate(individual) if v == k]    
            load = sum(self.orders[i][0] for i in vehicle_orders)
            if load < self.vehicles[k][0] or load > self.vehicles[k][1]:
                return False
        return True

    def evolve(self):
        start_time = time.time()
        population = self.initialize_population()
        current_solution = None
        current_fitness = float('-inf')
        elitism_count = max(1, self.population_size // 10)

        for generation in range(self.generations):
            elapsed_time = time.time() - start_time
            if elapsed_time > self.time_limit:
                print("Time limit reached.")
                break

            fitness_scores = [self.fitness(ind) for ind in population]

            for i, fitness in enumerate(fitness_scores):
                if fitness > current_fitness and self.is_feasible(population[i]):
                    current_solution = population[i]
                    current_fitness = fitness

            sorted_population = [ind for _, ind in sorted(zip(fitness_scores, population), reverse=True)]
            elites = sorted_population[:elitism_count]

            new_population = elites[:]
            while len(new_population) < self.population_size:
                parent1, parent2 = self.select_parents(population, fitness_scores)
                child1, child2 = self.crossover(parent1, parent2)
                child1 = self.mutate(child1)
                child2 = self.mutate(child2)
                if len(new_population) < self.population_size:
                    new_population.append(child1)
                if len(new_population) < self.population_size:
                    new_population.append(child2)

            population = new_population[:self.population_size]

        return current_solution, current_fitness


input_file = "input.txt"
output_file = "output.txt"

try:
    with open(input_file, "r") as f:
        n, k = map(int, f.readline().strip().split())
        orders = [tuple(map(int, f.readline().strip().split())) for _ in range(n)]
        vehicles = [tuple(map(int, f.readline().strip().split())) for _ in range(k)]

    ga = GeneticAlgorithm(orders, vehicles, population_size=100, generations=100, mutation_rate=0.1, time_limit=20)
    best_solution, best_cost = ga.evolve()

    if best_solution is not None:
        with open(output_file, "w") as f:
            f.write(f"{best_cost}\n")
            for i in range(len(best_solution)):
                f.write(f"Order {i}: Vehicle {best_solution[i]}\n")

        print(f"Best cost: {best_cost} written to '{output_file}'.")
    else:
        print("No solution found.")
except Exception as e:
    print(f"Error reading input or processing the algorithm: {e}")
