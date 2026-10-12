"""PDF document generator for LegalEase using FPDF."""

import os
import re
from fpdf import FPDF
from document_generator.sanitizer import sanitize_text


try:
    from fpdf.enums import XPos, YPos
    HAS_FPDF_ENUMS = True
except ImportError:
    HAS_FPDF_ENUMS = False


class LegalDocumentPDF(FPDF):
    """Custom FPDF class with legal headers, footers, and page numbers."""

    def __init__(self, doc_title: str = "LEGAL AGREEMENT", logo_path: str | None = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.doc_title = sanitize_text(doc_title)[:45]
        self.logo_path = logo_path
        self.set_margins(20, 25, 20)
        self.set_auto_page_break(auto=True, margin=20)
        self.alias_nb_pages()

    def header(self):
        """Render running top header."""
        # Embed logo on top left if available
        if self.logo_path and os.path.exists(self.logo_path):
            try:
                self.image(self.logo_path, x=20, y=10, w=40)
            except Exception:
                pass

        self.set_font("Helvetica", "I", 8)
        self.set_text_color(128, 128, 128)
        if HAS_FPDF_ENUMS:
            self.cell(0, 10, self.doc_title, align="R", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        else:
            self.cell(0, 10, self.doc_title, align="R", ln=1)
        self.ln(5)

    def footer(self):
        """Render running bottom footer with page numbers."""
        self.set_y(-18)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(140, 140, 140)
        footer_text = f"LegalEase AI-Generated Document  |  Page {self.page_no()} of {{nb}}"
        self.cell(0, 10, footer_text, align="C")


def generate_pdf(
    content: str,
    title: str = "LEGAL AGREEMENT",
    logo_path: str | None = None,
) -> bytes:
    """Generate a professionally styled PDF document.

    Args:
        content: Raw or generated legal document body text.
        title: Title of the legal document.
        logo_path: Optional path to logo image.

    Returns:
        Bytes containing the binary PDF stream.
    """
    clean_content = sanitize_text(content)

    # Resolve logo safely
    resolved_logo = None
    if logo_path and os.path.exists(logo_path):
        resolved_logo = logo_path
    else:
        default_logo = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "logo.png")
        if os.path.exists(default_logo):
            resolved_logo = default_logo

    pdf = LegalDocumentPDF(doc_title=title, logo_path=resolved_logo, format="A4")
    pdf.add_page()

    lines = [line.strip() for line in clean_content.splitlines() if line.strip()]

    # Extract title from content if present
    start_idx = 0
    main_title = title
    if lines:
        first = lines[0]
        if first.isupper() or "AGREEMENT" in first.upper() or "CONTRACT" in first.upper() or "LETTER" in first.upper():
            main_title = first
            start_idx = 1

    # Render Document Title
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(15, 23, 42)
    pdf.multi_cell(0, 8, main_title, align="C")
    pdf.ln(8)

    # Render document body
    table_buffer = []

    def _flush_pdf_table(tbl):
        if not tbl:
            return
        pdf.ln(2)
        # Header row
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_fill_color(30, 58, 138)
        pdf.set_text_color(255, 255, 255)
        pdf.cell(55, 7, "Provision / Item", border=1, fill=True)
        if HAS_FPDF_ENUMS:
            pdf.cell(115, 7, "Agreed Terms & Specification", border=1, fill=True, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        else:
            pdf.cell(115, 7, "Agreed Terms & Specification", border=1, ln=1, fill=True)

        # Rows
        pdf.set_font("Helvetica", "", 9)
        for idx, (k, v) in enumerate(tbl):
            fill = (idx % 2 == 1)
            pdf.set_fill_color(248, 250, 252) if fill else pdf.set_fill_color(255, 255, 255)
            pdf.set_text_color(30, 41, 59)
            pdf.cell(55, 6.5, sanitize_text(k)[:30], border=1, fill=fill)
            if HAS_FPDF_ENUMS:
                pdf.cell(115, 6.5, sanitize_text(v)[:70], border=1, fill=fill, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            else:
                pdf.cell(115, 6.5, sanitize_text(v)[:70], border=1, ln=1, fill=fill)
        pdf.ln(3)

    for line in lines[start_idx:]:
        # Detect table markdown rows
        if line.startswith("|") and line.endswith("|") and not line.startswith("|---"):
            parts = [p.strip() for p in line.strip("|").split("|")]
            if len(parts) >= 2:
                table_buffer.append((parts[0], parts[1]))
                continue
        elif table_buffer:
            _flush_pdf_table(table_buffer)
            table_buffer = []

        is_heading = bool(
            re.match(r'^(SECTION|ARTICLE|CLAUSE|\d+\.|\([A-Z0-9]+\))\s+', line, re.IGNORECASE)
            or (line.isupper() and len(line) < 60 and not line.startswith("BY:") and not line.startswith("NAME:") and not line.startswith("DATE:"))
        )

        is_signature_line = any(line.startswith(prefix) for prefix in ["BY:", "NAME:", "TITLE:", "DATE:", "SIGNATURE:"])

        if is_heading:
            pdf.ln(4)
            pdf.set_font("Helvetica", "B", 11)
            pdf.set_text_color(15, 23, 42)
            pdf.multi_cell(0, 6, line)
            pdf.ln(2)
        elif is_signature_line:
            pdf.ln(2)
            pdf.set_font("Helvetica", "B", 10)
            pdf.set_text_color(15, 23, 42)
            sig_display = line.ljust(45, "_") if len(line) < 25 else line
            if HAS_FPDF_ENUMS:
                pdf.cell(0, 6, sig_display, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            else:
                pdf.cell(0, 6, sig_display, ln=1)
        elif line.startswith("[DISCLAIMER") or line.startswith("DISCLAIMER:"):
            pdf.ln(6)
            pdf.set_font("Helvetica", "I", 8)
            pdf.set_text_color(100, 116, 139)
            pdf.multi_cell(0, 4, line)
        elif line.startswith("*") or line.startswith("- "):
            pdf.set_font("Helvetica", "", 10)
            pdf.set_text_color(30, 41, 59)
            bullet_line = "   - " + line.lstrip("*- ")
            pdf.multi_cell(0, 5, bullet_line)
            pdf.ln(1)
        else:
            pdf.set_font("Helvetica", "", 10)
            pdf.set_text_color(30, 41, 59)
            pdf.multi_cell(0, 5.5, line)
            pdf.ln(2)

    if table_buffer:
        _flush_pdf_table(table_buffer)

    # Output bytes
    pdf_bytes = pdf.output()
    if isinstance(pdf_bytes, str):
        return pdf_bytes.encode("latin-1", errors="replace")
    elif isinstance(pdf_bytes, bytearray):
        return bytes(pdf_bytes)
    return bytes(pdf_bytes)


