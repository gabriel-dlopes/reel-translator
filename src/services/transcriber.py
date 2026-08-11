from faster_whisper import WhisperModel
from pathlib import Path


class Transcriber:
    def __init__(self, output_directory: Path) -> None:
        self.output_directory = output_directory
        self.model = WhisperModel("small", device="cpu", compute_type = "int8")

    def transcribe(self, audio_path: Path) -> Path:
        # Pre-conditions for transcription to start
        if not audio_path.exists():
            raise FileNotFoundError(f"Audio file does not exist: {audio_path}")

        if audio_path.suffix.lower() != ".mp3":
            raise ValueError("Transcriber requires an .mp3 audio file.")

        # Running the model on an audio path
        segments, info = self.model.transcribe(str(audio_path))

        # Turning the segments into a full transcribed text
        text = " ".join(segment.text.strip() for segment in segments)

        # Create the output directory
        self.output_directory.mkdir(parents=True, exist_ok=True)
        
        # Create the text file
        transcript_path = self.output_directory / f"{audio_path.stem}.txt"
        transcript_path.write_text(text, encoding="utf-8")

        return transcript_path



