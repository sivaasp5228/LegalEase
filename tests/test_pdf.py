"""Test suite for PDF export generation."""

from document_generator.pdf_generator import generate_pdf


def test_generate_pdf_produces_valid_pdf_bytes():
    """Verify generate_pdf returns valid PDF binary stream starting with %PDF."""
    sample_content = (
        "EMPLOYMENT OFFER LETTER\n\n"
        "SECTION 1: POSITION AND DUTIES\n"
        "Employee shall serve as Senior Software Engineer.\n\n"
        "* Compensation: $160,000 per annum\n"
        "* Benefits: Health, Dental, Vision\n\n"
        "SECTION 2: AT-WILL EMPLOYMENT\n"
        "Employment remains at-will at all times.\n\n"
        "[DISCLAIMER: For informational use only.]"
    )

    pdf_bytes = generate_pdf(sample_content, title="EMPLOYMENT OFFER LETTER")
    assert isinstance(pdf_bytes, bytes)
    assert len(pdf_bytes) > 0
    # PDF magic bytes
    assert pdf_bytes.startswith(b"%PDF")


def test_generate_pdf_nonexistent_logo_fallback():
    """Verify generate_pdf does not crash when an invalid logo path is provided."""
    sample_content = "LEASE AGREEMENT\n\nSection 1: Premises address."
    pdf_bytes = generate_pdf(
        sample_content,
        title="LEASE AGREEMENT",
        logo_path="non_existent_path/fake_logo.png",
    )
    assert isinstance(pdf_bytes, bytes)
    assert pdf_bytes.startswith(b"%PDF")


def test_generate_pdf_with_table_and_signatures():
    """Verify generate_pdf handles table rows and signature block lines."""
    sample = (
        "SETTLEMENT AGREEMENT\n\n"
        "| Term | Specification |\n"
        "| Sum | $50,000 USD |\n\n"
        "SECTION 1: RELEASE\n"
        "Parties hereby release claims.\n\n"
        "BY:\n"
        "NAME: Jane Doe\n"
        "TITLE: General Counsel"
    )
    pdf_bytes = generate_pdf(sample, title="SETTLEMENT AGREEMENT")
    assert isinstance(pdf_bytes, bytes)
    assert pdf_bytes.startswith(b"%PDF")
    assert len(pdf_bytes) > 2000

