x = slice(1, 50, 10)
x = (slice(5), slice(6), slice(7))

s1 = slice(0, 2, 1)
s2 = slice(2, 4, 1)

s = (s1, s2)

import numpy as np


x = np.zeros((5, 5))

print(x)

y = x[*s]
print(y)


# if i

# print(q)

# q = (*x, 5)

# print(q)


# for y in x:
#     print(y)
