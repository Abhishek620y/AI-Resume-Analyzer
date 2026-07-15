"""
Skills score (max 20).

Rubric — scaled by number of distinct recognized skills:
  0 skills    -> 0
  1-2 skills  -> 8
  3-5 skills  -> 14
  6-9 skills  -> 18
  10+ skills  -> 20

Thresholds rather than pure linear scaling because a resume that lists
zero recognized skills is far worse than the gap between, say, 9 and 10.
"""


def score_skills(skills: list[str]) -> tuple[float, list[str]]:
    count = len(skills)
    notes = []

    if count == 0:
        score = 0.0
        notes.append("No recognized skills found — add a dedicated Skills section.")
    elif count <= 2:
        score = 8.0
        notes.append("Few skills detected — consider listing more relevant technical skills.")
    elif count <= 5:
        score = 14.0
    elif count <= 9:
        score = 18.0
    else:
        score = 20.0

    return score, notes
