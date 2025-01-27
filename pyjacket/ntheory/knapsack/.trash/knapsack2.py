import numpy as np
from collections import Counter

class Collection(Counter):

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
    # We will evaluate for each state:
    value = {}   # state -> value
    weight = {}  # stae -> weight
    
    def eval_state(state: Collection, rem: Collection, v_sum=0, w_sum=0):
        print(f"{state}, {rem}, {v_sum = }, {w_sum = }")

        if state in value and state in weight:
            return value[state], weight[state]

        # Base case: there are no items
        if not rem:
            value[state] = 0
            weight[state] = 0
            return value[state], weight[state]

        # Base case: I can carry all items. 
        if w_sum + sum(n*w for (_, w), n in rem.items()) <= capacity:
            value[state] = v_sum + sum(n*v for (v, _), n in rem.items())
            weight[state] = w_sum + sum(n*w for (_, w), n in rem.items())
            return value[state], weight[state]

        # Otherwise, this state is worth as much as the best one it could become
        v, w = max(eval_state(state.add(x), rem.sub(x), v_sum+x[0], w_sum+x[1]) for x in rem)
        value[state] = v
        weight[state] = w
        return

    eval_state(Collection(), rem=items)
    
    # find the state that has the highest value
    subset = max(value, key=value.get)

    return subset, value[subset], weight[subset]







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

    capacity = 5

    solution = knapsack(items, capacity)
    print(solution)
    return solution



if __name__ == "__main__":
    main()