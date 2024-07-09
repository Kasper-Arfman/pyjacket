import numpy as np

""" 
TODO: consider movies instead of images
"""

""" _____ Get array bit information _____"""
def type_max(dtype: np.dtype):
    """Get the maximum value that can be represented by the given data type"""
    try:                return np.finfo(dtype).max
    except ValueError:  return np.iinfo(dtype).max

def bytes(dtype):
    return dtype.itemsize

def bits(dtype):
    return 8 * bytes(dtype)


""" _____ Type conversions _____"""
def round_astype(arr, dtype=np.uint8):
    arr = np.rint(arr)
    arr = arr.astype(dtype)
    return arr


""" _____ Rescaling functions _____ """
def rescale(arr: np.ndarray, lb, ub, dst_dtype=None) -> np.ndarray:
    """Fits the bits into the requested window.
    If the image is of type uint, convert it back after rescaling"""
    src_dtype = arr.dtype
    dst_dtype = dst_dtype or src_dtype
    if src_dtype != np.float32 or dst_dtype != np.float32: 
        arr = arr.astype(np.float32) 
        arr = rescale(arr, lb, ub, np.float32)
        arr = round_astype(arr, dst_dtype or src_dtype)
        return arr
        
    mi = arr.min()
    ma = arr.max()
    # arr = (ub - lb) * (arr-mi)/(ma-mi) + lb
    # Perform operations in place to prevent memory issues.
    arr -= mi
    arr *= (ub - lb)
    arr /= (ma - mi)
    arr += lb
    return arr

def normalize(arr: np.ndarray) -> np.ndarray[np.float32]:
    """Represent image as floating point numbers between 0 and 1."""
    return rescale(arr, 0, 1)

def rescale_distribute(arr: np.ndarray): 
    """Rescale image to use the full bit range that the source image allows. """
    return rescale(arr, 0, type_max(arr.dtype))

def rescale_saturate(arr: np.ndarray, percent_bottom: float, percent_top: float):
    """rescale such as to saturate <p_lower>% of the pixels."""    
    i1 = np.percentile(arr, percent_bottom)
    i2 = np.percentile(arr, 100-percent_top)
    arr = fix_between(arr, 
                      round_astype(i1, arr.dtype),
                      round_astype(i2, arr.dtype))
    return rescale_distribute(arr)

def rescale_astype(arr: np.ndarray, type: np.dtype):
    target_type_max = type_max(type)
    return rescale(arr, 0, target_type_max, dst_dtype=type) #.astype(type)

"""_____ Truncations _____"""
def fix_between(arr, lb, ub):
    """Trucate data smaller than lb or greater than ub"""
    return truncate_above(truncate_below(arr, lb), ub)

def truncate_below(arr, lb):
    return np.where(arr < lb, lb, arr)
    
def truncate_above(arr, ub):
    return np.where(arr > ub, ub, arr)