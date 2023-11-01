import numpy as np
import cv2 as cv
from skimage.morphology import skeletonize



ring = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 1, 1, 1, 0, 0, 0],
    [0, 0, 1, 1, 1, 1, 1, 0, 0, 0],
    [0, 0, 1, 1, 1, 1, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
], np.uint8) * 255






img = ring

skel = (skeletonize(img) * 255).astype(np.uint8)

print(skel)



img_resized = cv.resize(img, (400, 400), interpolation=0)
skel_resized = cv.resize(skel, (400, 400), interpolation=0)


cv.imshow('image', img_resized)
cv.imshow('skeleton', skel_resized)
cv.waitKey(0)