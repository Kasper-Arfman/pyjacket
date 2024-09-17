from functools import cache


@cache
def cut_rod(p, l, n):  # O(n^2)
    """We are given a rod of length n
    And we sell rod-segments of various length.
    
    A rod segment of length L[i] has a value of p[i]
    
    The goal is to find the optimal way to cut the rod, such that
    value is maximized
    """
    # Base case: zero-length rod isn't worth anything
    if n == 0:  return 0
    
    # Consider cutting of each possible length
    # Note down their value
    # Choose the one that gives the most value
    ma = 0
    for i in range(n):
        length = l[i]
        value = p[i] + cut_rod(p, l, n-length)
        
        # Keep track of the maximum
        ma = max(ma, value)
        
    return ma


@cache
def cut_stock(l, n):
    """We are given a rod of length n
    And a order-list of lengths that needed to be cut
    
    Not all orders can be fulfilled by a single rod.
    The goal is to find how much of the rod can be brought to use.
    """
    # base case: zero-length rod
    if n == 0:  return 0
    
    # Consider each item in the order
    # imagine cutting int
    # choose the that gives the most value (uses as much of the rod as possible)
    ma = 0 
    for i in range(n):
        length = l[i]
        
        # Fulfilling order l[i], so we can scratch it
        # We already checked orders l[:i] in previous iterations.
        remaining_order = l[i+1:]
        
        # Value in case we choose to fulfil this order
        value = length + cut_stock(remaining_order, n-length)
        
        # In case we don't fulfil this order, we can try fulfilling the next one
        # this is done in the next iteration.
        
        ma = max(ma, value)
        
    return ma
    
@cache
def cut_stock(l, n):
    """We are given a rod of length n
    And a order-list of lengths that needed to be cut
    
    Not all orders can be fulfilled by a single rod.
    The goal is to find:
     - the maximum value 
     - and which orders lead to this maximum
     
    recursive approach: easy to implement, but uses more memory than iterative counterpart.
    """
    # base case: zero-length rod
    ma, choices = 0, []
    if n <= 0:  return ma, choices
    
    # Consider each item in the order
    # imagine cutting it
    # choose the one that gives the most value (uses as much of the rod as possible)
    for i, length in enumerate(l):
        # Cannot cut a part larger than the stock
        if length > n:  continue
        
        # We fulfil order l[i], so it is left hereafter
        # We already checked orders l[:i] in previous iterations, so these are left out as well
        remaining_order = l[i+1:]
        
        # Value in case we choose to fulfil this order
        rest_length, rest_choices = cut_stock(remaining_order, n-length)
        value = length + rest_length
        
        # In case we don't fulfil this order, we can try fulfilling the next one
        # this is done in the next iteration.
        if value > ma:
            ma, choices = value, [length] + rest_choices
            
    return ma, choices

# p = (1, 5, 8, 9, 10, 17, 17, 20, 24, 30)
# l = (1, 2, 3, 4,  5,  6,  7,  8,  9, 10)

# sorting the orders in descending order ensures the large components get used first
l = (5, 4, 1, 1, 1, 1, 1, 1, 1, 1)

# for i in range(11):
r = cut_stock(l, 9)
print(r)