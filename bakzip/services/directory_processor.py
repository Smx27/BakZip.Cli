import os
import fnmatch

def get_ignore_list(directory):
    ignore_list = []
    ignore_file = './.bakzipignore'
    # ignore_file = os.path.join(directory, '.bakzipignore')
    if os.path.exists(ignore_file):
        with open(ignore_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):  # Ignore comments and empty lines
                    ignore_list.append(line)
                    if(line.endswith('/')):
                        ignore_list.append(line + '*')
                        ignore_list.append('*/' + line)
                    if(line.find('.') == -1 and not line.endswith('/')):
                        ignore_list.append(line + '/')
                        ignore_list.append(line + '/*')
                        ignore_list.append('*/' + line)
                        
    return ignore_list

def should_ignore(path, ignore_list):
    for pattern in ignore_list:
        if fnmatch.fnmatch(path, pattern):
            return True
    return False

def process_directory(directory, log_file_path):
    ignore_list = get_ignore_list(directory)
    files_to_include = []
    skipped_files = []
    total_skipped_size = 0
    with open(log_file_path, 'w') as log_file:
        for root, dirs, files in os.walk(directory, topdown=True):
            dirs[:] = [d for d in dirs if not should_ignore(os.path.relpath(os.path.join(root, d), directory), ignore_list)]
            for file in files:
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, directory)
                file_size = os.path.getsize(file_path)
                if not should_ignore(rel_path, ignore_list):
                    files_to_include.append(file_path)
                else:
                    skipped_files.append(file_path)
                    total_skipped_size += os.path.getsize(file_path)
    return files_to_include, skipped_files, total_skipped_size
