"""
Experience score (max 20).

Rubric — up to 2 experience entries counted, each worth up to 10 points:
  has a title       : 3 pts
  has a company     : 3 pts
  has a duration    : 2 pts
  has a description : 2 pts

Resumes with no work experience (common for students/freshers) score 0
here but that's expected to be offset by a stronger Projects section —
this is why Projects and Experience are weighted equally at 20 each.
"""

MAX_COUNTED_EXPERIENCE = 2
POINTS_PER_EXPERIENCE = 10


def score_experience(experience: list[dict]) -> tuple[float, list[str]]:
    notes = []

    if not experience:
        notes.append("No work experience found — if you're a student, strong projects can help offset this.")
        return 0.0, notes

    score = 0.0
    for entry in experience[:MAX_COUNTED_EXPERIENCE]:
        pts = 0.0
        if entry.get("title"):
            pts += 3
        if entry.get("company"):
            pts += 3
        if entry.get("duration"):
            pts += 2
        else:
            notes.append(f"Experience entry '{entry.get('title', 'Untitled')}' is missing a clear duration.")
        if entry.get("description"):
            pts += 2
        else:
            notes.append(f"Experience entry '{entry.get('title', 'Untitled')}' has no description of responsibilities.")
        score += pts

    return round(min(score, 20), 1), notes
