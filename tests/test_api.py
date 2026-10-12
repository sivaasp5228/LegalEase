"""Test suite for FastAPI backend endpoints."""

from unittest.mock import patch
import pytest
from fastapi.testclient import TestClient
from app.backend.main import app

client = TestClient(app)


def test_root_endpoint():
    """Verify that root GET / returns operational status."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "operational"
    assert data["app"] == "LegalEase API"


def test_health_endpoint():
    """Verify that health check GET /health returns healthy."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_generate_missing_parties_validation():
    """Verify validation error when parties are missing or empty."""
    payload = {
        "document_type": "NDA",
        "parties": "",
        "terms": "Mutual confidentiality for 2 years",
        "dates": "2026-10-01",
    }
    response = client.post("/generate", json=payload)
    assert response.status_code == 422


def test_generate_missing_terms_validation():
    """Verify validation error when terms are missing or empty."""
    payload = {
        "document_type": "NDA",
        "parties": "Acme Corp and Beta LLC",
        "terms": "",
        "dates": "2026-10-01",
    }
    response = client.post("/generate", json=payload)
    assert response.status_code == 422


def test_generate_successful_with_mock():
    """Verify successful generation using a mocked Gemini generator."""
    payload = {
        "document_type": "NDA",
        "parties": "Disclosing Inc and Receiving LLC",
        "terms": "Standard mutual confidentiality for two years.",
        "dates": "2026-10-01",
    }

    mock_text = (
        "NON-DISCLOSURE AGREEMENT\n\n"
        "SECTION 1: DEFINITIONS\n"
        "Confidential information shall mean proprietary technical data.\n\n"
        "SECTION 2: OBLIGATIONS\n"
        "The receiving party shall maintain utmost confidentiality."
    )

    with patch("app.backend.routes.GeminiDocumentGenerator.generate_document", return_value=mock_text):
        response = client.post("/generate", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["document_type"] == "NDA"
        assert "NON-DISCLOSURE AGREEMENT" in data["content"]


def test_generate_with_api_key_override():
    """Verify that api_key can be passed in request body to override env."""
    payload = {
        "document_type": "Contract",
        "parties": "First Corp and Second LLC",
        "terms": "Software development services at $120/hr",
        "dates": "2026-10-01",
        "api_key": "custom_override_key",
    }
    with patch("app.backend.routes.GeminiDocumentGenerator") as MockGen:
        instance = MockGen.return_value
        instance.generate_document.return_value = "CONTRACT\n\nThis is a contract."
        response = client.post("/generate", json=payload)
        assert response.status_code == 200
        MockGen.assert_called_once_with(api_key="custom_override_key")

