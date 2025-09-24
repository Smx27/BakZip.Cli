# BakZip v2.0

BakZip is a powerful and easy-to-use command-line interface (CLI) tool designed to simplify the process of backing up directories. With its v2.0 refactor, it now features a modern, rich-powered interface, more flexible compression options, and the ability to offload your backups to remote storage.

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/smx27/BakZip.Cli)](https://github.com/smx27/BakZip.Cli/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/smx27/BakZip.Cli)](https://github.com/smx27/BakZip.Cli/network/members)
[![GitHub Issues](https://img.shields.io/github/issues/smx27/BakZip.Cli)](https://github.com/smx27/BakZip.Cli/issues)
[![GitHub Pull Requests](https://img.shields.io/github/issues-pr/smx27/BakZip.Cli)](https://github.com/smx27/BakZip.Cli/pulls)

## Features

- **Modern & Rich CLI**: A completely new interface powered by the `rich` library provides a beautiful and informative user experience, with panels, tables, and a real-time progress bar.
- **Interactive Prompts**: If you forget to provide a required argument like the directory, BakZip will interactively prompt you for it.
- **Advanced Compression**:
    - **ZIP**: Choose from multiple compression levels: `none`, `fast`, `normal`, and `maximum`.
    - **TAR**: Create tarballs with `gz` (gzip), `bz2` (bzip2), or `xz` (lzma) compression, or no compression at all.
- **Remote Offloading**: Automatically upload your completed backup to a remote storage provider.
    - **GitHub**: Upload your backup as a release asset to a specified GitHub repository.
- **Password Protection**: Secure your ZIP archives with a password using AES encryption.
- **Exclude Files**: Use a `.bakzipignore` file to specify files and directories to exclude. You can generate a default ignore file with `bakzip --generate-ignore` or use a custom one with `--ignore-file`.
- **Filtered Local Copy**: Instead of creating an archive, you can copy the directory contents to another local destination, respecting the ignore rules.
- **Verbose Logging**: Get detailed information about the backup process, including skipped files and sizes.

## Installation

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/Smx27/BakZip.Cli.git
    cd BakZip.Cli
    ```

2.  **Create a Virtual Environment (Recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install Dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

4.  **Install BakZip in Editable Mode:**
    ```bash
    pip install -e .
    ```
    This allows you to run `bakzip` from anywhere on your system.

## Usage

The basic command structure is:

```bash
bakzip [DIRECTORY] [OPTIONS]
```

If you don't provide a directory, BakZip will prompt you to enter one.

> **Note for previous users:** In older versions, you might have run the application with `python main.py`. After installing the package with `pip install -e .`, the tool is now available as a command-line application that you can run directly as `bakzip` from any directory.

### Arguments

-   `directory`: The directory to be backed up (positional argument). If not provided, you will be prompted for it.
-   `-o, --output`: The name of the output backup file (e.g., `my_backup`). The extension is added automatically.
-   `-p, --password`: The password to protect the ZIP file (optional).
-   `--compression`: The compression level for **zip** files.
    -   Choices: `none`, `fast`, `normal`, `maximum`. Default: `normal`.
-   `--tar-compression`: The compression type for **tar** files.
    -   Choices: `none`, `gz`, `bz2`, `xz`. Default: `gz`.
-   `-e, --encryption`: The encryption algorithm (not fully implemented yet). Default: `none`.
-   `-f, --format`: The backup format.
    -   Choices: `zip`, `tar`. Default: `zip`.
-   `--remote`: The remote storage provider to upload to.
    -   Choices: `github`, `google_drive` (Google Drive not yet implemented).
-   `--ignore-file`: Path to a custom ignore file (e.g., `/path/to/.myignore`).
-   `--generate-ignore`: Generate a default `.bakzipignore` file in the current directory and exit.
-   `--copy-to`: Perform a filtered copy to a local directory instead of creating an archive.
-   `-v, --verbose`: Enable verbose logging (optional).

### Examples

**1. Create a simple ZIP backup of the current directory:**

```bash
bakzip .
```

**2. Create a TAR backup with `bzip2` compression:**

```bash
bakzip /path/to/my/project -f tar --tar-compression bz2 -o my_project_archive
```

**3. Create a password-protected ZIP with maximum compression:**

```bash
bakzip /path/to/my/project -f zip --compression maximum -p "my-secret-password"
```

**4. Create a backup and upload it to a GitHub release:**

```bash
bakzip /path/to/my/project --remote github
```

**5. Generate a default `.bakzipignore` file:**
```bash
bakzip --generate-ignore
```

**6. Use a custom ignore file for your backup:**
```bash
bakzip /path/to/my/project --ignore-file /path/to/my/custom.ignore
```

**7. Copy a directory to another location, ignoring files:**
```bash
bakzip /path/to/my/project --copy-to /path/to/my/destination
```

> **Note:** When using `--remote github` for the first time, you will be prompted to enter your GitHub username, the repository (`owner/repo`), and a Personal Access Token (PAT) with `repo` scope.

### Advanced Examples

Here are some examples of how to combine the features for more complex workflows.

**1. Create a `tar.xz` archive and upload it to GitHub:**

This command will back up the specified directory, compress it using the `xz` algorithm (which is slow but provides a high compression ratio), name the output file `my-app-backup`, and then upload it as a release asset to your configured GitHub repository.

```bash
bakzip /path/to/my/app -f tar --tar-compression xz -o my-app-backup --remote github
```

**2. Perform a filtered copy to a backup folder, using a custom ignore file:**

This is useful for creating a clean, local copy of your project for testing or deployment, without creating an archive.

```bash
bakzip . --copy-to ./my-project-clean-copy --ignore-file ./.production.ignore
```

**3. Create a verbose, password-protected zip backup with maximum compression:**

This command will provide detailed output of the files being processed, use the strongest (but slowest) zip compression algorithm, and protect the final archive with a password.

```bash
bakzip /path/to/your/files -f zip --compression maximum -p "your-secret-password" -v
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
 