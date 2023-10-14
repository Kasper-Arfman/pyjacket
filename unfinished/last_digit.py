
CYCLE = {
    3: [3, 9, 7, 1],   # 3, 9, 27, 81, etc.
}



def last_digit(n):
    return n % 10




def last_digit_raised(a, p):
    if not p: return 1


    base_last = last_digit(a)

    cycle = CYCLE[base_last]
    N = len(cycle)



    pow_index = (p-1) % N



    return cycle[pow_index]


def last_digit_product(a, b):
    return last_digit(last_digit(a) * last_digit(b))



def remainder_sum(a, b, mod):
    return (a%mod + b%mod) % mod


def remainder_prod(a, b, mod):
    return (a%mod * b%mod) % mod

def remainder_pow(a, b, mod):
    if b == 2:
        return square_odd(a, mod)



    # return (a%mod ** (b%mod)) % mod


def square_odd(a, mod):
    """if N is odd, then N^2 % 8 = 1"""
    if mod==8 and a%2==1:
        return 1


if __name__ == "__main__":
    q = None

    assert last_digit_raised(13, 100) == 1
    assert remainder_sum(48, 54, 7) == 4 

    assert remainder_prod(19, 12, 8) == 4

    assert remainder_prod(5, 2, 6) == 4

    assert remainder_pow(123456789, 2, 8) == 1




    print(q)




