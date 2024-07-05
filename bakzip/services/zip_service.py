import os
import pyzipper
from tqdm import tqdm

def create_zip(files, output, password=None, compression='normal'):
    compression_level = {
        'fast': pyzipper.ZIP_LZMA,
        'normal': pyzipper.ZIP_DEFLATED,
        'maximum': pyzipper.ZIP_BZIP2
    }.get(compression, pyzipper.ZIP_DEFLATED)

    with pyzipper.AESZipFile(output, 'w', compression=compression_level) as zip_file:
        if password:
            zip_file.setpassword(password.encode())
            zip_file.setencryption(pyzipper.WZ_AES)

        for file in tqdm(files, desc="Zipping files", unit="file"):
            arcname = os.path.relpath(file, os.path.dirname(files[0]))
            try:
                zip_file.write(file, arcname)
            except Exception as e:
                print(f"Error writing {file} to zip file: {e}")

if __name__ == "__main__":
    create_zip(["test.txt"], "test.zip", "password", "normal")
