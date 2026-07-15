"""
Analysis service — runs a resume through the ATS engine, the Matching
Engine (if a JD is specified), and the AI Suggestion service. Persists
the full result.
"""
from sqlalchemy.orm import Session

from app.models.resume import Resume
from app.models.job_description import JobDescription
from app.models.analysis import Analysis
from app.models.score import Score
from app.ats.engine import calculate_ats_score
from app.matcher.engine import run_match
from app.ai.base import SuggestionContext
from app.ai.suggestion_service import generate_suggestions


def run_analysis(db: Session, resume_id: int, jd_id: int | None = None) -> Analysis:
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if not resume:
        raise ValueError("Resume not found")

    jd = None
    if jd_id is not None:
        jd = db.query(JobDescription).filter(JobDescription.id == jd_id).first()
        if not jd:
            raise ValueError("Job description not found")

    result = calculate_ats_score(
        name=resume.name,
        email=resume.email,
        phone=resume.phone,
        education=resume.education or [],
        experience=resume.experience or [],
        projects=resume.projects or [],
        skills=resume.skills or [],
        raw_text=resume.raw_text or "",
    )

    match_score = None
    matched_skills: list[str] = []
    missing_skills: list[str] = []
    recommendations = list(result["notes"])  # rule-based ATS notes, always available

    if jd is not None:
        match_result = run_match(
            resume_skills=resume.skills or [],
            resume_text=resume.raw_text or "",
            required_skills=jd.required_skills or [],
            jd_text=jd.description or "",
        )
        match_score = match_result["match_score"]
        matched_skills = match_result["matched_skills"]
        missing_skills = match_result["missing_skills"]
        if missing_skills:
            recommendations.append(
                f"Missing skills for '{jd.title}': {', '.join(missing_skills)}."
            )

    # AI Suggestions (mock fallback if no provider configured / call fails).
    suggestion_context = SuggestionContext(
        resume_name=resume.name,
        resume_text=resume.raw_text or "",
        skills=resume.skills or [],
        ats_score=result["total"],
        ats_notes=result["notes"],
        jd_title=jd.title if jd else None,
        jd_description=jd.description if jd else None,
        missing_skills=missing_skills,
        match_score=match_score,
    )
    ai_result = generate_suggestions(suggestion_context)
    feedback = ai_result["feedback"]
    recommendations.extend(ai_result["recommendations"])

    analysis = Analysis(
        resume_id=resume.id,
        jd_id=jd_id,
        ats_score=result["total"],
        match_score=match_score,
        matched_skills=matched_skills,
        missing_skills=missing_skills,
        feedback=feedback,
        recommendations=recommendations,
    )
    db.add(analysis)
    db.flush()  # get analysis.id before creating the Score row

    score = Score(
        analysis_id=analysis.id,
        formatting=result["breakdown"]["formatting"],
        skills=result["breakdown"]["skills"],
        projects=result["breakdown"]["projects"],
        experience=result["breakdown"]["experience"],
        education=result["breakdown"]["education"],
        grammar=result["breakdown"]["grammar"],
        total=result["total"],
    )
    db.add(score)
    db.commit()
    db.refresh(analysis)
    return analysis


def get_analysis(db: Session, analysis_id: int) -> Analysis | None:
    return db.query(Analysis).filter(Analysis.id == analysis_id).first()
