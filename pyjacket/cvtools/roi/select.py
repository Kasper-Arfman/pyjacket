import cv2 as cv
from screeninfo import get_monitors
from tkinter.filedialog import FileDialog, askopenfilename


import sys; from os import path
THIS_DIR = path.abspath(path.dirname( __file__ ))
sys.path.append(path.abspath(path.join(THIS_DIR, '../'*3)))

# from src.cvtools._imread import imread
# print(imread())


# print('finished')
# exit()

def min_resolution(p=1.0):
    h = p * min(m.height for m in get_monitors())
    w = p * min(m.width for m in get_monitors())
    return int(h), int(w)
    
def rescale_to_window(src, window=None):
    H, W = min_resolution(p=0.8) if window is None else window
    h, w = src.shape
    scale_factor = max(h//H, w//W)
    h, w = (h//scale_factor, w//scale_factor)
    return cv.resize(src, (h, w))
    

def select_rois(src):
    src = rescale_to_window(src)
    
    rois = []
    while True:
        roi = cv.selectROI('select rois:', src, showCrosshair=False, fromCenter=True)
        
        if not any(roi):
            break
        
        x, y, dx, dy = roi
        rois.append(roi)
        cv.rectangle(src, (x, y), (x+dx, y+dy), 255)
        
    return rois



def crop_roi():
    pass






if __name__ == '__main__':
    file=r'C:\Users\arfma005\GitHub\kaspy\src\cvtools\roi\test.tif'
    src = cv.imread(file, cv.IMREAD_GRAYSCALE)
    
    
    select_rois(
        src
    )