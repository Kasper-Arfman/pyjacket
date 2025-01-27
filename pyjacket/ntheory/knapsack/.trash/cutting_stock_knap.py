import numpy as np
np.set_printoptions(linewidth=200)
from functools import cache

# def knapsack(weights, W):
#     """Generate the LUT to find the maximum value that can be carried.
#     """
#     LUT = np.zeros((len(values), W+1), dtype=np.uint32)
#     LUT[0, weights[0]:] = values[0]
#     for i, (val, wt) in enumerate(zip(values[1:], weights[1:]), 1):
#         LUT[i, :wt] = LUT[i-1, :wt]  # item weight exceeds capacity
#         for j in range(wt, W+1):
#             LUT[i, j] = max(
#                 val + LUT[i-1, j - wt],
#                 LUT[i-1, j]
#             )
#     return LUT 
    
# @cache
def knapsack(weights, W):
    # No weights left to carry
    if not weights:  return 0
    
    # Can't carry any of the weights
    if min(weights) > W:  return 0
    
    # Zero capacity
    if W == 0:  return 0
    
    
    
    w0 = weights[0]
    
    include = 0
    
    if w0 < W:
    
        include = w0 + knapsack(weights[1:], W-w0)
    
    exclude = knapsack(weights[1:], W)
    
    if include >= exclude:
        print(f'{w0 = } should be included ({include})')
    
    
    return max(include, exclude)




q = knapsack([30, 24, 21, 20, 10, 5], 55)

print(q)