# Reel Translator

Local Python CLI application for processing an Instagram Reel URL into a Portuguese (Portugal) translation report.

The planned workflow is:

1. Download the Instagram Reel.
2. Extract the audio from the downloaded video.
3. Transcribe the audio.
4. Translate the transcript to Portuguese (Portugal).
5. Generate a summary and explanation.
6. Create a PDF report.

## Project Status

This repository is scaffolded for future implementation. The architecture is intended to use clear object-oriented service boundaries and dependency injection through a central pipeline class.

## Planned Architecture

```text
reel-translator/
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
├── main.py
├── src/
│   ├── config.py
│   ├── pipeline.py
│   ├── models/
│   ├── services/
│   └── utils/
├── data/
│   ├── input/
│   ├── audio/
│   ├── transcripts/
│   └── output/
└── tests/
```

## Planned Service Classes

The application is expected to use the following service classes:

- `ReelDownloader`: downloads Instagram Reels using `yt-dlp`.
- `AudioExtractor`: extracts audio from downloaded video files using `moviepy` and `ffmpeg`.
- `Transcriber`: transcribes audio using OpenAI APIs.
- `Translator`: translates transcripts to Portuguese (Portugal) using OpenAI APIs.
- `Summarizer`: generates a summary and explanation using OpenAI APIs.
- `PDFGenerator`: creates a final PDF report using `fpdf2`.

The `ReelTranslationPipeline` class will orchestrate these services using dependency injection.

## Requirements

- Python 3.12 or newer
- `ffmpeg` installed and available on your system path
- OpenAI API key

Planned Python dependencies:

- `yt-dlp`
- `moviepy`
- `openai`
- `fpdf2`
- `python-dotenv`
- `pytest`

## Installation

Clone the repository and enter the project directory:

```bash
git clone <repository-url>
cd reel-translator
```

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate the virtual environment:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## Configuration

Create a local environment file from the example:

```bash
cp .env.example .env
```

Add your OpenAI API key:

```text
OPENAI_API_KEY=your_api_key_here
```

The `.env` file should not be committed to version control.

## Usage

After implementation, the CLI is expected to run with:

```bash
python main.py "https://www.instagram.com/reel/..."
```

The expected output will be a PDF report written to:

```text
data/output/
```

Intermediate files should be stored in:

- `data/input/` for downloaded video files
- `data/audio/` for extracted audio
- `data/transcripts/` for transcript artifacts
- `data/output/` for final reports

## Testing

After implementation, run tests with:

```bash
pytest
```

## Development Notes

Implementation should follow these principles:

- Python 3.12+
- Type hints throughout
- Dataclasses where appropriate
- Logging for pipeline progress and service-level events
- Dependency injection for testability and future extension
- Clear separation between configuration, models, services, utilities, and orchestration
