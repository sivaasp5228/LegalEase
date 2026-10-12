"""Microsoft Word (.docx) document generator for LegalEase."""

import io
import os
import re
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

from document_generator.sanitizer import sanitize_text


def _set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Set inner margins for a table cell in twips."""
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)


def _set_cell_borders(cell, color="CCCCCC", sz="4", val="single"):
    """Set custom light borders for a table cell."""
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcBorders = OxmlElement('w:tcBorders')
    for b in ['top', 'left', 'bottom', 'right']:
        node = OxmlElement(f'w:{b}')
        node.set(qn('w:val'), val)
        node.set(qn('w:sz'), sz)
        node.set(qn('w:space'), '0')
        node.set(qn('w:color'), color)
        tcBorders.append(node)
    tcPr.append(tcBorders)


def _set_cell_shading(cell, color_hex="F1F5F9"):
    """Set background fill color for a table cell."""
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), color_hex)
    tcPr.append(shd)


def _render_terms_table(doc, table_data: list[tuple[str, str]]):
    """Render a formal two-column key-value terms table."""
    if not table_data:
        return
    table = doc.add_table(rows=len(table_data) + 1, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False

    # Header Row
    hdr_cells = table.rows[0].cells
    hdr_cells[0].width = Inches(2.2)
    hdr_cells[1].width = Inches(4.3)
    hdr_cells[0].paragraphs[0].text = "Provision / Item"
    hdr_cells[1].paragraphs[0].text = "Agreed Terms & Specification"

    for c in hdr_cells:
        _set_cell_shading(c, "1E3A8A")
        _set_cell_margins(c, top=120, bottom=120, left=140, right=140)
        p = c.paragraphs[0]
        p.runs[0].font.name = "Times New Roman"
        p.runs[0].font.size = Pt(10)
        p.runs[0].font.bold = True
        p.runs[0].font.color.rgb = RGBColor(255, 255, 255)

    # Data Rows
    for idx, (k, v) in enumerate(table_data, start=1):
        row_cells = table.rows[idx].cells
        row_cells[0].width = Inches(2.2)
        row_cells[1].width = Inches(4.3)
        row_cells[0].paragraphs[0].text = k
        row_cells[1].paragraphs[0].text = v

        bg = "F8FAFC" if idx % 2 == 0 else "FFFFFF"
        for c in row_cells:
            _set_cell_shading(c, bg)
            _set_cell_borders(c, color="E2E8F0")
            _set_cell_margins(c, top=100, bottom=100, left=140, right=140)
            p = c.paragraphs[0]
            if p.runs:
                p.runs[0].font.name = "Times New Roman"
                p.runs[0].font.size = Pt(9.5)

    # Add spacing after table
    sp = doc.add_paragraph()
    sp.paragraph_format.space_after = Pt(10)


def generate_docx(
    content: str,
    title: str = "LEGAL AGREEMENT",
    logo_path: str | None = None,
) -> bytes:
    """Generate a professionally styled Microsoft Word document (.docx).

    Args:
        content: Raw or generated legal document body text.
        title: Document title to place in header/first page.
        logo_path: Path to optional logo image file.

    Returns:
        Bytes representing the binary .docx file.
    """
    clean_content = sanitize_text(content)
    doc = Document()

    # Configure 1-inch margins
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

        # Configure Running Footer
        footer = section.footer
        f_p = footer.paragraphs[0]
        f_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        f_run = f_p.add_run("LegalEase AI Document Generator  |  Confidential  |  Consult qualified counsel")
        f_run.font.name = "Times New Roman"
        f_run.font.size = Pt(8.5)
        f_run.font.color.rgb = RGBColor(128, 128, 128)

    # Base style configurations
    normal_style = doc.styles["Normal"]
    normal_style.font.name = "Times New Roman"
    normal_style.font.size = Pt(11)
    normal_style.font.color.rgb = RGBColor(30, 41, 59)

    # Optional Logo insertion
    resolved_logo = None
    if logo_path and os.path.exists(logo_path):
        resolved_logo = logo_path
    else:
        default_logo = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "logo.png")
        if os.path.exists(default_logo):
            resolved_logo = default_logo

    if resolved_logo:
        try:
            logo_p = doc.add_paragraph()
            logo_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            logo_p.paragraph_format.space_after = Pt(12)
            logo_p.add_run().add_picture(resolved_logo, width=Inches(2.4))
        except Exception:
            pass  # Fall back gracefully if image cannot be read

    # Parse and structure document paragraphs
    lines = clean_content.splitlines()

    # Determine title from content if first non-empty line looks like a title
    body_lines = [line.strip() for line in lines if line.strip()]
    first_title = title
    start_idx = 0
    if body_lines:
        first_candidate = body_lines[0]
        if first_candidate.isupper() or "AGREEMENT" in first_candidate.upper() or "CONTRACT" in first_candidate.upper() or "LETTER" in first_candidate.upper():
            first_title = first_candidate
            start_idx = 1

    # Add Title
    title_p = doc.add_paragraph()
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title_p.paragraph_format.space_before = Pt(6)
    title_p.paragraph_format.space_after = Pt(18)
    title_run = title_p.add_run(first_title)
    title_run.font.name = "Times New Roman"
    title_run.font.size = Pt(18)
    title_run.bold = True
    title_run.font.color.rgb = RGBColor(15, 23, 42)

    # Process remaining lines
    current_lines = body_lines[start_idx:]
    i = 0
    table_buffer = []

    while i < len(current_lines):
        line = current_lines[i]

        # Check for markdown or key-value table lines: e.g. "| key | val |" or "Term: Value" inside a terms block
        if line.startswith("|") and line.endswith("|") and not line.startswith("|---"):
            parts = [p.strip() for p in line.strip("|").split("|")]
            if len(parts) >= 2:
                table_buffer.append((parts[0], parts[1]))
                i += 1
                continue
        elif table_buffer:
            _render_terms_table(doc, table_buffer)
            table_buffer = []

        # Detect Section Headings (e.g. "SECTION 1:", "ARTICLE I", uppercase headings)
        is_heading = bool(
            re.match(r'^(SECTION|ARTICLE|CLAUSE|\d+\.|\([A-Z0-9]+\))\s+', line, re.IGNORECASE)
            or (line.isupper() and len(line) < 60 and not line.startswith("BY:") and not line.startswith("NAME:") and not line.startswith("DATE:"))
        )

        # Detect Signature block triggers
        is_signature_line = any(line.startswith(prefix) for prefix in ["BY:", "NAME:", "TITLE:", "DATE:", "SIGNATURE:"])

        if is_heading:
            h_p = doc.add_paragraph()
            h_p.paragraph_format.space_before = Pt(14)
            h_p.paragraph_format.space_after = Pt(4)
            h_p.paragraph_format.keep_with_next = True
            h_run = h_p.add_run(line)
            h_run.font.name = "Times New Roman"
            h_run.font.size = Pt(12)
            h_run.bold = True
            h_run.font.color.rgb = RGBColor(15, 23, 42)
        elif is_signature_line:
            sig_p = doc.add_paragraph()
            sig_p.paragraph_format.space_before = Pt(4)
            sig_p.paragraph_format.space_after = Pt(4)
            sig_run = sig_p.add_run(line.ljust(50, "_") if len(line) < 30 else line)
            sig_run.font.name = "Times New Roman"
            sig_run.font.size = Pt(10.5)
            sig_run.bold = True
        elif line.startswith("[DISCLAIMER") or line.startswith("DISCLAIMER:"):
            d_p = doc.add_paragraph()
            d_p.paragraph_format.space_before = Pt(20)
            d_p.paragraph_format.space_after = Pt(6)
            d_run = d_p.add_run(line)
            d_run.font.name = "Times New Roman"
            d_run.font.size = Pt(9)
            d_run.italic = True
            d_run.font.color.rgb = RGBColor(100, 116, 139)
        elif line.startswith("*") or line.startswith("- "):
            p = doc.add_paragraph(style='List Bullet')
            p.paragraph_format.space_after = Pt(4)
            run = p.add_run(line.lstrip("*- "))
            run.font.name = "Times New Roman"
            run.font.size = Pt(11)
        else:
            p = doc.add_paragraph()
            p.paragraph_format.space_after = Pt(6)
            p.paragraph_format.line_spacing = 1.15
            run = p.add_run(line)
            run.font.name = "Times New Roman"
            run.font.size = Pt(11)

        i += 1

    if table_buffer:
        _render_terms_table(doc, table_buffer)

    # Save to in-memory bytes buffer
    docx_io = io.BytesIO()
    doc.save(docx_io)
    docx_io.seek(0)
    return docx_io.getvalue()

