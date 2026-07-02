from pathlib import Path
from unittest.mock import MagicMock
import pytest
from src.services.transcriber import Transcriber

def test_rejects_missing_file(tmp_path: Path) -> None: # Pytest detects the tmp_path and creates it
    # Arrange
    transcriber = Transcriber(Path("data/output")) # Creating the object that will be tested

    # Mock audio
    missing_audio= tmp_path / "missing.mp3"

    # Act and Assert
    with pytest.raises(FileNotFoundError):
        transcriber.transcribe(missing_audio)

def test_rejects_invalid_file(tmp_path: Path) -> None:
    # Arrange
    transcriber = Transcriber(Path("data/audio")) # Creating the object that will be tested

    # Mock audio
    audio_path = tmp_path / "audio.txt"
    audio_path.touch() # creating a temporary file

    # Act and Assert
    with pytest.raises(ValueError):
        transcriber.transcribe(audio_path)



