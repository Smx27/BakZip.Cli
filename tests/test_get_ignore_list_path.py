import os
import pytest
from bakzip.services.directory_processor import get_ignore_list

def test_get_ignore_list_with_directory(tmp_path):
    # Create a directory and a .bakzipignore inside it
    target_dir = tmp_path / "target"
    target_dir.mkdir()
    ignore_file = target_dir / ".bakzipignore"
    ignore_file.write_text("ignored_pattern")

    # Now it should find it when passing the directory
    patterns = get_ignore_list(str(target_dir))
    assert "ignored_pattern" in patterns

def test_get_ignore_list_wrong_directory(tmp_path):
    # Create a directory and a .bakzipignore inside it
    target_dir = tmp_path / "target"
    target_dir.mkdir()
    ignore_file = target_dir / ".bakzipignore"
    ignore_file.write_text("ignored_pattern")

    # It should NOT find it when passing a different directory
    other_dir = tmp_path / "other"
    other_dir.mkdir()
    patterns = get_ignore_list(str(other_dir))
    assert "ignored_pattern" not in patterns
