import requests
from pathlib import Path
from src.services.report import ReportContent

class LocalLLMClient:
    def __init__(
        self,
        model_name: str = "llama3.1:8b",
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
    Translate the following transcript to Portuguese from Portugal.

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

        summary = self._generate_summary(translated_text)
        explanation = self._generate_explanation(translated_text)
        key_takeaways = self._generate_key_takeaways(translated_text)

        return ReportContent(
            title="Reel Translation Report",
            source_url=reel_url,
            transcript=transcript_text,
            translation=translated_text,
            summary=summary,
            explanation=explanation,
            key_takeaways=key_takeaways,
        )

    def _generate_summary(self, translated_text: str) -> str:
        prompt = f"""
Summarize the following text in European Portuguese.
Be concise and clear.

Text:
{translated_text}
"""
        return self.llm_client.generate(prompt)

    def _generate_explanation(self, translated_text: str) -> str:
        prompt = f"""
Explain the main ideas of the following text in European Portuguese.
Make the explanation useful for someone who wants to understand the content deeply.

Text:
{translated_text}
"""
        return self.llm_client.generate(prompt)

    def _generate_key_takeaways(self, translated_text: str) -> str:
        prompt = f"""
Extract the key takeaways from the following text in European Portuguese.
Return each takeaway as a short bullet point.

Text:
{translated_text}
"""
        return self.llm_client.generate(prompt)