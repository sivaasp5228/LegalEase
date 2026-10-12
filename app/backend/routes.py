"""FastAPI route handlers for document generation."""

from fastapi import APIRouter, HTTPException, status
from app.backend.models import DocumentRequest, DocumentResponse
from ai_core.gemini_generator import GeminiDocumentGenerator

router = APIRouter(tags=["Document Generation"])


@router.post(
    "/generate",
    response_model=DocumentResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate a structured legal document",
    description="Validates document parameters and generates legal agreement text using Google Gemini 1.5 Pro.",
)
def generate_document(request: DocumentRequest) -> DocumentResponse:
    """Handle document generation request."""
    # Validate non-empty fields
    if not request.parties.strip():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Parties involved cannot be empty.",
        )
    if not request.terms.strip():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Terms and conditions cannot be empty.",
        )
    if not request.dates.strip():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Effective date cannot be empty.",
        )

    try:
        generator = GeminiDocumentGenerator(api_key=request.api_key)
        generated_text = generator.generate_document(
            document_type=request.document_type,
            parties=request.parties,
            terms=request.terms,
            dates=request.dates,
        )

        return DocumentResponse(
            status="success",
            document_type=request.document_type,
            effective_date=request.dates,
            content=generated_text,
        )
    except ValueError as val_err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(val_err),
        )
    except RuntimeError as run_err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(run_err),
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred during document generation: {str(exc)}",
        )
