import os
import shutil
import sys
from unittest.mock import MagicMock

# Mock pyzipper before importing zip_service
mock_pyzipper = MagicMock()
sys.modules['pyzipper'] = mock_pyzipper
mock_tqdm = MagicMock()
sys.modules['tqdm'] = mock_tqdm

from bakzip.services.zip_service import create_zip

def test_zip_path_traversal_protection(tmpdir):
    # Setup
    test_dir = tmpdir.mkdir("base_dir")
    test_file = test_dir.join("test.txt")
    test_file.write("content")

    # File outside the base directory
    outside_dir = tmpdir.mkdir("outside_dir")
    outside_file = outside_dir.join("outside.txt")
    outside_file.write("outside content")

    files = [str(test_file), str(outside_file)]
    output_zip = str(tmpdir.join("output.zip"))

    # Configure mock
    mock_zip_instance = mock_pyzipper.AESZipFile.return_value.__enter__.return_value

    # Run the function
    create_zip(files, output_zip)

    # Verify that zip_file.write was called for test.txt but NOT for outside.txt
    # arcname for test.txt should be "test.txt"
    # arcname for outside.txt would be "../outside_dir/outside.txt"

    called_arcnames = [call.args[1] for call in mock_zip_instance.write.call_args_list]

    assert "test.txt" in called_arcnames
    assert not any(".." in name for name in called_arcnames)
    assert not any(os.path.isabs(name) for name in called_arcnames)

    print("Security test verified with mocks.")

if __name__ == "__main__":
    # If run directly without pytest
    class TmpDir:
        def mkdir(self, name):
            d = os.path.join("/tmp", name)
            if not os.path.exists(d): os.makedirs(d)
            return Path(d)
    class Path:
        def __init__(self, p): self.p = p
        def join(self, n): return Path(os.path.join(self.p, n))
        def write(self, c):
            with open(self.p, "w") as f: f.write(c)
        def __str__(self): return self.p

    test_zip_path_traversal_protection(TmpDir())
