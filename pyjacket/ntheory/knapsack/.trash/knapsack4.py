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

class Knapsack:

    State = tuple[list, Collection]

    def __init__(self, items: Collection, capacities: list[float]):
        self.items = Collection(items)
        self.capacities = capacities

        # Cache variables
        self._V = {}
        self._P = {}

    def solve(self):
        # Initial state
        storage = tuple((0, 0) for _ in self.capacities) # v, w
        items = self.items
        state = (storage, items)

        # Compute the solution
        self.V(state)

        # Traverse the solution to find how to distribute items across containers
        distribution = self.gather(state)  
        return distribution

    def V(self, state):
        """Value of a state"""
        if state not in self._V:
            storage, items = state
            if not items:
                self._V[state] = sum(v for v, w in storage)
            else:
                self._V[state] = max(self.V(self.T(state, a)) for a in self.actions(state))
            
        return self._V[state]
        
    def W(self, state):
        """Weight of a state"""
        storage, items = state
        return sum(w for v, w in storage)

    def P(self, state):
        """Action to make at state"""
        if state not in self._P:
            self._P[state] = max(self.actions(state), key=lambda a: self.V(self.T(state, a)))
            
        return self._P[state]

    def T(self, state: State, action):
        """Modify state by action"""
        storage, remaining = state
        storage = list(storage)

        x = next(iter(remaining))
        dv, dw = x

        # Exclude item
        if not action:
            # storage = storage.copy()
            remaining = remaining.remove(x)

        # Include item in container i
        else:
            i_container = action-1
            v, w = storage[i_container] 
            storage[i_container] = (v+dv, w+dw)

            remaining = remaining.sub(x)

        state = tuple(storage), remaining
        return state

    def actions(self, state):
        """Actions to choose from"""
        r = [0]  # exclude this item

        # include item in container i
        rem_items = state[1] # get the remaining items from state
        v, w = next(iter(rem_items))
        for i_container, capacity in enumerate(self.capacities, 1):
            if self.W(state) + w <= capacity:
                r.append(i_container)

        return r
    
    def gather(self, state):
        print(f"\n== Traceback:")
        allocation = [Collection() for _ in self.capacities]



        while state[1]:
            # print(f"{allocation = }")
            # print(f"{state = }")
            a = self.P(state)
            items = state[1]
            x = next(iter(items))

            if a:
                allocation[a-1] = allocation[a-1].add(x)

            # print(f"{a = }")
            state = self.T(state, a)
            # print(state)

        return allocation


def knapsack(items, capacities):
    return Knapsack(items, capacities).solve()

def main():
    items = Collection({
        (2, 1): 4,
        (4, 2): 4,
        (5, 2): 4,
        (1, 1): 4,
        (3, 2): 4,
    })
    
    solution = knapsack(items, [6, 3])
    print(solution)
    return solution



if __name__ == "__main__":
    main()