from .base import RemoteStorage

class GoogleDriveStorage(RemoteStorage):
    """A remote storage provider for Google Drive."""

    def configure(self):
        """Configure the Google Drive storage provider."""
        pass

    def upload(self, filepath: str):
        """
        Upload a file to Google Drive.

        Args:
            filepath: The path to the file to upload.
        """
        print(f"Uploading {filepath} to Google Drive... (not implemented)")
        pass
