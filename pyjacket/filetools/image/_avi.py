import cv2

def write(filepath, data, fps=30):
    """_summary_

    Args:
        filepath (_type_): _description_
        data (np.ndarray | ImageHandle): _description_
        fps (int, optional): _description_. Defaults to 30.
    """
    
    frames, height, width, *channels = data.shape
    
    # Handle color or grayscale
    if not channels:
        isColor = False
    elif len(channels) == 1 and channels[0]==3:
        isColor = True
    else:
        raise ValueError(f"Cannot interpret data of shape {data.shape}")
    
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(filepath, fourcc, fps, (width, height), isColor=isColor)
    for frame in data:
        out.write(frame)

    out.release()
    return

if __name__ == '__main__':
    import numpy as np
    # Create a sample 3D NumPy array (e.g., 100 frames of 256x256 grayscale images)
    frames = 100
    height = 256
    width = 256
    video_data = np.random.randint(0, 256, (frames, height, width), dtype=np.uint8)
    write('output_video.avi', video_data)
