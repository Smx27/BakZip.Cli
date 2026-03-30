import unittest
from unittest.mock import patch
from bakzip.utilities.command_line_options import parse_arguments

class TestCommandLineOptions(unittest.TestCase):
    def test_default_arguments(self):
        """Test that default values are correctly assigned when no arguments are provided."""
        with patch('sys.argv', ['bakzip']):
            args = parse_arguments()
            self.assertEqual(args.directory, '.')
            self.assertEqual(args.output, 'default')
            self.assertFalse(args.password)
            self.assertEqual(args.compression, 'normal')
            self.assertEqual(args.encryption, 'none')
            self.assertEqual(args.format, 'zip')
            self.assertFalse(args.verbose)

    def test_custom_long_arguments(self):
        """Test that long-form arguments are correctly parsed."""
        test_args = [
            'bakzip',
            '--directory', '/home/user/data',
            '--output', 'my_backup',
            '--password',
            '--compression', 'maximum',
            '--encryption', 'aes',
            '--format', 'tar',
            '--verbose'
        ]
        with patch('sys.argv', test_args):
            args = parse_arguments()
            self.assertEqual(args.directory, '/home/user/data')
            self.assertEqual(args.output, 'my_backup')
            self.assertTrue(args.password)
            self.assertEqual(args.compression, 'maximum')
            self.assertEqual(args.encryption, 'aes')
            self.assertEqual(args.format, 'tar')
            self.assertTrue(args.verbose)

    def test_custom_short_arguments(self):
        """Test that short-form arguments are correctly parsed."""
        test_args = [
            'bakzip',
            '-d', './src',
            '-o', 'src_backup',
            '-p',
            '-c', 'fast',
            '-e', 'rsa',
            '-f', 'gz',
            '-v'
        ]
        with patch('sys.argv', test_args):
            args = parse_arguments()
            self.assertEqual(args.directory, './src')
            self.assertEqual(args.output, 'src_backup')
            self.assertTrue(args.password)
            self.assertEqual(args.compression, 'fast')
            self.assertEqual(args.encryption, 'rsa')
            self.assertEqual(args.format, 'gz')
            self.assertTrue(args.verbose)

    def test_password_flag_only(self):
        """Test that the password argument acts as a flag when provided without a value."""
        with patch('sys.argv', ['bakzip', '--password']):
            args = parse_arguments()
            self.assertIs(args.password, True)

        with patch('sys.argv', ['bakzip', '-p']):
            args = parse_arguments()
            self.assertIs(args.password, True)

    def test_invalid_compression_choice(self):
        """Test that an invalid compression choice triggers a SystemExit."""
        with patch('sys.argv', ['bakzip', '--compression', 'ultra']):
            with patch('sys.stderr', new_callable=unittest.mock.MagicMock()): # Suppress error output
                with self.assertRaises(SystemExit):
                    parse_arguments()

    def test_invalid_encryption_choice(self):
        """Test that an invalid encryption choice triggers a SystemExit."""
        with patch('sys.argv', ['bakzip', '--encryption', 'des']):
            with patch('sys.stderr', new_callable=unittest.mock.MagicMock()):
                with self.assertRaises(SystemExit):
                    parse_arguments()

    def test_invalid_format_choice(self):
        """Test that an invalid format choice triggers a SystemExit."""
        with patch('sys.argv', ['bakzip', '--format', 'rar']):
            with patch('sys.stderr', new_callable=unittest.mock.MagicMock()):
                with self.assertRaises(SystemExit):
                    parse_arguments()

if __name__ == '__main__':
    unittest.main()
