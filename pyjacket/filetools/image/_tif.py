import cv2 as cv
from skimage import io
import tifffile

# def read(filepath):
#     return io.imread(filepath)

def read(filepath):
    return tifffile.imread(filepath)

def write(filepath, data, meta=None):
    return tifffile.imwrite(filepath, data, metadata=meta)
    
    

         
def read_exif(filename):
    tif = tifffile.TiffFile(filename)
    exif = tif.pages[0].tags
    return exif