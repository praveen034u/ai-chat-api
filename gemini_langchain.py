
try:
    from langchain_core.language_models import LLM
except ImportError:
    from langchain.llms.base import LLM
from typing import Optional, List
import google.generativeai as genai
import os

class GeminiLLM(LLM):
    model_name: str = "gemini-2.5-flash-lite-preview-06-17"
    temperature: float = 0.7
    max_tokens: int = 2048
    api_key: Optional[str] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.api_key:
            self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY environment variable is not set. Please check your .env file.")
        # Configure the API key for google.generativeai
        genai.configure(api_key=self.api_key)

    @property
    def _llm_type(self) -> str:
        return "google-genai"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        # Use the modern google.generativeai API
        model = genai.GenerativeModel(self.model_name)
        
        try:
            response = model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=self.temperature,
                    max_output_tokens=self.max_tokens
                )
            )
            return response.text if response.text else ""
        except Exception as e:
            raise ValueError(f"Error calling Gemini API: {str(e)}")
