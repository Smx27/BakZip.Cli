import pytest
from unittest.mock import patch, MagicMock
from bakzip.services.remote.github import GitHubStorage

@patch('rich.prompt.Prompt.ask')
def test_githubstorage_configure(mock_ask):
    """
    Tests the configure method of GitHubStorage.
    """
    mock_ask.side_effect = ['testuser', 'testowner/testrepo', 'testtoken']
    storage = GitHubStorage()
    storage.configure()

    assert mock_ask.call_count == 3
    assert storage.username == 'testuser'
    assert storage.repo == 'testowner/testrepo'
    assert storage.token == 'testtoken'

@patch('requests.post')
def test_githubstorage_upload_success(mock_post, tmp_path):
    """
    Tests the upload method of GitHubStorage for a successful upload.
    """
    # Create a dummy file to upload
    dummy_file = tmp_path / "backup.zip"
    dummy_file.write_text("dummy content")

    # Mock the response from the GitHub API for release creation
    mock_release_response = MagicMock()
    mock_release_response.status_code = 201
    mock_release_response.json.return_value = {
        'upload_url': 'https://uploads.github.com/repos/testowner/testrepo/releases/1/assets{?name,label}'
    }

    # Mock the response for the asset upload
    mock_upload_response = MagicMock()
    mock_upload_response.status_code = 201

    mock_post.side_effect = [mock_release_response, mock_upload_response]

    storage = GitHubStorage()
    storage.username = 'testuser'
    storage.repo = 'testowner/testrepo'
    storage.token = 'testtoken'

    storage.upload(str(dummy_file))

    assert mock_post.call_count == 2
    # You could add more specific assertions here about the calls made to requests.post

@patch('requests.post')
def test_githubstorage_upload_failure(mock_post, tmp_path, capsys):
    """
    Tests the upload method of GitHubStorage for a failed upload.
    """
    dummy_file = tmp_path / "backup.zip"
    dummy_file.write_text("dummy content")

    mock_failure_response = MagicMock()
    mock_failure_response.status_code = 404
    mock_failure_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")
    mock_failure_response.text = "Not Found"

    mock_post.return_value = mock_failure_response

    storage = GitHubStorage()
    storage.username = 'testuser'
    storage.repo = 'testowner/testrepo'
    storage.token = 'testtoken'

    storage.upload(str(dummy_file))

    captured = capsys.readouterr()
    assert "An error occurred while uploading to GitHub" in captured.out
