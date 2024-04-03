def cyclic(arr):
    """Cycle through a word.
    Example:
    >>> Apple
    ... [Apple ppleA pleAp leApp eAppl]
    """
    for i in range(len(arr)):
        yield arr[i:] + arr[:i]

def batched(iterable, n: int, filler=None):
    """Iterate through the iterable in chunks of size <n>.
    Providing a filler value ensures all chunks are of equal size."""
    if filler is not None: raise NotImplementedError('Filler value not implemented yet')
    # WARNING THIS DOES NOT WORK FOR A GENERATOR YET
    N = len(iterable)
    for i in range(0, N, n):
        yield iterable[i:i+n] 
        
def slider(iterable, n: int):
    """Iterate chunks of a sliding window
    Example:
    >>> Applejuice, 4
    ... [Appl pple plej leju ejui juic uice]
    """
    iterable = iter(iterable)
    v = tuple(next(iterable) for _ in range(n))
    yield v
    for e in iterable:
        v = (*v[1:], e)
        yield v    



if __name__ == '__main__':

    arr = 'applejuice'
    n = 4


    q = slider(arr, n)
    q = list(q)

    print(q)