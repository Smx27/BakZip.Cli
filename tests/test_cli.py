import os
import shutil
import pytest
from bakzip.utilities.command_line_options import parse_arguments
from bakzip.services.directory_processor import process_directory
from bakzip.services.zip_service import create_zip
from bakzip.services.tar_service import create_tar

@pytest.fixture
def temp_directory(tmpdir):
    # Create a temporary directory for testing
    test_dir = tmpdir.mkdir("test_dir")
    yield test_dir
    # Clean up the temporary directory after the tests
    shutil.rmtree(str(test_dir))


def test_process_directory(temp_directory):
    # Test the directory processing
    test_dir = temp_directory
    test_file = test_dir.join("test.txt")
    test_file.write("Hello, World!")
    test_subdir = test_dir.mkdir("subdir")
    test_subfile = test_subdir.join("subfile.txt")
    test_subfile.write("Subfile content")

    files_to_include, skipped_files, total_skipped_size = process_directory(str(test_dir), "bakzip.log")
    assert len(files_to_include) == 2
    assert len(skipped_files) == 0
    assert total_skipped_size == 0

def test_create_zip(temp_directory):
    # Test the ZIP file creation
    test_dir = temp_directory
    test_file = test_dir.join("test.txt")
    test_file.write("Hello, World!")
    files_to_include = [str(test_file)]
    output_file = "test.zip"
    create_zip(files_to_include, output_file, None, 'normal')
    assert os.path.exists(output_file)
    os.remove(output_file)

def test_create_tar(temp_directory):
    # Test the TAR file creation
    test_dir = temp_directory
    test_file = test_dir.join("test.txt")
    test_file.write("Hello, World!")
    files_to_include = [str(test_file)]
    output_file = "test.tar"
    create_tar(files_to_include, output_file, 'normal')
    assert os.path.exists(output_file)
    os.remove(output_file)
