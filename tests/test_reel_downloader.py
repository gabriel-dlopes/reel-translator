from pathlib import Path
from unittest.mock import MagicMock, patch
import pytest
from src.services.reel_downloader import ReelDownloader

def test_rejects_invalid_url() -> None:
    # Arrange
    downloader = ReelDownloader(Path("data/input")) # creating the object that will be tested

    # Act and Assert
    with pytest.raises(ValueError):
        downloader.download("https://example.com/video") # the test itself

def test_downloads_reel_successfully(tmp_path: Path) -> None:
    # Temporary path where the test output's will be stored
    output_directory = tmp_path / "input"

    # Valid URL for the test
    reel_url = "https://www.instagram.com/reel/ABC123/"

    # Path that would be expected in a correct scenario
    expected_file = output_directory / "ABC123.mp4"

    # Initiates the object form class MagicMock that will pretend to be yt_dlp object
    fake_downloader = MagicMock()

    # Necessary because of "with" behavior after
    fake_downloader.__enter__.return_value = fake_downloader
    fake_downloader.__exit__.return_value = None

    # Defining the metadata returned by the fake_downloader
    fake_downloader.extract_info.return_value = {
        "id": "ABC123",
        "ext": "mp4",
    }

    # Defining the filename returned by prepare_filename
    fake_downloader.prepare_filename.return_value = str(expected_file)

    # Replace yt_dlp.YoutubeDL with our fake downloader during this test
    with patch("src.services.reel_downloader.yt_dlp.YoutubeDL", return_value=fake_downloader):
        downloader = ReelDownloader(output_directory)
        downloaded_file = downloader.download(reel_url)

    # Making shure that function calling was well behaved and gave the correct output
    assert downloaded_file == expected_file
    assert output_directory.exists()

    # Making shure if the the yt_dlp function was called correctly
    fake_downloader.extract_info.assert_called_once_with(reel_url, download=True)
    fake_downloader.prepare_filename.assert_called_once_with(
        {
            "id": "ABC123",
            "ext": "mp4",
        }
    )
