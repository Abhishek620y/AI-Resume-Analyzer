"""
Grammar & keywords score (max 15) — not a spellchecker, but three
rule-based, explainable signals commonly used by real ATS tools:

- Action verbs: % of bullet-style lines that start with a strong action
  verb (built, led, improved, etc.): up to 8 pts
- Quantifiable achievements: presence of numbers/percentages, a strong
  signal of measurable impact ("increased X by 30%"): up to 4 pts
- Readability: average line length isn't excessive (very long lines
  hurt ATS parsing and human readability): up to 3 pts
"""
import re

from app.ats.rules import ACTION_VERBS

PERCENT_OR_NUMBER_RE = re.compile(r"\d+%|\b\d{2,}\b")


def score_grammar(raw_text: str) -> tuple[float, list[str]]:
    notes = []
    lines = [l.strip() for l in raw_text.splitlines() if l.strip()]

    if not lines:
        return 0.0, ["No content available to evaluate."]

    # --- Action verbs (8 pts) ---
    bullet_like_lines = [l for l in lines if len(l.split()) >= 3]
    if bullet_like_lines:
        action_verb_lines = sum(
            1 for l in bullet_like_lines
            if l.split()[0].strip(".,-•").lower() in ACTION_VERBS
        )
        ratio = action_verb_lines / len(bullet_like_lines)
        action_score = round(ratio * 8, 1)
        if ratio < 0.2:
            notes.append("Few bullet points start with strong action verbs (e.g. 'Built', 'Led', 'Improved').")
    else:
        action_score = 0.0

    # --- Quantifiable achievements (4 pts) ---
    quantifiable_lines = sum(1 for l in lines if PERCENT_OR_NUMBER_RE.search(l))
    if quantifiable_lines >= 3:
        quant_score = 4.0
    elif quantifiable_lines > 0:
        quant_score = 2.0
        notes.append("Add more quantifiable achievements (e.g. 'reduced load time by 40%').")
    else:
        quant_score = 0.0
        notes.append("No quantifiable achievements found — numbers make impact concrete.")

    # --- Readability (3 pts) ---
    avg_line_length = sum(len(l) for l in lines) / len(lines)
    if avg_line_length <= 120:
        readability_score = 3.0
    else:
        readability_score = 1.5
        notes.append("Some lines are very long — shorter, punchy bullet points read better.")

    total = round(action_score + quant_score + readability_score, 1)
    return min(total, 15), notes
