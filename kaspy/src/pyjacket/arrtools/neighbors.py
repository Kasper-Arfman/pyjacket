import numpy as np

def neighbors(arr: np.ndarray, y, x):
    """List the neighboring cells in the ndarray, excluding out of bounds
    
    TODO:
     add modes for out of bounds: wrap, fill, skip
    
    """
    Y, X = arr.shape

    r = []
    if y > 0: r.append(arr[y-1, x  ])
    if x > 0: r.append(arr[y  , x-1])
    if x < X-1: r.append(arr[y  , x+1])
    if y < Y-1: r.append(arr[y+1, x  ])
    return r


def main():
    arr = np.array([
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],
    ])
    
    for y in range(3):
        for x in range(3):
            print(y, x, '->', neighbors(arr, y, x))  




if __name__ == "__main__":
    main()






