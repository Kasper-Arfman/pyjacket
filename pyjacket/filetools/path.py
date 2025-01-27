import os

def iter_dir(directory: str, ext: str=None):
    """Iterate over files in directory.

    Args:
        directory (str): absolute path to folder
        ext (str, optional): type of file to return.
            - None: all file types
            - '/': directories only
            - '*': files only
            - '.png': only png
    
    """
    for file in os.listdir(directory):

        abs_path = os.path.join(directory, file)
        is_dir = os.path.isdir(abs_path)

        if ext=='/':  # Dirs only
            if not is_dir:  continue

        elif ext is not None:
            if ext=='*':  # Files only
                if is_dir:  continue
            
            else:  # .ext files only
                path_ext = os.path.splitext(abs_path)[1]
                if ext!=path_ext:  continue

        elif ext is None:  # All dirs all files
            pass

        yield file
