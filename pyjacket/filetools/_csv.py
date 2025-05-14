import pandas as pd

def read_csv(file_path: str, autodetect=True, **kwargs) -> pd.DataFrame:
    """Read csv data into a pandas dataframe"""
    kwargs.setdefault('index_col', 0)

    # Detect delimiter
    if autodetect:
        with open(file_path, 'r', encoding='utf-8') as f:
            first_line = f.readline()

        sep = kwargs.get('sep')
        if sep is not None:
            sep_guess = max(',;', key=first_line.count)
            if first_line.count(sep_guess) > first_line.count(sep):
                print('detected delimiter:', sep_guess)
                kwargs['sep'] = sep_guess

    return pd.read_csv(file_path, **kwargs)

def write_csv(filepath: str, data: pd.DataFrame, **kwargs):
    kwargs.setdefault('float_format', '%.5f') 
    data.to_csv(filepath, **kwargs)