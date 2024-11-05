import numpy as np
import os
from typing import Union
from .metadata import Metadata
from .image_handle import ImageHandle
from . import _mp4, _tif, _nd2, _avi, _png, _jpg


"""Convention:
All arrays must be of shape
 - (height, width)
 - (frames, height, width)
 - (frames, height, width, colors)
"""



def imread(filepath: str, lazy=False, unzip_channels=1, **kwargs) -> np.ndarray:
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

    folder = False
    if os.path.isdir(filepath):
        print(f'Folder detected!')
        folder = True


    _, ext = os.path.splitext(filepath)  # ext may be missing
    ext = ext.lstrip('.')

    if lazy:
        read_function = {
            '': _tif.MMStack if folder else _tif.TifImageHandle,
            'tif': _tif.TifImageHandle,
            'tiff': _tif.TifImageHandle,
        }.get(ext)

        if read_function is None:
            raise ValueError(f'Cannot lazy-read data of type {ext}')

        h: ImageHandle = read_function(filepath, **kwargs)
        return h
  

    elif not lazy:

        if folder:  raise NotImplementedError('Cant read folders yet unless its lazy')

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








# def unzip(img: np.ndarray, channels=2):
#     assert img.ndim == 3, ValueError(f'Expected img or shape (frames, y, x), got {img.shape}')
    
#     rem = img.shape[0] % channels
#     if rem:
#         warnings.warn(Warning('Encountered odd number of frames, omitting last frame(s)'))
#         img = img[:-rem]
#     t, y, x = img.shape
#     return img.reshape((t//channels, channels, y, x)).transpose(0, 2, 3, 1)   
    
