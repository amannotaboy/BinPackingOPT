import random
import math
import time
import os

class SimulatedAnnealing:
    def __init__(self, orders, vehicles, initial_temp, cooling_rate, time_limit):
        self.orders = orders  
        self.vehicles = vehicles  
        self.initial_temp = initial_temp
        self.cooling_rate = cooling_rate
        self.time_limit = time_limit  
        self.best_solution = None
        self.best_cost = 0

    def initialize_solution(self):
        solution = [-1] * len(self.orders)
        for i, (d, _) in enumerate(self.orders):
            for v, (c1, c2) in enumerate(self.vehicles):
                current_quantity = sum(self.orders[j][0] for j in range(len(solution)) if solution[j] == v)
                if current_quantity + d <= c2:
                    solution[i] = v
                    break
        return solution

    def is_feasible(self, solution):
        for v in range(len(self.vehicles)):
            c1, c2 = self.vehicles[v]
            total_quantity = sum(self.orders[i][0] for i in range(len(solution)) if solution[i] == v)
            if total_quantity < c1 or total_quantity > c2:
                return False
        return True

    def calculate_cost(self, solution):
        total_cost = sum(self.orders[i][1] for i in range(len(solution)) if solution[i] != -1)
        return total_cost

    def get_neighbor(self, solution):
        neighbor = solution[:]
        i = random.randint(0, len(solution) - 1)

        j = random.randint(0, len(solution) - 1)
        if i != j:
            neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
        return neighbor

    def simulated_annealing(self):
        start_time = time.time()
        temp = self.initial_temp
        current_solution = self.initialize_solution()
        current_cost = self.calculate_cost(current_solution) if self.is_feasible(current_solution) else 0
        self.best_solution = current_solution[:]
        self.best_cost = current_cost

        while temp > 1 and (time.time() - start_time) < self.time_limit:
            neighbor = self.get_neighbor(current_solution)
            if self.is_feasible(neighbor):
                neighbor_cost = self.calculate_cost(neighbor)
                delta = neighbor_cost - current_cost

                if delta > 0 or random.random() < math.exp(delta / temp):
                    current_solution = neighbor[:]
                    current_cost = neighbor_cost

                    if current_cost > self.best_cost:
                        self.best_solution = current_solution[:]
                        self.best_cost = current_cost

            temp *= self.cooling_rate

        return current_solution, current_cost 

input_file = "input.txt"
output_file = "output.txt"

with open(input_file, "r") as f:

    n, k = map(int, f.readline().split())
    orders = [tuple(map(int, f.readline().split())) for _ in range(n)]              
    vehicles = [tuple(map(int, f.readline().split())) for _ in range(k)]

    sa = SimulatedAnnealing(orders, vehicles, initial_temp=10000, cooling_rate=0.85, time_limit=120)  
    current_solution, current_cost = sa.simulated_annealing()

with open(output_file, "w") as f:
    f.write(str(current_cost) + "\n")

print(f"Total cost has been written to '{output_file}'.")

# with open("all_outputs1.txt", "w") as output_file:
        
#     input_directory = "./TestFrom(0-250, 0-25)"  

#     for input_filename in os.listdir(input_directory):
#         if input_filename.endswith(".txt"): 
#             file_path = os.path.join(input_directory, input_filename)

#             with open(file_path, "r") as f:
#                 n, k = map(int, f.readline().split())
#                 orders = [tuple(map(int, f.readline().split())) for _ in range(n)]
#                 vehicles = [tuple(map(int, f.readline().split())) for _ in range(k)]

#             sa = SimulatedAnnealing(orders, vehicles, initial_temp=10000, cooling_rate=0.85, time_limit=120)  
#             current_solution, current_cost = sa.simulated_annealing()
                
#             output_file.write(f"Total cost of served orders for {input_filename}: {current_cost}\n")
#             print(f"Output for {input_filename} has been successfully appended to 'all_outputs.txt'.")

# print("All results have been written to 'all_outputs1.txt'.")