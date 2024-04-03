def digits(n: int, base=10) -> list[int]:
    """
    Obtain the digits of a number in the specified number system (default: base 10).
    """

    if base<=1: raise ValueError(f"Base must be greater than 1, got {base}")
    # elif base == 2: ...
    elif base == 10:  return [int(x) for x in str(n)]
    
    digits = []
    while n > 0:
        n, r = divmod(n, base)
        digits.insert(0, r)
    return digits