"""
Make a selection of units that maximizes sum(unit.value)
whilst maintaining sum(unit.weight) < capacity
"""

from collections import Counter

class Collection(Counter):
    """Record elements and their frequencies.

    Elements must have positive (nonzero) frequencies, else they are removed.
    """

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self._keep_positive()

    def __add__(self, other):
        return Collection(super().__add__(other))
    
    def __sub__(self, other):
        return Collection(super().__sub__(other))

    def add(self, element):
        return self.__add__(Collection([element]))
    
    def sub(self, element):
        return self.__sub__(Collection([element]))
    
    def remove(self, element):
        self[element] = 0
        return Collection(self)
    
    def __hash__(self):
        keys = tuple(sorted(x for x in self))
        values = tuple(self[k] for k in keys)
        return hash((keys, values))

def knapsack(items: Collection, capacity):
    """You are given a list of valuable items, but you can't carry them all.
    Find the most valuable subset of items that you *can* carry (sum weights < capacity).

    Approach: consider taking each item in the collection
    Base case: if there is nothing to choose from, or we can take everything, easy.
    Otherwise: choose the best state outcome
    """
    # Caching:
    # Intermediate solutions are recorded in the variables below.
    # We can use it as a look-up table when we need to solve the same sub-problem twice.
    policy = {}  # state -> state (which items should I take)
    value = {}   # state -> value
    weight = {}  # state -> weight
    
    def solve(state: Collection, options: Collection, v_sum, w_sum):
        # Cache: have we computed this problem before?
        if state not in policy:
        
            # Base case: there is nothing to select => stop.
            if not options:
                policy[state] = state
                value[state] = v_sum
                weight[state] = w_sum
            
            # Recursive step: choose to include or exclude the next item
            else:
                next_item = next(iter(options))

                # - Exclude the item
                choices = [solve(state, options.remove(next_item), v_sum, w_sum)]

                # - Include the item (if we can carry it)
                v, w = next_item
                if w_sum + w <= capacity:
                    choices += [solve(state.add(next_item), options.sub(next_item), v_sum+v, w_sum+w)]

                # Decide which option is best.
                # - If they give the same value, choose the one with the lowest weight
                p, v, w = max(choices, key=lambda item: (item[0], -item[1]))
                policy[state] = p
                value[state] = v
                weight[state] = w
        
        return policy[state], value[state], weight[state]
            
    subset, subset_value, subset_weight = solve(state=Collection(), options=items, v_sum=0, w_sum=0)
    return subset, subset_value, subset_weight
    

def main():

    items = Collection([
        # value, weight
        (1, 1),
        (1, 1),
        (1, 1),
        (1, 1),
        (2, 2),
        (4, 3),
        (2, 1),
    ])

    capacity = 6

    solution = knapsack(items, capacity)
    print(solution)
    return solution



if __name__ == "__main__":
    main()