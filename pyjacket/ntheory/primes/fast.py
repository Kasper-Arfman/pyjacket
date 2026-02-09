from math import gcd
from collections import Counter

def is_prime(n: int) -> bool:
    """Check if a number is prime (maximum 64 bit)"""
    if n < 2:
        return False
    small_primes = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29)
    for p in small_primes:
        if n % p == 0:
            return n == p
    # write n-1 = d * 2^s
    d = n - 1
    s = 0
    while d & 1 == 0:
        d >>= 1
        s += 1
    # Deterministic bases for 64-bit integers
    for a in (2, 325, 9375, 28178, 450775, 9780504, 1795265022):
        if a % n == 0:
            continue
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = (x * x) % n
            if x == n - 1:
                break
        else:
            return False
    return True

def pollards_rho(n: int) -> int:
    """Obtain all integer factorizations"""
    if n % 2 == 0:
        return 2
    if n % 3 == 0:
        return 3
    # try different constants c deterministically
    c = 1
    while True:
        x = 2
        y = 2
        d = 1
        while d == 1:
            x = (x * x + c) % n
            y = (y * y + c) % n
            y = (y * y + c) % n
            d = gcd(abs(x - y), n)
        if d != n:
            return d
        c += 1  # change polynomial; guaranteed to find a factor eventually



def factorize(n):
    factors = []

    def recurse(n):
        if is_prime(n):
            factors.append(n)
        elif n > 1:
            factor = pollards_rho(n)
            while factor == n:
                factor = pollards_rho(n)

            recurse(factor)
            recurse(n // factor)

    recurse(n)
    
    return Counter(factors)