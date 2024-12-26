import random

def generate_test_case():
    # Randomize N (number of orders) and K (number of vehicles)
    N = random.randint(0, 50)  # Large values close to the upper limit
    K = random.randint(0, 10)    # Large values close to the upper limit

    # Generate orders: each order has quantity d(i) and cost c(i)
    orders = [(random.randint(1, 100), random.randint(1, 100)) for _ in range(N)]
    total_order_demand = sum(d for d, _ in orders)  # Total demand from all orders
    total_order_cost = sum(c for _, c in orders)  # Total cost from all orders

    # Generate vehicles: each vehicle has low-bound c1(k) and up-bound c2(k)
    vehicles = []
    total_vehicle_capacity = 0  # Total vehicle capacity

    # To ensure feasible solution, we make sure the total capacity is enough to serve all orders
    for _ in range(K):
        min_capacity = random.randint(1, 100)  # Vehicle's minimum capacity
        max_capacity = random.randint(min_capacity, 200)  # Vehicle's maximum capacity
        vehicles.append((min_capacity, max_capacity))
        total_vehicle_capacity += max_capacity  # Sum up total vehicle capacity

    # If the total vehicle capacity is less than total order demand, adjust vehicle capacities
    if total_vehicle_capacity < total_order_demand:
        # Increase the capacities of the vehicles to make sure the total vehicle capacity is enough
        diff = total_order_demand - total_vehicle_capacity
        for i in range(K):
            min_capacity, max_capacity = vehicles[i]
            # Add additional capacity to each vehicle
            additional_capacity = min(diff, 200 - max_capacity)
            vehicles[i] = (min_capacity, max_capacity + additional_capacity)
            diff -= additional_capacity
            total_vehicle_capacity += additional_capacity
            if diff <= 0:
                break

    # Combine everything into a test case
    test_case = []
    test_case.append(f"{N} {K}")
    for d, c in orders:
        test_case.append(f"{d} {c}")
    for c1, c2 in vehicles:
        test_case.append(f"{c1} {c2}")

    # Ensure the total cost of the served orders is greater than 0
    # If it's not, adjust the order costs randomly to ensure a positive total cost
    if total_order_cost == 0:
        for i in range(N):
            demand, cost = orders[i]
            orders[i] = (demand, random.randint(1, 100))  # Assign new random cost
        total_order_cost = sum(c for _, c in orders)  # Recalculate total cost

    test_case = []
    test_case.append(f"{N} {K}")
    for d, c in orders:
        test_case.append(f"{d} {c}")
    for c1, c2 in vehicles:
        test_case.append(f"{c1} {c2}")

    return "\n".join(test_case)


def generate_test_cases(num_cases=10):
    test_cases = []
    for _ in range(num_cases):
        test_cases.append(generate_test_case())
    return test_cases


# Generate 10 test cases and save them to files
test_cases = generate_test_cases()
for i, test_case in enumerate(test_cases, 1):
    with open(f"test_case_{i}.txt", "w") as f:
        f.write(test_case)

print("10 test cases generated and saved as test_case_1.txt to test_case_10.txt")
