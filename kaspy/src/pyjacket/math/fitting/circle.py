"""
Example script for fitting (full) circles using the circle_fit library
If your data does not sample the full circle, but only partially, see circular_arc.py

Circle_fit offers various fitting algorithms, here a standard least squares is used.
https://pypi.org/project/circle-fit/
"""

from circle_fit import standardLSQ as fit_circle
import numpy as np
import matplotlib.pyplot as plt

def circle_polar(t: np.ndarray, r: float, xc: float=0, yc: float=0):
    """Get coordinates of n equally spaced points around a circle"""
    x = r * np.cos(t) + xc
    y = r * np.sin(t) + yc
    return x, y

# Define a circle
R = 100
X0 = 10
Y0 = 13
t = np.linspace(0, 2*np.pi, 400)
xtrue, ytrue = circle_polar(t, R, X0, Y0)

# Generate noisy data approximating the true circle
N = 20
REL_ERROR = 0.05
tdata = np.linspace(0, 2*np.pi, N)
xdata, ydata = circle_polar(tdata, R, X0, Y0)
xdata += REL_ERROR * np.random.normal(0, R, N)
ydata += REL_ERROR * np.random.normal(0, R, N)

# Fit noisy data
x0f, y0f, rf, s = fit_circle(np.array([xdata, ydata]).T)  # <-- fitparameters are obtained here
xfit, yfit = circle_polar(t, rf, x0f, y0f)

# draw everything
plt.plot(xtrue, ytrue, 'k-', label='True circle')
plt.plot(xdata, ydata, 'b.', label='input data')
plt.plot(xfit, yfit, 'r-', label='fit')
plt.legend()
plt.show()