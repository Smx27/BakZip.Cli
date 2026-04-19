import os
from bakzip.services.directory_processor import get_ignore_list

def test_get_ignore_list_from_specified_directory(tmpdir):
    # Create a target directory
    target_dir = tmpdir.mkdir("target")
    ignore_file = target_dir.join(".bakzipignore")
    ignore_file.write("*.log\n# comment\nsecret.txt")

    # Now get_ignore_list should take directory as an argument
    # and use it to find '.bakzipignore'.
    patterns = get_ignore_list(str(target_dir))

    # It should correctly parse the patterns
    assert "secret.txt" in patterns
    assert "*.log" in patterns
    assert "# comment" not in patterns
    assert len(patterns) >= 2 # plus some auto-generated ones for directories/wildcards

def test_get_ignore_list_no_file(tmpdir):
    # If the file doesn't exist, it should return an empty list
    target_dir = tmpdir.mkdir("empty")
    patterns = get_ignore_list(str(target_dir))
    assert patterns == []
