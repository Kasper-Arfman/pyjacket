# import math
# import numpy as np
# import cv2

# from typing import Union

# from pyjacket import arrtools
# # from pyjacket.filetools.image._image import ImageHandle

# def read(filepath):
#     ...
    

# def false_color(img: np.ndarray, colors: list[tuple]):
#     """Convert multi-channel image data into a false-colored RGB image/movie""" 
#     shape_out = (*img.shape[:-1], 3)
    
#     Rmax, Gmax, Bmax = np.array(colors).sum(axis=0)

    
#     out = np.zeros(shape_out, dtype=img.dtype)
#     for i, (R, G, B) in enumerate(colors):
#         channel = img[..., i]
#         out[..., 0] += cast(channel, R, Rmax)
#         out[..., 1] += cast(channel, G, Gmax)
#         out[..., 2] += cast(channel, B, Bmax)
#     return out

# def cast(data: np.ndarray, num: int, denom: int):
#     """ data * num / denom  (uint)
    
#     Multiply uint data by a floating point number, 
#     without changing datatype to float.
#     """
#     return (
#         data.astype(np.uint32) * num // denom
#     ).astype(data.dtype)

# def rearrange_dimensions(data, order):
#     for arr in data:
#         yield np.transpose(arr, order)


# def false_color_lazy(data, colors):
#     # convert channels
#     for arr in data:
#         yield false_color(arr, colors)

# def do_both(data, order, colors):
#     for arr in data:
#         arr = false_color(arr, colors)
#         arr = np.transpose(arr, order)
#         yield arr


    
# def write(filepath, data: Union[np.ndarray], meta=None, frame_time=1/10, max_fps=60, scale=None):
#     """Data needs to be 3d array of shape (frames, height, width)"""

#     if data.ndim not in [3, 4]:
#         raise ValueError(f"Cannot interpret data that has {data.ndim} dimensions")
    
#     elif data.ndim == 3:
#         raise NotImplementedError('Still need to do this sorry')
#         # 3 dimensions: assume (t, h, w)
#         # add the last dimension
#         # convert to an iterator of np.array shaped (h, w, 1)

#     # 4 dimensions: assume (t, h, w, ch)
#     order = (2, 0, 1)
#     colors = [
#         [255,   0, 255],
#         [  0, 255,   0],
#     ]
    
#     # data.__iter__ = false_color_lazy(data, )
#     # data.__iter__ = rearrange_dimensions(data, (2, 0, 1))

#     data.operator = do_both(data, order, colors)

#     # ch = data.shape[-1]

#     # if ch != 3:
#     #     data = false_color(data, color_map)

#     # if data.ndim == 4:
#         # assert data.shape[-1] == 3, ValueError('Color data must have 3 channels. Consider using arrtools.false_color')
        
#     return write_color(filepath, data, meta=meta, frame_time=frame_time, max_fps=max_fps, scale=scale)

#     # return write_grayscale(filepath, data, meta=meta, frame_time=frame_time, max_fps=max_fps, scale=scale)
        
        



# def write_grayscale(filepath, data: np.ndarray, meta=None, frame_time=1/10, max_fps=60):
#     """Data needs to be 3d array of shape (frames, height, width)"""
#     # Determine fps, ensuring it below max_fps
#     fps = 1 / frame_time
#     if fps > max_fps:
#         step = math.ceil(fps / max_fps)
#         fps /= step
#         data = data[::step]
        
#     # scale data to use full dynamic range
#     mi = np.min(data)
#     ma = np.max(data)
#     factor = 255/(ma - mi)

#     _, height, width = data.shape
#     fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # mp4 is always lossy
#     out = cv2.VideoWriter(filepath, fourcc, fps, (width, height), isColor=False)
#     for frame in data:

#         # This should be featured in arrtools ....
#         frame = frame.astype(np.float32)
#         frame = (frame - mi) * factor
#         frame = frame.astype(np.uint8)
        
#         out.write(frame) 
#     out.release()


# def write_color(filepath, data, meta=None, frame_time=1/10, max_fps=60, scale=None):
#     """openCV requires uint8 data, we convert it here, so uint16 input is OK"""

#     fps = 1 / frame_time
#     if fps > max_fps:
#         print('WARNING: Converting FPS')
#         step = math.ceil(fps / max_fps)
#         fps /= step
#         data = data[::step]
        
        
#     # Define a percentage of pixels to saturate
#     if scale is not None:
#         lb, ub = scale
#     else:
#         lb, ub = 0, arrtools.type_max(data[0].dtype)

#     _, height, width, colors = data.shape
#     fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # mp4 is always lossy
#     out = cv2.VideoWriter(filepath, fourcc, fps, (width, height), isColor=True)
    
#     # print(f"\nRescaling data...")
#     for frame in data:
#         # print(frame[0, :10], frame.shape)

#         # Rescale data between lb and ub and cast to np.uint8
#         frame = frame.astype(np.float32)
#         frame = arrtools.subtract_uint(frame, lb) * 255 // (ub - lb)
#         frame[frame > 255] = 255
#         frame = frame.astype(np.uint8)
        
#         out.write(frame) 
#     out.release()


    
# def read_exif(filename):
#     ...