from dataclasses import dataclass

# Defining the PDF structure
@dataclass(frozen=True)
class ReportContent:
    title: str
    source_url: str
    transcript: str
    translation: str
    summary: str
    explanation: str
    key_takeaways: str