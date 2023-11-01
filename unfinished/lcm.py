if __name__ == '__main__': 
    import sys; sys.path.append(r'C:\Users\Kasper\Documents\GitHub\kaspy')


from prime_factorization import prime_factors
from math import gcd


def pf_lcm(pf1, pf2):
    pf1 = pf1.copy()
    for k, v2  in pf2.items():
        v1 = pf1.setdefault(k, 0)
        if v2 > v1:
            pf1[k] = v2
    return pf1


def lcm(a, b):
    x = pf_lcm(prime_factors(a), prime_factors(b))

    r = 1
    for k, v in x.items():
        r *= k**v
    return r

def coprime(a, b):
    return gcd(a, b) == 1



if __name__ == "__main__":
    q = prime_factors(24)
    # print(q)

    q = lcm(24, 5)
    q = lcm(3, 7) == 21
    q = lcm(27, 12) == 108


    q = pf_lcm(prime_factors(294), prime_factors(364)) == {2: 2, 3: 1, 7: 2, 13: 1}

    assert lcm(24, 54) == 216
    assert lcm(45, 75) == 225
    assert lcm(72, 108) == 216

    assert (coprime(15, 24)) == False
    assert (coprime(16, 25)) == True
    assert (coprime(17, 26)) == True
    assert coprime(189, 245) == False
    assert coprime(242, 165) == False
    assert coprime(231, 260) == True


    assert gcd(24, 30) == 6


    q = prime_factors(101)



    print(q)