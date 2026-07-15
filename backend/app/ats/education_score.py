"""
Education score (max 10).

Rubric — based on the first (most relevant) education entry:
  has at least 1 entry        : 5 pts
  entry has a degree field    : 3 pts
  entry has a year            : 2 pts
"""


def score_education(education: list[dict]) -> tuple[float, list[str]]:
    notes = []

    if not education:
        notes.append("No education details found.")
        return 0.0, notes

    score = 5.0
    entry = education[0]

    if entry.get("degree"):
        score += 3
    else:
        notes.append("Education entry is missing a clear degree/qualification.")

    if entry.get("year"):
        score += 2
    else:
        notes.append("Education entry is missing a graduation year.")

    return round(min(score, 10), 1), notes
