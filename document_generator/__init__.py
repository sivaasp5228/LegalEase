"""LegalEase document generators and formatting package."""

from document_generator.sanitizer import sanitize_text
from document_generator.txt_generator import generate_txt

__all__ = [
    "sanitize_text",
    "generate_txt",
]

try:
    from document_generator.docx_generator import generate_docx
    __all__.append("generate_docx")
except ImportError:
    pass

try:
    from document_generator.pdf_generator import generate_pdf
    __all__.append("generate_pdf")
except ImportError:
    pass

try:
    from document_generator.html_preview import generate_html_preview
    __all__.append("generate_html_preview")
except ImportError:
    pass

