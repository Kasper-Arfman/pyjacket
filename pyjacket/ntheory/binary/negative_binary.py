

def bin2int(b: str, nbit: int=32):
    """Get the int32 value of a binary string
    Negatives are represented using two's complement"""
    n = int(b, 2)
    if b.startswith('1'):
        n -= 2**nbit
    return n

def binary(n, nbit=8):
    return bin(n)[2:].zfill(nbit)

def int2bin(n, nbit: int=32):
    """Get the signed binary representation of a number.
    Negatives are represented using two's complement"""
    if n < 0:  n += 2**nbit
    return bin(n)[2:].zfill(nbit)