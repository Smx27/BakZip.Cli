import pytest
import os
import tarfile
from unittest.mock import patch, MagicMock
from bakzip.services.tar_service import create_tar

def test_create_tar_os_error(capsys):
    """
    Test that OSError during tar.add is caught and logged to stdout.
    """
    files = ["test.txt"]
    output = "test.tar.gz"

    with patch("tarfile.open") as mock_open, \
         patch("bakzip.services.tar_service.tqdm", side_effect=lambda x, **kwargs: x):
        mock_tar = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_tar
        mock_tar.add.side_effect = OSError("Mock OS Error")

        create_tar(files, output, base_dir=".")

        captured = capsys.readouterr()
        assert "Error adding test.txt to tar file: Mock OS Error" in captured.out

def test_create_tar_path_traversal(capsys):
    """
    Test that potential path traversal is detected and skipped.
    """
    # Use paths that will definitely result in ".." or absolute arcname
    files = ["/tmp/absolute_file.txt", "../../outside_file.txt"]
    output = "test.tar.gz"
    base_dir = "/app/cwd"

    with patch("tarfile.open") as mock_open, \
         patch("bakzip.services.tar_service.tqdm", side_effect=lambda x, **kwargs: x):
        mock_tar = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_tar

        # Mocking relpath and isabs to ensure deterministic behavior across platforms
        with patch("os.path.relpath") as mock_relpath, \
             patch("os.path.isabs") as mock_isabs:
            mock_relpath.side_effect = ["/tmp/absolute_file.txt", "../../outside_file.txt"]
            # First one is absolute, second one is not but contains ..
            mock_isabs.side_effect = [True, False]

            create_tar(files, output, base_dir=base_dir)

            captured = capsys.readouterr()
            assert "Security Warning: Skipping /tmp/absolute_file.txt due to potential path traversal" in captured.out
            assert "Security Warning: Skipping ../../outside_file.txt due to potential path traversal" in captured.out
            assert mock_tar.add.call_count == 0

def test_create_tar_success(tmpdir):
    """
    Test successful TAR creation (happy path).
    """
    test_file = tmpdir.join("test.txt")
    test_file.write("hello")
    output = str(tmpdir.join("test.tar.gz"))

    # We use base_dir to ensure arcname is just 'test.txt'
    with patch("bakzip.services.tar_service.tqdm", side_effect=lambda x, **kwargs: x):
        create_tar([str(test_file)], output, base_dir=str(tmpdir))

    assert os.path.exists(output)
    assert tarfile.is_tarfile(output)
    with tarfile.open(output, "r:gz") as tar:
        names = tar.getnames()
        assert "test.txt" in names
