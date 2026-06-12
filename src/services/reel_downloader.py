from pathlib import Path
import yt_dlp

class ReelDownloader:
    def __init__(self, output_directory: Path) -> None:
        self.output_directory = output_directory
    
    # Creating the output directory if necessary
    def download(self, reel_url: str) -> Path:
        self._validate_url(reel_url)
        self.output_directory.mkdir(parents=True, exist_ok=True)
        
        
        # Define the options to be used in the yt_dlp function
        options = {
            "outtmpl": str(self.output_directory/ "%(id)s.%(ext)s"), # id ans ext come from the reel's metadata that yt_dlp reads
            "format": "best[ext=mp4]/best",
            "noplaylist":True
        }

        with yt_dlp.YoutubeDL(options) as downloader: # creating the downloader object that belongs to the YoutubeDL class
            reel_info = downloader.extract_info(reel_url, download=True) # reads the reel metadata and downloads it
            downloaded_file = downloader.prepare_filename(reel_info) # builds the filename using the metadata
        
        return Path(downloaded_file)

    # Validate the URL
    def _validate_url(self,reel_url: str) -> None:
        if not reel_url.startswith(
            (
            "https://www.instagram.com/reel/", 
            "https://instagram.com/reel/"
            )
        ):
            raise ValueError("A valid Instagram Reel URL is required.")

