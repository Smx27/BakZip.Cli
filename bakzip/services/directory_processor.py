"""
This module provides functions for processing directories, including
filtering files based on a .bakzipignore file and identifying files to
include in a backup.
"""
import os
import fnmatch


def get_ignore_list():
    """
    Returns a list of ignore patterns from a .bakzipignore file.

    Args:
        directory: The directory to search for the .bakzipignore file.

    Returns:
        A list of ignore patterns.
    """
    ignore_list = []
    ignore_file = './.bakzipignore'
    if os.path.exists(ignore_file):
        with open(ignore_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                # Ignore comments and empty lines
                if line and not line.startswith('#'):
                    ignore_list.append(line)
                    if line.endswith('/'):
                        if not line.startswith('*/') and not line.startswith('/'):
                            ignore_list.extend([line + '*', '*/' + line, '*/' + line + '*'])

                    if '.' not in line and not line.endswith('/'):
                        ignore_list.extend([line + '/', line + '/*', '*/' + line, '*/' + line + '/*'])

    return ignore_list


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
        if fnmatch.fnmatch(path, pattern):
            return True
    return False


def process_directory(directory, log_file_path, verbose=False):
    """
    Processes a directory, filtering files based on a .bakzipignore file.

    Args:
        directory: The directory to process.
        log_file_path: The path to the log file.
        verbose: Whether to enable verbose logging and file size calculation for skipped files.

    Returns:
        A tuple containing:
            - A list of files to include in the backup.
            - A list of skipped files.
            - The total size of skipped files (calculated only if verbose is True).
    """
    ignore_list = get_ignore_list()
    files_to_include = []
    skipped_files = []
    total_skipped_size = 0

    log_file = None
    if verbose:
        log_file = open(log_file_path, 'w', encoding='utf-8')

    try:
        for root, dirs, files in os.walk(directory, topdown=True):
            filtered_dirs = []
            for d in dirs:
                full_path = os.path.join(root, d)
                relative_path = os.path.relpath(full_path, directory)
                if not should_ignore(relative_path, ignore_list):
                    filtered_dirs.append(d)
            dirs[:] = filtered_dirs

            log_entries = []
            for file in files:
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, directory)
                if not should_ignore(rel_path, ignore_list):
                    files_to_include.append(file_path)
                else:
                    skipped_files.append(file_path)
                    if verbose:
                        file_size = os.path.getsize(file_path)
                        total_skipped_size += file_size
                        log_entries.append(f"Skipped: {file_path} Size: {file_size} \n")

            if verbose:
                if log_entries:
                    log_file.write("".join(log_entries))
                log_file.write(f"Processed directory: {root} \n")
    finally:
        if log_file:
            log_file.close()

    return files_to_include, skipped_files, total_skipped_size
