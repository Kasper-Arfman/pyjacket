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



def is_prime(n):

    pf = prime_factors(n)
    print(pf)

    c = sum(pf.values())


    return c == 1






if __name__ == "__main__":
    q = None
    
    assert is_prime(6) == False
    assert is_prime(31) == True
    assert is_prime(49) == False 
    assert is_prime(91) == False
    assert is_prime(99) == False

    print(q)