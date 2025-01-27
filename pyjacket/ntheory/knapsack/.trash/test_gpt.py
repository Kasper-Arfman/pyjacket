from itertools import product

def knapsack_solver(weights, values, bin_capacities):
    num_items = len(weights)
    num_bins = len(bin_capacities)

    # Helper function to calculate total value and check constraints.
    def is_valid_assignment(assignment):
        bin_weights = [0] * num_bins
        bin_values = [0] * num_bins

        for item, bin_idx in enumerate(assignment):
            if bin_idx >= 0:  # Item is assigned to a bin.
                bin_weights[bin_idx] += weights[item]
                bin_values[bin_idx] += values[item]

        # Check if any bin exceeds its capacity.
        if any(bin_weights[b] > bin_capacities[b] for b in range(num_bins)):
            return False, 0

        # Return the total value of the assignment.
        return True, sum(bin_values)

    # Generate all possible assignments of items to bins (-1 means not assigned).
    all_assignments = product(range(-1, num_bins), repeat=num_items)

    # Try each assignment and keep track of the best one.
    best_value = 0
    best_assignment = None

    for assignment in all_assignments:
        valid, total_value = is_valid_assignment(assignment)
        if valid and total_value > best_value:
            best_value = total_value
            best_assignment = assignment

    return best_value, best_assignment

def main():
    data = {}
    data["weights"] = [48, 30, 42, 36, 36, 48, 42, 42, 36, 24, 30, 30, 42, 36, 36]
    data["values"] = [10, 30, 25, 50, 35, 30, 15, 40, 30, 35, 45, 10, 20, 30, 25]
    data["bin_capacities"] = [100, 100, 100, 100, 100]

    best_value, best_assignment = knapsack_solver(
        data["weights"], data["values"], data["bin_capacities"]
    )

    print(f"Total packed value: {best_value}")
    total_weight = 0

    for b in range(len(data["bin_capacities"])):
        print(f"Bin {b}")
        bin_weight = 0
        bin_value = 0
        for i, bin_idx in enumerate(best_assignment):
            if bin_idx == b:
                print(
                    f"Item {i} weight: {data['weights'][i]} value: {data['values'][i]}"
                )
                bin_weight += data["weights"][i]
                bin_value += data["values"][i]
        print(f"Packed bin weight: {bin_weight}")
        print(f"Packed bin value: {bin_value}\n")
        total_weight += bin_weight

    print(f"Total packed weight: {total_weight}")

if __name__ == "__main__":
    main()
