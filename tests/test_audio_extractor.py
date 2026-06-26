from pathlib import Path
from unittest.mock import MagicMock
import pytest
from src.services.audio_extractor import AudioExtractor

def test_rejects_missing_file(tmp_path: Path) -> None: # Pytest detects the tmp_path and creates it
    # Arrange
    extractor = AudioExtractor(Path("data/audio")) # Creating the object that will be tested

    # Mock video
    missing_video = tmp_path / "missing.mp4"

    # Act and Assert
    with pytest.raises(FileNotFoundError):
        extractor.extract(missing_video)

def test_rejects_invalid_file(tmp_path: Path) -> None:
    # Arrange
    extractor = AudioExtractor(Path("data/audio")) # Creating the object that will be tested

    # Mock video
    video_path = tmp_path / "video.txt"
    video_path.touch() # creating a temporary file

    # Act and Assert
    with pytest.raises(ValueError):
        extractor.extract(video_path)

