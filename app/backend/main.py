"""FastAPI main application entrypoint for LegalEase."""

import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from app.backend.routes import router as document_router

# Reliably load LegalEase/.env from repository root regardless of current working directory
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILE = ROOT_DIR / ".env"
load_dotenv(dotenv_path=ENV_FILE, override=True)

# Initialize FastAPI instance
app = FastAPI(
    title="LegalEase API",
    description="AI-Powered Legal Document Generator Backend powered by Google Gemini 1.5 Pro.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS for local Streamlit frontend
FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "http://localhost:8501")
ALLOWED_ORIGINS = [
    FRONTEND_ORIGIN,
    "http://127.0.0.1:8501",
    "http://localhost:8501",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["System"])
def root():
    """Service root endpoint returning basic operational metadata."""
    return {
        "app": "LegalEase API",
        "version": "1.0.0",
        "status": "operational",
        "docs_url": "/docs",
        "description": "AI-Powered Legal Document Generator Backend",
    }


@app.get("/health", tags=["System"])
def health():
    """Health check endpoint for liveness and monitoring."""
    load_dotenv(dotenv_path=ENV_FILE, override=True)
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    model_name = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite").strip()
    gemini_configured = bool(api_key and api_key != "your_api_key_here")
    return {
        "status": "healthy",
        "service": "LegalEase Backend",
        "gemini_configured": gemini_configured,
        "model_name": model_name,
    }


# Include document generation router
app.include_router(document_router)
