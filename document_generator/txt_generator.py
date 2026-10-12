"""Plain-text document generation module."""

from document_generator.sanitizer import sanitize_text


def generate_txt(content: str) -> bytes:
    """Convert legal document text into a sanitized UTF-8 encoded byte stream.

    Args:
        content: The legal document body text.

    Returns:
        Bytes ready for file export or HTTP download.
    """
    clean_text = sanitize_text(content)
    return clean_text.encode("utf-8")
