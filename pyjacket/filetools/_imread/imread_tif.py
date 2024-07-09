import cv2 as cv
from skimage import io
import tifffile

# def imread_tif(file):
#     return cv.imread(file, cv.IMREAD_UNCHANGED)

def imread_tif(file):
    return io.imread(file)


# class MetadataTif:
    
#     def __init__(self, filename):
#         self._md = dict()
#         with tifffile.TiffFile(filename) as tif:
#             metadata = tif.pages[0].tags
#             for tag in metadata.values():
#                 self._md[tag.name] = tag.value
                
                
class MetadataTif(dict):
    
    def __init__(self, filename):
        super().__init__(self)
        with tifffile.TiffFile(filename) as tif:
            metadata = tif.pages[0].tags
            for tag in metadata.values():
                self[tag.name] = tag.value