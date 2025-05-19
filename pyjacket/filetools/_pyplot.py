import matplotlib.pyplot as plt

# DEFAULT_DPI = 300
DEFAULT_PAD = 0.03

PyplotHandle = tuple[plt.Figure, plt.Axes]

def current_handle():
    return plt.gcf(), plt.gca()

def savefig(filepath: str, handle: PyplotHandle=None, close: bool=True, **kwargs):
    fig, ax = handle or current_handle()
    # kwargs.setdefault("dpi", DEFAULT_DPI)
    kwargs.setdefault('pad_inches', DEFAULT_PAD)

    fig.savefig(filepath, **kwargs)

    if close:
        plt.close(fig)
