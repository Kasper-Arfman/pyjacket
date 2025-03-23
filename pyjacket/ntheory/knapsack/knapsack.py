import numpy as np
np.set_printoptions(linewidth=2000, threshold=500, edgeitems=5000)

""" Given an assortment of items with weights and values, and a capacity C ...

A) ... find the maximum value obtainable from a subset whose weight does not exceed C

B) ... and find a subset that produces this optimum


TODO: check if I need to add one extra row and column to the integer version.
"""

def integer_knapsack(v: list, w: list, C: int):
    """ find the maximum value obtainable without exceeding the weight limit.

    INPUTS
    v (list[int]): Values of the items
    w (list[int]): Weights of the items
    C (int): Weight limit

    APPROACH
    Solve using dynamic programming. This entails solving many variants of the same problem, but at each step reducing the size of the input.
    The input gets smaller and smaller until the solution becomes trivial. This is a bottom-up approach: 
    solve trivial problems first and using their solutions to solve more complex variants.

    The key is realising that for each item there are only two choices: include or exclude.
    
    N.B. This function finds the maximum value (problem A), not the set of items that produces it (problem B).
    But this information can be extracted from the output of this function.
    """

    # Let result[i, c] be the solution if you had only the first i items, and a capacity of c
    I = len(v) - 1  # index of the last item
    result = np.zeros((I+1, C+1), dtype=np.uint32)

    # Base case: only one item to consider. Choice is simple: include if you have enough capacity
    result[0, w[0]:] = v[0]

    # Iterative step: Build solutions from the ground up, starting with low capacity and few items.
    for i in range(1, I+1):

        # - check if you can carry this item at all. If not (w[i] > c), then you cannot include it:
        result[i, :w[i]] = result[i-1, :w[i]]
        
        # - consider two cases: exclude or include the item
        for c in range(w[i], C+1):
            result[i, c] = max(
                result[i-1, c],  # exclude
                v[i] + result[i-1, c - w[i]],  # include
            )
    return result


import numpy as np

def integer_knapsack_traceback(v, w, C, result):
    """Finds the subset of items that produce the maximum value.

    Parameters:
    v (list[int]): Values of the items
    w (list[int]): Weights of the items
    C (int): Weight limit
    result (np.array): The DP table from integer_knapsack function

    Returns:
    list[int]: Indices of items included in the optimal subset
    """

    I = len(v) - 1  # Last item's index
    c = C  # Start at full capacity
    selected_items = []

    for i in range(I, -1, -1):  # Work backwards
        if i == 0:
            if result[i, c] > 0:  # First item was included
                selected_items.append(i)
        elif result[i, c] != result[i - 1, c]:  # Item was included
            selected_items.append(i)
            c -= w[i]  # Reduce remaining capacity
            if c <= 0:
                break  # Stop early if no capacity remains

    selected_items.reverse()  # Optional: return items in order of input
    return selected_items




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
    
    # w, v = zip(*sorted(zip(w, v)))  # small performance boost


    # print(w)

    result = integer_knapsack(v, w, C)

    subset = integer_knapsack_traceback(v, w, C, result)

    print(f"\n{v = }")
    print(f"{w = }")
    print(f"{C = }")

    print(f"result:\n{result}")

    print(f"The maximum value, constrained to a weight limit of {C}, is {result[-1, -1]}")

    print(f"\nSubset that produces this maximum:")
    print(f"v = {[v[i] for i in subset]}")
    print(f"w = {[w[i] for i in subset]}")





    # print(f"{q.T}\nMax value: {q[-1, -1]}")

    # q = knapsack(v, w, C)
    # print(f"Max value: {q}")

    
if __name__ == '__main__':
    main()