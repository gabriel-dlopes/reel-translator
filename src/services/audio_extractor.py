from pathlib import Path
import subprocess

class AudioExtractor:
    def __init__(self, output_directory: Path) -> None:
        self.output_directory = output_directory
    
    def extract(self, video_path: Path) -> Path:

        # Pre-conditions for extraction to start
        if not video_path.exists():
            raise FileNotFoundError(f"Video file does not exist: {video_path}")

        if video_path.suffix.lower() != ".mp4":
            raise ValueError("AudioExtractor requires an .mp4 video file.")

        # Creating the audio directory
        self.output_directory.mkdir(parents=True, exist_ok=True)

        # Creating final audio_path with the output directory and file name
        audio_path = self.output_directory / f"{video_path.stem}.mp3" 
        subprocess.run(
            [
                "ffmpeg", # The executable
                "-y",   # Overwrite output file if it already exists
                "-i",   # Signals the input file
                str(video_path), # Input file
                "-vn",  # Keep only audio
                "-acodec", # Signals the encoding type
                "libmp3lame", # Encodes audio as mp3
                "-q:a", # Signals audio quality
                "2", # Audio quality
                str(audio_path), # Output file
            ],
            check=True,
        )

        return audio_path