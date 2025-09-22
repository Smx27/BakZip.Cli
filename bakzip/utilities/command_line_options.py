import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description='BakZip - A CLI tool to backup directories, excluding specified files and folders.')
    parser.add_argument('directory', nargs='?', type=str, help='The directory to be backed up.', default=None)
    parser.add_argument('-o','--output', type=str, help='The name of the output backup file.', default=None)
    parser.add_argument('-p','--password', type=str, help='The password to protect the backup file', default=None)
    parser.add_argument('--compression', type=str, choices=['none', 'fast', 'normal', 'maximum'], help='The compression level for zip files.', default='normal')
    parser.add_argument('--tar-compression', type=str, choices=['none', 'gz', 'bz2', 'xz'], help='The compression for tar archives.', default='gz')
    parser.add_argument('-e','--encryption', type=str, choices=['none', 'aes', 'rsa'], help='The encryption algorithm', default='none')
    parser.add_argument('-f','--format', type=str, choices=['zip', 'tar', 'gz'], help='The backup format', default='zip')
    parser.add_argument('-v','--verbose', action='store_true', help='Enable verbose logging')
    parser.add_argument('--remote', type=str, choices=['github', 'google_drive'], help='The remote storage provider to use.', default=None)
    parser.add_argument('--ignore-file', type=str, help='Path to a custom ignore file.', default=None)
    parser.add_argument('--generate-ignore', action='store_true', help='Generate a default .bakzipignore file and exit.')
    return parser.parse_args()
