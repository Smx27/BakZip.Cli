import os
import unittest
import shutil
from unittest.mock import patch
from bakzip.main import generate_ignore_file, DEFAULT_IGNORE_CONTENT
from bakzip.utilities.file_system import should_ignore, get_ignore_list

class TestIgnore(unittest.TestCase):
    def setUp(self):
        self.test_dir = "test_ignore_data"
        os.makedirs(self.test_dir, exist_ok=True)
        self.cwd = os.getcwd()
        os.chdir(self.test_dir)

    def tearDown(self):
        os.chdir(self.cwd)
        shutil.rmtree(self.test_dir)

    def test_generate_ignore_file(self):
        generate_ignore_file()
        self.assertTrue(os.path.exists(".bakzipignore"))
        with open(".bakzipignore", "r") as f:
            content = f.read()
        self.assertEqual(content, DEFAULT_IGNORE_CONTENT)

    def test_generate_ignore_file_existing(self):
        with open(".bakzipignore", "w") as f:
            f.write("existing content")

        # Capture stdout to verify message
        with patch('sys.stdout') as fake_out:
            generate_ignore_file()

        with open(".bakzipignore", "r") as f:
            content = f.read()
        self.assertEqual(content, "existing content")

    def test_should_ignore_logic(self):
        ignore_file = ".bakzipignore"
        with open(ignore_file, "w") as f:
            f.write("*.log\nnode_modules/\nsecret.txt")

        # Get the processed list of patterns
        ignore_list = get_ignore_list(".", ignore_filepath=ignore_file)

        # Files to test
        # Format: (filepath, expected_ignore_result)
        test_cases = [
            ("app.log", True),
            ("src/app.log", True),
            ("node_modules/package.json", True),
            ("src/node_modules/foo", True),
            ("secret.txt", True),
            ("not_secret.txt", False),
            ("main.py", False),
        ]

        for filepath, expected in test_cases:
            result = should_ignore(filepath, ignore_list)
            self.assertEqual(result, expected, f"Failed for {filepath}: expected {expected}, got {result}")

if __name__ == "__main__":
    unittest.main()
