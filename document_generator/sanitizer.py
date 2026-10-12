"""Text sanitizer for cleaning typographic quotes, dashes, and unsupported unicode characters."""

import unicodedata

# Mapping of problematic typographic Unicode characters to safe ASCII equivalents
REPLACEMENT_MAP = {
    # Curly double quotes
    "\u201c": '"',
    "\u201d": '"',
    "\u201e": '"',
    "\u201f": '"',
    "\u00ab": '"',
    "\u00bb": '"',
    # Curly single quotes & apostrophes
    "\u2018": "'",
    "\u2019": "'",
    "\u201a": "'",
    "\u201b": "'",
    "\u0060": "'",
    "\u00b4": "'",
    # Dashes & hyphens
    "\u2013": "-",    # En-dash
    "\u2014": "--",   # Em-dash
    "\u2015": "--",   # Horizontal bar
    "\u2212": "-",    # Minus sign
    # Spaces & line breaks
    "\u00a0": " ",    # Non-breaking space
    "\u200b": "",     # Zero-width space
    "\u2002": " ",    # En-space
    "\u2003": " ",    # Em-space
    "\u2009": " ",    # Thin space
    # Symbols & bullets
    "\u2022": "*",    # Bullet
    "\u2023": "*",    # Triangular bullet
    "\u25cf": "*",    # Black circle
    "\u2026": "...",  # Ellipsis
    "\u00a9": "(c)",  # Copyright
    "\u00ae": "(R)",  # Registered
    "\u2122": "(TM)", # Trademark
    "\u00a7": "Section ", # Section sign
}


def sanitize_text(text: str) -> str:
    """Sanitize input text by replacing problematic typographical characters.

    Args:
        text: Raw text potentially containing smart quotes, em-dashes, or special symbols.

    Returns:
        Sanitized text safe for plain text, DOCX, and FPDF rendering.
    """
    if not text:
        return ""

    # Replace mapped characters
    result = text
    for char, replacement in REPLACEMENT_MAP.items():
        result = result.replace(char, replacement)

    # Filter control characters and ensure character can be encoded in Latin-1/CP1252
    clean_chars = []
    for c in result:
        category = unicodedata.category(c)
        if category.startswith("C"):
            if c in ("\n", "\r", "\t"):
                clean_chars.append(c)
            # Skip unprintable control characters
            continue

        # Valid Latin-1 character
        if ord(c) < 256:
            clean_chars.append(c)
        else:
            # Handle out-of-range Unicode (emojis, complex symbols, etc.)
            decomp = unicodedata.normalize("NFKD", c)
            ascii_chars = [ch for ch in decomp if ord(ch) < 128 and not unicodedata.category(ch).startswith("M")]
            if ascii_chars:
                clean_chars.extend(ascii_chars)
            # Unconvertible symbols/emojis are omitted so PDF/Word never crash

    return "".join(clean_chars)
