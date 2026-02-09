import pickle

def read_pickle(filepath: str, **kwargs):
    if not filepath.endswith('.pkl'):
        filepath += '.pkl'

    with open(filepath, 'rb') as f:
        return pickle.load(f, **kwargs)
      
def write_pickle(filepath: str, data, **kwargs):
    with open(filepath, 'wb') as f:
        pickle.dump(data, f, **kwargs)