import unittest
from unittest.mock import patch, MagicMock
import os
import sys
from bakzip.main import main

class TestSecurityFix(unittest.TestCase):
    @patch('bakzip.main.parse_arguments')
    @patch('bakzip.main.getpass.getpass')
    @patch('bakzip.main.pyfiglet.figlet_format', return_value='BakZIP')
    @patch('bakzip.main.process_directory', return_value=([], [], 0))
    @patch('bakzip.main.create_zip')
    def test_password_from_env(self, mock_create_zip, mock_process, mock_figlet, mock_getpass, mock_parse_args):
        """Test that password is taken from BAKZIP_PASSWORD environment variable."""
        mock_args = MagicMock()
        mock_args.password = True
        mock_args.directory = '.'
        mock_args.output = 'test'
        mock_args.format = 'zip'
        mock_args.compression = 'normal'
        mock_args.encryption = 'none'
        mock_args.verbose = False
        mock_parse_args.return_value = mock_args

        with patch.dict(os.environ, {'BAKZIP_PASSWORD': 'env_password'}):
            main()
            mock_getpass.assert_not_called()
            # The password is the 3rd argument to create_zip
            mock_create_zip.assert_called_once()
            args, kwargs = mock_create_zip.call_args
            self.assertEqual(args[2], 'env_password')

    @patch('bakzip.main.parse_arguments')
    @patch('bakzip.main.getpass.getpass')
    @patch('bakzip.main.pyfiglet.figlet_format', return_value='BakZIP')
    @patch('bakzip.main.process_directory', return_value=([], [], 0))
    @patch('bakzip.main.create_zip')
    def test_password_from_prompt(self, mock_create_zip, mock_process, mock_figlet, mock_getpass, mock_parse_args):
        """Test that user is prompted if BAKZIP_PASSWORD is not set."""
        mock_args = MagicMock()
        mock_args.password = True
        mock_args.directory = '.'
        mock_args.output = 'test'
        mock_args.format = 'zip'
        mock_args.compression = 'normal'
        mock_args.encryption = 'none'
        mock_args.verbose = False
        mock_parse_args.return_value = mock_args
        mock_getpass.return_value = 'prompt_password'

        with patch.dict(os.environ, {}, clear=True):
            main()
            mock_getpass.assert_called_once()
            mock_create_zip.assert_called_once()
            args, kwargs = mock_create_zip.call_args
            self.assertEqual(args[2], 'prompt_password')

    @patch('bakzip.main.parse_arguments')
    @patch('bakzip.main.getpass.getpass')
    @patch('bakzip.main.pyfiglet.figlet_format', return_value='BakZIP')
    @patch('bakzip.main.process_directory', return_value=([], [], 0))
    @patch('bakzip.main.create_zip')
    def test_no_password_flag(self, mock_create_zip, mock_process, mock_figlet, mock_getpass, mock_parse_args):
        """Test that no password is used if the flag is not provided."""
        mock_args = MagicMock()
        mock_args.password = False
        mock_args.directory = '.'
        mock_args.output = 'test'
        mock_args.format = 'zip'
        mock_args.compression = 'normal'
        mock_args.encryption = 'none'
        mock_args.verbose = False
        mock_parse_args.return_value = mock_args

        with patch.dict(os.environ, {'BAKZIP_PASSWORD': 'env_password'}):
            main()
            mock_getpass.assert_not_called()
            mock_create_zip.assert_called_once()
            args, kwargs = mock_create_zip.call_args
            self.assertIsNone(args[2])

if __name__ == '__main__':
    unittest.main()
