"""
Constants used by the rule-based ATS scoring engine — action verbs for
the grammar/keyword check, and the max points per category (must sum
to 100, matching the spec's breakdown).
"""

MAX_SCORES = {
    "formatting": 15,
    "skills": 20,
    "projects": 20,
    "experience": 20,
    "education": 10,
    "grammar": 15,
}
assert sum(MAX_SCORES.values()) == 100

# Strong action verbs recruiters/ATS systems look for at the start of bullet points.
ACTION_VERBS = {
    "achieved", "built", "created", "delivered", "designed", "developed",
    "drove", "engineered", "established", "executed", "founded", "improved",
    "increased", "initiated", "implemented", "launched", "led", "managed",
    "optimized", "orchestrated", "pioneered", "produced", "reduced",
    "redesigned", "resolved", "spearheaded", "streamlined", "transformed",
}
