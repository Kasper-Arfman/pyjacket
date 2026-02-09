import pandas as pd

def df_apply(df: pd.DataFrame, modify: callable, *args, **kwargs):
    return pd.DataFrame(
        modify(df.to_numpy(), *args, **kwargs), 
        index=df.index, columns=df.columns)

def apply_to_columns(df: pd.DataFrame, modify: callable):
    return df.apply(lambda col: modify(col.to_numpy()), axis=0)

def apply_to_rows(df: pd.DataFrame, modify: callable):
    return apply_to_columns(df.T, modify).T