"""
Splits raw resume text into sections (education, experience, projects,
skills, certifications) by detecting common header lines. This is a
heuristic approach — resumes have no standard format — but covers the
vast majority of conventional resume layouts.
"""
import re

# Maps a section key to the header phrases that mark its start.
SECTION_HEADERS: dict[str, list[str]] = {
    "education": ["education", "academic background", "academic qualifications"],
    "experience": ["experience", "work experience", "professional experience", "employment history"],
    "projects": ["projects", "personal projects", "academic projects"],
    "skills": ["skills", "technical skills", "core competencies"],
    "certifications": ["certifications", "certificates", "licenses & certifications"],
}

_ALL_HEADER_PHRASES = [
    (key, phrase) for key, phrases in SECTION_HEADERS.items() for phrase in phrases
]
# Longest phrases first, so "technical skills" matches before generic "skills".
_ALL_HEADER_PHRASES.sort(key=lambda kp: len(kp[1]), reverse=True)


def _match_header(line: str) -> str | None:
    """Returns the section key if `line` looks like a section header, else None."""
    stripped = line.strip().strip(":").lower()
    if len(stripped) > 40:  # header lines are short; long lines are body text
        return None
    for key, phrase in _ALL_HEADER_PHRASES:
        if stripped == phrase or re.fullmatch(re.escape(phrase), stripped):
            return key
    return None


def split_into_sections(text: str) -> dict[str, str]:
    """
    Returns {section_key: section_body_text}. Text before the first
    recognized header is not included (treated as header/contact block).
    """
    lines = text.splitlines()
    sections: dict[str, list[str]] = {key: [] for key in SECTION_HEADERS}

    current_section = None
    for line in lines:
        header_key = _match_header(line)
        if header_key:
            current_section = header_key
            continue
        if current_section:
            sections[current_section].append(line)

    return {key: "\n".join(body).strip() for key, body in sections.items()}
