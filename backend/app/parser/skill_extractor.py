"""
Skill extraction — deliberately NOT AI-based, per the project spec.
Matches resume/JD text against the controlled vocabulary in skill_data.py
using case-insensitive word-boundary regex, so "React" doesn't spuriously
match inside "Reaction" etc.
"""
import re

from app.parser.skill_data import SKILL_ALIASES

# Pre-compile one pattern per canonical skill covering all its aliases.
_SKILL_PATTERNS: dict[str, re.Pattern] = {}
for canonical, aliases in SKILL_ALIASES.items():
    variants = [canonical] + aliases
    # Escape each variant, join as alternation, wrap with word boundaries.
    # Variants containing non-word chars (C++, C#) need a boundary that
    # works either side of punctuation, so we use lookaround instead of \b.
    escaped = "|".join(re.escape(v) for v in variants)
    # Wrap in a non-capturing group — without it, alternation has lower
    # precedence than the surrounding lookarounds, so only the first
    # alternative gets the lookbehind and only the last gets the lookahead
    # (e.g. "Go|golang" would let bare "Go" match inside "Google").
    pattern = re.compile(rf"(?<![A-Za-z0-9])(?:{escaped})(?![A-Za-z0-9])", re.IGNORECASE)
    _SKILL_PATTERNS[canonical] = pattern


def extract_skills(text: str) -> list[str]:
    """Returns the list of canonical skill names found anywhere in `text`."""
    found = []
    for canonical, pattern in _SKILL_PATTERNS.items():
        if pattern.search(text):
            found.append(canonical)
    return found
