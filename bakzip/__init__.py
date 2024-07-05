"""
BakZIP - A simple command-line backup utility.

This package provides the core functionality for the BakZIP CLI application,
including:

- Parsing command-line arguments.
- Processing the specified directory for files to include in the backup.
- Creating the backup archive (ZIP or TAR) based on user preferences.
- Providing feedback to the user on the backup process.

Usage:

"""
from .main import main
from .utilities.command_line_options import parse_arguments
from .services.directory_processor import get_ignore_list, should_ignore, process_directory
from .services.process_directory import process_directory,get_ignore_list,should_ignore
from .services.tar_service import create_tar
from .services.zip_service import create_zip
from .config.bakzipignore import process_directory,get_ignore_list,should_ignore
