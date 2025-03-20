""" A skeleton is a grid whose features are 1-pixel wide"""

import numpy as np
from scipy.ndimage import convolve
import numpy as np

BRANCH_PATTERNS = np.array([
    [[0, 1, 0],
     [1, 1, 1],
     [0, 0, 0]],

    [[1, 0, 1,],
     [0, 1, 0,],
     [1, 0, 0,]],

    [[1, 0, 1],
     [0, 1, 0],
     [0, 1, 0]],

    [[0, 1, 0],
     [1, 1, 0],
     [0, 0, 1]],

    [[0, 0, 1],
     [1, 1, 1],
     [0, 1, 0]],

    [[1, 0, 0],
     [1, 1, 1],
     [0, 1, 0]],

    [[0, 1, 0],
     [1, 1, 0],
     [0, 1, 0]],

    [[0, 0, 0],
     [1, 1, 1],
     [0, 1, 0]],

    [[0, 1, 0],
     [0, 1, 1],
     [0, 1, 0]],

    [[1, 0, 0],
     [0, 1, 0],
     [1, 0, 1]],

    [[0, 0, 1],
     [0, 1, 0],
     [1, 0, 1]],

    [[1, 0, 1],
     [0, 1, 0],
     [0, 0, 1]],

    [[1, 0, 0],
     [0, 1, 1],
     [1, 0, 0]],

    [[0, 1, 0],
     [0, 1, 0],
     [1, 0, 1]],

    [[0, 0, 1],
     [1, 1, 0],
     [0, 0, 1]],

    [[0, 0, 1],
     [1, 1, 0],
     [0, 1, 0]],

    [[1, 0, 0],
     [0, 1, 1],
     [0, 1, 0]],

    [[0, 1, 0],
     [0, 1, 1],
     [1, 0, 0]],

    [[1, 1, 0],
     [0, 1, 1],
     [0, 1, 0]],

    [[0, 1, 0],
     [1, 1, 1],
     [1, 0, 0]],

    [[0, 1, 0],
     [1, 1, 0],
     [0, 1, 1]],

    [[0, 1, 0],
     [0, 1, 1],
     [1, 1, 0]],

    [[0, 1, 0],
     [1, 1, 1],
     [0, 0, 1]],

    [[0, 1, 1],
     [1, 1, 0],
     [0, 1, 0]],

    [[0, 1, 0],
     [1, 1, 1],
     [0, 1, 0]],

    [[1, 0, 1],
     [0, 1, 0],
     [1, 0, 1]],
    
    ])

print(BRANCH_PATTERNS)


NEIGHBOR_KERNEL = np.array([[1, 1, 1], 
                            [1, 0, 1], 
                            [1, 1, 1]])

def critical_points(skeleton: np.ndarray):
    """Finds end points and branch points for a skeleton image"""
    assert skeleton.dtype == np.uint8, ValueError('Skeleton must be np.uint8')
    
    neighbor_count = convolve(skeleton, NEIGHBOR_KERNEL, mode="constant", cval=0)

    end_points = np.argwhere(skeleton & (neighbor_count == 1))

    branch_candidates = np.argwhere(skeleton & (neighbor_count >= 3))
    branch_points = [yx for yx in branch_candidates if is_branch_point(skeleton, *yx)]
    return end_points, branch_points

def is_branch_point(skeleton: np.ndarray, y, x):
    return any((
        np.all(pattern==skeleton[y-1:y+2, x-1:x+2]) \
            for pattern in BRANCH_PATTERNS
    ))
