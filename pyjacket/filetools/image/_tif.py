import cv2 as cv
from skimage import io
import tifffile
import numpy as np

from typing import Union
# from pyjacket.filetools.image._image import TifImageHandle

# def read(filepath):
#     return io.imread(filepath)

def read(filepath):
    return tifffile.imread(filepath)

def write(filepath, data: Union[np.ndarray], meta=None, **kwargs):
    # if isinstance(data, TifImageHandle):
    #     pass
    # elif isinstance(data, np.ndarray):
    #     pass
    # else:
    #     raise ValueError(f'Unexpected data type: {type(data)}')
    
    # Tif expects dimensions order (frames, ch, y, x)
    # But we provide order (frames, y, x, ch), so need to adjust this
    if data.ndim == 4:
        data = np.transpose(data, (0, 3, 1, 2))
    
    kwargs.setdefault('imagej', True)
    return tifffile.imwrite(filepath, data, metadata=meta, **kwargs)
    
    

         
def read_exif(filename):
    tif = tifffile.TiffFile(filename)
    exif = tif.pages[0].tags
    return exif