import numpy as np
import cv2

from pyjacket import arrtools

def read(filepath):
    ...
    
    
def write(filepath, data: np.ndarray, fps=30, meta=None):
    """Data needs to be 3d array of shape (frames, height, width)"""
    _, height, width = data.shape
    fourcc = cv2.VideoWriter_fourcc(*'ffv1')  # FFV1 is a lossless codec supported by ffmpeg
    out = cv2.VideoWriter(filepath, fourcc, fps, (width, height), isColor=False)
    for frame in data:
        frame = arrtools.rescale_astype(frame, np.uint8)
        out.write(frame) 
    out.release()

    
def read_exif(filename):
    ...