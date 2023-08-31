import numpy as np

# from .imread_nd2 import imread_nd2, MetadataND2
from .imwrite_tif import imwrite_tif


def imwrite(filepath: str, data: np.ndarray):
    if not '.' in filepath: 
        filepath += '.tif'
    
    ext = filepath.split('.')[-1]
    
    # allow reading various data formats
    write_function = {
        # 'nd2': imwrite_nd2,
        'tif': imwrite_tif,
    }.get(ext)
    
    if not write_function:
        raise NotImplementedError(f'Cannot write image of type {ext}')
    
    write_function(filepath, data)



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