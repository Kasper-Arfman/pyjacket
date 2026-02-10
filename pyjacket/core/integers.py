def digits(n: int, base: int=10) -> list[int]:
    """Obtain the digits of an integer in any number base

    Parameters
    ----------
    n : int
        number of which to obtain the digits
    base : int, optional
        base of number system, by default 10

    Returns
    -------
    list
        digits of n

    Raises
    ------
    ValueError
        Number base must be larger than 1
        Number should be an integer

    Examples
    --------
    >>> digits(137)
    [1, 3, 7]

    >>> digits(254, 16)
    [15, 14]  # 255 = 15*16 + 14
    """
    if not isinstance(n, int): raise ValueError(f'pyjacket.digits takes an integer, got {type(n)}')
    
    if base<=1: raise ValueError(f"Base must be greater than 1, got {base}")
    # elif base == 2: ...
    elif base == 10:  return [int(x) for x in str(n)]
    
    digits = []
    while n > 0:
        n, r = divmod(n, base)
        digits.insert(0, r)
    return digits




