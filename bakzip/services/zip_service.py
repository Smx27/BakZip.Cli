#! /usr/env/bin python
"""
This module provides functions for creating ZIP archives.

The `#! /usr/env/bin python` function allows you to create a TAR archive from a list of files,
with optional compression using pyzipper.
"""
import os
import pyzipper
from tqdm import tqdm

def create_zip(files, output, password=None, compression='normal', base_dir=None):
    """
    Creates a ZIP archive from a list of files.

    Args:
        files (list): A list of file paths to include in the archive.
        output (str): The path to the output ZIP file.
        password (str, optional): The password to encrypt the archive. Defaults to None.
        compression (str, optional): The compression level to use. Defaults to 'normal'.
            Supported values: 'fast', 'normal', 'maximum'.
        base_dir (str, optional): The base directory for relative paths in the archive.
            Defaults to the directory of the first file if not provided.
    """
    compression_level = {
        'fast': pyzipper.ZIP_LZMA,
        'normal': pyzipper.ZIP_DEFLATED,
        'maximum': pyzipper.ZIP_BZIP2
    }.get(compression, pyzipper.ZIP_DEFLATED)

    if base_dir is None and files:
        base_dir = os.path.dirname(files[0])

    with pyzipper.AESZipFile(output, 'w', compression=compression_level) as zip_file:
        if password:
            zip_file.setpassword(password.encode())
            zip_file.setencryption(pyzipper.WZ_AES)

        for file in tqdm(files, desc="Zipping files", unit="file"):
            arcname = os.path.relpath(file, base_dir)
            if ".." in arcname or os.path.isabs(arcname):
                print(f"Security Warning: Skipping {file} due to potential path traversal (arcname: {arcname})")
                continue
            try:
                zip_file.write(file, arcname)
            except OSError as e:
                print(f"Error adding {file} to tar file: {e}")

if __name__ == "__main__":
    create_zip(["test.txt"], "test.zip", "password", "normal")
