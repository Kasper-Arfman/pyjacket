from itertools import filterfalse

def partition(condition, iterable):
    """Splits a list into two lists based on a condition"""
    return (
        [*filter(     condition, iterable)],
        [*filterfalse(condition, iterable)],
    )
    
# def exclude_filter(a, exclude=None):
#     return filter(lambda x: x != exclude, a)





# a = [1, 2, 3, None, 4, None, 5, 6]
# a = [*exclude_filter(a)]
# print(a)

