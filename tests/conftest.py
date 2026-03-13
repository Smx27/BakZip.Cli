import sys
from unittest.mock import MagicMock

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
