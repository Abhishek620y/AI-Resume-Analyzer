"""
Resume endpoints per the API design in the spec:

POST /api/upload-resume — upload + parse a PDF/DOCX resume
GET  /api/resume/{id}   — fetch a single parsed resume
GET  /api/resumes       — list resumes (current user's own, or all if admin)
"""
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User, UserRole
from app.schemas.resume import ResumeOut, ResumeListOut
from app.api.deps import get_current_user
from app.services import resume_service

router = APIRouter(tags=["Resume"])


@router.post("/upload-resume", response_model=ResumeOut, status_code=status.HTTP_201_CREATED)
def upload_resume(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return resume_service.upload_and_parse_resume(db, current_user.id, file)


@router.get("/resume/{resume_id}", response_model=ResumeOut)
def get_resume(
    resume_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    resume = resume_service.get_resume(db, resume_id)
    if not resume:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found")

    if resume.user_id != current_user.id and current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view this resume")

    return resume


@router.get("/resumes", response_model=list[ResumeListOut])
def list_resumes(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Admins see everyone's resumes (needed for the dashboard); recruiters see only their own uploads.
    user_filter = None if current_user.role == UserRole.ADMIN else current_user.id
    return resume_service.list_resumes(db, user_id=user_filter)
