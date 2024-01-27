import numpy as np

def _knapsack_LUT(values, weights, W):
    """Generate the LUT to find the maximum value that can be carried.
    """
    LUT = np.zeros((len(values), W+1))
    LUT[0, weights[0]:] = values[0]
    for i, (val, wt) in enumerate(zip(values[1:], weights[1:]), 1):
        LUT[i, :wt] = LUT[i-1, :wt]  # item weight exceeds capacity
        for j in range(wt, W+1):
            LUT[i, j] = max(
                val + LUT[i-1, j - wt],
                LUT[i-1, j]
            )
    return LUT 
  
def _gen_knapsack_solutions(values, weights, W): 
    LUT = _knapsack_LUT(values, weights, W)
    
    print(LUT)
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
                r = r.copy() + [(wt, val)]
                yield from recurse(i-1, j - wt, r)
    
    
    return recurse(I-1, J-1, [])


def knapsack_maxval(values, weights, W):
    """Given a set of items, their cost and their weights,
    Given a maximum carrying capacity W
    
    return the maximal price that can be produced by a subset of items, 
    such that their collective weight does not exceed W
    """
    return _knapsack_LUT(values, weights, W)[-1, -1]

def knapsack_solution(values, weights, W):
    """Given a set of items, their cost and their weights,
    Given a maximum carrying capacity W
    
    return a subset of items that maximizes value, 
    such that their collective weight does not exceed W
    """
    return next(_gen_knapsack_solutions(values, weights, W))

def knapsack_solutions(values, weights, W):
    """Given a set of items, their cost and their weights,
    Given a maximum carrying capacity W
    
    return all subsets of items that maximizes value, 
    such that their collective weight does not exceed W
    """
    return list(_gen_knapsack_solutions(values, weights, W))
    
    
    

    
    
    
    

    