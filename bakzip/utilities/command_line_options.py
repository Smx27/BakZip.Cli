import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description='BakZip - A CLI tool to backup directories, excluding specified files and folders.')
    parser.add_argument('-d','--directory', type=str, help='The directory to be backed up', default='.')
    parser.add_argument('-o','--output', type=str, help='The name of the output backup file', default='default')
    parser.add_argument('-p','--password', type=str, help='The password to protect the backup file', default=None)
    parser.add_argument('-c','--compression', type=str, choices=['fast', 'normal', 'maximum'], help='The compression level', default='normal')
    parser.add_argument('-e','--encryption', type=str, choices=['none', 'aes', 'rsa'], help='The encryption algorithm', default='none')
    parser.add_argument('-f','--format', type=str, choices=['zip', 'tar', 'gz'], help='The backup format', default='zip')
    parser.add_argument('-v','--verbose', action='store_true', help='Enable verbose logging')
    return parser.parse_args()
