"""Pydantic schemas for Analysis and its Score breakdown."""
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AnalyzeRequest(BaseModel):
    """Body for POST /analyze — jd_id is optional (pure ATS scan vs. full match)."""
    resume_id: int
    jd_id: int | None = None


class ScoreOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    formatting: float
    skills: float
    projects: float
    experience: float
    education: float
    grammar: float
    total: float


class AnalysisOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    resume_id: int
    jd_id: int | None
    ats_score: float | None
    match_score: float | None
    matched_skills: list[str] = []
    missing_skills: list[str] = []
    feedback: str | None
    recommendations: list[str] = []
    created_at: datetime
    score_breakdown: ScoreOut | None = None
