import os
import numpy as np
import pandas as pd

from . import _csv, _json, _path, _pickle, _pyplot, _text, image
from pyjacket import string

class Writeable:
    def write(self):
        raise NotImplementedError()
    
    def save(self):
        raise NotImplementedError()


class FileManager:
    """Make it easy to read/write files"""

    def __init__(self, 
        src_root: str=None, dst_root: str=None, rel_path: str='', base: str='', CSV_SEP: str=';'):
        """
        base: provide base name of file to wrap all results in an additional folder
        """
        self.src_root = src_root if src_root is not None else os.getcwd()
        self.dst_root = dst_root if dst_root is not None else os.getcwd()
        self.rel_path = rel_path
        self.base = base
        self.CSV_SEP = CSV_SEP

    @property
    def src_folder(self):
        return os.path.join(self.src_root, self.rel_path)

    @property
    def dst_folder(self):
        return os.path.join(self.dst_root, self.rel_path, self.base)


    """ === PATH ==="""

    def abs_path(self, dst: bool, filename: str='', folder: str=''):
        abspath = self.dst_path if dst else self.src_path
        return abspath(filename=filename, folder=folder)

    def src_path(self, filename: str='', folder: str=''):
        """Absolute path to a file in the src directory"""
        return os.path.join(self.src_folder, folder, filename).rstrip('\\')
    
    def dst_path(self, filename: str='', folder: str=''):
        """Absolute path to a file in the dst directory"""
        return os.path.join(self.dst_folder, folder, filename).rstrip('\\')

    def iter_dir(self, folder: str='', ext: str=None, dst=False, nat=True, exclude: set=None, **kwargs):
        """Obtain files/folders in the <root>/<rel_path>/<folder>
        
        ext: types of files to return
         - None: yield all file types
         - '/': yield directories only
         - '.png': yield only png.
        
        """
        # abspath = self.dst_path if dst else self.src_path
        # directory = abspath(folder=folder)
        directory = self.abs_path(dst, folder=folder)
        yield from _path.iter_dir(directory, ext, nat=nat, exclude=exclude, **kwargs)

    def list_dir(self, folder='', ext: str=None, dst=False, nat=True, exclude: set=None, **kwargs):
        # abspath = self.dst_path if dst else self.src_path
        # directory = abspath(folder=folder)
        directory = self.abs_path(dst, folder=folder)
        return _path.list_dir(directory, ext, nat, exclude, **kwargs)

    def walk(self, folder: str='', ext: str=None, depth: int=None, dst=False, **kwargs):
        # abspath = self.dst_path if dst else self.src_path
        # directory = abspath(folder=folder)
        directory = self.abs_path(dst, folder=folder)
        # print(f"{directory = }")

        yield from _path.walk(directory, ext, depth, **kwargs)

    def delete(self, filename: str, folder: str='', dst: bool=True, verbose=True):
        abs_path = self.abs_path(dst, filename, folder)
        print(f'Deleting', abs_path)

        if not self.exists(filename, folder, dst):
            raise ValueError('Cannot delete', abs_path)


        return _path.delete(abs_path, os.path.join(folder, filename), verbose)
        # if os.path.exists(abs_path):
        #     os.remove(abs_path)
        #     print('Deleted', filename)

    def exists(self, filename: str, folder: str, dst: bool=False):
        file_path = self.abs_path(dst, filename, folder)
        return os.path.exists(file_path)

    @staticmethod
    def explode(path: str, sep=os.sep, **kwargs):
        return _path.explode(path, sep, **kwargs)
        # """Convert path a/b/c into list [a, b, c]"""
        # return os.path.normpath(path).split(sep)

    @staticmethod
    def ensure_exists(path: str, verbose=True, **kwargs): 
        return _path.ensure_exists(path, verbose, **kwargs)
        # folder = os.path.dirname(path)
        # # print('folder:', folder)
        # if not os.path.exists(folder):
        #     os.makedirs(folder)
        #     print("Created", folder)

    @staticmethod
    def handle_extension(filename: str, valid_extensions: list, **kwargs):
        return _path.handle_extension(filename, valid_extensions, **kwargs)
        # default_ext = valid_extensions[0]
        # _, ext = os.path.splitext(filename)

        # if ext not in valid_extensions:
        #     if ext == '':  # no extension is provided
        #         filename = filename + default_ext
        #     else:  # non-supported extension
        #         warnings.warn(Warning(f'Unsupported file format ({ext}): {filename}, using {default_ext} instead.'))
        #         filename = filename + default_ext

        # return filename


    """ === STRING === """

    @staticmethod
    def ensure_endswith(s: str, extension: str, **kwargs):
        return string.ensure_endswith(s, extension, **kwargs)
        # return s if s.endswith(extension) else s + extension


    """ === READING/WRITING FILES ==="""

    def read_before(self, filename: str, folder: str, dst: bool, valid_extensions: list):
        """Prepare the filepath for reading a file
        
        filename: str
        
        folder: str
        
        dst: bool
        
        valid_extensions: list
          the first element of this list will be used as default.
        """
        filename = self.handle_extension(filename, valid_extensions)
        filepath = self.dst_path if dst else self.src_path  
        return filepath(filename, folder)
            
    # def read_after(self):
    #     """what to do after a file is read"""
    
    def write_before(self, filename: str, folder: str, valid_extensions: list):
        """Finds the absolute path and creates folders when necessary """
        if valid_extensions:
            filename = self.handle_extension(filename, valid_extensions)
        filepath = self.dst_path(filename, folder)
        self.ensure_exists(filepath)
        return filepath
        
    def write_after(self, filepath):
        """..."""
        rel_path = os.path.relpath(filepath, self.dst_folder)
        print(f'Saved: {rel_path}')
           
    def read(self, filename: str, *args, folder: str='', dst: bool=False, **kwargs):
        """Read files of a standard format such as .txt"""
        filepath = self.read_before(filename, folder, dst, [])
        with open(filepath, 'r') as f:
            return f.read(*args, **kwargs)
        
    def write(self, filename: str, data: Writeable, *args, folder: str='', **kwargs):
        """Writes any object that implements a write function"""
        filepath = self.write_before(filename, folder, [])
        if hasattr(data, 'write'):
            data.write(filepath, *args, **kwargs)
        elif hasattr(data, 'save'):
            data.save(filepath, *args, **kwargs)
        else:
            raise ValueError(f'Expected data obj that implements .save or .write, instead got data of type: {type(data)}. ')
        self.write_after(filepath)

    def read_pickle(self, filename: str, folder: str='', dst: bool=False, **kwargs):
        """Read a python object from a pickle file.
        
        dst_folder: bool
          read a file in the dst path rather than the src path
        """
        filepath = self.read_before(filename, folder, dst, ['.pkl'])
        return _pickle.read_pickle(filepath, **kwargs)

    def write_pickle(self, filename: str, data: object, *args, folder: str='', **kwargs):
        """Write a python object to a pickle file."""
        filepath = self.write_before(filename, folder, ['.pkl'])
        _pickle.write_pickle(filepath, data, **kwargs)
        self.write_after(filepath)
            
    def read_csv(self, filename: str, folder: str='', dst: bool=False, **kwargs) -> pd.DataFrame:
        """Read csv data into a pandas dataframe"""
        filepath = self.read_before(filename, folder, dst, ['.csv'])
        kwargs.setdefault('sep', self.CSV_SEP)
        return _csv.read_csv(filepath, **kwargs)

    def write_csv(self, filename: str, data: pd.DataFrame, folder: str='', **kwargs):
        """Save a csv data to a csv file"""
        filepath = self.write_before(filename, folder, ['.csv'])
        kwargs.setdefault('sep', self.CSV_SEP)
        _csv.write_csv(filepath, data, **kwargs)
        self.write_after(filepath)
        
    def read_img(self, filename: str, folder='', dst=False, **kwargs):
        """Read image data into a numpy.ndarray of shape:
            (frames, t, y, x, channels)
        """
        valid_extensions = [
            '.tif', 
            '.tiff', 
            '.png', 
            '.jpg',
            '.avi',
            '.mov',
            '.mp4',
            '.bmp',
            '',  # allow folders to be specified
            ]
        filepath = self.read_before(filename, folder, dst, valid_extensions)
        # print(f'Reading: {filepath}')
        return image.read_img(filepath, **kwargs)
    
    def read_img_meta(self, filename: str, folder='', dst_folder=False):
        """Get the Exif (meta)data for an image file. 
        This contains various acquisition details such as exposure time
        """
        getter = self.dst_path if dst_folder else self.src_path  
        filepath = getter(filename, folder)
        return image.read_img_meta(filepath)
    
    def write_img(self, filename: str, data: np.ndarray, folder: str='', **kwargs):
        """Write numpy.ndarray data to img file format
        
        TODO: allow log scale display
        """
        valid_extensions = [
            '.tif', 
            '.tiff', 
            '.png', 
            '.jpg',
            '.avi',
            '.mov',
            '.mp4',
            '.bmp',
            ]
        filepath = self.write_before(filename, folder, valid_extensions)
        image.write_img(filepath, data, **kwargs)
        self.write_after(filepath)
        
    def read_json(self, filename: str, folder='', dst=False, **kwargs):
        filepath = self.read_before(filename, folder, dst, ['.json'])
        return _json.read_json(filepath, **kwargs)

    def write_json(self, filename: str, data: dict, folder: str='', **kwargs):
        filepath = self.write_before(filename, folder, ['.json'])
        _json.write_json(filepath, data, **kwargs)
        self.write_after(filepath)

    def read_txt(self, filename: str, folder: str='', dst=False, **kwargs):
        filepath = self.abs_path(dst, filename, folder)
        return _text.read_text(filepath, **kwargs)

    def write_txt(self, filename: str, data: dict, folder: str='', mode='a+', **kwargs):
        filepath = self.write_before(filename, folder, ['.txt'])
        return _text.write_text(filepath, data, mode, **kwargs)


    """ === Pyplot === """

    def savefig(self, filename, handle=None, folder='', close=True, **kwargs):
        """Called 'save' rather than 'write' because the original data cannot be retrieved from the file."""
        filepath = self.write_before(filename, folder, ['.png'])
        _pyplot.savefig(filepath, handle, close, **kwargs)
        self.write_after(filepath)



# if __name__ == "__main__":
#     # c = FileManager('data', 'results', '2023', 'test001')
#     c = FileManager.from_path('data', 'C::/idk/results/2023/test001')

#     print(c.src_root)
#     print(c.dst_root)
#     print(c.rel_path)
#     print(c.experiment)

#     print(c.abs_path('haha.md'))