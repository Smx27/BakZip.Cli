#! /usr/env/bin python
"""
Main function for the BakZIP CLI application.

This module handles the core logic of the BakZIP CLI application, including:
- Parsing command-line arguments.
- Processing the specified directory for files to include in the backup.
- Creating the backup archive (ZIP or TAR) based on user preferences.
- Providing feedback to the user on the backup process.
"""
import os
import time
import traceback
import getpass
import pyfiglet
from bakzip.utilities.command_line_options import parse_arguments
from bakzip.services.directory_processor import process_directory
from bakzip.services.zip_service import create_zip
from bakzip.services.tar_service import create_tar

def main():
    """
    Main function for the BakZIP CLI application.

    This function handles the core logic of the application, including:
    - Parsing command-line arguments.
    - Processing the specified directory for files to include in the backup.
    - Creating the backup archive (ZIP or TAR) based on user preferences.
    - Providing feedback to the user on the backup process.

    Raises:
        ValueError: If an unsupported format is specified.
        Exception: If any other error occurs during the backup process.
    """
    # Set restrictive umask (0o077) to ensure all created files (archives and logs)
    # have restrictive permissions (0o600 for files, 0o700 for directories).
    os.umask(0o077)
    result = pyfiglet.figlet_format("BakZIP", font = "slant")
    print(result)
    print('by @smx27 Github: @smx27')
    args = parse_arguments()
    password = None
    if args.password:
        password = os.environ.get('BAKZIP_PASSWORD')
        if not password:
            password = getpass.getpass("Enter password to protect the backup file: ")
    directory = args.directory
    output = args.output or f'backup_{os.path.basename(directory)}'
    if args.format == 'zip':
        output += '.zip'
    elif args.format == 'tar':
        output += '.tar'
        if args.compression == 'gz':
            output += '.gz'
    else:
        raise ValueError("Unsupported format")
    compression = args.compression
    verbose = args.verbose
    log_file_path = os.path.join(os.path.dirname(output), 'bakzip.log')
    start_time = time.time()
    if verbose:
        print(f'Processing directory: {directory}')
        print(f'Output file: {output}')
        print(f'Password: {"***" if password else "None"}')
        print(f'Compression: {compression}')
        print(f'Encryption: {args.encryption}')
        print(f'Format: {args.format}')
        print(f'Verbose: {verbose}')
        print(f'Log file: {log_file_path}')
    try:
        files_to_include, skipped_files, total_skipped_size = process_directory(directory, log_file_path, verbose=verbose)
        if args.format == 'zip':
            create_zip(files_to_include, output, password, compression, base_dir=directory)
        elif args.format == 'tar':
            create_tar(files_to_include, output, compression, base_dir=directory)
        else:
            raise ValueError("Unsupported format")
        end_time = time.time()
        total_time = end_time - start_time
        total_files = len(files_to_include)
        total_skipped_files = len(skipped_files)
        print('Backup completed successfully.')
        print(f'Output file: {output}')
        print(f'Total files: {total_files}')
        if verbose:
            print(f'Skipped files: {total_skipped_files}')
            print(f'Total skipped size: {total_skipped_size} bytes')
            print(f'Total skipped files: {total_skipped_files}')
            print(f'Backup format: {args.format}')
            print(f'Backup encryption: {args.encryption}')

        print(f'Total time taken: {total_time:.2f} seconds')
    except Exception as ex:
        print(f'An error occurred: {ex}')
        if verbose:
            # Log the traceback to the log file instead of printing it to stdout
            try:
                with open(log_file_path, 'a', encoding='utf-8') as log_file:
                    log_file.write(f"\nAn error occurred during the backup process: {ex}\n")
                    log_file.write(traceback.format_exc())
                print(f'Full traceback has been logged to: {log_file_path}')
            except Exception as log_err:
                print(f'Failed to log traceback to {log_file_path}: {log_err}')

if __name__ == '__main__':
    main()
