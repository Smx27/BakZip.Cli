"""
This module provides functions for processing directories, including
filtering files based on a .bakzipignore file and identifying files to
include in a backup.
"""
import os
from bakzip.config.bakzipignore import get_ignore_list


def should_ignore(path, ignore_list):
    """
    Checks if a given path should be ignored based on the ignore list.

    Args:
        path: The path to check.
        ignore_list: The list of ignore patterns.

    Returns:
        True if the path should be ignored, False otherwise.
    """
    for pattern in ignore_list:
        if pattern.endswith('/'):  # Directory ignore pattern
            if os.path.isdir(path) and os.path.relpath(path).startswith(pattern.rstrip('/')):
                return True
        elif path.endswith(pattern):  # File ignore pattern
            return True
    return False


def process_directory(directory):
    """
    Processes a directory, filtering files based on a .bakzipignore file.

    Args:
        directory: The directory to process.

    Returns:
        A list of files to include in the backup.
    """
    ignore_list = get_ignore_list()
    files_to_include = []
    for root, dirs, files in os.walk(directory):
        # Modify dirs in-place to remove ignored directories
        dirs[:] = [d for d in dirs if not should_ignore(os.path.join(root, d), ignore_list)]
        for file in files:
            file_path = os.path.join(root, file)
            if not should_ignore(file_path, ignore_list):
                files_to_include.append(file_path)
    return files_to_include
