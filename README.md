# BakZip

BakZip is a command-line interface (CLI) tool designed to simplify the process of backing up directories by compressing them into ZIP archives. It offers features like password protection, customizable compression levels, and the ability to exclude specific files and folders from the backup.
 
 [![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
 [![GitHub Stars](https://img.shields.io/github/stars/smx27/BakZip.Cli)](https://github.com/smx27/BakZip.Cli/stargazers)
 [![GitHub Forks](https://img.shields.io/github/forks/smx27/BakZip.Cli)](https://github.com/smx27/BakZip.Cli/network/members)
 [![GitHub Issues](https://img.shields.io/github/issues/smx27/BakZip.Cli)](https://github.com/smx27/BakZip.Cli/issues)
 [![GitHub Pull Requests](https://img.shields.io/github/issues-pr/smx27/BakZip.Cli)](https://github.com/smx27/BakZip.Cli/pulls)

## Features
The BakZip.Cli tool offers a comprehensive set of features to enhance your file compression and sharing experience:

- **Password Protection**: Secure your compressed files with a password to ensure only authorized access.
- **Encryption**: Utilize professional-grade encryption methods such as AES or RSA to protect your data.
- **Format Support**: Compatible with various formats including ZIP, RAR, TAR, and TAR.GZ for optimal compression.
- **Verbose Logging**: Enable verbose logging to get detailed information about which files are skipped or backed up.
- **Log Files**: Generate log files that contain information about skipped files for easy reference.
- **Advanced Compression**: Achieve best-in-class compression, with the potential to reduce file sizes by up to 250%.

## Installation
If you are using windows `powershell` please open that in administrator mode else you will find error. Also for unix use `sudo`.
1. **Clone the Repository:**
```bash
git clone https://github.com/Smx27/BakZip.Cli.git
cd BakZip.Cli
```

2. **Create a Virtual Environment (Recommended):**
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. **Install Dependencies:**
```sh
pip install -r requirements.txt
```
4. **Install BakZip Globally (Editable Mode):**
```bash
pip install -e .
```
This will install bakzip package in a way that allows you to make changes to the code and have them reflected immediately.
Now, you can run your CLI tool from anywhere in your system by using the command 
```bash
bakzip --directory /path/to/dir --output backup.zip --password mySecret123 --compression maximum --verbose
```
## Usage
Run the tool with the following command:
```bash
python main.py --directory /path/to/dir --output backup.zip --password mySecret123 --compression maximum --verbose
```

## Arguments:
- --directory: The directory to be backed up (default: current directory).
- --output: The name of the output backup file (default: backup_<directory_name>.<format>).
- --password: The password to protect the backup file (optional).
- --compression: The compression level (choices: fast, normal, maximum; default: normal).
- --encryption: The encryption algorithm (choices: none, aes, rsa; default: none).
- --format: The backup format (choices: zip, tar, gz; default: zip).
- --verbose: Enable verbose logging (optional).

### Example
```bash
bakzip --directory /path/to/dir --output backup.zip --password mySecret123 --compression maximum --encryption aes --format zip --verbose
```

### Notes
Ensure you have a .bakzipignore file in the root of the directory to specify files and folders to exclude.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

 