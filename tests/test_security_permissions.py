import os
import stat
import pytest
from unittest.mock import patch, MagicMock
from bakzip.main import main

def test_archive_permissions(tmp_path):
    """
    Test that the created archive has restrictive permissions (0o600).
    """
    test_dir = tmp_path / "test_dir"
    test_dir.mkdir()
    test_file = test_dir / "test.txt"
    test_file.write_text("test content")

    output_tar = tmp_path / "backup.tar"

    # Mock arguments for the main function
    class MockArgs:
        directory = str(test_dir)
        output = str(output_tar).replace(".tar", "") # main adds .tar
        format = 'tar'
        compression = None
        encryption = 'none'
        verbose = False
        password = None

    # We need to ensure output_tar includes the extension as main() would add it
    final_output = str(output_tar)

    with patch("bakzip.main.parse_arguments", return_value=MockArgs()), \
         patch("bakzip.main.pyfiglet.figlet_format", return_value="BakZIP"):
        main()

    assert os.path.exists(final_output)
    mode = os.stat(final_output).st_mode
    # 0o600 means read/write for owner only
    assert (mode & 0o777) == 0o600

def test_log_file_permissions(tmp_path):
    """
    Test that the log file created in verbose mode has restrictive permissions (0o600).
    """
    test_dir = tmp_path / "test_dir"
    test_dir.mkdir()

    output_tar = tmp_path / "backup.tar"
    log_file = tmp_path / "bakzip.log"

    class MockArgs:
        directory = str(test_dir)
        output = str(output_tar).replace(".tar", "")
        format = 'tar'
        compression = None
        encryption = 'none'
        verbose = True
        password = None

    with patch("bakzip.main.parse_arguments", return_value=MockArgs()), \
         patch("bakzip.main.pyfiglet.figlet_format", return_value="BakZIP"):
        main()

    assert os.path.exists(log_file)
    mode = os.stat(log_file).st_mode
    assert (mode & 0o777) == 0o600
