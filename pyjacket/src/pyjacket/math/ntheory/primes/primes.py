from typing import Dict

def generate_primes():... 

def is_prime(): ...


def prime_factors(n) -> Dict[int, int]:
    factors = {}
    divisor = 2
    while divisor * divisor <= n:
        if n % divisor == 0:
            factors[divisor] = factors.get(divisor, 0) + 1
            n //= divisor
        else:
            divisor += 1
    
    if n > 1:
        factors[n] = factors.get(n, 0) + 1     
    
    return factors

def num_prime_factors(n) -> int:
    return len(prime_factors(n))

def prime_factors_list(n):
    factors = []
    divisor = 2
    while divisor * divisor <= n:
        if n % divisor == 0:
            factors.append(divisor)
            n //= divisor
        else:
            divisor += 1
    if n > 1:
        factors.append(n)
    return factors


def primes_between(a, b):
    sieve = [True] * (b + 1) # Initialize sieve with all True values
    sieve[0] = sieve[1] = False # Set 0 and 1 to False since they are not prime
    
    for i in range(2, int(b**0.5) + 1):
        if sieve[i]:
            # Mark all multiples of i as composite (i.e., not prime)
            for j in range(i*i, b+1, i):
                sieve[j] = False
    
    # Generate a list of all primes between a and b
    primes = [i for i in range(a, b+1) if sieve[i]]
    return primes


def times_divides(num, factor):
    if not factor: return 0
    count = 0
    while num and num % factor == 0:
        num //= factor
        count += 1      
    return count
    




if __name__ == '__main__':
    
    # primes = primes_between(20, 50)
    # print(primes)
    
    
    x = times_divides(4, 2)
    print(x)