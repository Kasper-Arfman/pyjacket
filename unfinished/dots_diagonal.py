if __name__ == '__main__': 
    import sys; sys.path.append(r'C:\Users\Kasper\Documents\GitHub\kaspy')


from prime_factorization import prime_factors
from math import gcd

def reduce_fraction(a, b):
    d = gcd(a, b)
    return a//d, b//d


def num_dots_on_diagonal(a, b):
    return gcd(a, b) + 1




if __name__ == "__main__":
    q = None

    q = reduce_fraction(24, 30)


    assert num_dots_on_diagonal(6, 15) == 4
    assert num_dots_on_diagonal(7, 15) == 2
    assert num_dots_on_diagonal(8, 15) == 2
    assert num_dots_on_diagonal(5, 15) == 6
    assert num_dots_on_diagonal(9, 15) == 4

    assert num_dots_on_diagonal(24, 28) == 5
    assert num_dots_on_diagonal(12, 32) == 5
    assert num_dots_on_diagonal(72, 45) == 10

    print(q)