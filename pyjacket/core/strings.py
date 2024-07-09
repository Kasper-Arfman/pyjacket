
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


if __name__ == '__main__':
    s = 'Hello there mate'
    n = 6
    q = truncate_modulo(s, n)
    print(q)