import itertools
import numpy as np
from fractions import Fraction
from PIL.ExifTags import TAGS
import tifffile
import os

from . import _mp4, _tif, _nd2, _avi
from typing import Union
import imageio

"""Convention:
All arrays must be of shape
 - (height, width)
 - (frames, height, width)
 - (frames, height, width, colors)
 
 where colors are rgb by default.


"""

def slice_length(s: slice, n: int):
    """Compute how many elements belong to a slice of an iterable of size n"""
    start, stop, step = s.indices(n)
    if step > 0:
        return max(0, (stop - start + (step - 1)) // step)
    elif step < 0:
        return max(0, (start - stop - (step + 1)) // (-step))
    else:
        raise ValueError("Slice step cannot be zero")


class ExifTag:
    name: None 
    value: None

class Metadata:
    EXIF_READER = {
        'tif': _tif.read_exif,
    }

    def __init__(self, filename):
        self.filename = filename
        ext = filename.split('.')[-1]
        self.exif: dict[int, ExifTag] = self.EXIF_READER.get(ext, _tif.read_exif)(filename)
        
        self._resolution = (None, None)
        
    def get(self, i: int, default=None):
        x = self.exif.get(i)
        x = x.value if x is not None else default
        return x
    
    @property
    def shape(self):
        x = self.get(256) # tuple or None
        y = self.get(257) # tuple or None
        return (y, x)
        
   
    @property
    def bits(self):  # 258
        return self.get(258) # tuple or None
        
    @property
    def resolution(self):  # 282 and 283
        x = self.get(282) # tuple or None
        y = self.get(283) # tuple or None
        x = float(Fraction(*x)) if x else 1
        y = float(Fraction(*y)) if y else 1
        return (y, x)
    
    @property
    def resolution_unit(self):  # 296
        return self.get(296) # tuple or None
        
        
            
    # @property        
    # def exposure_time(self): ...
    
    # @property
    # def light_intensity(self): ...
    
    # @property
    # def period(self): ...
    
    # @property
    # def fps(self): ...
    
    # @property
    # def total_duration(self): ...
    
    
    @property
    def dict(self):
        return {t.name: t.value for i, t in self.exif.items() if i in TAGS}
    
    def __repr__(self):
        return f"Metadata({dir(self)})"
    
    
class ImageHandle:
    
    def __init__(self, filename, channel=None):
        self.filename = filename
        self.channel = channel or 1
        self.meta = Metadata(filename)
        self.data = self.get_data()
        self.slices = [slice(None, None, None)] * self.ndim        
        
    def get_data(self):
        raise NotImplementedError()
    
    @property
    def ndim(self):
        raise NotImplementedError()
    
    def get(self, i):
        """Go to the desired frame number. O(1)"""
        raise NotImplementedError()
        
        # N = self.max_shape[0]
        # if not (-N < i <= N):
        #     raise IndexError("Frame index out of range")
        # return self.data.asarray(key=i)
    
    """ === ...."""
    
    @property
    def max_shape(self):
        if self.data.ndim == 2:
            return self.data.shape
        
        elif self.data.ndim == 3:
            return self.data.shape
        
        elif self.data.ndim == 4:
            if self.channel:
                return self.data.shape[:3]
                
        return self.data.shape

    @property
    def shape(self):
        return [slice_length(s, n) for s, n in zip(self.slices, self.max_shape)]
    
    def copy(self):
        return type(self)(self.filename, channel=self.channel)
        
    def __iter__(self):
        start, stop, step = self.slices[0].indices(self.max_shape[0])
        for i in range(start, stop, step):
            frame = self.get(i)
            frame = frame[tuple(self.slices[1:])]
            yield frame
    
    def __repr__(self):
        base_name = os.path.basename(self.filename)
        return f'{type(self).__name__}({base_name})'
    
    def __getitem__(self, val):
        if isinstance(val, int):
            return self.get(val)
        
        elif isinstance(val, slice):
            obj = self.copy()
            obj.slices[0] = val
            return obj
        
        elif isinstance(val, tuple):
            obj = self.copy()
            obj.slices = self.slices[:]
            for i, s in enumerate(val):
                if s != slice(None, None, None):
                    obj.slices[i] = s
            return obj
            
    def __len__(self):
        return self.shape[0]
 
 
class TifImageHandle(ImageHandle):
    
    data: tifffile.TiffPage
    
    @property
    def ndim(self):
        return self.data.ndim 
    
    @property
    def dtype(self):
        return self.data.dtype
    
    def get_data(self):
        return tifffile.TiffFile(self.filename).series[0]
    
    def get(self, i):
        """Go to the desired frame number. O(1)"""
        N = self.data.shape[0]
        if not (-N < i <= N):
            raise IndexError("Frame index out of range")
        return self.data.asarray(key=i) 
    
    

    
    

def imread(filepath: str, lazy=False, channel=None) -> np.ndarray:
    """Read image data. Supports tif, nd2"""
    if not '.' in filepath: raise ValueError(f"missing extension in filename: {filepath}")
    
    ext = filepath.split('.')[-1]
    
    if lazy:
        read_function = {
            'tif': TifImageHandle,
        }.get(ext)
        return read_function(filepath, channel=channel)
  
    else:
        read_function = {
            'tif': _tif.read,
            'tiff': _tif.read,
            'png': imageio.imread,
            'jpg': imageio.imread,
            'nd2': _nd2.read,
            'avi': _avi.read,
        }.get(ext)
        
        if not read_function:
            raise NotImplementedError(f'Cannot read image of type {ext}')
    
        data = read_function(filepath)
        
        # Slice data for specified channel
        if channel is not None:
            if data.ndim == 4:
                data = data[:, channel-1, :, :]   
            else:
                raise NotImplementedError(f'Cant select channel with {data.ndim} dimensions')
            
        return data

def imwrite(filepath: str, data: Union[np.ndarray, ImageHandle], 
        meta: Metadata=None, frame_time=0.2, max_fps=30, **kwargs):
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
    
    return write_function(filepath, data, meta, 
        frame_time=frame_time, 
        max_fps=max_fps, 
        **kwargs
        )


















def imwrite_lazy(filename, h: ImageHandle, imagej=False):
    with tifffile.TiffWriter(filename) as tiff:
        for frame in h:
            tiff.write(frame, resolution=h.meta.resolution, metadata=h.meta.dict)

