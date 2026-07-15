"""
Formatting score (max 15).

Rubric:
- Contact info complete (name + email + phone all present): 6 pts
- Word count in a healthy range for a resume (150-1200 words): 5 pts
  (too short = likely thin content; too long = likely unfocused)
- Uses a reasonable number of distinct lines (structured, not one big
  paragraph blob): 4 pts
"""


def score_formatting(name: str | None, email: str | None, phone: str | None, raw_text: str) -> tuple[float, list[str]]:
    score = 0.0
    notes = []

    contact_fields_present = sum(1 for f in (name, email, phone) if f)
    contact_points = round((contact_fields_present / 3) * 6, 1)
    score += contact_points
    if contact_fields_present < 3:
        missing = [label for label, val in [("name", name), ("email", email), ("phone", phone)] if not val]
        notes.append(f"Missing contact info: {', '.join(missing)}.")

    word_count = len(raw_text.split())
    if 150 <= word_count <= 1200:
        score += 5
    elif word_count < 150:
        score += max(0, round((word_count / 150) * 5, 1))
        notes.append("Resume content seems short — consider adding more detail.")
    else:
        score += 3
        notes.append("Resume is quite long — consider tightening it for readability.")

    line_count = len([l for l in raw_text.splitlines() if l.strip()])
    if line_count >= 15:
        score += 4
    else:
        score += round((line_count / 15) * 4, 1)
        notes.append("Resume structure looks sparse — use clear section breaks and bullet points.")

    return round(min(score, 15), 1), notes
