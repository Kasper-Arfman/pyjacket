import math
import numpy as np
import cv2

from pyjacket import arrtools
# from pyjacket.filetools.image._image import ImageHandle

def read(filepath):
    ...
    
    
def write(filepath, data: np.ndarray, meta=None, frame_time=1/30, max_fps=60):
    """Data needs to be 3d array of shape (frames, height, width)"""
    
    # Determine fps, ensuring it below max_fps
    fps = 1 / frame_time
    if fps > max_fps:
        step = math.ceil(fps / max_fps)
        fps /= step
        data = data[::step]
        
    # scale data to use full dynamic range
    mi = np.min(data)
    ma = np.max(data)
    factor = 255/(ma - mi)

    _, height, width = data.shape
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # mp4 is always lossy
    out = cv2.VideoWriter(filepath, fourcc, fps, (width, height), isColor=False)
    for frame in data:

        # This should be featured in arrtools ....
        frame = frame.astype(np.float32)
        frame = (frame - mi) * factor
        frame = frame.astype(np.uint8)
        
        out.write(frame) 
    out.release()

    
def read_exif(filename):
    ...