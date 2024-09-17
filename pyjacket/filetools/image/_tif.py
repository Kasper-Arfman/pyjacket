import cv2 as cv
from skimage import io
import tifffile
import numpy as np

# def read(filepath):
#     return io.imread(filepath)

def read(filepath):
    return tifffile.imread(filepath)

def write(filepath, data: np.ndarray, meta=None, **kwargs):
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