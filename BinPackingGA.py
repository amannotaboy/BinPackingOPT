import random
import time
import os

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

            if self.is_feasible(individual):
                population.append(individual)
            else:
                individual = self.repair_individual(individual)
                population.append(individual)
        return population

    def repair_individual(self, individual):
        for i in range(self.num_orders):
            if individual[i] == -1:
                for vehicle_index in range(self.num_vehicles):
                    if self.is_feasible_for_order(i, vehicle_index, individual):
                        individual[i] = vehicle_index
                        break
        return individual

    def is_feasible_for_order(self, order_index, vehicle_index, individual):
        # Kiểm tra xem đơn hàng có thể được giao cho xe này mà không vượt quá khả năng của nó không
        vehicle_load = sum(self.orders[i][0] for i in range(self.num_orders) if individual[i] == vehicle_index)
        new_load = vehicle_load + self.orders[order_index][0]
        return self.vehicles[vehicle_index][0] <= new_load <= self.vehicles[vehicle_index][1]

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

with open("all_outputs1_ga.txt", "w") as output_file:
    
    input_directory = "./TestFrom(0-250, 0-25)"  

    for input_filename in os.listdir(input_directory):
        if input_filename.endswith(".txt"): 
            file_path = os.path.join(input_directory, input_filename)

            with open(file_path, "r") as f:
                n, k = list(map(int, f.readline().split()))
                orders = []
                for _ in range(n):
                    order = tuple(map(int, f.readline().split()))
                    orders.append(order)
    
                vehicles = []
                for _ in range(k):
                    vehicle = tuple(map(int, f.readline().split()))
                    vehicles.append(vehicle)
 
            ga = GeneticAlgorithm(orders, vehicles, population_size=100, generations=1000, mutation_rate=0.1, time_limit=120)  
            current_solution, current_cost = ga.evolve()
            
            output_file.write(f"Total cost of served orders for {input_filename}: {current_cost}\n")
            print(f"Output for {input_filename} has been successfully appended to 'all_outputs.txt' with GA.")

print("All results have been written to 'all_outputs1_ga.txt'.")
