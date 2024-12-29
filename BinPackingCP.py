from ortools.sat.python import cp_model
import os

class VehicleRoutingCP:
    def __init__(self, orders, vehicles):
        self.orders = orders
        self.vehicles = vehicles
        self.num_orders = len(orders)
        self.num_vehicles = len(vehicles)
        
        self.model = cp_model.CpModel()
        
        self.x = []
        for i in range(self.num_orders):
            self.x.append([self.model.NewBoolVar(f"x_{i}_{j}") for j in range(self.num_vehicles)])
        
        self.vehicle_load = [self.model.NewIntVar(0, sum(order[0] for order in orders), f"load_{j}") for j in range(self.num_vehicles)]
        
        self.total_cost = self.model.NewIntVar(0, sum(order[1] for order in orders), "total_cost")
        self.model.Add(self.total_cost == sum(self.x[i][j] * self.orders[i][1] for i in range(self.num_orders) for j in range(self.num_vehicles)))
        
        for i in range(self.num_orders):
            self.model.Add(sum(self.x[i][j] for j in range(self.num_vehicles)) == 1)  
        
        for j in range(self.num_vehicles):
            self.model.Add(self.vehicle_load[j] == sum(self.x[i][j] * self.orders[i][0] for i in range(self.num_orders)))
            self.model.Add(self.vehicle_load[j] >= self.vehicles[j][0]) 
            self.model.Add(self.vehicle_load[j] <= self.vehicles[j][1]) 

    def solve(self):
        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = 120  
        
        status = solver.Solve(self.model)
        
        if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            print(f"Total cost of served orders: {solver.Value(self.total_cost)}")
            for i in range(self.num_orders):
                for j in range(self.num_vehicles):
                    if solver.Value(self.x[i][j]) == 1:
                        print(f"Order {i} is assigned to Vehicle {j}")
            return solver.Value(self.total_cost)
        else:
            print("No solution found.")
            return None 
            
# Thư mục và tệp đầu vào
input_directory = "./TestFrom(0-250, 0-25)"  

with open("all_outputs1_ga.txt", "w") as output_file:
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
 
            # Khởi tạo và giải bài toán
            ga = VehicleRoutingCP(orders, vehicles)  
            total_cost = ga.solve()
            
            if total_cost is not None:
                output_file.write(f"Total cost of served orders for {input_filename}: {total_cost}\n")
            else:
                output_file.write(f"No solution found for {input_filename}\n")

print("All results have been written to 'all_outputs1_ga.txt'.")
