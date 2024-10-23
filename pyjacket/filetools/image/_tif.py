import cv2 as cv
from skimage import io
import tifffile
import numpy as np

from typing import Union
# from pyjacket.filetools.image._image import TifImageHandle

# def read(filepath):
#     return io.imread(filepath)

class TifImageHandle(ImageHandle):
    
    data: tifffile.TiffPage
    
    @property
    def ndim(self):
        n = self.data.ndim 
        if self.channels > 1:
            n += 1
        return n
    
    @property
    def shape(self):
        """Sizes of each of the dimensions"""
        if self.ndim < 4:
            return self.data.shape
        
        else:
            # Ensure channel becomes last dimension
            # This is needed to interface with imageJ format
            
            # If 
            if len(self.data.shape) == 3:
                t, y, x = self.data.shape
                
                
                t //= self.channels
                c = self.channels
                
            else:
                t, c, y, x = self.data.shape
            
            
            
            return (t, y, x, c)
    
    @property
    def dtype(self):
        return self.data.dtype
    
    def get_data(self):
        series = tifffile.TiffFile(self.filename).series
        page = series[0]
        return page
    
    def get(self, i):
        """Go to the desired frame number. O(1)"""
        N = self.shape[0]
        if not (-N < i <= N):
            raise IndexError("Frame index out of range")
        
        if self.ndim == 4:
            # 4d data is really stored in a 3d format for some reason
            # So we need to unzip the channels
            num_channels = self.shape[3]
            i *= num_channels
            
            # stack all of the color channels
            stack = [self.data.asarray(key=i+di) for di in range(num_channels)]
            frame = np.stack(stack, axis=-1)
        else:
            frame = self.data.asarray(key=i) 
        return frame
   

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


def imwrite_tif(file: str, arr):
    x = io.imsave(file, arr)
    return x