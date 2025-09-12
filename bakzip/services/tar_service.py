#! /usr/env/bin python
"""
This module provides functions for creating TAR archives.

The `create_tar` function allows you to create a TAR archive from a list of files,
with optional compression.
"""
import tarfile
import os

def create_tar(files, output, compression='gz'):
    """
    Creates a TAR archive from a list of files.

    Args:
        files (list): A list of file paths to include in the archive.
        output (str): The path to the output TAR file.
        compression (str, optional): The compression method to use. Defaults to 'gz'.
            Supported values: 'none', 'gz' (gzip), 'bz2', 'xz'.
    """
    mode = f"w:{compression}" if compression != 'none' else 'w'

    with tarfile.open(output, mode) as tar:
        for file in files:
            # Calculate a relative path for the file inside the tar.
            try:
                common_path = os.path.dirname(os.path.commonpath(files))
                arcname = os.path.relpath(file, common_path)
            except ValueError:
                arcname = os.path.basename(file)

            try:
                tar.add(file, arcname=arcname)
            except OSError as e:
                print(f"Error adding {file} to tar file: {e}")

if __name__ == "__main__":
    # Example usage
    if not os.path.exists("test_dir"):
        os.makedirs("test_dir")
    with open("test_dir/test1.txt", "w") as f:
        f.write("This is a test file.")

    create_tar(["test_dir/test1.txt"], "test.tar.gz", "gz")
    print("Created test.tar.gz")
