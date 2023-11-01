from math import gcd, ceil, floor

def divides(a, b):
    """is a a multiple of b"""
    return a % b == 0

def bezout(*args) -> bool:
    """Determine whether a solution exists to equation
    ax + by + ... = d
    """
    *coefs, d = args
    return divides(d, gcd(*coefs))


def diophantine(a, b, c):
    """Solve ax + by = c
    Returns:
         x,  y  --  arbitrary solution
        dx, dy  --  period of solution intervals
    """
    div, x, y = extended_gcd(a, b)
    r = c // div
    solution = (r * x, r * y)
    period = (b//div, -a//div)
    return solution, period


def positive_solutions(solution, period):
    """ Get the positive solutions to a diophantine equation

    Might be a lot, so a generator approach is used.    
    """

    # print('\nsolving', solution, period)

    x, y = solution
    dx, dy = period

    lb, ub = sorted([-x/dx, -y/dy])
    # lb, ub = ceil(lb), floor(ub)  # round to integers
    # print('bounds', lb, ub)

    # print('rage', list(range(-7, )))

    for m in range(lb, ub+1):
        yield (x+m*dx, y+m*dy)
        # print('solution', x+m*dx, y+m*dy)






def extended_gcd(a, b):
    """ax + by = gcd(a, b)"""
    if a == 0:  return b, 0, 1
    gcd, x, y = extended_gcd(b % a, a)
    x, y = y - (b // a)*x, x
    return gcd, x, y


if __name__ == "__main__":
    q = None

    assert bezout(14, 91, 53) == False
    assert bezout(12, 21, 80) == False
    assert bezout(12, 8, 68) == True
    assert bezout(141, 34, 30) == True
    q = bezout(28, 30, 31, 365)




    # assert diophantine(1, 1, 0) == (0, 0)
    # assert diophantine(1, 1, 1) == (1, 0)
    # assert diophantine(3, 5, 1) == (2, -1)
    assert diophantine(21, 7, 14) == ((0, 2), (1, -3))
    assert diophantine(7, 11, 1) == ((-3, 2), (11, -7))
    assert diophantine(141, 34, 30) == ((210, -870), (34, -141))
    assert diophantine(4, 7, 97) == ((194, -97), (7, -4))
    # q = diophantine(75, 32, 83)
    
    # q = positive_solutions(*q)




    # assert list(positive_solutions((194, -97), (7, -4))) == [(5, 11), (12, 7), (19, 3)]


    




    # assert (f := extended_gcd(1, 1)) == (1, 1, 0), f'got {f}'
    # assert (f := extended_gcd(2, 37)) == (1, -18, 1), f'got {f}'
    # assert (f := extended_gcd(5, 25)) == (5, 1, 0), f'got {f}'
    # assert extended_gcd(0, 0) == 0
    # assert extended_gcd(0, 0) == 0
    # assert extended_gcd(0, 0) == 0
    # assert extended_gcd(0, 0) == 0
    # assert extended_gcd(0, 0) == 0
    # assert extended_gcd(0, 0) == 0
    


    print(q)
    pass

