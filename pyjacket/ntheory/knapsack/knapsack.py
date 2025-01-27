import numpy as np
np.set_printoptions(linewidth=2000, threshold=500, edgeitems=5000)

"""
TODO: check if I need to add one extra row and column to the integer version.
"""

def integer_knapsack(v, w, C):
    I = len(v) - 1  # last item
    # Base case solutions
    # - zero capacity: zeros (because you can't carry anything)
    value = np.zeros((I+1, C+1), dtype=np.uint32)
    # - first item: v[0] if you can carry it, else 0
    value[0, w[0]:] = v[0]

    # Build solutions from the ground up, starting with low capacity and few items.
    for i in range(1, I+1):
        # If the capacity is smaller than the weight of the item
        value[i, :w[i]] = value[i-1, :w[i]]
        
        # Otherwise, consider all capacities in (w, W)
        for c in range(w[i], C+1):
            value[i, c] = max(
                v[i] + value[i-1, c - w[i]],  # include item
                value[i-1, c]  # exclude item
            )
    return value

def knapsack(v, w, C):
    w_cum = np.cumsum(w)
    v_cum = np.cumsum(v)
    I = len(v) - 1  # last item

    _value = {}
    def value(i, c):
        if (i, c) not in _value:
            # BASE CASE: no capacity
            if c <= 0:
                _value[i, c] = 0
            # BASE CASE: no items (left)
            if i <= 0: 
                _value[i, c] = v[0] if w[0] <= c else 0
            # BASE CASE: can carry everything (left)
            elif w_cum[i] <= c: 
                _value[i, c] = v_cum[i]

            else:
                options = [value(i-1, c)]  # exclude
                if w[i] <= c:
                    options += [v[i] + value(i-1, c - w[i])]  # include
                _value[i, c] = max(options)

        return _value[i, c]
    value(I, C)  # build the cache

    # table = np.zeros((I+1, C+1), dtype=np.uint32)
    # for i in range(I+1):
    #     for c in range(C+1):
    #         table[i, c] = value(i, c)
    # print(table.T)

    def traceback(c=C):
        """Find the policy based on the value network"""
        result = tuple()
        for i in range(I, -1, -1):
            if value(i, c) != value(i-1, c):
                c -= w[i]
                result = (i, *result)
        return result
    selection = traceback()
    val = sum(v[i] for i in selection)
    wt = sum(w[i] for i in selection)
    return selection, val, wt

def _gen_knapsack_solutions(values, weights, LUT: np.ndarray): 
    I, J = LUT.shape

    def recurse(i, j, r: list):
        val = values[i]
        wt = weights[i]
        
        # base case
        if LUT[i, j] == 0:
            yield r
        
        else:
            # You can maximize by excluding this item
            if i>0 and LUT[i, j] == LUT[i-1, j]:
                yield from recurse(i-1, j, r)
                
            #  You can maximize by including this item
            if i==0 or (j>=wt and LUT[i, j] == val + LUT[i-1, j - wt]):
                r = r.copy() + [(i, wt, val)]
                yield from recurse(i-1, j - wt, r)
    
    
    return recurse(I-1, J-1, [])

def main():
    v = [10, 30, 25, 50, 35, 30, 15, 40, 30, 35, 45, 10, 20, 30, 25]
    w = [48, 30, 42, 36, 36, 48, 42, 42, 36, 24, 30, 30, 42, 36, 36]
    C = 100

    v = [ 1,  6, 18, 22, 28]
    w = [ 1,  2,  5,  6, 7]
    C = 11
    
    w, v = zip(*sorted(zip(w, v)))  # small performance boost

    q = integer_knapsack(v, w, C)
    print(f"{q.T}\nMax value: {q[-1, -1]}")

    q = knapsack(v, w, C)
    print(f"Max value: {q}")

    
if __name__ == '__main__':
    main()