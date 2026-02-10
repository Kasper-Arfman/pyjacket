from itertools import filterfalse, zip_longest
from typing import Iterable, Callable

def partition(condition: Callable, it: Iterable) -> tuple[list, list]:
    """Split an iterable into (truths, falses)
    
    Parameters
    ----------
    condition : callable
        function to evaluate elements of iterable
    iterable : iterable
        sequence of elements to partition.

    Returns
    -------
    list   
        elements that evaluated true
    list
        elements that evaluated false

    Examples
    --------
    >>> Partition(lambda x: x<5, [1, 2, 3, 4, 5, 6, 7, 8])
    [1, 2, 3, 4], [5, 6, 7, 8] 
    """
    return (
        [*filter(     condition, it)],
        [*filterfalse(condition, it)],
    )
    
def index_nth(it: Iterable, element, n: int=-1) -> int:
    """Find nth (default: last) occurence of element in iterable.
    
    Parameters
    ----------
    iterable : iterable

    element : Any
        element to find in iterable

    n : int
        n'th occurence of element to find. Default is -1 and finds the last  element.

    Returns
    -------
    int:
        index of the n'th occurence

    Raises
    ------
    ValueError
        n must be nonzero
        iterable does not contain element
        iterable does not contain element n times

    Examples
    --------
    >>> find_nth([1, 2, 3, 4, 1, 2, 3, 1, 1, 1, 2], 1, 3)
    7
    """    
    it = list(it)
    if n == 0:
        raise ValueError(f"n must be nonzero")

    if n < 0:  
        idx = len(it) - index_nth(it[::-1], element, -n) - 1
    
    else:
        idx = it.index(element)  # Raise ValueError if not found
        try:
            while idx >= 0 and n > 1:
                idx = it.index(element, idx+1)
                n -= 1
        except ValueError:
            raise ValueError(f"iterable has no {n}'th element")
            
    return idx

def cyclic_shifts(it: Iterable):
    """Find all the cyclic arrangements of the iterable

    Parameters
    ----------
    iterable : iterable
        iterable to cycle

    Yields
    ------
    tuple
        shifted permutation of iterable

    Examples
    --------
    >>> cyclic_shifts([1, 2, 3, 4, 5])
    (1, 2, 3, 4, 5)
    (2, 3, 4, 5, 1)
    (3, 4, 5, 1, 2)
    (4, 5, 1, 2, 3)
    (5, 1, 2, 3, 4)
    """
    it = tuple(it)
    for i in range(len(it)):
        yield (*it[i:], *it[:i])

def batched(it: Iterable, batch_size: int, fill_value = None):
    """
    Yield successive batches from the iterable.

    Args:
        iterable: An iterable to batch.
        batch_size: The size of each batch.
        fill_value: The value to fill in for incomplete batches.

    Yields:
        Lists containing the batches of specified size.

    Examples:
    ---------
    >>> batched('0123456789', 4, '#')
    ('0', '1', '2', '3')
    ('4', '5', '6', '7')
    ('8', '9', '#', '#')
    """
    if batch_size <= 0:
        raise ValueError("Batch size must be greater than zero.")

    it = iter(it)
    return zip_longest(*[it] * batch_size, fillvalue=fill_value)
            
def sortby(it: Iterable, val: Iterable) -> list:
    """Sort iterable by the values of another iterables

    Parameters
    ----------
    it : Iterable
        iterable that requires sorting
    Y : Iterable
        values on which sorting is based

    Returns
    -------
    list
        sorted it
    """
    return [x for (y,x) in sorted(zip(val,it), key=lambda pair: pair[0])] 

def sliding_window(iterable: Iterable, n: int):
    """Iterate the sliding windows of size n

    Parameters
    ----------
    iterable : Iterable
        iterable to slide across
    n : int
        window size

    Yields
    ------
    tuple
        elements of the sliding window

    Examples
    --------
    >>> sliding_window('abcdefg', 4)
    ('a', 'b', 'c', 'd')
    ('b', 'c', 'd', 'e')
    ('c', 'd', 'e', 'f')
    ('d', 'e', 'f', 'g')
    """
    iterable = iter(iterable)
    v = tuple(next(iterable) for _ in range(n))
    yield v
    for e in iterable:
        v = (*v[1:], e)
        yield v       