#! /usr/env/bin python
"""
This module provides functions for creating TAR archives.

The `create_tar` function allows you to create a TAR archive from a list of files,
with optional compression using gzip.
"""
import tarfile
import os
from tqdm import tqdm

def create_tar(files, output, compression='gz', base_dir=None):
    """
    Creates a TAR archive from a list of files.

    Args:
        files (list): A list of file paths to include in the archive.
        output (str): The path to the output TAR file.
        compression (str, optional): The compression method to use. Defaults to 'gz'.
            Supported values: 'gz' (gzip), None (no compression).
        base_dir (str, optional): The base directory for relative paths in the archive.
            Defaults to the directory of the first file if not provided.
    """
    mode = 'w:gz' if compression == 'gz' else 'w'
    if base_dir is None and files:
        base_dir = os.path.dirname(files[0])

    with tarfile.open(output, mode) as tar:
        for file in tqdm(files, desc="Creating TAR file", unit="file"):
            arcname = os.path.relpath(file, base_dir)
            if ".." in arcname or os.path.isabs(arcname):
                print(f"Security Warning: Skipping {file} due to potential path traversal (arcname: {arcname})")
                continue
            try:
                tar.add(file, arcname=arcname)
            except OSError as e:
                print(f"Error adding {file} to tar file: {e}")

if __name__ == "__main__":
    create_tar(["test.txt"], "test.tar.gz")
