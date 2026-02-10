import numpy as np

def format_bytes(size):
    """1024 Bytes -> 1 KB"""
    power = 2**10
    n = 0
    power_labels = {0 : 'Bytes', 1: 'KB', 2: 'MB', 3: 'GB', 4: 'TB'}
    while size > power:  # I think this can be replaced by a log for speedup
        size /= power
        n += 1
    return size, power_labels[n]


def intel(movie: np.ndarray, title=None) -> None:
    """Print a summary of imarray properties"""
    size, unit = format_bytes(movie.size * movie.itemsize)
    print("\n".join((
        f"\n=== {title or ''} (intel) ===",
        f"movie shape: {movie.shape},  [dtype: {movie.dtype}]",
        f"intensity range: {movie.min()} - {movie.max()}",
        f"memory: {size:.2f} {unit}",
    )))