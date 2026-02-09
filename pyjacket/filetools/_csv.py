import pandas as pd

def read_csv(file_path: str, autodetect=True, **kwargs) -> pd.DataFrame:
    """Read csv data into a pandas dataframe"""
    kwargs.setdefault('index_col', 0)

    # Auto-detect separator
    if autodetect and kwargs.get('sep') is None:
        with open(file_path, 'r', encoding='utf-8') as f:
            first_line = f.readline()
        kwargs['sep'] = max(',;', key=first_line.count)
        print('detected delimiter:', kwargs['sep'])

    return pd.read_csv(file_path, **kwargs)

def write_csv(filepath: str, data: pd.DataFrame, **kwargs):
    kwargs.setdefault('float_format', '%.10e') 
    data.to_csv(filepath, **kwargs)