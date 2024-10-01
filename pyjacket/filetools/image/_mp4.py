import math
import numpy as np
import cv2

from pyjacket import arrtools
# from pyjacket.filetools.image._image import ImageHandle

def read(filepath):
    ...
    
    
def write(filepath, data: np.ndarray, meta=None, frame_time=1/10, max_fps=60, saturate=None):
    """Data needs to be 3d array of shape (frames, height, width)"""
    if data.ndim == 4:
        # assert data.shape[-1] == 3, ValueError('Color data must have 3 channels. Consider using arrtools.false_color')
        
        return write_color(filepath, data, meta=meta, frame_time=frame_time, max_fps=max_fps, saturate=saturate)

    return write_grayscale(filepath, data, meta=meta, frame_time=frame_time, max_fps=max_fps, saturate=saturate)
        
        



def write_grayscale(filepath, data: np.ndarray, meta=None, frame_time=1/10, max_fps=60):
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


def write_color(filepath, data, meta=None, frame_time=1/10, max_fps=60, saturate=None):
    """openCV requires uint8 data, we convert it here, so uint16 input is OK"""

    fps = 1 / frame_time
    if fps > max_fps:
        step = math.ceil(fps / max_fps)
        fps /= step
        data = data[::step]
        
        
    # Define a percentage of pixels to saturate
    if saturate:
        if isinstance(saturate, (int, float)):
            percentiles = saturate
            
        else:
            percentiles = [saturate[0], 100-saturate[1]]
    else:
        percentiles = [5.0, 99.95]
    
    print(f'\nComputing percentiles for rescaling: {percentiles}')
    lb, ub = np.percentile(data, percentiles, axis=tuple(range(data.ndim-1)))
    print(f"{lb = }\n{ub = }")

    _, height, width, colors = data.shape
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # mp4 is always lossy
    out = cv2.VideoWriter(filepath, fourcc, fps, (width, height), isColor=True)
    
    print(f"\nRescaling data...")
    for frame in data:

        # Rescale data between lb and ub and cast to np.uint8
        frame = frame.astype(np.float32)
        frame = arrtools.subtract_uint(frame, lb) * 255 // (ub - lb)
        frame[frame > 255] = 255
        frame = frame.astype(np.uint8)
        
        out.write(frame) 
    out.release()


    
def read_exif(filename):
    ...