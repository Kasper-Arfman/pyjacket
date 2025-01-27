"""
We are given a few containers, each having their own capacity.

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
        self._V = {}
        self._P = {}
        self._T = {}

    def solve(self):
        # Initial state
        storage = tuple((0, 0) for _ in self.capacities) # v, w
        remaining = self.items.copy()
        state = (storage, remaining)

        # Compute the solution
        self.V(state)

        # print the actions
        for state in self._P:
            print(state, self._P[state])

        # Traverse the solution to find how to distribute items across containers
        distribution = self.gather(state) 
        for k in distribution:
            print(k)

        for k in distribution:
            print(f"value: {sum(v for v, w in k)}, weight: {sum(w for v, w in k)}")

        return distribution

    def V(self, state):
        """Value of a state"""
        if state not in self._V:
            # print(state)
            storage, remaining = state
            if not remaining:
                self._V[state] = sum(v for v, w in storage)
            else:
                self._V[state] = max(self.V(self.T(state, a)) for a in self.actions(state))


            value = self._V[state]
            # if value >= 200:
            print(state[0], value)
        else:
            # print('cached', state)
            pass

        return self._V[state]
        
    # def W(self, state):
    #     """Weight of a state"""
    #     storage, items = state
    #     return sum(w for v, w in storage)

    def P(self, state):
        """Action to make at state"""
        if state not in self._P:
            self._P[state] = max(self.actions(state), key=lambda a: self.V(self.T(state, a)))
            
        return self._P[state]
    
    # def P(self, state):
    #     """Action to make at state"""
    #     if state not in self._P:

    #         while True:
    #             a = self._P[state] = max(self.actions(state), key=lambda a: self.V(self.T(state, a)))

    #             new_state = self.T(state, a)

    #             if new_state == state:
    #                 break

            
    #     return self._P[state]

    def T(self, state: State, action):
        """Modify state by action"""
        if (state, action) not in self._T:
            storage, remaining = state
            remaining = remaining.copy()
        
            item = next(iter(remaining))
        
            # Exclude item
            if action==0:
                # storage = storage.copy()
                remaining = remaining.remove(item)

            # Include item in container i
            elif action > 0:
                i_container = action-1

                # - put item in storage i
                storage = list(storage)
                v, w = storage[i_container] 
                dv, dw = item
                storage[i_container] = (v+dv, w+dw)
                storage = tuple(storage)

                remaining = remaining.sub(item)

            self._T[state, action] = (storage, remaining)
        else:
            # print('cached T:', state, self._T[state, action])
            pass

        return self._T[state, action]  # state

    def actions(self, state):
        """Actions to choose from"""
        storage, remaining = state

        r = [0]  # exclude this item

        # include item in container i
        v, w = next(iter(remaining))
        for i, capacity in enumerate(self.capacities):
            if storage[i][1] + w <= capacity:
                r.append(i+1)

        return r
    
    def gather(self, state):
        print(f"\n== Traceback:")
        allocation = [Collection() for _ in self.capacities]



        while remaining := state[1]:
            a = self.P(state)
            x = next(iter(remaining))

            if a:
                allocation[a-1] = allocation[a-1].add(x)

            state = self.T(state, a)

        return allocation


def knapsack(items, capacities):
    return Knapsack(items, capacities).solve()

    

def main():
    w = [48, 30, 42, 36, 36, 48, 42, 42, 36, 24, 30, 30, 42, 36, 36]
    v = [10, 30, 25, 50, 35, 30, 15, 40, 30, 35, 45, 10, 20, 30, 25]
    capacity = [100, 100, 100]  ##, 100, 100]
    
    items = Collection(zip(v, w))

    

    solution = knapsack(items, capacity)
    # print(solution)
    
    return solution

"""
Total packed value: 395.0
Bin  0

Item 3 - weight: 36  value: 50
Item 13 - weight: 36  value: 30
Packed bin weight: 72
Packed bin value: 80

Bin  1

Item 5 - weight: 48  value: 30
Item 7 - weight: 42  value: 40
Packed bin weight: 90
Packed bin value: 70

Bin  2

Item 1 - weight: 30  value: 30
Item 10 - weight: 30  value: 45
Item 14 - weight: 36  value: 25
Packed bin weight: 96
Packed bin value: 100

Bin  3

Item 2 - weight: 42  value: 25
Item 12 - weight: 42  value: 20
Packed bin weight: 84
Packed bin value: 45

Bin  4

Item 4 - weight: 36  value: 35
Item 8 - weight: 36  value: 30
Item 9 - weight: 24  value: 35
Packed bin weight: 96
Packed bin value: 100

Total packed weight: 438
"""

if __name__ == "__main__":
    main()