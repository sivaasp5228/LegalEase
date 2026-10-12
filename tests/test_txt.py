"""Test suite for plain text generation and unicode sanitization."""

from document_generator.sanitizer import sanitize_text
from document_generator.txt_generator import generate_txt


def test_sanitize_text_curly_quotes_and_dashes():
    """Verify that smart quotes and dashes are converted to safe equivalents."""
    raw = '“Section 1: The ‘Confidential Information’—as defined herein.”'
    cleaned = sanitize_text(raw)
    assert '“' not in cleaned
    assert '”' not in cleaned
    assert '‘' not in cleaned
    assert '’' not in cleaned
    assert '—' not in cleaned
    assert '"Section 1: The \'Confidential Information\'--as defined herein."' == cleaned


def test_sanitize_text_bullets_and_symbols():
    """Verify replacement of bullets and non-breaking spaces."""
    raw = "• Item one\xa0with non-breaking space © 2026"
    cleaned = sanitize_text(raw)
    assert "•" not in cleaned
    assert "\xa0" not in cleaned
    assert "* Item one with non-breaking space (c) 2026" == cleaned


def test_generate_txt_returns_bytes():
    """Verify generate_txt returns valid UTF-8 bytes."""
    text = "LEGAL AGREEMENT\n\nSection 1: Scope of Work."
    data = generate_txt(text)
    assert isinstance(data, bytes)
    assert b"LEGAL AGREEMENT" in data
    assert data.decode("utf-8").startswith("LEGAL AGREEMENT")


def test_generate_html_preview():
    """Verify generate_html_preview creates valid parchment HTML with tables and titles."""
    from document_generator.html_preview import generate_html_preview
    sample = (
        "CONFIDENTIALITY AGREEMENT\n\n"
        "| Term | Details |\n"
        "| Period | 2 Years |\n\n"
        "SECTION 1: PURPOSE\n"
        "Mutual discussion.\n\n"
        "[DISCLAIMER: AI generated.]"
    )
    html_output = generate_html_preview(sample)
    assert '<div class="legal-parchment">' in html_output
    assert '<h1 class="legal-doc-title">CONFIDENTIALITY AGREEMENT</h1>' in html_output
    assert '<h2 class="legal-section-heading">SECTION 1: PURPOSE</h2>' in html_output
    assert '<table' in html_output
    assert 'Period' in html_output
    assert '<div class="legal-disclaimer-box">' in html_output

