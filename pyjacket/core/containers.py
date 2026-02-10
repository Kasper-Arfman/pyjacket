from collections import Counter

class PositiveCounter(Counter):
    """Variant of `collections.Counter` that only keeps positive counts.

    Example:
    --------
    >>> pc = PositiveCounter()
    >>> pc.add('apple')
    >>> pc.add('apple')
    >>> pc.remove('apple')
    >>> pc
    PositiveCounter({'apple': 1})
    >>> pc.remove('apple')
    >>> pc
    PositiveCounter({})
    """

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self._keep_positive()

    def __add__(self, other):
        return PositiveCounter(super().__add__(other))
    
    def __sub__(self, other):
        return PositiveCounter(super().__sub__(other))

    def add(self, element):
        """Increment the count for `element` by 1."""
        return self.__add__(PositiveCounter([element]))
    
    def sub(self, element):
        """Decrement the count for `element` by 1; remove if count <= 0."""
        return self.__sub__(PositiveCounter([element]))
    
    def remove(self, element):
        """Subtract 1 from `element` count; remove if count <= 0."""
        self[element] = 0
        return PositiveCounter(self)
    


if __name__ == '__main__':

    def test():
        c1 = PositiveCounter({1:3, 2:4, 3: 3, 4:-2, 5: 0, 6:1})
        c2 = PositiveCounter({1:2, 2:5, 3:-1, 4: 3, 5:-1, 6:0})

        # Zero counts should be removed
        assert 5 not in c1, 'Zero should be removed'
        assert 5 not in c2, 'Negatives should be removed'

        # __sub__
        assert 2 not in c1-c2, 'No negative counts after subtracting'

        # .add
        x = c1.add(1)
        assert x[1] == 4, 'Adding element directly'
        
        # .sub
        x = c1.sub(1)
        assert x[1] == 2, 'Adding element directly'
        x = c1.sub(1).sub(1).sub(1)
        assert 1 not in x, 'Zero value should be removed'
        assert x.sub(1) == x, 'Subtracting missing item => donothing'

        # in place addition
        c1 -= Counter([6, 5])
        print(c1)

        # removal
        x = c2.remove(4)
        print(x)

        

        
    test()