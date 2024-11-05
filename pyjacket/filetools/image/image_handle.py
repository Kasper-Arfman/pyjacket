from .metadata import Metadata
import os

def slice_length(s: slice, n: int):
    """Compute how many elements belong to a slice of an iterable of size n"""
    start, stop, step = s.indices(n)
    if step > 0:
        return max(0, (stop - start + (step - 1)) // step)
    elif step < 0:
        return max(0, (start - stop - (step + 1)) // (-step))
    else:
        raise ValueError("Slice step cannot be zero")

# class ImageHandle:
    
#     slices: list[slice]
#     operator: object
    
#     def __init__(self, filename, 
#                  channels=1
#                  ):
#         self.filename = filename
#         self.channels = channels
#         # self.meta = Metadata(filename)
#         self.data = self.get_data()
        
#         self.slices = [slice(None, None, None)] * self.ndim
        
#         self.operator = None
        
#     @property
#     def ndim(self):
#         raise NotImplementedError()
    
#     @property
#     def shape(self):
#         raise NotImplementedError()
    
#     @property
#     def dtype(self):
#         raise NotImplementedError()
    
#     def close(self):
#         raise NotImplementedError()
    
#     def get_data(self):
#         raise NotImplementedError()
    
#     def get(self, i: int):
#         """Go to the desired frame number. O(1)"""
#         raise NotImplementedError()
    

#     @property
#     def slice_shape(self):
#         """The shape of a cropped variant of this data"""
#         return [slice_length(s, n) for s, n in zip(self.slices, self.shape)]
    
#     def copy(self):
#         return type(self)(self.filename, channels=self.channels)
    

#     def __iter__(self):
#         """Return image data frame by frame"""
#         start, stop, step = self.slices[0].indices(self.shape[0])
#         for i in range(start, stop, step):
            
#             if self.operator:
#                 frame = self.operator(self, i)
#             else:
#                 frame = self.get(i)
                
                
#             frame = frame[tuple(self.slices[1:])]
#             yield frame
    
#     def __repr__(self):
#         base_name = os.path.basename(self.filename)
#         return f'{type(self).__name__}({base_name})'
    
#     def __getitem__(self, val):
#         if not all(x == slice(None, None, None) for x in self.slices):
#             print(f'\n\nWARNING: slices of slices are not supported! Instead, a new slice of the full data is computed')
        
        
        
#         if isinstance(val, int):
#             return self.get(val)
        
#         elif isinstance(val, slice):
#             obj = self.copy()
#             obj.slices[0] = val
#             return obj
        
#         elif isinstance(val, tuple):
#             obj = self.copy()
#             obj.slices = self.slices[:]
#             for i, s in enumerate(val):
#                 if s != slice(None, None, None):
#                     obj.slices[i] = s
#             return obj
            
#     def __len__(self):
#         return self.slice_shape[0]
    
#     def __enter__(self):
#         return self
    
#     def __exit__(self, *args):
#         print(f"exiting:", args)
#         self.close()
#         # super().__del__()
 
 

class ImageHandle:
    """Access image data in a lazy fashion and mimic numpy slicing.
    
    Base class, we will use it through inheritance
    """
    
    slices: list[slice]
    operator: object
    
    def __init__(self, filename, channels=2):
        self.filename = filename
        self.channels = channels
        self.data = self.open()
        # self.meta = self.get_meta()
        self.max_shape = self.get_max_shape()
        self.slices = [slice(None, None, None)] * len(self.max_shape)
        self.operator = None
        
        self.dtype = self.get(0).dtype
        
    # == IMPLEMENT THIS YOURSELF == #
    def open(self): 
        raise NotImplementedError()
    
    def close(self):
        raise NotImplementedError() 
                
    def get(self, i: int):
        raise NotImplementedError()
        
    def get_max_shape(self):
        raise NotImplementedError()
        
      
    # ============================= #
    @property
    def ndim(self):
        return len(self.shape)
 
    @property
    def shape(self):
        """The shape of a cropped variant of this data"""
        return tuple(slice_length(s, n) for s, n in zip(self.slices, self.max_shape))
    
    def copy(self):
        return type(self)(self.filename, channels=self.channels)

    def __del__(self):
        """Ensure all files are closed when the object is deleted."""
        self.close()

    def __getitem__(self, val):
        if not all(x == slice(None, None, None) for x in self.slices):
            print(f'\n\nWARNING: slices of slices are not supported! Instead, a new slice of the full data is computed')
        
        if isinstance(val, int):
            return self.get(val)
        
        elif isinstance(val, slice):
            obj = self.copy()
            obj.slices[0] = val
            return obj
        
        elif isinstance(val, tuple):
            obj = self.copy()
            obj.slices = self.slices[:]
            for i, s in enumerate(val):
                if s != slice(None, None, None):
                    obj.slices[i] = s
            return obj
 
    def __iter__(self):
        """Return image data frame by frame"""
        start, stop, step = self.slices[0].indices(self.max_shape[0])
        for i in range(start, stop, step):
            if self.operator:
                frame = self.operator(self, i)
            else:
                frame = self.get(i)
            frame = frame[tuple(self.slices[1:])]
            yield frame

    def __len__(self):
        return self.shape[0]
   
    def __repr__(self):
        base_name = os.path.basename(self.filename)
        return f'{type(self).__name__}({base_name})'