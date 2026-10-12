"""Pydantic data models for the LegalEase backend API."""

from enum import Enum
from pydantic import BaseModel, Field


class DocumentType(str, Enum):
    """Supported legal document types."""
    AGREEMENT = "Agreement"
    CONTRACT = "Contract"
    NDA = "NDA"
    LEASE_AGREEMENT = "Lease Agreement"
    EMPLOYMENT_OFFER_LETTER = "Employment Offer Letter"


class DocumentRequest(BaseModel):
    """Input payload schema for legal document generation."""
    document_type: str = Field(
        ...,
        description="Type of legal document (Agreement, Contract, NDA, Lease Agreement, Employment Offer Letter)",
        examples=["NDA"]
    )
    parties: str = Field(
        ...,
        min_length=2,
        description="Names, roles, and entities of all parties involved in the document",
        examples=["Apex Tech Corp (Disclosing Party) and Beacon Labs Inc (Receiving Party)"]
    )
    terms: str = Field(
        ...,
        min_length=5,
        description="Key terms, covenants, obligations, deliverables, or compensation",
        examples=["Mutual confidentiality for 2 years regarding proprietary algorithms and client lists."]
    )
    dates: str = Field(
        ...,
        min_length=2,
        description="Effective date and any expiration, term length, or milestones",
        examples=["October 1, 2026"]
    )
    api_key: str | None = Field(
        default=None,
        description="Optional API key override for Google Gemini",
        examples=["AIzaSy..."]
    )


class DocumentResponse(BaseModel):
    """Output schema for successfully generated legal documents."""
    status: str = Field(default="success", description="Status of the generation operation")
    document_type: str = Field(..., description="Echoed document type")
    effective_date: str = Field(..., description="Echoed effective date")
    content: str = Field(..., description="Generated legal document text")
    disclaimer: str = Field(
        default=(
            "LegalEase is an AI-powered legal document generator and informational tool. "
            "The generated content does not constitute formal legal advice and should be "
            "reviewed by a licensed, qualified legal professional before execution."
        ),
        description="Standard legal advisory disclaimer"
    )
