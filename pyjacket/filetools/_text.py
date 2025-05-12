def read_text(filepath: str, **kwargs):
    with open(filepath, 'r') as f:
        return f.read(**kwargs)

def write_text(filepath: str, data: str, mode='a+', **kwargs):
    if 'a+' in mode: data += '\n'

    with open(filepath, mode) as f:
        f.write(data, **kwargs)
    return