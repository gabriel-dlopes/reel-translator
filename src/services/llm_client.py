import requests
from pathlib import Path

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

    # Define summarizer function
    def summarize(self, translated_text: str) -> str:
        prompt = f"""
    Summarize and explain the content of the following transcript, in Portuguese from Portugal.

    Transcript:
    {translated_text}
    """

        return self.llm_client.generate(prompt)