import abc


class RemoteStorage(abc.ABC):
    """Abstract base class for remote storage providers."""

    @abc.abstractmethod
    def configure(self):
        """Configure the remote storage provider with necessary credentials."""
        raise NotImplementedError

    @abc.abstractmethod
    def upload(self, filepath: str):
        """
        Upload a file to the remote storage.

        Args:
            filepath: The path to the file to upload.
        """
        raise NotImplementedError
