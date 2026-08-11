from pathlib import Path

from fpdf import FPDF

from src.services.report import ReportContent


class PDFGenerator:
    def __init__(self, output_directory: Path) -> None:
        self.output_directory = output_directory

    def generate(self, report: ReportContent) -> Path:
        self.output_directory.mkdir(parents=True, exist_ok=True)

        report_path = self.output_directory / "reel_report.pdf"

        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()

        pdf.set_font("Helvetica", "B", 16)
        pdf.cell(0, 10, self._normalize_text(report.title), new_x="LMARGIN", new_y="NEXT")

        self._add_section(pdf, "URL de Origem", report.source_url)
        self._add_section(pdf, "Resumo", report.summary)
        self._add_section(pdf, "Explicação", report.explanation)
        self._add_section(pdf, "Principais Pontos", report.key_takeaways)
        self._add_section(pdf, "Tradução", report.translation)
        self._add_section(pdf, "Transcrição Original", report.transcript)

        pdf.output(report_path)

        return report_path

    def _add_section(self, pdf: FPDF, title: str, body: str) -> None:
        pdf.ln(6)

        pdf.set_font("Helvetica", "B", 13)
        pdf.multi_cell(0, 8, self._normalize_text(title), new_x="LMARGIN", new_y="NEXT")

        pdf.set_font("Helvetica", "", 11)
        pdf.multi_cell(0, 7, self._normalize_text(body), new_x="LMARGIN", new_y="NEXT")

    def _normalize_text(self, text: str) -> str:
        replacements = {
            "•": "-",
            "–": "-",
            "—": "-",
            "“": '"',
            "”": '"',
            "‘": "'",
            "’": "'",
            "…": "...",
        }

        for original, replacement in replacements.items():
            text = text.replace(original, replacement)

        return text.encode("latin-1", errors="replace").decode("latin-1")
