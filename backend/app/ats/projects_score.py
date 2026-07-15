"""
Projects score (max 20).

Rubric — up to 2 projects counted (the first 2 listed), each worth up to
10 points:
  has a title            : 5 pts
  has a description      : 3 pts
  has a detected tech stack : 2 pts

A resume with 0 projects scores 0. A resume with 1 complete project caps
at 10; 2+ complete projects reach the full 20.
"""

MAX_COUNTED_PROJECTS = 2
POINTS_PER_PROJECT = 10


def score_projects(projects: list[dict]) -> tuple[float, list[str]]:
    notes = []

    if not projects:
        notes.append("No projects found — add 1-2 relevant projects with a short description.")
        return 0.0, notes

    score = 0.0
    for project in projects[:MAX_COUNTED_PROJECTS]:
        pts = 0.0
        if project.get("title"):
            pts += 5
        if project.get("description"):
            pts += 3
        else:
            notes.append(f"Project '{project.get('title', 'Untitled')}' has no description.")
        if project.get("tech_stack"):
            pts += 2
        else:
            notes.append(f"Project '{project.get('title', 'Untitled')}' doesn't mention specific technologies used.")
        score += pts

    if len(projects) < MAX_COUNTED_PROJECTS:
        notes.append("Consider adding more projects to strengthen this section.")

    return round(min(score, 20), 1), notes
