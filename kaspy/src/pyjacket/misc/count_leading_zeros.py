import numpy as np 



a = np.array([0, 0, 0, 0, 0, 0, 0.00001, 1, -1, 5, 0, 0, 0])



def count_leading_zeros(x: np.ndarray):
    result = 0 
    for element in x:
        if element != 0:
            break
        else:
            result += 1 
    return result



z = count_leading_zeros(a)

print(z)
