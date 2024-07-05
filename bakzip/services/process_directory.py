import os
from bakzip.config.bakzipignore import get_ignore_list 

def should_ignore(path, ignore_list):
    for pattern in ignore_list:
        if pattern.endswith('/'):  # Directory ignore pattern
            if os.path.isdir(path) and os.path.relpath(path).startswith(pattern.rstrip('/')):
                return True
        elif path.endswith(pattern):  # File ignore pattern
            return True
    return False

def process_directory(directory):
    ignore_list = get_ignore_list(directory)
    files_to_include = []
    for root, dirs, files in os.walk(directory):
        # Modify dirs in-place to remove ignored directories
        dirs[:] = [d for d in dirs if not should_ignore(os.path.join(root, d), ignore_list)]
        for file in files:
            file_path = os.path.join(root, file)
            if not should_ignore(file_path, ignore_list):
                files_to_include.append(file_path)
    return files_to_include
