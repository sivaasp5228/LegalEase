"""Gemini Document Generator interface for LegalEase."""

import os
from pathlib import Path
from dotenv import load_dotenv
from ai_core.prompts import LEGAL_SYSTEM_INSTRUCTION, build_prompt

# Reliably locate project root .env regardless of working directory
ROOT_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = ROOT_DIR / ".env"
load_dotenv(dotenv_path=ENV_FILE, override=True)


class GeminiDocumentGenerator:
    """Manages legal document generation using Google Gemini 1.5 Pro."""

    def __init__(self, api_key: str | None = None, model_name: str | None = None):
        """Initialize the Gemini client with the configured API key."""
        load_dotenv(dotenv_path=ENV_FILE, override=True)
        self._explicit_key = api_key is not None
        if self._explicit_key:
            self.api_key = api_key.strip()
        else:
            self.api_key = os.getenv("GEMINI_API_KEY")
        self.model_name = model_name or os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")
        self._model = None

    def _ensure_client(self):
        """Ensure the Gemini API client is initialized."""
        if not self._explicit_key and (not self.api_key or self.api_key.strip() in ("", "your_api_key_here", "YOUR_GEMINI_API_KEY")):
            load_dotenv(dotenv_path=ENV_FILE, override=True)
            self.api_key = os.getenv("GEMINI_API_KEY")

        if not self.api_key or self.api_key.strip() in ("", "your_api_key_here", "YOUR_GEMINI_API_KEY"):
            raise ValueError(
                "GEMINI_API_KEY environment variable is missing. "
                "Please configure GEMINI_API_KEY in your .env file or environment."
            )

        if self._model is None:
            try:
                import google.generativeai as genai
                genai.configure(api_key=self.api_key)
                self._model = genai.GenerativeModel(
                    model_name=self.model_name,
                    system_instruction=LEGAL_SYSTEM_INSTRUCTION,
                )
            except ImportError:
                raise ImportError(
                    "The 'google-generativeai' package is not installed. "
                    "Install dependencies via 'pip install -r requirements.txt'."
                )

    def generate_document(
        self,
        document_type: str,
        parties: str,
        terms: str,
        dates: str,
    ) -> str:
        """Generate structured legal text using Gemini models.

        Args:
            document_type: Type of document (e.g. NDA, Agreement, Contract).
            parties: Descriptions of the involved parties.
            terms: The operational and legal terms.
            dates: Effective and termination dates.

        Returns:
            Clean, structured legal document text.
        """
        self._ensure_client()
        prompt = build_prompt(
            document_type=document_type,
            parties=parties,
            terms=terms,
            dates=dates,
        )

        try:
            # Low temperature ensures deterministic, legally structured generation
            generation_config = {
                "temperature": 0.2,
                "top_p": 0.95,
            }
            request_options = {
                "timeout": 45,
            }
            try:
                response = self._model.generate_content(
                    prompt,
                    generation_config=generation_config,
                    request_options=request_options,
                )
            except Exception as model_err:
                err_msg = str(model_err).lower()
                # If model is deprecated or exceeded specific model quota, try fallback models
                if any(x in err_msg for x in ["not found", "no longer available", "quota", "429", "resourceexhausted", "deadline", "timed out"]):
                    import google.generativeai as genai
                    fallback_models = ["gemini-3.5-flash-lite", "gemini-3.1-flash-lite", "gemini-3.7-flash"]
                    response = None
                    last_err = model_err
                    for fb_name in fallback_models:
                        if fb_name == self.model_name:
                            continue
                        try:
                            fb_model = genai.GenerativeModel(
                                model_name=fb_name,
                                system_instruction=LEGAL_SYSTEM_INSTRUCTION,
                            )
                            response = fb_model.generate_content(
                                prompt,
                                generation_config=generation_config,
                                request_options=request_options,
                            )
                            if response:
                                self.model_name = fb_name
                                break
                        except Exception as fb_err:
                            last_err = fb_err
                            continue
                    if response is None:
                        if "429" in str(last_err) or "resourceexhausted" in str(last_err).lower():
                            raise RuntimeError(
                                "Gemini API rate limit or quota exceeded (429). "
                                "Please wait a moment, verify your Google AI Studio quota, or provide a custom API key in the sidebar."
                            ) from last_err
                        raise last_err
                else:
                    raise

            if not response:
                raise RuntimeError(f"No response returned from Gemini model ({self.model_name}).")

            # Validate candidate finish reason if text accessor throws
            try:
                text = response.text
            except (ValueError, AttributeError) as accessor_err:
                candidate = response.candidates[0] if response.candidates else None
                finish_reason = getattr(candidate, "finish_reason", "UNKNOWN")
                raise RuntimeError(
                    f"Gemini output could not be retrieved (finish_reason: {finish_reason}): {str(accessor_err)}"
                ) from accessor_err

            if not text or not text.strip():
                raise RuntimeError("Empty text generated by Gemini model.")

            return text.strip()
        except Exception as e:
            raise RuntimeError(f"Gemini document generation failed: {str(e)}") from e

