#! /usr/env/bin python
"""
This module provides functions for creating ZIP archives.

The `create_zip` function allows you to create a ZIP archive from a list of files,
with optional compression and encryption using pyzipper.
"""
import os
import pyzipper

def create_zip(files, output, password=None, compression='normal'):
    """
    Creates a ZIP archive from a list of files.

    Args:
        files (list): A list of file paths to include in the archive.
        output (str): The path to the output ZIP file.
        password (str, optional): The password to encrypt the archive. Defaults to None.
        compression (str, optional): The compression level to use. Defaults to 'normal'.
            Supported values: 'none', 'fast', 'normal', 'maximum'.
    """
    compression_method = pyzipper.ZIP_DEFLATED
    compresslevel = None

    if compression == 'none':
        compression_method = pyzipper.ZIP_STORED
        compresslevel = None
    elif compression == 'fast':
        compresslevel = 1
    elif compression == 'normal':
        compresslevel = None # Use pyzipper's default for normal
    elif compression == 'maximum':
        compresslevel = 9

    with pyzipper.AESZipFile(output, 'w', compression=compression_method, compresslevel=compresslevel) as zip_file:
        if password:
            zip_file.setpassword(password.encode())
            zip_file.setencryption(pyzipper.WZ_AES)

        for file in files:
            # Calculate a relative path for the file inside the zip.
            # This avoids storing the full absolute path.
            # We need a common base path to make this work reliably. If files are from all over,
            # we just use the file's basename.
            try:
                common_path = os.path.dirname(os.path.commonpath(files))
                arcname = os.path.relpath(file, common_path)
            except ValueError:
                arcname = os.path.basename(file)

            try:
                zip_file.write(file, arcname)
            except OSError as e:
                print(f"Error adding {file} to zip file: {e}")

if __name__ == "__main__":
    # Example usage
    if not os.path.exists("test_dir"):
        os.makedirs("test_dir")
    with open("test_dir/test1.txt", "w") as f:
        f.write("This is a test file.")
    with open("test_dir/test2.txt", "w") as f:
        f.write("This is another test file.")

    create_zip(["test_dir/test1.txt", "test_dir/test2.txt"], "test.zip", "password", "maximum")
    print("Created test.zip")
