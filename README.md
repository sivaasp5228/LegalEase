# LegalEase — AI-Powered Legal Document Generator

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-green.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-red.svg)](https://streamlit.io/)
[![Google Gemini 1.5 Pro](https://img.shields.io/badge/LLM-Gemini%201.5%20Pro-purple.svg)](https://ai.google.dev/)

---

## 1. Project Overview
**LegalEase** is a modern web application that democratizes and accelerates the creation of customized, editable legal documents using Google Gemini 1.5 Pro. Users specify the document type, participating entities, operational terms and conditions, and effective dates. LegalEase processes these inputs through a structured prompt pipeline, generates rigorous and standardized legal text, provides an interactive in-browser preview with live editing capabilities, and allows one-click exports into plain text (**TXT**), formatted Word document (**DOCX**), and printable document format (**PDF**).

---

## 2. Features
* **5 Core Document Types**:
  * Agreements (Service, Partnership, General)
  * Commercial Contracts
  * Non-Disclosure Agreements (NDAs - Unilateral and Mutual)
  * Residential & Commercial Lease Agreements
  * Employment Offer Letters
* **AI-Assisted Legal Synthesis**: Powered by Google Gemini 1.5 Pro (`google-generativeai` SDK) adhering to legal drafting conventions without fabricating party details.
* **Human-in-the-Loop Live Editing**: In-browser toggle allows immediate refinement, clause adjustment, and text customization prior to export.
* **Multi-Format Export Engine**:
  * **TXT**: Clean, lightweight UTF-8 plain text.
  * **DOCX**: Formatted Microsoft Word files using `python-docx` with formal Times New Roman typography, 1-inch margins, structured headers, and signature lines.
  * **PDF**: Printable PDFs with document headers, branding logo, body formatting, and dynamic page numbering (`FPDF`/`fpdf2`).
* **Text Sanitization Layer**: Pre-processes typographic characters (smart quotes, em-dashes, non-breaking spaces) to ensure error-free binary document encoding.
* **Decoupled Architecture**: High-speed asynchronous FastAPI backend paired with a reactive, clean Streamlit frontend.

---

## 3. Architecture

```
User Browser (Streamlit Frontend)
               │
               ▼  HTTP POST /generate
FastAPI Backend (REST API Service)
               │
               ▼  Pydantic Schema Validation (DocumentRequest)
GeminiDocumentGenerator (AI Core)
               │
               ▼  Google GenAI SDK
Google Gemini 1.5 Pro LLM
               │
               ▼  Structured Legal Text Output
Formatting & Export Engine
   ├── Sanitizer (Unicode normalization)
   ├── HTML Preview (Browser rendering)
   ├── TXT Generator (Plain text bytes)
   ├── DOCX Generator (Word document styling)
   └── PDF Generator (Header, footer, page numbering)
```

---

## 4. Technology Stack
* **Programming Language**: Python 3.10+
* **Backend Framework**: FastAPI & Uvicorn
* **Frontend Framework**: Streamlit
* **Generative AI Model**: Google Gemini 1.5 Pro
* **AI SDK**: `google-generativeai`
* **Data Validation**: Pydantic v2
* **Document Processing**: `python-docx`, `fpdf2`, `Pillow`
* **HTTP Client**: `requests`, `httpx`
* **Configuration**: `python-dotenv`
* **Testing**: `pytest`

---

## 5. Project Structure

```
LegalEase/
│
├── 1. Brainstorming & Ideation/     # Problem statement, idea overview, target users, use cases
├── 2. Requirement Analysis/         # Functional, non-functional, and tech requirements
├── 3. Project Design Phase/         # Architecture, data flow, API design, UI wireframes
├── 4. Project Planning Phase/       # Milestones, task breakdown, development roadmap
├── 5. Project Development Phase/    # Implementation notes and module descriptions
├── 6. Project Testing/              # Test strategy, test cases, execution templates
├── 7. Project Documentation/        # User guide, developer guide, API docs, installation
├── 8. Project Demonstration/        # Live demo scripts, flows, and screenshot guides
│
├── app/
│   ├── backend/                     # FastAPI Application
│   │   ├── main.py                  # App entry point, CORS, health endpoints
│   │   ├── routes.py                # REST endpoints (/generate)
│   │   ├── models.py                # Pydantic schemas (DocumentRequest, DocumentResponse)
│   │   └── __init__.py
│   │
│   ├── frontend/                    # Streamlit Web UI
│   │   ├── app.py                   # Main UI entry point
│   │   ├── components.py            # Reusable UI widgets & headers
│   │   ├── styles.py                # Custom CSS styles
│   │   └── __init__.py
│   │
│   └── __init__.py
│
├── ai_core/                         # Generative AI Logic
│   ├── gemini_generator.py          # Gemini 1.5 Pro client & orchestration
│   ├── prompts.py                   # Structured legal drafting prompts
│   └── __init__.py
│
├── document_generator/              # Document Exporters & Formatters
│   ├── docx_generator.py            # python-docx formatting engine
│   ├── pdf_generator.py             # FPDF printable PDF engine
│   ├── txt_generator.py             # UTF-8 plain text exporter
│   ├── html_preview.py              # In-app styled HTML previewer
│   ├── sanitizer.py                 # Typographic quote & unicode cleaner
│   └── __init__.py
│
├── assets/                          # Branding & Static Assets
│   ├── logo.png                     # Application and document logo
│   └── fonts/                       # Custom typography assets
│
├── tests/                           # Automated Pytest Suite
│   ├── test_api.py                  # API endpoints and validation tests
│   ├── test_ai_generation.py        # Gemini client & prompt formatting tests
│   ├── test_document_types.py       # Cross-exporter tests for all 5 document types
│   ├── test_docx.py                 # Word document generation tests
│   ├── test_e2e_pipeline.py         # End-to-end API, error handling & pipeline tests
│   ├── test_pdf.py                  # PDF layout and byte generation tests
│   └── test_txt.py                  # Plaintext & sanitization tests
│
├── .env.example                     # Environment variables template
├── .gitignore                       # Git ignore definitions
├── requirements.txt                 # Project dependencies
└── README.md                        # Master project documentation
```

---

## 6. Installation

### 1. Prerequisites
Ensure you have Python 3.10 or newer installed:
```bash
python --version
```

### 2. Set Up a Virtual Environment
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 7. Environment Variable Setup
Copy the `.env.example` file to create your `.env`:
```bash
cp .env.example .env
```
Open `.env` and set your Google Gemini API key:
```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
BACKEND_URL=http://127.0.0.1:8000
```
> Obtain your key at [Google AI Studio](https://aistudio.google.com/).

---

## 8. Running Backend
Launch the FastAPI backend with Uvicorn:
```bash
uvicorn app.backend.main:app --reload --port 8000
```
* **Interactive API Docs (Swagger UI)**: `http://127.0.0.1:8000/docs`
* **Health Check**: `http://127.0.0.1:8000/health`

---

## 9. Running Frontend
In a separate terminal tab, launch the Streamlit frontend:
```bash
streamlit run app/frontend/app.py
```
The interface will automatically launch in your default web browser at `http://localhost:8501`.

---

## 10. API Endpoint Documentation

### `GET /`
Returns service metadata and operational status.

### `GET /health`
Liveness check returning `{"status": "healthy"}`.

### `POST /generate`
Generates a structured legal document based on user inputs.

**Request Body (`application/json`)**:
```json
{
  "document_type": "NDA",
  "parties": "Alpha Corp (Disclosing Party) and Beta Inc (Receiving Party)",
  "terms": "Mutual confidentiality for 2 years, non-disclosure of source code and proprietary trade secrets.",
  "dates": "2026-10-01"
}
```

**Response (`200 OK`)**:
```json
{
  "status": "success",
  "document_type": "NDA",
  "effective_date": "2026-10-01",
  "content": "MUTUAL NON-DISCLOSURE AGREEMENT\n\nThis Mutual Non-Disclosure Agreement...",
  "disclaimer": "This document was generated using generative artificial intelligence and is provided for informational and drafting assistance only. It does not constitute formal legal counsel."
}
```

---

## 11. Document Export Information
* **TXT Export**: Outputs UTF-8 plain text preserving paragraph breaks.
* **DOCX Export**: Microsoft Word format styled with:
  * 1-inch (72pt) margins on all sides.
  * Formal Times New Roman font (12pt body text, 1.15 line spacing).
  * Styled section headings in bold.
  * Branding logo on the first page when present.
  * Formatted execution and signature lines.
* **PDF Export**: Standard printable PDF output built via `fpdf2`:
  * Running header with document title and logo.
  * Running footer with date and dynamic page numbering (`Page {page} of {nb}`).
  * Formatted section titles and bullet-style list rendering where applicable.

---

## 12. Testing
Execute the complete automated test suite with pytest:
```bash
pytest -v
```
To run specific test modules:
```bash
pytest tests/test_api.py -v
pytest tests/test_docx.py -v
pytest tests/test_pdf.py -v
```

---

## 13. Security Notes
* **Secrets Isolation**: The `GEMINI_API_KEY` is loaded exclusively from environment variables or local `.env` files. It is strictly excluded by `.gitignore` and is never exposed in client bundles or logged to console.
* **CORS Restrictions**: FastAPI is configured with explicit CORS origins, disallowing arbitrary external origins from consuming the API.
* **Input Sanitization**: Inbound content is sanitized before PDF generation to prevent encoding errors and unprintable character exploits.

---

## 14. Legal Disclaimer
> **IMPORTANT NOTICE**: LegalEase is an AI-assisted document drafting and informational tool. The documents generated by this system are produced by generative artificial intelligence (Google Gemini 1.5 Pro) based upon user-provided parameters. LegalEase **DOES NOT** provide legal advice, legal representation, or attorney-client privileged services. Laws vary significantly across jurisdictions, states, and countries. Users must have any generated document reviewed, verified, and amended by a licensed, qualified attorney prior to signing or execution.
