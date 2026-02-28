import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from rich.prompt import Prompt
from rich.console import Console
from rich.progress import Progress, TextColumn, BarColumn, DownloadColumn, TransferSpeedColumn
from .base import RemoteStorage


class GoogleDriveStorage(RemoteStorage):
    """A remote storage provider for Google Drive."""

    def __init__(self):
        self.creds_path = None
        self.folder_id = None
        self.console = Console()
        self.SCOPES = ["https://www.googleapis.com/auth/drive.file"]
        self.config_dir = os.path.expanduser("~/.bakzip")
        self.config_file = os.path.join(self.config_dir, "google_drive.json")

    def _load_config(self):
        """Load configuration from disk."""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r") as f:
                    config = json.load(f)
                    self.creds_path = config.get("creds_path")
                    self.folder_id = config.get("folder_id")
            except Exception as e:
                self.console.print(f"[yellow]Failed to load config: {e}[/yellow]")

    def _save_config(self):
        """Save configuration to disk."""
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir, exist_ok=True)
        try:
            with open(self.config_file, "w") as f:
                json.dump({
                    "creds_path": self.creds_path,
                    "folder_id": self.folder_id
                }, f)
            self.console.print(f"[green]Configuration saved to {self.config_file}[/green]")
        except Exception as e:
            self.console.print(f"[red]Failed to save config: {e}[/red]")

    def configure(self):
        """Configure the Google Drive storage provider."""
        self._load_config()

        if self.creds_path and os.path.exists(self.creds_path):
             use_existing = Prompt.ask(
                 f"Found existing credentials at [cyan]{self.creds_path}[/cyan]. Use them?",
                 choices=["y", "n"], default="y"
             )
             if use_existing == "y":
                 # If user wants to change folder ID, we should probably ask?
                 # But standard flow usually assumes full config reuse.
                 # Let's verify if folder_id is set or ask.
                 if not self.folder_id:
                     self.folder_id = Prompt.ask(
                        "[bold yellow]Enter the Folder ID to upload to (optional, press Enter for root)[/bold yellow]",
                        default="",
                     )
                     self._save_config()
                 return

        self.creds_path = Prompt.ask(
            "[bold yellow]Enter the path to your Google Service Account JSON file[/bold yellow]"
        )
        if not os.path.exists(self.creds_path):
            self.console.print(f"[bold red]File not found: {self.creds_path}[/bold red]")
            # Retry once
            self.creds_path = Prompt.ask(
                "[bold yellow]Please enter a valid path to your Google Service Account JSON file[/bold yellow]"
            )

        self.folder_id = Prompt.ask(
            "[bold yellow]Enter the Folder ID to upload to (optional, press Enter for root)[/bold yellow]",
            default="",
        )

        self._save_config()

    def upload(self, filepath: str):
        """
        Upload a file to Google Drive.

        Args:
            filepath: The path to the file to upload.
        """
        if not self.creds_path:
            self.configure()

        try:
            creds = service_account.Credentials.from_service_account_file(
                self.creds_path, scopes=self.SCOPES
            )
            service = build("drive", "v3", credentials=creds)

            file_metadata = {"name": os.path.basename(filepath)}
            if self.folder_id:
                file_metadata["parents"] = [self.folder_id]

            file_size = os.path.getsize(filepath)

            # Use a chunk size of 1MB (must be a multiple of 256*1024)
            chunk_size = 1024 * 1024

            media = MediaFileUpload(
                filepath,
                mimetype="application/octet-stream",
                resumable=True,
                chunksize=chunk_size
            )

            request = service.files().create(
                body=file_metadata, media_body=media, fields="id"
            )

            response = None

            self.console.print(f"Uploading {filepath} to Google Drive...")

            with Progress(
                TextColumn("[bold blue]{task.description}"),
                BarColumn(),
                "[progress.percentage]{task.percentage:>3.0f}%",
                DownloadColumn(),
                TransferSpeedColumn(),
                console=self.console,
                transient=True
            ) as progress:
                task = progress.add_task("Uploading...", total=file_size)

                while response is None:
                    status, response = request.next_chunk()
                    if status:
                        progress.update(task, completed=status.resumable_progress)

                # Ensure 100% completion is shown at the end
                progress.update(task, completed=file_size)

            self.console.print(
                f"[bold green]Successfully uploaded {filepath} to Google Drive (File ID: {response.get('id')})[/bold green]"
            )

        except Exception as e:
            self.console.print(
                f"[bold red]An error occurred while uploading to Google Drive: {e}[/bold red]"
            )
