def similarity(a: str, b: str) -> int:
    """ Minimal number of edits to required to change string a into b
    https://en.wikipedia.org/wiki/Levenshtein_distance
    """   
    return levenshtein(a, b, cache={})

def levenshtein(a: str, b: str, cache: dict=None) -> int:
    """ Minimal number of edits to required to change string a into b
    https://en.wikipedia.org/wiki/Levenshtein_distance
    """
    cache = cache or {}
    if (a, b) not in cache:    
        if not a: return len(b)
        if not b: return len(a)
        if a[0] == b[0]:
            return levenshtein(a[1:], b[1:], cache)
        
        cache[(a, b)] = 1 + min(
            levenshtein(a[1:], b    , cache),
            levenshtein(a,     b[1:], cache),
            levenshtein(a[1:], b[1:], cache),
        )
    return cache[(a, b)]