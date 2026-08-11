# Reel Translator

Local CLI application that receives an Instagram Reel URL and generates a Portuguese report as a PDF.

The application downloads the Reel, extracts its audio, transcribes it locally, translates the transcript with a local LLM, generates report content, and writes a PDF report.

## Current Workflow

```text
Instagram Reel URL
-> Download video with yt-dlp
-> Extract audio with FFmpeg
-> Transcribe audio locally with faster-whisper
-> Translate and analyse text with Ollama
-> Generate a PDF report with fpdf2
```

Only the Reel download requires internet access. Transcription, translation, summarisation, and PDF generation run locally after the media file has been downloaded.

## Requirements

- Python 3.12+
- FFmpeg
- Ollama
- An Ollama model, currently `qwen2.5:14b`

Python dependencies are listed in `requirements.txt`.

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd reel-translator
```

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

Install Python dependencies:

```bash
python -m pip install -r requirements.txt
```

Install FFmpeg on macOS:

```bash
brew install ffmpeg
```

Check FFmpeg:

```bash
ffmpeg -version
```

Install Ollama:

```bash
brew install ollama
```

Start Ollama in a separate terminal:

```bash
ollama serve
```

Pull the local LLM model:

```bash
ollama pull qwen2.5:14b
```

Check that Ollama can see the model:

```bash
ollama list
```

## Usage

Activate the virtual environment:

```bash
source .venv/bin/activate
```

Make sure Ollama is running:

```bash
ollama serve
```

In another terminal, run the application:

```bash
python main.py "https://www.instagram.com/reel/REEL_ID/"
```

Use quotes around the URL. Instagram URLs often contain characters such as `?` and `&`, which shells may interpret incorrectly if the URL is not quoted.

The generated files are written to:

```text
data/input/        downloaded video files
data/audio/        extracted audio files
data/transcripts/  generated transcript files
data/output/       generated PDF reports
```

The final report is currently written to:

```text
data/output/reel_report.pdf
```

## Troubleshooting

If `yt-dlp` fails on an accessible public Reel, update it:

```bash
python -m pip install --upgrade yt-dlp
```

If Ollama is not reachable, start the server:

```bash
ollama serve
```

If the model is missing:

```bash
ollama pull qwen2.5:14b
```

If the shell rejects the Reel URL, wrap it in quotes:

```bash
python main.py "https://www.instagram.com/reel/REEL_ID/"
```

## Testing

Run the test suite with:

```bash
python -m pytest -v
```

Run a single test file:

```bash
python -m pytest tests/test_reel_downloader.py -v
```

## Project Structure

```text
.
├── main.py
├── requirements.txt
├── src/
│   ├── services/
│   │   ├── audio_extractor.py
│   │   ├── llm_client.py
│   │   ├── pdf_generator.py
│   │   ├── reel_downloader.py
│   │   ├── report.py
│   │   └── transcriber.py
│   ├── config.py
│   └── pipeline.py
├── data/
│   ├── input/
│   ├── audio/
│   ├── transcripts/
│   ├── translations/
│   └── output/
└── tests/
```

## Notes

Generated media, transcript, translation, and PDF files are ignored by Git.

Some Instagram Reels may require authentication or cookies. The current version is intended for public Reels.
