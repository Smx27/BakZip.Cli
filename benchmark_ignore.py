import time
import fnmatch
import re
import os
import sys
from unittest.mock import MagicMock

# Mock missing dependencies as in tests/conftest.py
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

# Add the current directory to sys.path
sys.path.append(os.getcwd())

# Define the original implementation manually
def should_ignore_original(path, ignore_list):
    for pattern in ignore_list:
        if fnmatch.fnmatch(path, pattern):
            return True
    return False

# Import the optimized implementation
from bakzip.services.directory_processor import should_ignore as should_ignore_optimized

def benchmark_original(paths, ignore_list):
    start_time = time.time()
    ignored_count = 0
    for path in paths:
        if should_ignore_original(path, ignore_list):
            ignored_count += 1
    end_time = time.time()
    return end_time - start_time, ignored_count

def benchmark_optimized(paths, ignore_list):
    start_time = time.time()
    ignored_count = 0
    for path in paths:
        if should_ignore_optimized(path, ignore_list):
            ignored_count += 1
    end_time = time.time()
    return end_time - start_time, ignored_count

def run_benchmark():
    # Generate some patterns
    ignore_list = [
        "*.pyc", "*.pyo", "__pycache__", ".git", ".svn", ".hg",
        "node_modules", "vendor", "dist", "build", "*.log", "*.tmp",
        "temp_*", "cache/*", "logs/*.log", "coverage/*", ".env"
    ] * 10 # Increase pattern count

    # Generate some paths
    paths = []
    for i in range(1000):
        paths.append(f"src/module_{i}/file_{i}.py")
        paths.append(f"src/module_{i}/file_{i}.pyc")
        paths.append(f"node_modules/pkg_{i}/index.js")
        paths.append(f"dist/bundle_{i}.js")
        paths.append(f"logs/error_{i}.log")
        paths.append(f"src/module_{i}/temp_data.txt")

    print(f"Benchmarking with {len(ignore_list)} patterns and {len(paths)} paths...")

    orig_time, orig_count = benchmark_original(paths, ignore_list)
    print(f"Original should_ignore: {orig_time:.4f}s (Ignored: {orig_count})")

    opt_time, opt_count = benchmark_optimized(paths, ignore_list)
    print(f"Optimized (regex):      {opt_time:.4f}s (Ignored: {opt_count})")

    if orig_count != opt_count:
        print(f"WARNING: Counts differ! Original: {orig_count}, Optimized: {opt_count}")

    if opt_time < orig_time:
        improvement = (orig_time - opt_time) / orig_time * 100
        print(f"Improvement: {improvement:.2f}%")
    else:
        print("No improvement detected.")

if __name__ == "__main__":
    run_benchmark()
