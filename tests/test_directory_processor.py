from bakzip.services.directory_processor import should_ignore

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
