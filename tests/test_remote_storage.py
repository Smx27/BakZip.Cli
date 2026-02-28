import os
import unittest
import json
from unittest.mock import MagicMock, patch, mock_open
from bakzip.services.remote.github import GitHubStorage
from bakzip.services.remote.google_drive import GoogleDriveStorage

class TestRemoteStorage(unittest.TestCase):

    @patch("bakzip.services.remote.github.requests.post")
    @patch("bakzip.services.remote.github.Prompt.ask")
    @patch("builtins.open", new_callable=mock_open, read_data=b"test data")
    @patch("os.path.getsize", return_value=9)
    def test_github_upload(self, mock_getsize, mock_file, mock_prompt, mock_post):
        # Setup
        storage = GitHubStorage()
        storage.username = "user"
        storage.repo = "owner/repo"
        storage.token = "token"

        # Mock responses
        mock_release_response = MagicMock()
        mock_release_response.json.return_value = {"upload_url": "https://uploads.github.com/repos/owner/repo/releases/1/assets{?name,label}"}
        mock_release_response.raise_for_status.return_value = None

        mock_upload_response = MagicMock()
        mock_upload_response.raise_for_status.return_value = None

        # Side effect for sequential calls to post (create release, then upload asset)
        mock_post.side_effect = [mock_release_response, mock_upload_response]

        # Execute
        storage.upload("test.zip")

        # Verify
        self.assertEqual(mock_post.call_count, 2)
        # Check first call (create release)
        args, kwargs = mock_post.call_args_list[0]
        self.assertIn("api.github.com", args[0])
        # Check second call (upload asset)
        args, kwargs = mock_post.call_args_list[1]
        self.assertIn("uploads.github.com", args[0])

    @patch("bakzip.services.remote.google_drive.service_account.Credentials.from_service_account_file")
    @patch("bakzip.services.remote.google_drive.build")
    @patch("bakzip.services.remote.google_drive.MediaFileUpload")
    @patch("bakzip.services.remote.google_drive.Prompt.ask")
    @patch("os.path.exists", return_value=True)
    @patch("os.path.getsize", return_value=100)
    @patch("json.load")
    @patch("json.dump")
    @patch("builtins.open", new_callable=mock_open)
    def test_google_drive_upload(self, mock_file, mock_dump, mock_load, mock_getsize, mock_exists, mock_prompt, mock_media, mock_build, mock_creds):
        # Setup
        storage = GoogleDriveStorage()
        # Mock config loading to return nothing so configure runs fully
        mock_load.side_effect = Exception("No config")

        # storage.creds_path = "/path/to/creds.json"
        # storage.folder_id = "folder123"
        # We need to simulate configure() being called or manually set them.
        # But wait, upload() calls configure() if not set.

        # Mock Prompt.ask to provide values
        mock_prompt.side_effect = ["/path/to/creds.json", "folder123"]

        # Mock Google API service
        mock_service = MagicMock()
        mock_build.return_value = mock_service

        mock_files = MagicMock()
        mock_service.files.return_value = mock_files

        mock_create = MagicMock()
        mock_files.create.return_value = mock_create

        # Mock resumable upload response
        mock_status = MagicMock()
        mock_status.resumable_progress = 50

        # First call: In progress, Second call: Done (response object returned)
        mock_create.next_chunk.side_effect = [(mock_status, None), (None, {"id": "file_id_123"})]

        # Execute
        storage.upload("test.zip")

        # Verify
        mock_creds.assert_called_with("/path/to/creds.json", scopes=["https://www.googleapis.com/auth/drive.file"])
        mock_build.assert_called_with("drive", "v3", credentials=mock_creds.return_value)
        mock_media.assert_called()
        mock_files.create.assert_called()
        self.assertEqual(mock_create.next_chunk.call_count, 2)
        # Verify config was saved
        mock_dump.assert_called()

if __name__ == "__main__":
    unittest.main()
