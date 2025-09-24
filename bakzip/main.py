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
import shutil
import time
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.prompt import Prompt
from rich.progress import Progress
from bakzip.utilities.command_line_options import parse_arguments
from bakzip.utilities.file_system import process_directory
from bakzip.services.zip_service import create_zip
from bakzip.services.tar_service import create_tar
from bakzip.services.remote.github import GitHubStorage
from bakzip.services.remote.google_drive import GoogleDriveStorage


def perform_filtered_copy(source_dir, dest_dir, files_to_copy, progress):
    """Copies a list of files from a source to a destination, preserving structure."""
    copy_task = progress.add_task(
        "[bold blue]Copying files...", total=len(files_to_copy)
    )

    for src_path in files_to_copy:
        rel_path = os.path.relpath(src_path, source_dir)
        dest_path = os.path.join(dest_dir, rel_path)

        # Create destination subdirectory if it doesn't exist
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)

        shutil.copy2(src_path, dest_path)
        progress.update(copy_task, advance=1)


DEFAULT_IGNORE_CONTENT = """\
# Default .bakzipignore file
# Add files and directories to exclude from the backup.
# Supports standard .gitignore patterns.

# General
*.log
*.tmp
*.swp
*~

# Python
__pycache__/
*.pyc
*.pyo
.venv/
venv/
env/

# Node.js
node_modules/
npm-debug.log*

# OS specific
.DS_Store
Thumbs.db
"""


def generate_ignore_file():
    """Creates a default .bakzipignore file in the current directory."""
    if os.path.exists(".bakzipignore"):
        print("'.bakzipignore' file already exists.")
        return
    with open(".bakzipignore", "w") as f:
        f.write(DEFAULT_IGNORE_CONTENT)
    print("Default '.bakzipignore' file created.")


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
    console = Console()

    # Banner
    title = Text("BakZIP", style="bold magenta", justify="center")
    subtitle = Text("by @smx27", style="bold cyan", justify="center")
    banner = Panel(
        Text.assemble(title, "\n", subtitle), title="Welcome", border_style="green"
    )

    args = parse_arguments()

    if args.generate_ignore:
        generate_ignore_file()
        return

    console.print(banner)
    directory = args.directory
    if not directory:
        while True:
            directory = Prompt.ask(
                "[bold yellow]Enter the directory to back up[/bold yellow]"
            )
            if os.path.isdir(directory):
                break
            else:
                console.print(
                    "[bold red]Invalid directory. Please try again.[/bold red]"
                )

    output = args.output or f"backup_{os.path.basename(directory)}"
    if args.format == "zip":
        output += ".zip"
    elif args.format == "tar":
        output += ".tar"
        if args.tar_compression != "none":
            output += f".{args.tar_compression}"
    else:
        console.print("[bold red]Error: Unsupported format specified.[/bold red]")
        return

    password = args.password
    verbose = args.verbose
    log_file_path = os.path.join(os.path.dirname(output) or ".", "bakzip.log")

    start_time = time.time()

    if verbose:
        verbose_table = Table(title="Backup Configuration", show_header=False, box=None)
        verbose_table.add_row("Processing directory:", f"[cyan]{directory}[/cyan]")
        verbose_table.add_row("Output file:", f"[cyan]{output}[/cyan]")
        verbose_table.add_row(
            "Password:", "[cyan]Yes[/cyan]" if password else "[cyan]No[/cyan]"
        )
        if args.format == "zip":
            verbose_table.add_row("Compression:", f"[cyan]{args.compression}[/cyan]")
        elif args.format == "tar":
            verbose_table.add_row(
                "Tar Compression:", f"[cyan]{args.tar_compression}[/cyan]"
            )
        verbose_table.add_row("Encryption:", f"[cyan]{args.encryption}[/cyan]")
        verbose_table.add_row("Format:", f"[cyan]{args.format}[/cyan]")
        verbose_table.add_row("Log file:", f"[cyan]{log_file_path}[/cyan]")
        console.print(Panel(verbose_table, border_style="blue"))

    try:
        if args.copy_to:
            with Progress(
                "[progress.description]{task.description}",
                "[progress.percentage]{task.percentage:>3.0f}%",
                "[progress.bar]{task.bar}",
                "{task.completed} of {task.total} files",
                "Elapsed: [progress.elapsed]",
                "ETA: [progress.remaining]",
                console=console,
                transient=True,
            ) as progress:
                processing_task = progress.add_task(
                    "[bold green]Scanning files...", total=None
                )
                files_to_include, _, _ = process_directory(
                    directory,
                    log_file_path,
                    progress,
                    processing_task,
                    args.ignore_file,
                )
                perform_filtered_copy(
                    directory, args.copy_to, files_to_include, progress
                )

            console.print(
                Panel(
                    f"[bold green]Successfully copied {len(files_to_include)} files to {args.copy_to}[/bold green]",
                    border_style="green",
                )
            )
            return

        with Progress(
            "[progress.description]{task.description}",
            "[progress.percentage]{task.percentage:>3.0f}%",
            "[progress.bar]{task.bar}",
            "{task.completed} of {task.total} files",
            "Elapsed: [progress.elapsed]",
            "ETA: [progress.remaining]",
            console=console,
            transient=True,
        ) as progress:
            processing_task = progress.add_task(
                "[bold green]Processing files...", total=None
            )
            files_to_include, skipped_files, total_skipped_size = process_directory(
                directory, log_file_path, progress, processing_task, args.ignore_file
            )

            zipping_task = progress.add_task(
                "[bold green]Creating backup archive...", total=None
            )
            if args.format == "zip":
                create_zip(files_to_include, output, password, args.compression)
            elif args.format == "tar":
                create_tar(files_to_include, output, args.tar_compression)
            progress.update(zipping_task, completed=1, total=1)

            if args.remote:
                upload_task = progress.add_task(
                    f"[bold blue]Uploading to {args.remote}...", total=None
                )
                remote_storage = None
                if args.remote == "github":
                    remote_storage = GitHubStorage()
                elif args.remote == "google_drive":
                    remote_storage = GoogleDriveStorage()

                if remote_storage:
                    remote_storage.configure()
                    remote_storage.upload(output)

                progress.update(upload_task, completed=1, total=1)

        end_time = time.time()
        total_time = end_time - start_time
        total_files = len(files_to_include)
        total_skipped_files = len(skipped_files)

        console.print(
            Panel(
                "[bold green]Backup completed successfully![/bold green]",
                border_style="green",
            )
        )

        summary_table = Table(title="Backup Summary")
        summary_table.add_column(
            "Statistic", justify="right", style="cyan", no_wrap=True
        )
        summary_table.add_column("Value", style="magenta")

        summary_table.add_row("Output File", output)
        summary_table.add_row("Total Files", str(total_files))
        if verbose:
            summary_table.add_row("Skipped Files", str(total_skipped_files))
            summary_table.add_row("Total Skipped Size", f"{total_skipped_size} bytes")
        summary_table.add_row("Backup Format", args.format)
        summary_table.add_row("Encryption", str(args.encryption))
        summary_table.add_row("Total Time Taken", f"{total_time:.2f} seconds")

        console.print(summary_table)

    except Exception:
        console.print_exception(show_locals=True)


if __name__ == "__main__":
    main()
