from dataclasses import dataclass
import os
import pickle
import pims
import numpy as np
from matplotlib.figure import Figure
from imageio import mimwrite
import pandas as pd
import matplotlib.pyplot as plt

@dataclass
class FileManager:
    data_root: str
    result_root: str
    session: str
    experiment: str
    background: str = ""
    image_filetype: str = ".bmp"
    
    # CSV_SEP = ';'

    @classmethod
    def from_path(cls, result_root, path, background: str="", image_filetype: str=".bmp"):
        """Alternate clsas constructor: Infer class attributes from the experiment pathname"""
        obj = cls.__new__(cls)
        super(cls, obj).__init__()
        obj.result_root = result_root  
        obj.data_root, obj.session, obj.experiment = cls.explode(path)[-4:-1]
        obj.background: str = background
        obj.image_filetype: str = image_filetype
        return obj

    @property
    def data_folder(self):
        return os.path.join(self.data_root, self.session, self.experiment)

    @property
    def result_folder(self):
        return os.path.join(self.result_root, self.session, self.experiment)

    @property
    def background_path(self):
        return os.path.join(self.data_root, self.session, self.background) if self.background else ''

    def abs_path(self, filename, folder=''):
        # IDK why there sometimes appears \ in the end of file (not folder)
        return os.path.join(self.result_folder, folder, filename).rstrip('\\')
        # return os.path.join(self.result_root, self.session, self.experiment, folder, filename).rstrip('\\')

    def pickle_save(self, data, filename, folder=''):
        filepath = self.abs_path(self.ensure_endswith(filename, ".pkl"), folder)
        self.ensure_exists(filepath)
        with open(filepath, 'wb') as f:
            pickle.dump(data, f)

    def pickle_load(self, filename, folder=''):
        filepath = self.abs_path(self.ensure_endswith(filename, ".pkl"), folder)
        with open(os.path.join(filepath), 'rb') as f:
            return pickle.load(f)

    def save_dataframe(self, data: pd.DataFrame, filename, folder=''):
        filename = self.ensure_endswith(filename, ".csv")
        filepath = self.abs_path(filename, folder)
        self.ensure_exists(filepath)
        data.to_csv(filepath, sep=';', float_format='%.5f')

    def load_dataframe(self, filename, folder=''):
        filepath = self.abs_path(filename, folder)
        return pd.read_csv(filepath, sep=';', index_col=0)

    def save_fig(self, handle, filename, folder=''):
        fig, _ = handle
        img_path = self.abs_path(filename, folder)
        print(f"saving figure {img_path = }")
        self.ensure_exists(img_path)
        fig.savefig(img_path, dpi=300)
        plt.close(fig)
        print(f'Saved: {folder}/{filename}')

    def load_fig(self): pass


    def save_movie(self, movie, filename, source_frames, source_fps, folder='', **kwargs):
        """
        Convert 3D array of shape (frames, height, width) to a movie file

        TODO: 
        - if this is slow, try skipping frames
        """
        speedup = None
        result_fps = 25
        result_time = 20  # [s]

        source_time = source_frames / source_fps
        print(f"original movie takes  {source_time:.0f}s ({source_time//60}min)")
        result_frames = result_fps * result_time
        df = max(source_frames // result_frames, 1)
        movie = movie[::df]
        speedup = max(source_time / result_time, 1)
        print(f"speeding up by factor {speedup:.1f}")

        if speedup > 1:
            filename = f'{speedup:.1f}x_' + filename

        mov_path = self.abs_path(filename, folder)
        mimwrite(mov_path, movie, fps=result_fps, **kwargs)
        print(f'Saved: {folder}/{filename}')


    def load_movie(self, folder='', dtype=np.uint8):
        movie_path = self.abs_path("*"+self.image_filetype, folder)
        return np.array(pims.open(movie_path), dtype=dtype)


    def read_textfile(self, filename, folder=''):
        filename = self.abs_path(filename, folder)
        with open(filename, 'r') as f:
            return f.read()


    """Useful Static Methods"""
    @staticmethod
    def explode(p, sep=os.sep):
        """Convert path a/b/c into list [a, b, c]"""
        return os.path.normpath(p).split(sep)

    @staticmethod
    def ensure_endswith(s, extension):
        # print('checking end:', s)
        return s if s.endswith(extension) else s + extension

    @staticmethod
    def ensure_exists(path): 
        folder = os.path.dirname(path)
        print('folder:', folder)
        if not os.path.exists(folder):
            os.makedirs(folder)
            print("Created", folder)

pass


if __name__ == "__main__":
    # c = FileManager('data', 'results', '2023', 'test001')
    c = FileManager.from_path('data', 'C::/idk/results/2023/test001')

    print(c.data_root)
    print(c.result_root)
    print(c.session)
    print(c.experiment)

    print(c.abs_path('haha.md'))