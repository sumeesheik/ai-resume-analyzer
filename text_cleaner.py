
import re


def clean_text(text: str) -> str:
    """Normalize resume text without deleting important skill symbols."""
    text = text.lower()

    # Standardize common technology names.
    text = re.sub(r"\bscikit[\s-]?learn\b", "scikit-learn", text)
    text = re.sub(r"\bpowerbi\b", "power bi", text)
    text = re.sub(r"\bnode\.js\b", "node.js", text)

    # Keep letters, numbers, whitespace, and useful technical symbols.
    text = re.sub(r"[^a-z0-9+#./\s-]", " ", text)

    # Collapse repeated spaces and line breaks.
    text = re.sub(r"\s+", " ", text).strip()

    return text
