"""Resume service — business logic layer between the API and the DB/parser."""
from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.models.resume import Resume
from app.utils.file_utils import validate_resume_file, save_upload_file
from app.parser.resume_parser import parse_resume


def upload_and_parse_resume(db: Session, user_id: int, file: UploadFile) -> Resume:
    extension = validate_resume_file(file)
    file_path = save_upload_file(file, extension)

    parsed = parse_resume(file_path, extension)

    resume = Resume(
        user_id=user_id,
        name=parsed["name"],
        email=parsed["email"],
        phone=parsed["phone"],
        education=parsed["education"],
        experience=parsed["experience"],
        projects=parsed["projects"],
        skills=parsed["skills"],
        certifications=parsed["certifications"],
        resume_path=file_path,
        raw_text=parsed["raw_text"],
    )
    db.add(resume)
    db.commit()
    db.refresh(resume)
    return resume


def get_resume(db: Session, resume_id: int) -> Resume | None:
    return db.query(Resume).filter(Resume.id == resume_id).first()


def list_resumes(db: Session, user_id: int | None = None) -> list[Resume]:
    query = db.query(Resume)
    if user_id is not None:
        query = query.filter(Resume.user_id == user_id)
    return query.order_by(Resume.created_at.desc()).all()
