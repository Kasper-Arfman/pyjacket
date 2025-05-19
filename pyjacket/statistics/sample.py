import numpy as np
from scipy import stats


def std(data: np.ndarray, n = None, **kwargs):
    if 'ddof' in kwargs:
        if kwargs['ddof'] != 1:
            raise ValueError('sample std must have ddof=1')
    return np.std(data, ddof=1)


def sem():
    ...


def ci(data: np.ndarray):
    df = len(data) - 1
    t95 = stats.t.isf(0.05/2, df)
    sem = stats.sem(data, ddof=1)
    return t95 * sem