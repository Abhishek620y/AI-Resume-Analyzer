"""
Analysis endpoints per the API design in the spec:

POST /api/analyze        — run the ATS engine on a resume (optionally scoped to a JD)
GET  /api/analysis/{id}  — fetch a stored analysis with its score breakdown
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User, UserRole
from app.schemas.analysis import AnalyzeRequest, AnalysisOut
from app.api.deps import get_current_user
from app.services import analysis_service, resume_service

router = APIRouter(tags=["Analysis"])


@router.post("/analyze", response_model=AnalysisOut, status_code=status.HTTP_201_CREATED)
def analyze(
    payload: AnalyzeRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    resume = resume_service.get_resume(db, payload.resume_id)
    if not resume:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found")
    if resume.user_id != current_user.id and current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to analyze this resume")

    try:
        return analysis_service.run_analysis(db, payload.resume_id, payload.jd_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/analysis/{analysis_id}", response_model=AnalysisOut)
def get_analysis(
    analysis_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    analysis = analysis_service.get_analysis(db, analysis_id)
    if not analysis:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Analysis not found")

    resume = resume_service.get_resume(db, analysis.resume_id)
    if resume and resume.user_id != current_user.id and current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view this analysis")

    return analysis
