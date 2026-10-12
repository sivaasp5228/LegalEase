"""Styled HTML preview generator for legal documents in Streamlit."""

import html
import re
from document_generator.sanitizer import sanitize_text


def generate_html_preview(content: str) -> str:
    """Generate a clean, styled HTML parchment container for displaying legal text.

    Args:
        content: Plain legal text to render.

    Returns:
        HTML string with scoped inline CSS styles for high-fidelity legal document preview.
    """
    clean_text = sanitize_text(content)
    lines = clean_text.splitlines()

    body_html_parts = []
    table_buffer = []

    def _flush_html_table(tbl):
        if not tbl:
            return ""
        rows = []
        # Header
        hdr0, hdr1 = tbl[0]
        rows.append(f'<tr><th style="background:#1E3A8A; color:white; padding:8px 12px; border:1px solid #CBD5E1; text-align:left;">{html.escape(hdr0)}</th><th style="background:#1E3A8A; color:white; padding:8px 12px; border:1px solid #CBD5E1; text-align:left;">{html.escape(hdr1)}</th></tr>')
        for k, v in tbl[1:]:
            rows.append(f'<tr><td style="padding:6px 12px; border:1px solid #E2E8F0; background:#F8FAFC; font-weight:600;">{html.escape(k)}</td><td style="padding:6px 12px; border:1px solid #E2E8F0;">{html.escape(v)}</td></tr>')
        rows_str = "\n".join(rows)
        return f'<table style="width:100%; border-collapse:collapse; margin:14px 0; font-size:0.9rem;">\n{rows_str}\n</table>'

    i = 0
    while i < len(lines):
        line = lines[i]
        line_stripped = line.strip()

        if not line_stripped:
            if table_buffer:
                body_html_parts.append(_flush_html_table(table_buffer))
                table_buffer = []
            body_html_parts.append('<div class="legal-spacer"></div>')
            i += 1
            continue

        # Check for pipe table
        if line_stripped.startswith("|") and line_stripped.endswith("|") and not line_stripped.startswith("|---"):
            parts = [p.strip() for p in line_stripped.strip("|").split("|")]
            if len(parts) >= 2:
                table_buffer.append((parts[0], parts[1]))
                i += 1
                continue
        elif table_buffer:
            body_html_parts.append(_flush_html_table(table_buffer))
            table_buffer = []

        escaped = html.escape(line_stripped)

        # Detect Title / Main Heading
        if (
            escaped.isupper()
            and (
                "AGREEMENT" in escaped
                or "CONTRACT" in escaped
                or "LETTER" in escaped
                or "NDA" in escaped
            )
            and len(escaped) < 80
        ):
            body_html_parts.append(f'<h1 class="legal-doc-title">{escaped}</h1>')
            i += 1
            continue

        # Detect Section Headings
        is_heading = bool(
            re.match(r'^(SECTION|ARTICLE|CLAUSE|\d+\.|\([A-Z0-9]+\))\s+', line_stripped, re.IGNORECASE)
            or (line_stripped.isupper() and len(line_stripped) < 60 and not line_stripped.startswith("BY:") and not line_stripped.startswith("NAME:") and not line_stripped.startswith("DATE:"))
        )

        if is_heading:
            body_html_parts.append(f'<h2 class="legal-section-heading">{escaped}</h2>')
        elif line_stripped.startswith("[DISCLAIMER") or line_stripped.startswith("DISCLAIMER:"):
            body_html_parts.append(f'<div class="legal-disclaimer-box">{escaped}</div>')
        elif line_stripped.startswith("*") or line_stripped.startswith("- "):
            bullet_text = escaped.lstrip("*- ")
            body_html_parts.append(f'<li class="legal-bullet">{bullet_text}</li>')
        elif line_stripped.startswith("BY:") or line_stripped.startswith("NAME:") or line_stripped.startswith("DATE:") or line_stripped.startswith("TITLE:"):
            body_html_parts.append(f'<div class="legal-signature-line">{escaped}</div>')
        else:
            body_html_parts.append(f'<p class="legal-paragraph">{escaped}</p>')

        i += 1

    if table_buffer:
        body_html_parts.append(_flush_html_table(table_buffer))

    body_html = "\n".join(body_html_parts)

    html_container = f"""
    <div class="legal-parchment">
        <div class="legal-ribbon">CONFIDENTIAL &amp; BINDING</div>
        <div class="legal-body">
            {body_html}
        </div>
    </div>
    """
    return html_container

