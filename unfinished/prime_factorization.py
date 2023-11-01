

# Python program to print prime factors
 
import math
from math import isqrt
 

def prime_factors(n):
    if not n: return {1: 0}
    if n == 1: return {1: 1}

    r = {}
   
    while n % 2 == 0:
        n //= 2
        r[2] = r.get(2, 0) + 1
         
    for i in range(3, isqrt(n)+1, 2):
        while n % i== 0:
            n //=  i
            r[i] = r.get(i, 0) + 1

    if n>2:
        r[n] = 1
            
    return r


def perfect_square(pf):
    return all(x%2==0 for x in pf.values())


def perfect_cube(pf):
    return all(x%3==0 for x in pf.values())

         

if __name__ == "__main__":

    q = None

    assert prime_factors(150) == {2: 1, 3: 1, 5: 2}
    assert prime_factors(17) == {17: 1}
    assert prime_factors(17820) == {2: 2, 3: 4, 5: 1, 11: 1}
    assert prime_factors(1728) == {2: 6, 3: 3}

    q = prime_factors(120)

    assert perfect_cube({2: 6, 3: 3}) == True 



    print(q)