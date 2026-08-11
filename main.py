import sys
from pathlib import Path

from src.services.reel_downloader import ReelDownloader
from src.services.audio_extractor import AudioExtractor
from src.services.transcriber import Transcriber
from src.services.llm_client import LocalLLMClient, Translator, Summarizer
from src.services.pdf_generator import PDFGenerator


def main() -> None: # O "-> None" means that the function only execute functions, it doesnt return
    # Checking if the reel_url argument was provided
    if len(sys.argv) < 2:
        print("Usage: python main.py <reel_url>")
        raise SystemExit(1) # Terminates the program

    reel_url = sys.argv[1]
    downloader = ReelDownloader(Path("data/input")) # Creating the ReelDownloader object
    downloaded_file = downloader.download(reel_url) # Using the object to download the reel and store the returned file path

    print(f"Reel downloaded to: {downloaded_file}")

    # Audio extraction from reel video
    extractor = AudioExtractor(Path("data/audio"))
    extracted_audio = extractor.extract(downloaded_file)

    print(f"Audio extracted to: {extracted_audio}")

    # Text extraction from audio file
    transcriber = Transcriber(Path("data/transcripts"))
    transcribed_text = transcriber.transcribe(extracted_audio)

    print(f"Transcribed text extracted to: {transcribed_text}")

    # Initate model through creating the LLM Client
    llm_client = LocalLLMClient()

    # Translation from transcribed text
    translator = Translator(llm_client)
    translated_text = translator.translate(transcribed_text)

    print(f"Translated text: {translated_text}")

    # Summarize the translation
    summarizer = Summarizer(llm_client)
    report_content = summarizer.create_report(
        reel_url=reel_url,
        transcript_path=transcribed_text,
        translated_text=translated_text,
    )

    print(f"Report content created: {report_content.title}")

    # Generate PDF report
    pdf_generator = PDFGenerator(Path("data/output"))
    pdf_path = pdf_generator.generate(report_content)

    print(f"PDF report created at: {pdf_path}")


if __name__ == "__main__":
    main()
