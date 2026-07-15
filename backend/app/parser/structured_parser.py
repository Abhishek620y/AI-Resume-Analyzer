"""
Heuristic structured parsing for education, experience, and project
entries, given the raw text of each section (from section_extractor).

Resumes vary too much for a fully general parser, so this uses pragmatic
heuristics: entries are separated by blank lines (or, if there are none,
one entry per line), and a 4-digit year is extracted where present. The
rest of the entry text is kept so no information is lost even when the
degree/company/title can't be confidently isolated.
"""
import re

YEAR_RE = re.compile(r"\b(19|20)\d{2}\b")


def _split_entries(section_text: str) -> list[str]:
    """
    Splits a section's text into individual entries (e.g. one per job,
    one per degree). Blank lines are the primary separator between
    entries. If there are no blank lines at all, the whole section is
    treated as a single entry rather than guessing per-line boundaries —
    this avoids incorrectly fragmenting a single multi-line entry (title
    + description) into unrelated pieces. Resumes that list several
    entries as bare single lines with no blank-line separation are a
    known limitation of this heuristic parser.
    """
    if not section_text.strip():
        return []

    blocks = [b.strip() for b in re.split(r"\n\s*\n", section_text) if b.strip()]
    return blocks


def parse_education(section_text: str) -> list[dict]:
    entries = []
    for block in _split_entries(section_text):
        year_match = YEAR_RE.search(block)
        year = year_match.group(0) if year_match else None
        # First line/segment before a comma or dash is usually the degree.
        first_segment = re.split(r"[,\u2013\u2014-]", block, maxsplit=1)[0].strip()
        remainder = block[len(first_segment):].strip(" ,-\u2013\u2014")
        entries.append({
            "degree": first_segment or None,
            "institution": remainder or None,
            "year": year,
        })
    return entries


def parse_experience(section_text: str) -> list[dict]:
    entries = []
    for block in _split_entries(section_text):
        lines = [l.strip() for l in block.splitlines() if l.strip()]
        header = lines[0] if lines else block
        description = "\n".join(lines[1:]) if len(lines) > 1 else None

        # Header often looks like "Title - Company (Duration)" or "Title, Company".
        title, company = None, None
        parts = re.split(r"[\u2013\u2014-]|,", header, maxsplit=1)
        if parts:
            title = parts[0].strip() or None
            if len(parts) > 1:
                company = parts[1].strip() or None

        duration_match = re.search(
            r"(\b\w+\s\d{4}\b.*?(?:present|current|\b\w+\s\d{4}\b))", header, re.IGNORECASE
        )
        duration = duration_match.group(0) if duration_match else None

        entries.append({
            "title": title,
            "company": company,
            "duration": duration,
            "description": description,
        })
    return entries


def parse_projects(section_text: str, known_skills: list[str] | None = None) -> list[dict]:
    from app.parser.skill_extractor import extract_skills

    entries = []
    for block in _split_entries(section_text):
        lines = [l.strip() for l in block.splitlines() if l.strip()]
        title = lines[0] if lines else block
        description = "\n".join(lines[1:]) if len(lines) > 1 else None
        tech_stack = extract_skills(block)
        entries.append({
            "title": title or None,
            "description": description,
            "tech_stack": tech_stack,
        })
    return entries


def parse_certifications(section_text: str) -> list[str]:
    return [line.strip() for line in section_text.splitlines() if line.strip()]
