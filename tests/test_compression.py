import os
import unittest
import shutil
import zipfile
import tarfile
import pyzipper
from bakzip.services.zip_service import create_zip
from bakzip.services.tar_service import create_tar

class TestCompression(unittest.TestCase):
    def setUp(self):
        self.test_dir = "test_compression_data"
        self.output_dir = "test_compression_output"
        os.makedirs(self.test_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)

        # Create dummy files
        self.files = []
        for i in range(3):
            filepath = os.path.join(self.test_dir, f"file_{i}.txt")
            with open(filepath, "w") as f:
                f.write(f"Content for file {i}" * 100) # Ensure some size
            self.files.append(filepath)

    def tearDown(self):
        shutil.rmtree(self.test_dir)
        shutil.rmtree(self.output_dir)

    def test_zip_creation_normal(self):
        output_zip = os.path.join(self.output_dir, "test.zip")
        create_zip(self.files, output_zip, compression="normal")

        self.assertTrue(os.path.exists(output_zip))
        with zipfile.ZipFile(output_zip, 'r') as zf:
            self.assertEqual(len(zf.namelist()), 3)
            # Verify relative paths
            for name in zf.namelist():
                self.assertFalse(os.path.isabs(name))

    def test_zip_creation_password(self):
        output_zip = os.path.join(self.output_dir, "test_encrypted.zip")
        password = "secret_password"
        create_zip(self.files, output_zip, password=password, compression="fast")

        self.assertTrue(os.path.exists(output_zip))

        # Verify encryption using pyzipper
        with pyzipper.AESZipFile(output_zip, 'r') as zf:
            zf.setpassword(password.encode())
            # Use the full relative path as stored in the zip (including the directory)
            # Because create_zip uses os.path.dirname(os.path.commonpath(files)),
            # it preserves the parent directory name.
            expected_path = self.files[0]
            content = zf.read(expected_path)
            self.assertTrue(len(content) > 0)

    def test_tar_creation_gz(self):
        output_tar = os.path.join(self.output_dir, "test.tar.gz")
        create_tar(self.files, output_tar, compression="gz")

        self.assertTrue(os.path.exists(output_tar))
        self.assertTrue(tarfile.is_tarfile(output_tar))

        with tarfile.open(output_tar, "r:gz") as tf:
            self.assertEqual(len(tf.getnames()), 3)

    def test_tar_creation_bz2(self):
        output_tar = os.path.join(self.output_dir, "test.tar.bz2")
        create_tar(self.files, output_tar, compression="bz2")

        self.assertTrue(os.path.exists(output_tar))
        with tarfile.open(output_tar, "r:bz2") as tf:
            self.assertEqual(len(tf.getnames()), 3)

if __name__ == "__main__":
    unittest.main()
