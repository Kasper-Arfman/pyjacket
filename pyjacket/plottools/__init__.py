from .styler import style
from .error import shaded_plot



# def image_scatter_overlay(img, x, y, ax=None, **kwargs):
#     cmap = kwargs.setdefault('cmap', 'Greys_r')
#     marker = kwargs.setdefault('marker', '.')
#     linestyle = kwargs.setdefault('linestyle', 'none')
#     color = kwargs.setdefault('color', None)

#     ax = ax or plt.gca()
#     ax.imshow(img, cmap=cmap)
#     ax.plot(x, y, marker=marker, linestyle=linestyle, color=color)
#     ax.set_axis_off()  ##('off')
#     ax.axis('equal')
#     plt.tight_layout()
#     return ax


__all__ =[
    'style',
]