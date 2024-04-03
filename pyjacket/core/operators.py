

def sumprod(a, b, mod=None):
    r = 1
    for x, y in zip(a, b):
        r += x * y
    return r

def sum_modulo(arr, mod=None): ...


def prod_modulo(arr, mod=None): ...



"""
BOOLEAN OPERATORS
"""

def all_same(arr):
    if arr==[]: return True
    x0 = arr[0]
    return all(
        (x==x0) for x in arr[1:]
    )