"""Test suite for AI core prompt generation and Gemini client handling."""

from unittest.mock import MagicMock, patch
import pytest
from ai_core.prompts import build_prompt
from ai_core.gemini_generator import GeminiDocumentGenerator


def test_build_prompt_contains_all_fields():
    """Verify that build_prompt injects user arguments into the prompt text."""
    prompt = build_prompt(
        document_type="Employment Offer Letter",
        parties="TechCorp and Jane Doe",
        terms="Salary $150,000, 4 weeks PTO, health insurance",
        dates="November 1, 2026",
    )
    assert "Employment Offer Letter" in prompt
    assert "TechCorp and Jane Doe" in prompt
    assert "Salary $150,000" in prompt
    assert "November 1, 2026" in prompt


def test_gemini_generator_missing_api_key_raises():
    """Verify that GeminiDocumentGenerator raises ValueError when API key is absent."""
    generator = GeminiDocumentGenerator(api_key="")
    with pytest.raises(ValueError, match="GEMINI_API_KEY environment variable is missing"):
        generator.generate_document("NDA", "Parties", "Terms", "2026-10-01")


def test_gemini_generator_mock_success():
    """Verify that GeminiDocumentGenerator handles response text correctly."""
    generator = GeminiDocumentGenerator(api_key="test_dummy_key")

    mock_model = MagicMock()
    mock_response = MagicMock()
    mock_response.text = "AGREEMENT\n\nThis is a mocked legal agreement."
    mock_model.generate_content.return_value = mock_response

    generator._model = mock_model

    result = generator.generate_document(
        document_type="Agreement",
        parties="Alpha and Beta",
        terms="Standard terms",
        dates="2026-10-01",
    )

    assert "This is a mocked legal agreement" in result
    mock_model.generate_content.assert_called_once()
