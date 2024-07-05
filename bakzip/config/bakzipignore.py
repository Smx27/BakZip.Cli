"""
This module handles file and directory exclusion based on a .bakzipignore file.
"""
import os
import fnmatch

# def get_ignore_list(directory):
#     ignore_file = os.path.join(directory, '.bakzipignore')
#     ignore_list = []
#     if os.path.exists(ignore_file):
#         with open(ignore_file, 'r') as file:
#             for line in file:
#                 line = line.strip()
#                 if line and not line.startswith('#'):
#                     ignore_list.append(line)
#     return ignore_list


def get_ignore_list():
    """
    Returns a list of patterns from a .bakzipignore file in the given directory.
    """
    ignore_list = []
    ignore_file = os.path.join('./.bakzipignore')
    if os.path.exists(ignore_file):
        with open(ignore_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    ignore_list.append(line)
    return ignore_list


def should_ignore(path, ignore_list):
    """
    Checks if a given path matches any pattern in the ignore list.
    """
    for pattern in ignore_list:
        if fnmatch.fnmatch(path, pattern):
            return True
    return False


def process_directory(directory, log_file_path):
    """
    Processes a directory, excluding files and directories based on the ignore list.
    """
    ignore_list = get_ignore_list()
    files_to_include = []
    skipped_files = []
    total_skipped_size = 0
    with open(log_file_path, 'w', encoding='utf-8') as log_file:
        for root, dirs, files in os.walk(directory, topdown=True):
            filtered_dirs = []
            for d in dirs:
                full_path = os.path.join(root, d)
                relative_path = os.path.relpath(full_path, directory)
                if not should_ignore(relative_path, ignore_list):
                    filtered_dirs.append(d)
            dirs[:] = filtered_dirs
            for file in files:
                file_path = os.path.join(root, file)
                if not should_ignore(os.path.relpath(file_path, directory), ignore_list):
                    files_to_include.append(file_path)
                else:
                    skipped_files.append(file_path)
                    total_skipped_size += os.path.getsize(file_path)
                    log_file.write(f"Skipped: {file_path}\n")
    return files_to_include, skipped_files, total_skipped_size
