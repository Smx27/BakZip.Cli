import sys
from unittest.mock import MagicMock, patch

# Mock missing dependencies
mock_pyfiglet = MagicMock()
sys.modules["pyfiglet"] = mock_pyfiglet

mock_pyzipper = MagicMock()
mock_pyzipper.ZIP_LZMA = 1
mock_pyzipper.ZIP_DEFLATED = 2
mock_pyzipper.ZIP_BZIP2 = 3
sys.modules["pyzipper"] = mock_pyzipper

mock_tqdm_mod = MagicMock()
sys.modules["tqdm"] = mock_tqdm_mod
mock_tqdm_mod.tqdm = MagicMock()

import timeit
import os
import shutil
from bakzip.services.directory_processor import process_directory

def setup_benchmark_dir(num_files=1000):
    test_dir = 'benchmark_test_dir'
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    os.makedirs(test_dir)

    for i in range(num_files):
        with open(os.path.join(test_dir, f'file_{i}.txt'), 'w') as f:
            f.write('content')

    return test_dir

def run_benchmark():
    test_dir = setup_benchmark_dir(5000)
    log_file = 'benchmark.log'
    # Define a mock ignore list to use for the benchmark
    mock_ignore = ['file_1*', '*.log', 'temp/']

    def test_func():
        # Patch get_ignore_list to return our mock ignore list consistently
        with patch('bakzip.services.directory_processor.get_ignore_list', return_value=mock_ignore):
            process_directory(test_dir, log_file, verbose=False)

    timer = timeit.Timer(test_func)
    # Run once to warm up cache
    test_func()

    iterations = 20
    total_time = timer.timeit(number=iterations)
    avg_time = total_time / iterations

    print(f"Average time for process_directory with 5000 files: {avg_time:.5f} seconds")

    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    if os.path.exists(log_file):
        os.remove(log_file)

if __name__ == "__main__":
    run_benchmark()
