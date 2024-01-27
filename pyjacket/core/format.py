def truncate_to_multiple(s, n):
    r = len(s) % n
    if r: s = s[:-r]
    return s

def extend_to_multiple(s: str, n:int, fillval='0'):
    s += fillval * (-len(s) % n)
    return s