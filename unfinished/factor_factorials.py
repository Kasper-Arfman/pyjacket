from math import isqrt
 

def prime_factors(n):
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



def factorial_divisible(n, mod):
    """ Determine if n! % mod == 0"""

    return


def factor_divisible(pf1, pf2):
    for k, v in pf2.items():
        if pf1.get(k, 0) < v:
            return False
    return True

def num_divisors(pf):
    r = 1
    for v in pf.values():
        r *= v+1
    return r

         

if __name__ == "__main__":

    q = None

    assert prime_factors(5040) == {2: 4, 3: 2, 5: 1, 7: 1}

    pf1 = {2: 4, 3: 2, 5: 1, 7: 1}
    assert factor_divisible(pf1, {2: 1, 5:1}) == True
    assert factor_divisible(pf1, {11: 1}) == False


    assert num_divisors({2:2, 3:1, 5:1}) == 12
    assert num_divisors({2:3, 3:2, 5:1}) == 24


    assert num_divisors(prime_factors(180)) == 18
    
    for i in range(1, 101):
        q = num_divisors(prime_factors(i))
    
        if q % 2:
            print(i, q)