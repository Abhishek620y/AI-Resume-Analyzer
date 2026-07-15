"""
Contact info extraction: name, email, phone.

Email/phone use regex — reliable and deterministic for these formats.
Name extraction uses a heuristic (first non-empty, non-header line near
the top of the resume) with spaCy's PERSON NER as a cross-check when the
model is available. If spaCy's model isn't installed (e.g. not yet
downloaded via `python -m spacy download en_core_web_sm`), extraction
degrades gracefully to the heuristic alone rather than failing.
"""
import re

EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")

# Matches formats like: +91 98765 43210, (123) 456-7890, 123-456-7890, 9876543210
PHONE_RE = re.compile(
    r"(?:\+?\d{1,3}[-.\s]?)?(?:\(\d{2,4}\)[-.\s]?)?\d{3,5}[-.\s]?\d{3,5}[-.\s]?\d{0,4}"
)

_SECTION_HEADER_WORDS = {
    "education", "experience", "skills", "projects", "certifications",
    "certificates", "summary", "objective", "profile", "contact",
    "work experience", "professional experience", "achievements",
}

_nlp = None


def _get_spacy_model():
    """Lazily load spaCy's English model; return None if unavailable."""
    global _nlp
    if _nlp is not None:
        return _nlp
    try:
        import spacy
        _nlp = spacy.load("en_core_web_sm")
    except Exception:
        _nlp = False  # sentinel: "tried and failed"
    return _nlp or None


def extract_email(text: str) -> str | None:
    match = EMAIL_RE.search(text)
    return match.group(0) if match else None


def extract_phone(text: str) -> str | None:
    for match in PHONE_RE.finditer(text):
        digits = re.sub(r"\D", "", match.group(0))
        # Real phone numbers have 10-13 digits; filters out stray number fragments (years, scores).
        if 10 <= len(digits) <= 13:
            return match.group(0).strip()
    return None


def extract_name(text: str) -> str | None:
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    # Heuristic: name is usually one of the first few lines, short,
    # title-cased, and not a section header or contact line.
    candidate = None
    for line in lines[:6]:
        lower = line.lower()
        if lower in _SECTION_HEADER_WORDS:
            continue
        if EMAIL_RE.search(line) or PHONE_RE.search(line):
            continue
        word_count = len(line.split())
        if 1 <= word_count <= 4 and not any(char.isdigit() for char in line):
            candidate = line
            break

    # Cross-check with spaCy NER if available — prefer a PERSON entity
    # found near the top of the document if it disagrees with the heuristic.
    nlp = _get_spacy_model()
    if nlp:
        top_text = "\n".join(lines[:6])
        doc = nlp(top_text)
        persons = [ent.text.strip() for ent in doc.ents if ent.label_ == "PERSON"]
        if persons:
            return persons[0]

    return candidate
