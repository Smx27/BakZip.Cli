# Release Notes - BakZip v2.0

BakZip v2.0 introduces a major overhaul of the CLI interface, enhanced compression options, and robust remote offloading capabilities.

## New Features

### 🎨 Modern & Rich CLI
- **Interactive UI**: The entire user interface is now powered by the `rich` library, offering beautiful panels, tables, and real-time progress bars.
- **Interactive Prompts**: Forgot an argument? BakZip will now helpfully prompt you for missing information like the target directory or authentication tokens.

### ☁️ Remote Offloading
- **GitHub Integration**: Automatically upload your backups to GitHub Releases. The integration now features a real-time progress bar for uploads.
- **Google Drive Integration**: New in v2.0! Seamlessly upload your backups to Google Drive using a Service Account. Includes support for specifying target folders and a real-time upload progress bar.

### 📦 Advanced Compression & Filtering
- **Enhanced Compression**:
  - **ZIP**: Support for multiple compression levels (`none`, `fast`, `normal`, `maximum`) and AES encryption via `pyzipper`.
  - **TAR**: Create tarballs with `gz`, `bz2`, or `xz` compression.
- **Filtered Local Copy**: Use the `--copy-to` argument to copy a directory structure to another location while respecting ignore rules—perfect for creating clean deployment builds.

### 🚫 Ignore File Management
- **.bakzipignore**: Exclude unwanted files and directories using standard patterns.
- **Auto-Generation**: Generate a default ignore file with `bakzip --generate-ignore`.

## Improvements & Fixes
- **Progress Bars**: Added detailed progress bars for both local file processing and remote uploads (GitHub and Google Drive).
- **Codebase Refactoring**: Modularized services for better maintainability and testing.
- **Updated Documentation**: Comprehensive `README.md` covering all new features and usage examples.

## Installation & Usage

Install the latest version with:
```bash
pip install -e .
```

To use the new Google Drive feature:
1. Obtain a `service_account.json` key from your Google Cloud Console.
2. Run `bakzip` with `--remote google_drive`.
3. Provide the path to your key file when prompted.
