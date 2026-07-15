"""
Keyword matcher — implements the Resume Matching Algorithm exactly as
specified in the doc's example:

    Resume Skills: Python, React, Node, SQL, Git
    JD Skills:     Python, Docker, SQL, AWS, Git
    Matched:       Python, SQL, Git  (3)
    Required:      5
    Match %:       60%

i.e. match_percentage = (matched skills) / (required skills count) * 100,
not divided by the resume's skill count — a resume that has extra
irrelevant skills shouldn't be penalized, and one that's missing
required skills should be.
"""


def match_skills(resume_skills: list[str], required_skills: list[str]) -> dict:
    resume_set = {s.lower() for s in resume_skills}
    required_set = {s.lower() for s in required_skills}

    # Preserve original casing from required_skills for display.
    lookup = {s.lower(): s for s in required_skills}

    matched = [lookup[s] for s in required_set & resume_set]
    missing = [lookup[s] for s in required_set - resume_set]

    if not required_set:
        # No required skills listed on the JD — nothing to measure against.
        match_percentage = 0.0
    else:
        match_percentage = round((len(matched) / len(required_set)) * 100, 1)

    return {
        "matched_skills": sorted(matched),
        "missing_skills": sorted(missing),
        "match_percentage": match_percentage,
    }
