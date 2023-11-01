if __name__ == '__main__': 
    import sys; sys.path.append(r'C:\Users\Kasper\Documents\GitHub\kaspy')


from prime_factorization import prime_factors
from math import gcd, lcm
from functools import reduce

def coprime(a, b):
    return gcd(a, b) == 1


def divisors(pf):
    # factors = list(factorGenerator(n))
    factors = list(pf.items())
    nfactors = len(factors)
    f = [0] * nfactors

    r = []



    while True:
        div = reduce(lambda x, y: x*y, [factors[x][0]**f[x] for x in range(nfactors)], 1)
        r.append(div)

        i = 0
        while True:
            f[i] += 1
            if f[i] <= factors[i][1]:
                break
            f[i] = 0
            i += 1
            if i >= nfactors:
                return r

    return r


def perfect(n):
    pf = prime_factors(n)
    # print(n, pf)
    return sum(divisors(pf)[:-1]) == n


if __name__ == "__main__":
    q = None



    for i in range(100):

        q = perfect(i)

        if q:
            print(i, q)

    print(q)


