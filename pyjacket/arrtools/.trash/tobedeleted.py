"""Iteration methods"""
def columns(arr):
    for i in range(arr.shape[1]):
        yield arr[:, i]
        
def bytes(dtype):
    """Number of bytes (8*bits) used to encode a number of this data type"""
    return dtype.itemsize