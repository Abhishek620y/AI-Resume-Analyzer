"""
Job Description endpoints per the API design in the spec:

POST /api/upload-jd — create a job description (required_skills auto-extracted if omitted)
GET  /api/jd/{id}    — fetch a single job description
GET  /api/jds        — list job descriptions (own, or all if admin)

Note: the spec's API list only names GET /jd/{id} explicitly, but a list
endpoint is needed for the frontend to let a recruiter pick a JD when
running a match (Module 7) — added here for consistency with the Resume
endpoints (GET /resumes).
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User, UserRole
from app.schemas.job_description import JobDescriptionCreate, JobDescriptionOut
from app.api.deps import get_current_user
from app.services import jd_service

router = APIRouter(tags=["Job Description"])


@router.post("/upload-jd", response_model=JobDescriptionOut, status_code=status.HTTP_201_CREATED)
def upload_jd(
    payload: JobDescriptionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return jd_service.create_job_description(db, current_user.id, payload)


@router.get("/jd/{jd_id}", response_model=JobDescriptionOut)
def get_jd(
    jd_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    jd = jd_service.get_job_description(db, jd_id)
    if not jd:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job description not found")

    if jd.user_id != current_user.id and current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view this job description")

    return jd


@router.get("/jds", response_model=list[JobDescriptionOut])
def list_jds(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user_filter = None if current_user.role == UserRole.ADMIN else current_user.id
    return jd_service.list_job_descriptions(db, user_id=user_filter)
