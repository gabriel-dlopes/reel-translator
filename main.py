import sys
from pathlib import Path

from src.services.reel_downloader import ReelDownloader
from src.services.audio_extractor import AudioExtractor
from src.services.transcriber import Transcriber

def main() -> None: # O "-> None" means that the function only execute functions, it doesnt return
    # Checking if the reel_url argument was provided
    if len(sys.argv) < 2:
        print("Usage: python main.py <reel_url>")
        raise SystemExit(1) # Terminates the program

    reel_url = sys.argv[1]
    downloader = ReelDownloader(Path("data/input")) # Creating the ReelDownloader object
    downloaded_file = downloader.download(reel_url) # Using the object to download the reel and store the returned file path

    print(f"Reel downloaded to: {downloaded_file}")

    extractor = AudioExtractor(Path("data/audio"))
    extracted_audio = extractor.extract(downloaded_file)

    print(f"Audio extracted to: {extracted_audio}")

    transcriber = Transcriber(Path("data/output"))
    transcribed_text = transcriber.transcribe(extracted_audio)

if __name__ == "__main__":
    main()