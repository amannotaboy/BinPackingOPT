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
            individual = [random.choice(range(self.num_vehicles)) for _ in range(self.num_orders)]
            population.append(individual)
        return population

    def fitness(self, individual):
        
        total_cost = 0
        for k in range(self.num_vehicles):
            vehicle_orders = [i for i, v in enumerate(individual) if v == k]
            load = sum(self.orders[i][0] for i in vehicle_orders)
            if self.vehicles[k][0] <= load <= self.vehicles[k][1]:
                total_cost += sum(self.orders[i][1] for i in vehicle_orders)
        return total_cost

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
        time_limit = self.time_limit    

        population = self.initialize_population()
        current_solution = None
        current_fitness = 0


        for generation in range(self.generations):
            if time.time() - start_time > time_limit:
                print("Time limit reached.")
                break

            fitness_scores = [self.fitness(ind) for ind in population]

            for i, fitness in enumerate(fitness_scores):
                if fitness > current_fitness and self.is_feasible(population[i]):
                    current_solution = population[i]
                    current_fitness = fitness
            print("Current best fitness:", current_fitness)

            new_population = []
            while len(new_population) < self.population_size:
                parent1, parent2 = self.select_parents(population, fitness_scores)
                child1, child2 = self.crossover(parent1, parent2)
                child1 = self.mutate(child1)
                child2 = self.mutate(child2)
                new_population.extend([child1, child2])

            population = new_population[:self.population_size]

        return current_solution, current_fitness

with open("all_outputs1_ga.txt", "w") as output_file:
    
    input_directory = "./TestFrom(0-250, 0-25)"  

    for input_filename in os.listdir(input_directory):
        if input_filename.endswith(".txt"): 
            file_path = os.path.join(input_directory, input_filename)

            with open(file_path, "r") as f:
                n, k = list(map(int, f.readline().split()))
                if not (1 <= n <= 1000):
                    raise ValueError(f"Invalid value for n: {n}. It must be between 1 and 1000.")
                if not (1 <= k <= 100):
                    raise ValueError(f"Invalid value for k: {k}. It must be between 1 and 100.")
                orders = []
                for _ in range(n):
                    order = tuple(map(int, f.readline().split()))
                    if not all(1 <= x <= 100 for x in order):  
                        raise ValueError(f"Invalid value in order: {order}. Each component must be between 1 and 1000.")
                    orders.append(order)
    
                vehicles = []
                for _ in range(k):
                    vehicle = tuple(map(int, f.readline().split()))
                    if not (1 <= vehicle[0] <= vehicle[1] <= 1000):  
                        raise ValueError(f"Invalid value in vehicle: {vehicle}. Each component must be between 1 and 1000.")
                    vehicles.append(vehicle)
 
            ga = GeneticAlgorithm(orders, vehicles, population_size=100, generations=200, mutation_rate=0.1, time_limit=120)  
            current_solution, current_cost = ga.evolve()
            
            output_file.write(f"Total cost of served orders for {input_filename}: {current_cost}\n")
            print(f"Output for {input_filename} has been successfully appended to 'all_outputs.txt' with GA.")

print("All results have been written to 'all_outputs.txt'.")