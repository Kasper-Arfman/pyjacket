
def truncate(s: str, n: int, symbol=''):
    """Fixes the length of a string. Use truncation symbol <symbol> to denote truncation."""

def truncate_modulo(s: str, mod: int):
    """Ensures length of a string <s> is a multiple of <n>"""
    r = len(s) % mod
    if r: s = s[:-r]
    return s

def extend(): ...

def extend_modulo(s: str, n:int, fillval='0'):
    s += fillval * (-len(s) % n)
    return s

def isplit(s: str, i):
    """split a string at index or list of indices"""
    if isinstance(i, int):
        i = [i]
        
    for i1, i2 in zip([None]+i, i+[None]):
        yield s[i1:i2]



if __name__ == '__main__':
    s = 'Hello there mate'
    n = 6
    q = truncate_modulo(s, n)
    print(q)