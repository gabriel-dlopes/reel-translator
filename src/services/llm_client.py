import requests
from pathlib import Path
from src.services.report import ReportContent

class LocalLLMClient:
    def __init__(
        self,
        model_name: str = "qwen2.5:14b",
        base_url: str = "http://localhost:11434",
        timeout: int = 120,
    ) -> None:
        self.model_name = model_name
        self.base_url = base_url
        self.timeout = timeout

    # This function creates the LLM response for a given prompt
    def generate(self, prompt: str) -> str:
        # Building the POST request to send to Ollama API
        response = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": self.model_name,
                "prompt": prompt,
                "stream": False,
            },
            timeout=self.timeout,
        )

        # Asking and returning the response payload
        response.raise_for_status()
        return response.json()["response"]

class Translator:
    # Initiate the translator object
    def __init__(self, llm_client: LocalLLMClient) -> None:
            self.llm_client = llm_client
    
    # Defining the translate function
    def translate(self, transcript_path: Path) -> str:
        transcript_text = transcript_path.read_text(encoding="utf-8")
        prompt = f"""
Translate the following transcript into natural European Portuguese.

Rules:
- Preserve the original meaning.
- Use natural Portuguese from Portugal.
- Do not use Brazilian Portuguese expressions.
- Prefer a faithful but readable translation over a literal word-by-word translation.
- If the source text is literary or poetic, preserve that tone while keeping the Portuguese clear.
- Do not summarize.
- Do not add explanations, notes, introductions, or conclusions.
- Return only the translated text.

Transcript:
{transcript_text}
"""

        return self.llm_client.generate(prompt)


class Summarizer:
    # Initiate the summarizer object
    def __init__(self, llm_client: LocalLLMClient) -> None:
        self.llm_client = llm_client

    # Create the content that will later populate the PDF report
    def create_report(
        self,
        reel_url: str,
        transcript_path: Path,
        translated_text: str,
    ) -> ReportContent:
        transcript_text = transcript_path.read_text(encoding="utf-8")

        summary = self._generate_summary(transcript_text, translated_text)
        explanation = self._generate_explanation(transcript_text, translated_text)
        key_takeaways = self._generate_key_takeaways(transcript_text, translated_text)

        return ReportContent(
            title="Relatório de Tradução do Reel",
            source_url=reel_url,
            transcript=transcript_text,
            translation=translated_text,
            summary=summary,
            explanation=explanation,
            key_takeaways=key_takeaways,
        )

    def _generate_summary(self, transcript_text: str, translated_text: str) -> str:
        prompt = f"""
Write a concise executive summary in European Portuguese.

Rules:
- Use natural Portuguese from Portugal.
- Do not use Brazilian Portuguese expressions.
- Write in the third person.
- Do not write in the voice of the speaker.
- Use 3 to 4 sentences maximum.
- Summarize the central meaning; do not paraphrase the full text.
- Do not include introductions such as "Aqui está" or "Segue".
- Do not mention that this is a summary.
- Do not use Brazilian gerunds such as "questionando", "lutando", or "experimentando"; prefer European Portuguese forms such as "a questionar", "a lutar", or "a viver".
- Return only the summary content.

Original transcript:
{transcript_text}

Portuguese translation:
{translated_text}
"""
        return self.llm_client.generate(prompt)

    def _generate_explanation(self, transcript_text: str, translated_text: str) -> str:
        prompt = f"""
Explain the main ideas of the following text in European Portuguese.
Make the explanation useful for someone who wants to understand the content deeply.

Rules:
- Use natural Portuguese from Portugal.
- Do not use Brazilian Portuguese expressions.
- Write in the third person.
- Do not include introductions such as "Vou explicar" or "Aqui está".
- Do not add reading suggestions.
- Avoid meta-commentary such as "Em resumo" or "Outro aspecto interessante".
- Do not use Brazilian gerunds such as "questionando", "lutando", or "experimentando"; prefer European Portuguese forms such as "a questionar", "a lutar", or "a viver".
- Return only the explanation content.

Original transcript:
{transcript_text}

Portuguese translation:
{translated_text}
"""
        return self.llm_client.generate(prompt)

    def _generate_key_takeaways(self, transcript_text: str, translated_text: str) -> str:
        prompt = f"""
Extract the key takeaways from the following text in European Portuguese.

Rules:
- Use natural Portuguese from Portugal.
- Do not use Brazilian Portuguese expressions.
- Return only short bullet points.
- Do not include introductions such as "Aqui estão os principais pontos".
- Each bullet point must start with "- ".
- Write in the third person.

Original transcript:
{transcript_text}

Portuguese translation:
{translated_text}
"""
        return self.llm_client.generate(prompt)
