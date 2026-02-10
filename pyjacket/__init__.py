"""Pyjacket.core contains features that extend the base language.
Its features are directly accessible from the top level:

>>> import pyjacket as pj
>>> pj.core.digits(123)  # works, but not intended
>>> pj.digits(123)
(1, 2, 3)
"""

from pyjacket.core import *

# from pyjacket import (
#     arrtools, 
#     # core,
#     # cvtools, 
#     # dna,
#     filetools, 
#     # graphs, 
#     # ntheory,
#     # stheory,
#     statistics,
#     )


__version__ = '0.2.5'

__all__ = [

    'PositiveCounter',
    # 'df_apply', 'apply_to_columns', 'apply_to_rows',
    'digits',
    'partition', 'index_nth', 'cyclic_shifts', 'batched', 'sortby', 'sliding_window',
    'sign', 'oom', 'truncate_num', 'extend_num', 'round_significant', 'truncate_significant',
    'sumprod', 'all_same',
    'slice_length',
    'truncate_str', 'extend_str', 'isplit',
]