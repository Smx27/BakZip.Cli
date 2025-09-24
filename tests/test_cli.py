import os
import shutil
import pytest
from bakzip.utilities.file_system import process_directory
from bakzip.services.zip_service import create_zip
from bakzip.services.tar_service import create_tar

@pytest.fixture
def temp_directory_for_processing(tmpdir):
    """
    Creates a temporary directory with a more complex structure for testing processing.
    """
    test_dir = tmpdir.mkdir("test_process")
    test_dir.join("file1.txt").write("content1")
    test_dir.mkdir("subdir").join("file2.txt").write("content2")
    test_dir.join("file_to_ignore.log").write("log content")

    # Create a .bakzipignore file in the test directory being processed
    ignore_file = test_dir.join(".bakzipignore")
    ignore_file.write("*.log\n.bakzipignore\n")

    yield str(test_dir)

    shutil.rmtree(str(test_dir))


@pytest.fixture
def temp_directory_for_archiving(tmpdir):
    """
    Creates a simple temporary directory for testing archive creation.
    """
    test_dir = tmpdir.mkdir("test_archive")
    test_file = test_dir.join("test.txt")
    test_file.write("Hello, World!")
    yield str(test_dir)
    shutil.rmtree(str(test_dir))


def test_process_directory(temp_directory_for_processing):
    """
    Test the directory processing with subdirectories and ignore files.
    """
    files_to_include, skipped_files, total_skipped_size = process_directory(temp_directory_for_processing, "bakzip.log", None, None)

    assert len(files_to_include) == 2
    assert any("file1.txt" in f for f in files_to_include)
    assert any("file2.txt" in f for f in files_to_include)

    assert len(skipped_files) == 2
    assert any("file_to_ignore.log" in f for f in skipped_files)
    assert any(".bakzipignore" in f for f in skipped_files)
    assert total_skipped_size > 0


@pytest.mark.parametrize("compression_level", ['none', 'fast', 'normal', 'maximum'])
def test_create_zip(temp_directory_for_archiving, compression_level):
    """
    Test the ZIP file creation with different compression levels.
    """
    files_to_include = [os.path.join(temp_directory_for_archiving, "test.txt")]
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
def test_create_tar(temp_directory_for_archiving, compression_type, extension):
    """
    Test the TAR file creation with different compression types.
    """
    files_to_include = [os.path.join(temp_directory_for_archiving, "test.txt")]
    output_file = f"test{extension}"
    create_tar(files_to_include, output_file, compression_type)
    assert os.path.exists(output_file)
    os.remove(output_file)
