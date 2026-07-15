"""
ATS scoring engine — orchestrates all category scorers and produces the
final explainable breakdown + total, per the spec's rubric:
Formatting 15, Skills 20, Projects 20, Experience 20, Education 10,
Grammar 15 = 100.
"""
from app.ats.formatting_score import score_formatting
from app.ats.skills_score import score_skills
from app.ats.projects_score import score_projects
from app.ats.experience_score import score_experience
from app.ats.education_score import score_education
from app.ats.grammar_score import score_grammar


def calculate_ats_score(
    name: str | None,
    email: str | None,
    phone: str | None,
    education: list[dict],
    experience: list[dict],
    projects: list[dict],
    skills: list[str],
    raw_text: str,
) -> dict:
    """
    Returns:
        {
            "breakdown": {formatting, skills, projects, experience, education, grammar},
            "total": float,
            "notes": [str, ...],  # rule-based, human-readable explanations
        }
    """
    formatting, formatting_notes = score_formatting(name, email, phone, raw_text)
    skills_pts, skills_notes = score_skills(skills)
    projects_pts, projects_notes = score_projects(projects)
    experience_pts, experience_notes = score_experience(experience)
    education_pts, education_notes = score_education(education)
    grammar_pts, grammar_notes = score_grammar(raw_text)

    breakdown = {
        "formatting": formatting,
        "skills": skills_pts,
        "projects": projects_pts,
        "experience": experience_pts,
        "education": education_pts,
        "grammar": grammar_pts,
    }
    total = round(sum(breakdown.values()), 1)

    notes = (
        formatting_notes + skills_notes + projects_notes
        + experience_notes + education_notes + grammar_notes
    )

    return {"breakdown": breakdown, "total": total, "notes": notes}
