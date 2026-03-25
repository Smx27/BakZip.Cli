from bakzip.services.directory_processor import should_ignore, process_directory
from unittest.mock import patch
import os

def test_should_ignore_exact_match():
    ignore_list = ["file.txt"]
    assert should_ignore("file.txt", ignore_list) is True
    assert should_ignore("other.txt", ignore_list) is False

def test_should_ignore_wildcard_match():
    ignore_list = ["*.tmp"]
    assert should_ignore("test.tmp", ignore_list) is True
    assert should_ignore("test.txt", ignore_list) is False

def test_should_ignore_subdirectory_wildcard():
    ignore_list = ["temp_*"]
    assert should_ignore("temp_data/file.txt", ignore_list) is True
    assert should_ignore("data/temp_file.txt", ignore_list) is False

def test_should_ignore_empty_list():
    ignore_list = []
    assert should_ignore("any_file.txt", ignore_list) is False

def test_should_ignore_path_in_subdirectory():
    ignore_list = ["sub/*.log"]
    assert should_ignore("sub/test.log", ignore_list) is True
    assert should_ignore("test.log", ignore_list) is False

def test_should_ignore_multiple_patterns():
    ignore_list = ["*.pyc", "__pycache__"]
    assert should_ignore("main.pyc", ignore_list) is True
    assert should_ignore("__pycache__", ignore_list) is True
    assert should_ignore("main.py", ignore_list) is False

def test_process_directory_skipped_size_calculation(tmpdir):
    include_file = tmpdir.join("include.txt")
    include_file.write("include")

    skip_file = tmpdir.join("skip.txt")
    skip_file.write("12345") # 5 bytes

    log_file = tmpdir.join("bakzip.log")

    # Ignore both skip.txt AND the log file itself to avoid it being included
    with patch('bakzip.services.directory_processor.get_ignore_list', return_value=['skip.txt', 'bakzip.log']):
        files_to_include, skipped_files, total_skipped_size = process_directory(str(tmpdir), str(log_file), verbose=True)

    assert len(files_to_include) == 1
    assert str(include_file) in files_to_include
    assert len(skipped_files) == 2
    assert str(skip_file) in skipped_files
    assert str(log_file) in skipped_files
    assert total_skipped_size >= 5 # log file size might be > 0

    assert os.path.exists(str(log_file))
    with open(str(log_file), 'r') as f:
        log_content = f.read()
        assert f"Skipped: {str(skip_file)} Size: 5 \n" in log_content
        assert f"Processed directory: {str(tmpdir)} \n" in log_content

def test_process_directory_no_size_when_not_verbose(tmpdir):
    include_file = tmpdir.join("include.txt")
    include_file.write("include")

    skip_file = tmpdir.join("skip.txt")
    skip_file.write("12345") # 5 bytes

    log_file = tmpdir.join("bakzip.log")

    with patch('bakzip.services.directory_processor.get_ignore_list', return_value=['skip.txt']):
        files_to_include, skipped_files, total_skipped_size = process_directory(str(tmpdir), str(log_file), verbose=False)

    assert len(files_to_include) == 1
    assert str(include_file) in files_to_include
    assert len(skipped_files) == 1
    assert str(skip_file) in skipped_files
    assert total_skipped_size == 0

    assert not os.path.exists(str(log_file))
