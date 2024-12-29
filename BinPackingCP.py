from ortools.sat.python import cp_model


class VehicleRoutingCPSAT:
    def __init__(self, orders, vehicles):
        self.orders = orders
        self.vehicles = vehicles
        self.num_orders = len(orders)
        self.num_vehicles = len(vehicles)
        self.model = cp_model.CpModel()

        # Decision variables
        self.x = [
            [self.model.NewBoolVar(f"x_{i}_{j}") for j in range(self.num_vehicles)]
            for i in range(self.num_orders)
        ]
        self.vehicle_load = [
            self.model.NewIntVar(0, sum(order[0] for order in orders), f"load_{j}")
            for j in range(self.num_vehicles)
        ]
        self.total_cost = self.model.NewIntVar(0, sum(order[1] for order in orders), "total_cost")

        self.add_constraints()

    def add_constraints(self):
        # Constraint 1: Each order is assigned to exactly one vehicle
        for i in range(self.num_orders):
            self.model.Add(sum(self.x[i][j] for j in range(self.num_vehicles)) == 1)

        # Constraint 2: Vehicle load must respect capacity limits
        for j in range(self.num_vehicles):
            self.model.Add(
                self.vehicle_load[j]
                == sum(self.x[i][j] * self.orders[i][0] for i in range(self.num_orders))
            )
            self.model.Add(self.vehicle_load[j] >= self.vehicles[j][0])  # Min capacity
            self.model.Add(self.vehicle_load[j] <= self.vehicles[j][1])  # Max capacity

        # Objective: Maximize the total cost of served orders
        self.model.Add(
            self.total_cost
            == sum(
                self.x[i][j] * self.orders[i][1]
                for i in range(self.num_orders)
                for j in range(self.num_vehicles)
            )
        )
        self.model.Maximize(self.total_cost)

    def solve(self):
        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = 60  # Limit runtime for larger inputs

        status = solver.Solve(self.model)

        if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            print(f"Total cost of served orders: {solver.Value(self.total_cost)}")
            assignments = []
            for i in range(self.num_orders):
                for j in range(self.num_vehicles):
                    if solver.Value(self.x[i][j]) == 1:
                        assignments.append((i + 1, j + 1))  # Convert to 1-based index
            for order, vehicle in assignments:
                print(f"Order {order} is assigned to Vehicle {vehicle}")
            return assignments, solver.Value(self.total_cost)
        else:
            print("No solution found.")
            return [], None


def read_input():
    # Read input from standard input
    n, k = map(int, input().split())
    orders = [tuple(map(int, input().split())) for _ in range(n)]
    vehicles = [tuple(map(int, input().split())) for _ in range(k)]
    return orders, vehicles


def main():
    # Read input
    orders, vehicles = read_input()

    # Edge case handling
    if len(orders) == 0 or len(vehicles) == 0:
        print("No solution possible. Either no orders or no vehicles.")
        return

    # Solve the problem
    vr_cp_sat = VehicleRoutingCPSAT(orders, vehicles)
    vr_cp_sat.solve()


if __name__ == "__main__":
    main()
