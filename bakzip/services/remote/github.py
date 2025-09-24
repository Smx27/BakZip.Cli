import os
import requests
from datetime import datetime
from rich.prompt import Prompt
from rich.console import Console
from .base import RemoteStorage


class GitHubStorage(RemoteStorage):
    """A remote storage provider for GitHub."""

    def __init__(self):
        self.username = None
        self.token = None
        self.repo = None
        self.console = Console()

    def configure(self):
        """Configure the GitHub storage provider."""
        self.username = Prompt.ask(
            "[bold yellow]Enter your GitHub username[/bold yellow]"
        )
        self.repo = Prompt.ask(
            "[bold yellow]Enter the repository (owner/repo)[/bold yellow]"
        )
        self.token = Prompt.ask(
            "[bold yellow]Enter your GitHub Personal Access Token[/bold yellow]",
            password=True,
        )

    def upload(self, filepath: str):
        """
        Upload a file to a new GitHub release.

        Args:
            filepath: The path to the file to upload.
        """
        if not all([self.username, self.token, self.repo]):
            self.configure()

        tag_name = f"bakzip-backup-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"
        release_name = f"Bakzip Backup {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        api_url = f"https://api.github.com/repos/{self.repo}/releases"

        headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json",
        }

        release_payload = {
            "tag_name": tag_name,
            "name": release_name,
            "body": "Automated backup created by Bakzip.",
            "draft": False,
            "prerelease": False,
        }

        try:
            self.console.print("Creating GitHub release...")
            response = requests.post(api_url, headers=headers, json=release_payload)
            response.raise_for_status()
            release_data = response.json()
            upload_url = release_data["upload_url"].split("{")[0]

            self.console.print(f"Uploading {filepath} to GitHub release...")
            with open(filepath, "rb") as f:
                file_data = f.read()

            upload_headers = {
                "Authorization": f"token {self.token}",
                "Accept": "application/vnd.github.v3+json",
                "Content-Type": "application/octet-stream",
            }

            upload_url_with_name = f"{upload_url}?name={os.path.basename(filepath)}"

            response = requests.post(
                upload_url_with_name, headers=upload_headers, data=file_data
            )
            response.raise_for_status()

            self.console.print(
                f"[bold green]Successfully uploaded {filepath} to GitHub release {release_name}[/bold green]"
            )

        except requests.exceptions.RequestException as e:
            self.console.print(
                f"[bold red]An error occurred while uploading to GitHub: {e}[/bold red]"
            )
            if e.response:
                self.console.print(f"[bold red]Response: {e.response.text}[/bold red]")
