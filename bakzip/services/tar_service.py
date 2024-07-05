import tarfile
import os
from tqdm import tqdm

def create_tar(files, output, compression='gz'):
    mode = 'w:gz' if compression == 'gz' else 'w'
    with tarfile.open(output, mode) as tar:
        for file in tqdm(files, desc="Creating TAR file", unit="file"):
            arcname = os.path.relpath(file, os.path.dirname(files[0]))
            try:
                tar.add(file, arcname=arcname)
            except Exception as e:
                print(f"Error adding {file} to tar file: {e}")

if __name__ == "__main__":
    create_tar(["test.txt"], "test.tar.gz")
