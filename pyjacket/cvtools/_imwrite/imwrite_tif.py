from skimage import io




def imwrite_tif(file: str, arr):
    x = io.imsave(file, arr)
    return x