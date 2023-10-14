def digits(n):
    return [int(d) for d in str(n)]

def digital_sum(n):
    return sum(digits(n))

def digital_root(n):
    # if digital_root(n) == 0
    # then n must be divisible by 9

    # if   n%9==0 -> 9
    # elif n%9==k -> k


    while n > 10:
        n = digital_sum(n)
    return n




def digital_root_prod(a, b):
    return digital_root(digital_root(a) * digital_root(b))



if __name__ == '__main__':
    q = None

    assert digital_root(3271) == 4
    assert digital_root(999921) == 3
    assert digital_root(9999999921) == 3


    q = digital_root_prod(1999, 9991)



    print(q)