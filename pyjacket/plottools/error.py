from matplotlib.axes import Axes
import matplotlib.pyplot as plt
import numpy as np

def error_plot(x: np.ndarray, y: np.ndarray, dy: np.ndarray, ax: Axes=None, **kwargs):
    x = np.array(x)
    y = np.array(y)
    dy = np.array(dy)
    ax = ax or plt.gca()

    line, = ax.plot(x, y, **kwargs)
    color = line.get_color()
    ax.plot(x, y+dy, color=color, linestyle='--')
    ax.plot(x, y-dy, color=color, linestyle='--')
    return

def shaded_plot(x, y, dy, ax: Axes=None, alpha=0.1, **kwargs):
    kwargs.setdefault('linestyle', '-')
    # kwargs.setdefault('marker', '*')


    x = np.array(x)
    y = np.array(y)
    dy = np.array(dy)
    ax = ax or plt.gca()

    if True:
        # Line
        line, = ax.plot(x, y, **kwargs)
        color = line.get_color()
    else:
        # Scatter
        sc = ax.scatter(x, y, **kwargs)
        color = sc.get_facecolor()

    ax.fill_between(x, y-dy, y+dy, color=color, alpha=alpha)
    return

if __name__ == "__main__":
    from styler import style

    def main():
        style.use('sprakel')

        x = [1, 2, 3, 4]
        y = [10, 11, 12, 13]
        y2 = [12.5, 12, 11.5, 11]

        dy = [.2, .3, .3, .2]


        shaded_plot(x, y, dy)
        shaded_plot(x, y2, dy, alpha=0.1)
        plt.show()


    main()