import numpy as np
import os
from typing import Union
from pyjacket.filetools import Metadata, ImageHandle
from . import _mp4, _tif, _nd2, _avi, _png, _jpg


"""Convention:
All arrays must be of shape
 - (height, width)
 - (frames, height, width)
 - (frames, height, width, colors)
"""



def imread(filepath: str, lazy=False, unzip_channels=1) -> np.ndarray:
    """Read image data into a numpy array.

    Args:
        filepath (str): Location of the image file
        lazy (bool, optional): Read lazy to save memory. Defaults to False.
        channels (int, optional): Unzip first dimension into multiple channels. Defaults to 1.

    Raises:
        ValueError: _description_
        NotImplementedError: _description_

    Returns:
        np.ndarray: _description_
    """
    _, ext = os.path.splitext(filepath)  # ext may be missing

    if lazy:
        read_function = {
            '': _tif.TifImageHandle,
            'tif': _tif.TifImageHandle,
            'tiff': _tif.TifImageHandle,
        }.get(ext)

        if read_function is None:
            raise ValueError(f'Cannot lazy-read data of type {ext}')

        h: ImageHandle = read_function(filepath, channels=unzip_channels)
        return h
  

    elif not lazy:
        read_function = {
            '': _tif.read,
            'tif': _tif.read,
            'tiff': _tif.read,
            # 'png': _png.read,
            # 'jpg': _jpg.read,
            'nd2': _nd2.read,
            'avi': _avi.read,
        }.get(ext)
        
        if read_function is None:
            raise NotImplementedError(f'Cannot read data of type {ext}')
    
        data: np.ndarray = read_function(filepath)        
        return data

def imread_meta(filename):
    return Metadata(filename)

def imwrite(filepath: str, data: Union[np.ndarray, ImageHandle], 
        meta: Metadata=None, **kwargs):
    """Write image data. Supports tif, nd2"""
    if not '.' in filepath: raise ValueError(f"missing extension in filename: {filepath}")
    ext = filepath.split('.')[-1]

    # if isinstance(data, ImageHandle):
    #     write_function = {
    #         'mp4': _mp4.write
    #     }.get(ext)
        
    #     return write_function(filepath, data, meta, frame_time=frame_time, **kw)
    # else:
    #     ...    
    
    write_function = {
        # 'nd2': nd2.write,
        'tif': _tif.write,
        'mp4': _mp4.write,
    }.get(ext)
    
    if not write_function:
        raise NotImplementedError(f'Cannot write image of type {ext}')
    
    return write_function(filepath, data, meta, **kwargs)




# def slice_length(s: slice, n: int):
#     """Compute how many elements belong to a slice of an iterable of size n"""
#     start, stop, step = s.indices(n)
#     if step > 0:
#         return max(0, (stop - start + (step - 1)) // step)
#     elif step < 0:
#         return max(0, (start - stop - (step + 1)) // (-step))
#     else:
#         raise ValueError("Slice step cannot be zero")



# def unzip(img: np.ndarray, channels=2):
#     assert img.ndim == 3, ValueError(f'Expected img or shape (frames, y, x), got {img.shape}')
    
#     rem = img.shape[0] % channels
#     if rem:
#         warnings.warn(Warning('Encountered odd number of frames, omitting last frame(s)'))
#         img = img[:-rem]
#     t, y, x = img.shape
#     return img.reshape((t//channels, channels, y, x)).transpose(0, 2, 3, 1)   
    
