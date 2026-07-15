"""
Job Description service.

If the recruiter doesn't supply an explicit required_skills list, we
auto-extract them from the description text using the same non-AI
skill extractor used for resumes (app.parser.skill_extractor) — this
keeps resume skills and JD skills on the same controlled vocabulary,
which matters a lot once the Matching Engine compares the two sets.
"""
from sqlalchemy.orm import Session

from app.models.job_description import JobDescription
from app.schemas.job_description import JobDescriptionCreate
from app.parser.skill_extractor import extract_skills


def create_job_description(db: Session, user_id: int, payload: JobDescriptionCreate) -> JobDescription:
    required_skills = payload.required_skills or extract_skills(payload.description)

    jd = JobDescription(
        user_id=user_id,
        title=payload.title,
        company=payload.company,
        description=payload.description,
        required_skills=required_skills,
    )
    db.add(jd)
    db.commit()
    db.refresh(jd)
    return jd


def get_job_description(db: Session, jd_id: int) -> JobDescription | None:
    return db.query(JobDescription).filter(JobDescription.id == jd_id).first()


def list_job_descriptions(db: Session, user_id: int | None = None) -> list[JobDescription]:
    query = db.query(JobDescription)
    if user_id is not None:
        query = query.filter(JobDescription.user_id == user_id)
    return query.order_by(JobDescription.created_at.desc()).all()
