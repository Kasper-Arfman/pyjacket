from functools import reduce
from math import isqrt
  
def factors(n):
    """return factors pairwise"""
    step = n%2 + 1
    return [[i, n//i] for i in range(1, isqrt(n)+1, step) if not n % i]



def divisors(n):
    """return factors pairwise"""
    step = n%2 + 1
    return sum(([i, n//i] for i in range(1, isqrt(n)+1, step) if not n % i), [])
    
    
    
    
def div_sum(n, proper=True):
    root = isqrt(n)
    r = -n if proper else 0
    if root * root == n:
        r -= root
    for x in range(1, root+1, n%2+1):
        if not n%x:
            r += x + n//x
    return r
    
        
        
        
# z = factors(124)

# print(z)