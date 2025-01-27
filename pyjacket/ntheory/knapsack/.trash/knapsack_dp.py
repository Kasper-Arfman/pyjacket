import numpy as np

     #    i < I
v = [10, 30, 25, 50, 35, 30, 15, 40, 30, 35, 45, 10, 20, 30, 25]
w = [48, 30, 42, 36, 36, 48, 42, 42, 36, 24, 30, 30, 42, 36, 36]
W = 100
I = len(v)

if True:
    # Base case solutions
    # - zero capacity: zeros (because you can't carry anything)
    knap = np.zeros((I, W+1))
    # - first item: v[0] if you can carry it, else 0
    knap[0, w[0]:] = v[0]

    # Build solutions from the ground up, starting with low capacity and few items.
    for i in range(1, I):
        # If the capacity is smaller than the weight of the item
        knap[i, :w[i]] = knap[i-1, :w[i]]
        
        # Otherwise, consider all capacities in (w, W)
        for c in range(w[i], W+1):
            knap[i, c] = max(
                v[i] + knap[i-1, c - w[i]],  # include item
                knap[i-1, c]  # exclude item
            )

    print(knap[-1, -1])
    print(f"Table approach: {knap.size} computations")

pass

# now we try the same, but recursively
# - advantage: we only compute states once we need them
# - disadvantage: we need to remember a lot of stuff

def solve():
    v = [10, 30, 25, 50, 35, 30, 15, 40, 30, 35, 45, 10, 20, 30, 25]
    w = [48, 30, 42, 36, 36, 48, 42, 42, 36, 24, 30, 30, 42, 36, 36]

    w, v = zip(*sorted(zip(w, v), reverse=False))
    print(v, w)

    w_cum = np.cumsum(w)
    v_cum = np.cumsum(v)
    print(w_cum)
    print(v_cum)

    W = 100
    I = len(v) - 1  # last item

    counter = 0
    _knap = {}
    def knap(i, c):
        if (i, c) not in _knap:
            nonlocal counter; counter+=1

            # Base case:
            if not c:  # no capacity (left)
                _knap[i, c] = 0
            elif not i: # no items (left)
                _knap[i, c] = v[0] if c >= W else 0
            elif w_cum[i] <= c: # can carry everything else
                _knap[i, c] = v_cum[i]

            # Recursion
            else:
                options = [knap(i-1, c)]  # exclude
                if w[i] <= c:
                    options += [v[i] + knap(i-1, c - w[i])]  # include
                _knap[i, c] = max(options)

        return _knap[i, c]

    knap(I, W)
    print(_knap[I, W])
    print(f"Recursive approach: {counter} function calls")

solve()