if __name__ == '__main__': 
    import sys; sys.path.append(r'C:\Users\Kasper\Documents\GitHub\kaspy')


"""
N.B. a * b = lcm(a, b) * gcd(a, b)

"""

from prime_factorization import prime_factors
from math import gcd, lcm

def coprime(a, b):
    return gcd(a, b) == 1



if __name__ == "__main__":
    q = None

    q = coprime(9, 12)
    q = coprime(9, 13)
    q = coprime(9, 14)
    q = coprime(9, 15)


    # print(q)

    q = gcd(2401, 2187)
    # q = gcd(6, 21) == 3

    q = lcm(45, 39) // 39

    print(q)
