
x = 5


def imread():
    return 'x'

# from abc import ABC
# import numpy as np

# from .imread_nd2 import imread_nd2, MetadataND2
# from .imread_tif import imread_tif





# def imread(filepath: str) -> np.ndarray:
#     """
#     """
#     if not '.' in filepath: raise ValueError(f"missing extension in filename: {filepath}")
    
#     ext = filepath.split('.')[-1]
    
#     # allow reading various data formats
#     read_function = {
#         'nd2': imread_nd2,
#         'tif': imread_tif,
#     }.get(ext)
    
#     if not read_function:
#         raise NotImplementedError(f'Cannot read image of type {ext}')
    
#     return read_function(filepath)



# class Metadata(ABC):
            
#     @property        
#     def exposure_time(self): ...
    
#     @property
#     def light_intensity(self): ...
    
#     @property
#     def period(self): ...
    
#     @property
#     def fps(self): ...
    
#     @property
#     def total_duration(self): ...






# def imread_meta(filepath: str) -> Metadata:
#     """
#     """
#     if not '.' in filepath: raise ValueError(f"missing extension in filename: {filepath}")
    
#     ext = filepath.split('.')[-1]
    
#     # allow reading various data formats
#     Constructor = {
#         'nd2': MetadataND2,
#     }.get(ext)
    
#     return Constructor(filepath)