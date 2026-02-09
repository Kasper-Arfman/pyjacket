from functools import wraps
import os
import natsort
import warnings

def ensure_exists(filepath, verbose=True): 
    folder = os.path.dirname(filepath)
    if not os.path.exists(folder):
        os.makedirs(folder)
        if verbose:  print("Created", folder)

def explode(path: str, sep=os.sep):
    """Convert path a/b/c into list [a, b, c]"""
    return os.path.normpath(path).split(sep)

@wraps(os.path.exists)
def exists(path: str, *args, **kwargs):
    return os.path.exists(path, *args, **kwargs)

def delete(path: str, alias=None, verbose=True):
    if os.path.exists(path):
        os.remove(path)
        if verbose:  print('Deleted', alias or path)


def handle_extension(filename: str, valid_extensions: list):
    default_ext = valid_extensions[0]
    _, ext = os.path.splitext(filename)

    if ext not in valid_extensions:
        if ext == '':  # no extension is provided
            filename = filename + default_ext
        else:  # non-supported extension
            warnings.warn(Warning(f'Unsupported file format ({ext}): {filename}, using {default_ext} instead.'))
            filename = filename + default_ext

    return filename

def iter_dir(dirpath: str, ext: str=None, nat=True, exclude: set=None):
    """Obtain files/folders in the <root>/<rel_path>/<folder>
    
    ext: types of files to return
        - None: yield all file types
        - '/': yield directories only
        - '.png': yield only png.
    """
    exclude = set(exclude) if exclude is not None else set()

    files = os.listdir(dirpath)
    if nat:
        files = natsort.natsorted(files)

    for file in files:

        if file in exclude:  continue

        if ext is not None:
            abs_path = os.path.join(dirpath, file)
            is_dir = os.path.isdir(abs_path)
            path_ext = os.path.splitext(abs_path)[1]
            is_match = lambda ext: ext.lstrip('.')==path_ext.lstrip('.')

            if isinstance(ext, str):
                if ext=='/':  # Dirs only
                    if not is_dir:  continue

                elif ext=='*':  # Files only
                    if is_dir:  continue

                elif not is_match(ext):
                    continue
            
            elif isinstance(ext, (list, tuple)):
                if not any(is_match(ext_item) for ext_item in ext):
                    continue
                    
        yield file

def list_dir(dirpath: str, ext: str=None, nat=True, exclude: set=None, **kwargs):
    return list(iter_dir(dirpath, ext, nat, exclude, **kwargs))

def walk(path: str, ext: str=None, depth: int=None):
    """
    Yield paths to files or directories at a specific depth, filtered by extension.

    Args:
        root_path (str): Root directory to search.
        ext (str, optional): File type to return. Use
            - None : all files and directories
            - /    : directories only
            - *    : files only
            - .txt : txt files only
        depth (int, optional): Depth to search. None means all depths.

    Yields:
        str: File or directory path matching the criteria.

    Example:
        >>> for path in walk("measurement", ext=".tif", depth=3):
        ...     print(path)
    """
    # print(f"{path = } {ext = } {depth = }")

    path = os.path.abspath(path)
    root_depth = path.count(os.sep)

    for child_path, _, files in os.walk(path):
        child_depth = os.path.abspath(child_path).count(os.sep) - root_depth
        rel_dir_path = os.path.relpath(child_path, path) if child_path != path else ''

        # print(child_path)

        # yield folders
        if depth is None or child_depth == depth + 1:
            if ext in [None, '/']:
                yield rel_dir_path

        # yield files
        if depth is None or child_depth == depth:
            if ext != '/':
                for file_name in files:
                    if ext not in [None, '*']:
                        _, file_ext = os.path.splitext(file_name)
                        if file_ext.lstrip('.') != ext.lstrip('.'):
                            continue

                    rel_file_path = os.path.join(rel_dir_path, file_name) if rel_dir_path else file_name
                    yield rel_file_path

if __name__ == "__main__":

    def main():
        root = r'C:\Users\arfma005\Documents\GitHub\pyjacket\pyjacket'
        for rel_path in walk(root, ext=None, depth=1):
            print(rel_path)



    main()
    print('\nFinished')