import os
import shutil
import pytest
from bakzip.utilities.file_system import process_directory
from bakzip.services.zip_service import create_zip
from bakzip.services.tar_service import create_tar

@pytest.fixture
def temp_directory(tmpdir):
    """
    Creates a temporary directory for testing.
    """
    test_dir = tmpdir.mkdir("test_dir")
    # Create a dummy file in the test directory
    test_file = test_dir.join("test.txt")
    test_file.write("Hello, World!")
    yield test_dir
    shutil.rmtree(str(test_dir))

def test_process_directory(temp_directory):
    """
    Test the directory processing.
    """
    files_to_include, skipped_files, total_skipped_size = process_directory(str(temp_directory), "bakzip.log", None, None)
    assert len(files_to_include) == 1
    assert "test.txt" in files_to_include[0]
    assert len(skipped_files) == 0
    assert total_skipped_size == 0

@pytest.mark.parametrize("compression_level", ['none', 'fast', 'normal', 'maximum'])
def test_create_zip(temp_directory, compression_level):
    """
    Test the ZIP file creation with different compression levels.
    """
    files_to_include = [str(temp_directory.join("test.txt"))]
    output_file = f"test_{compression_level}.zip"
    create_zip(files_to_include, output_file, None, compression_level)
    assert os.path.exists(output_file)
    os.remove(output_file)

@pytest.mark.parametrize("compression_type, extension", [
    ('none', '.tar'),
    ('gz', '.tar.gz'),
    ('bz2', '.tar.bz2'),
    ('xz', '.tar.xz')
])
def test_create_tar(temp_directory, compression_type, extension):
    """
    Test the TAR file creation with different compression types.
    """
    files_to_include = [str(temp_directory.join("test.txt"))]
    output_file = f"test{extension}"
    create_tar(files_to_include, output_file, compression_type)
    assert os.path.exists(output_file)
    os.remove(output_file)
