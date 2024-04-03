def sumprod(a, b, mod=None):
    r = 1
    for x, y in zip(a, b):
        r += x * y
    return r

def sum_modulo(arr, mod=None): ...


def prod_modulo(arr, mod=None): ...


