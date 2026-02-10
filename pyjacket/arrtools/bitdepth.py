"""Bit depth manipulations"""

import numpy as np

def minmax(a: np.ndarray):
    """Simultaneously obtain min and max of the array

    Parameters
    ----------
    a : np.ndarray
        array of which to compute min and max

    Returns
    -------
    scalar
        minimum of a
    scalar
        maximum of a
    """    
    return np.min(a), np.max(a)

""" _____ Get array bit information _____"""

def type_min(dtype: np.dtype):
    """Get the minimum value that can be represented by the given data type"""
    try:                return np.finfo(dtype).min
    except ValueError:  return np.iinfo(dtype).min

def type_max(dtype: np.dtype):
    """Get the maximum value that can be represented by the given data type"""
    try:                return np.finfo(dtype).max
    except ValueError:  return np.iinfo(dtype).max

def bytes(dtype: np.dtype) -> int:
    """Number of bytes (8bit) per array element

    Parameters
    ----------
    dtype : np.dtype
        array datatype

    Returns
    -------
    int
        number of bytes
    """
    return dtype.itemsize

def bits(dtype: np.dtype) -> int:
    """Number of bits per array element

    Parameters
    ----------
    dtype : np.dtype
        array datatype

    Returns
    -------
    int
        number of bits
    """
    return 8 * bytes(dtype)  # NumPy guarantees bytes are 8 bits

def saturated(a: np.ndarray):
    """Determine which pixels are saturated"""
    return a >= type_max(a.dtype)


""" _____ Type conversions _____"""
def clip_astype(a: np.ndarray, dtype: np.dtype=np.uint8):
    """Convert datatype without changing content. 
    Out of bounds entries are clipped to the new datatype

    Parameters
    ----------
    a: np.ndarray
        input array

    dtype: np.dtype, optional
        target datatype. The default is uint8.

    Returns
    -------
    int
        number of bits

    Examples
    --------
    >>> a = np.array([-200, -100, 0, 100, 200], dtype=np.int32)
    >>> clip_astype(a, np.int8)
    array([-128, -100, 0, 100, 127])
    """
    a = np.clip(a, type_min(dtype), type_max(dtype))
    return np.rint(a).astype(dtype)

def rescale(a: np.ndarray, lb: float, ub: float, dtype:np.dtype=None, mi: float=None, ma: float=None) -> np.ndarray:
    """Rescale array inputs to fit in a requested window (lb, ub) in the specified datatype

    Parameters
    ----------
    a : np.ndarray
        array containing elements to rescale
    lb : scalar
        lower bound
    ub : scalar
        upper bound
    dtype : np.dtype, optional
        target data type, by default a.dtype
    mi : scalar
        value to map to lb, default min(a)
    ma : scalar
        value to map to ub, default max(a)

    Returns
    -------
    np.ndarray
        rescaled array
    """
    dtype = dtype or a.dtype
    # Convert to float32 for improved accuracy
    if a.dtype != np.float32 or dtype != np.float32: 
        a = a.astype(np.float32) 
        a = rescale(a, lb, ub, np.float32)
        a = clip_astype(a, dtype or a.dtype)
        return a
    
    # Perform rescaling in float datatype
    mi = mi or np.min(a)
    ma = ma or np.max(a)
    return (np.clip(a, mi, ma)-mi) * (ub-lb)/(ma-mi) + lb


def distribute(a: np.ndarray, dtype:np.dtype=None, p1: float=0, p2: float=0): 
    """Rescale array elements using the maximum dynamic range.
    Optionally, saturate part of the the contents based on percentile
    
    a : np.ndarray
        array containing elements to rescale
    dtype : np.dtype, optional
        target data type, by default a.dtype
    p1 : scalar
        percentile of lower bound
    p2 : scalar
        percentile of upper bound
    """
    if p1 == p2 == 0:
        mi, ma = minmax(a)
    else:
        mi, ma = np.percentile(a, (p1, 100-p2))

    dtype = dtype or a.dtype
    return rescale(a, type_min(dtype), type_max(dtype), dtype=dtype, mi=mi, ma=ma)

def normalize(a: np.ndarray) -> np.ndarray[np.float32]:
    """Rescales contents between 0 and 1."""
    a = a.astype(np.float32)
    return rescale(a, 0, 1, dtype=np.float32)






# def convert_type(a: np.ndarray, dtype:np.dtype=np.uint8):

#     src_max = type_max(a.dtype) + 1
#     dst_max = type_max(dtype) + 1
    
#     if src_max > dst_max:
#         scale_factor = src_max//dst_max
#         scaled = a // scale_factor
#         return scaled.astype(dtype)

#     if dst_max > src_max:
#         scale_factor = dst_max//src_max
#         return(a.astype(dtype) + 1)*scale_factor - 1
        
#     return ValueError()

# def distribute_astype(arr: np.ndarray, type: np.dtype):
#     """Convert datatype and rescale content to use full dynamic range
    
#     This minimizes loss in resolution, but brightness info is lost.
#     """
#     target_type_max = type_max(type)
#     return rescale(arr, 0, target_type_max, dst_dtype=type) #.astype(type)

# def saturate_astype(*args, **kwargs):
#     """Convert datatype and rescale content to saturate part of the data
    
#     Sacrifice dim and bright information to maintain good resolution for the bulk of data.
#     """
#     raise NotImplementedError()

# """ _____ Rescaling functions _____ (change contents, but not dtype)"""






# def rescale_saturate(arr: np.ndarray, percent_bottom: float, percent_top: float):
#     """rescale such as to saturate <p_lower>% of the pixels."""    
#     i1 = np.percentile(arr, percent_bottom)
#     i2 = np.percentile(arr, 100-percent_top)
#     arr = fix_between(arr, 
#                       clip_astype(i1, arr.dtype),
#                       clip_astype(i2, arr.dtype))
#     return distribute(arr)



# """_____ Truncations _____"""
# def fix_between(arr, lb, ub):
#     """Trucate data smaller than lb or greater than ub"""
#     return truncate_above(truncate_below(arr, lb), ub)

# def truncate_below(arr, lb):
#     return np.where(arr < lb, lb, arr)
    
# def truncate_above(arr, ub):
#     return np.where(arr > ub, ub, arr)