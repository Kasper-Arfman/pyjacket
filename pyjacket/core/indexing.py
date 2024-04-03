def index_nth(iterable: list, element, n: int=-1) -> int:
    """Find index of nth (default: last) occurence of element in iterable."""    
    if n == 0:
        raise ValueError(f"n must be nonzero")

    if n < 0:  
        idx = len(iterable) - index_nth(iterable[::-1], element, -n) - 1
    
    else:
        idx = iterable.index(element)
        while idx >= 0 and n > 1:
            idx = iterable.index(element, idx+1)
            n -= 1
            
    return idx


# def index_nth(s: str, *args, **kwargs):
#     return s.rfind(*args, **kwargs)


def main():
    
    x = []
    y = 0
    z = -1
    
    
    q = index_nth(x, y, z)
    print(q)
    


if __name__ == '__main__':
    main()