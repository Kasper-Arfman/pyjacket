"""
Example script for fitting (circular) arcs to a circle.

Circle_fit offers various fitting algorithms, here a standard least squares is used.
https://pypi.org/project/circle-fit/
"""

from circle_fit import standardLSQ as fit_circle  # pip install circle_fit==0.2.1
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def circle_polar(angles: np.ndarray, r, xc=0, yc=0):
    """Obtain coordinates of a circle at the specified angles.
    
    The polar coordinate system is used to allow the circle to be sampled evenly.   
    https://en.wikipedia.org/wiki/Polar_coordinate_system
    """
    x = r * np.cos(angles) + xc
    y = r * np.sin(angles) + yc
    return x, y

# Define a circle
R = 100
X0 = 10
Y0 = 13
t = 2*np.pi*np.linspace(0, 1, 400)
xtrue, ytrue = circle_polar(t, R, X0, Y0)

# Generate noisy data approximating an arc (part) of the full true circle
N = 20
REL_ERROR = 0.02
T = 5
for t1, t2 in zip(np.linspace(0.1, -0.1, T), np.linspace(0.4, 0.6, T)):
    tdata = 2 * np.pi * np.linspace(t1, t2, N)
    xdata, ydata = circle_polar(tdata, R, X0, Y0)
    xdata += REL_ERROR * np.random.normal(0, R, N)
    ydata += REL_ERROR * np.random.normal(0, R, N)

# Fit noisy data
x0f, y0f, rf, s = fit_circle(np.array([xdata, ydata]).T)  # input data should be array[[x1, y1], [x2, y2], ...]. Achieved by transposing [[x1, x2, ...], [y1, y2, ...]]
xfit, yfit = circle_polar(t, rf, x0f, y0f)

# draw everything
plt.plot(xtrue, ytrue, 'k-', label='True circle')
plt.plot(xfit, yfit, 'r-', label='fit')
plt.plot(xdata, ydata, 'b.', label='input data')
plt.legend()
plt.show()