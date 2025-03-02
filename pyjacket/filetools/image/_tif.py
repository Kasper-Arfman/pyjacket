import tifffile
import numpy as np
from .models import ImageHandle, Metadata, ImageReader, ExifTag

from pyjacket import arrtools
from fractions import Fraction


def get_axes(file_path):
    with tifffile.TiffFile(file_path) as tif:
        axes = tif.series[0].axes
    return axes

class TifMetadata(Metadata):

    def __init__(self, filename):
        self.filename = filename

        with tifffile.TiffFile(filename) as tif:
            series = tif.series[0]
            self._shape = series.shape
            self._dtype = series.dtype
            self._axes = series.axes
            self._bits = arrtools.bits(self._dtype)

            # r = self.get_resolution(tif)
            # print(r)

        self.exif = self.read_exif(filename)
        print(self.resolution)

    @property
    def shape(self): return self._shape

    @property
    def axes(self): return self._axes

    @property
    def bits(self): return self._bits

        

    
    def get_resolution(self, tif):
        if tif.pages[0].tags.get('XResolution') and tif.pages[0].tags.get('YResolution'):
            x_res = tif.pages[0].tags['XResolution'].value
            y_res = tif.pages[0].tags['YResolution'].value

            print(x_res, y_res)

            spatial_resolutions = (x_res[1] / x_res[0], y_res[1] / y_res[0])  # (x, y resolution)


            # Add z-resolution if provided
            z_res = None
            if 'CZ_LSMINFO' in tif.pages[0].tags:
                z_res = tif.pages[0].tags['CZ_LSMINFO'].value.get('VoxelSizeZ', None)
                if z_res:
                    spatial_resolutions = (*spatial_resolutions, z_res)

        # Resolution unit
        resolution_unit = tif.pages[0].tags.get('ResolutionUnit', None)
        if resolution_unit:
            resolution_unit = resolution_unit.value

        # Temporal resolution (if available)
        for page in tif.pages:
            if 'ImageDescription' in page.tags:
                desc = page.tags['ImageDescription'].value
                if 'Time' in desc:  # A common tag for temporal resolution
                    temporal_resolution = desc.split('Time=')[-1].split()[0]  # Example parsing

        return {
            'spatial_resolutions': spatial_resolutions,
            'resolution_unit': resolution_unit,
            'temporal_resolution': temporal_resolution,
        }


    def t_resolution():
        ...

    def z_resolution():
        ...

    def x_resolution(self):
        x = self.exif_value(282) # tuple or None
        return float(Fraction(*x)) if x else 1

    def y_resolution(self):
        x = self.exif_value(283) # tuple or None
        return float(Fraction(*x)) if x else 1
    
    def read_exif(self, file_path)  -> dict[int, ExifTag]:
        tif = tifffile.TiffFile(file_path)
        exif = tif.pages[0].tags
        return exif

    def exif_value(self, i: int, default=None):
        x = self._exif.get(i)
        x = x.value if x is not None else default
        return x

    @property
    def resolution(self):  # 282 and 283
        x = self.exif_value(282) # tuple or None
        y = self.exif_value(283) # tuple or None
        x = float(Fraction(*x)) if x else 1
        y = float(Fraction(*y)) if y else 1
        return (y, x)

    # @property
    # def resolution_unit(self):  # 296
    #     return self.exif_value(296) # tuple or None

    # @property
    # def dict(self):
    #     return {t.name: t.value for i, t in self._exif.items() if i in TAGS}

    def __repr__(self):
        return f"Metadata({dir(self)})"


class TifImageHandle(ImageHandle):
    """Read image data from a tif file"""
    
    data: tifffile.TiffPage
    
    def open(self):
        self.file = tifffile.TiffFile(self.file_path)
        data = self.file.series[0]  # TiffPage
        return data  
    
    def close(self):
        self.file.close()
    
    def get(self, i):
        """Go to the desired frame number. O(1)"""
        N = self.shape[0]
        if not (-N < i <= N):
            raise IndexError("Frame index out of range")

        i *= self.unzip
        frame: np.ndarray = self.data.asarray(key=i) 

        # Unzipping the data
        if self.unzip > 1:
            stack = np.empty((*frame.shape, self.unzip), dtype=frame.dtype)
            stack[..., 0] = frame
            for di in range(1, self.unzip):
                stack[..., di] = self.data.asarray(key=i+di) 
            frame = stack
        
        elif self.ndim == 4:

            # In case we need to transpose the axes
            # the indices might be different
            # reshuffle
            axes = get_axes(self.file_path)
            # print(f"{axes = }")
            if axes in ('ZCYX', 'TCYX'):
                self.data.asarray(key=i)

                num_channels = self.shape[-1]
                i *= num_channels
                stack = [self.data.asarray(key=i+di) for di in range(num_channels)]
                frame = np.stack(stack, axis=-1)

            # i *= num_channels

            else:
                raise ValueError(f'Unsupported axes format: {axes = }')


            # # 4d data is really stored in a 3d format for some reason
            # # So we need to unzip the channels
            # num_channels = self.shape[3]
            # i *= num_channels
            
            # # stack all of the color channels
            # stack = [self.data.asarray(key=i+di) for di in range(num_channels)]
            # frame = np.stack(stack, axis=-1)

        return frame
    
    def get_max_shape(self):
        

        # In case of transposing axes
        # Decide whether we need to transpose
        axes = get_axes(self.file_path)
        # print(f"{axes = }")
        if axes in ('ZCYX', 'TCYX'):
            t, ch, y, x = self.data.shape
            max_shape = (t, y, x, ch)
            self.transpose = (0, 2, 3, 1)

        elif axes in ('YXS', 'ZYX', 'ZYXS', 'YX'):
            max_shape = self.data.shape
            self.transpose = False

        else:
            raise ValueError(f'Unsupported axes format: {axes = }')


        # In case of unzipping
        ch = self.unzip
        if ch != 1:
            assert len(max_shape) == 3, ValueError(f'Can only unzip 3D data, got {len(max_shape)}')
            t, y, x = max_shape
            max_shape = (t//ch, y, x, ch)
            
        return max_shape


class TifReader(ImageReader):

    def read(self, file_path: str, **kwargs) -> np.ndarray:
        data = tifffile.imread(file_path)
        
        # Decide whether to transpose based on the meta data
        transpose = False
        axes = get_axes(file_path)
        print(f"{axes = }")

        transpose = False
        if axes in ('ZCYX', 'TCYX'):
            transpose = True
        elif axes in ('YXS', 'ZYX', 'ZYXS', 'YX'):
            transpose = False
        else:
            raise ValueError(f'new axes format: {axes = }')
        
        # Ensure channels are in last dimension
        if transpose and data.ndim == 4:
            data = np.transpose(data, (0, 2, 3, 1))

        return data

    def read_lazy(self, file_path: str, **kwargs) -> TifImageHandle:
        return TifImageHandle(file_path, **kwargs)

    def seq_read(self, file_path: str, **kwargs) -> np.ndarray:
        return self.read(file_path, **kwargs)

    def seq_read_lazy(self, file_path: str, **kwargs) -> TifImageHandle:
        raise NotImplementedError()


    def read_meta(self, file_path: str, **kwargs) -> TifMetadata:
        return TifMetadata(file_path)


    def write(self, file_path: str, data: np.ndarray, meta:Metadata=None, **kwargs):
        if meta is not None:
            kwargs.setdefault('metadata', meta)

        if data.ndim not in [2, 3, 4]:
            raise ValueError(f'Cannot write .tif with {data.ndim} dimensions')
        
        elif data.ndim == 2:  #    (y, x)
            ...      
        elif data.ndim == 3:  # (t, y, x)
            # 3 dimensions: assume (t, h, w)
            # add the last dimension
            ...
        elif data.ndim == 4:  # (t, y, x, ch)
            # Reshuffle dimensions to (t, ch, y, x)
            data = np.transpose(data, (0, 3, 1, 2))
        
        kwargs.setdefault('imagej', True)
        return tifffile.imwrite(file_path, data, **kwargs)

    def write_lazy(self, file_path: str, data: ImageHandle, meta:Metadata=None, **kwargs):
        return self.write(file_path, data, meta=None, **kwargs)