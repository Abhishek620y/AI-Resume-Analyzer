"""
Analysis model — the result of running a resume through the ATS engine and,
optionally, matching it against a job description + generating AI feedback.

jd_id is nullable because a user can run a pure ATS scan (resume only)
without matching against any specific job description.
"""
from datetime import datetime, timezone

from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, JSON, Text
from sqlalchemy.orm import relationship

from app.core.database import Base


class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.id"), nullable=False)
    jd_id = Column(Integer, ForeignKey("job_descriptions.id"), nullable=True)

    ats_score = Column(Float, nullable=True)        # 0-100, from the ATS engine
    match_score = Column(Float, nullable=True)       # 0-100 percent, from the matcher (only if jd_id set)

    matched_skills = Column(JSON, default=list)
    missing_skills = Column(JSON, default=list)

    feedback = Column(Text, nullable=True)            # AI-generated narrative feedback
    recommendations = Column(JSON, default=list)      # AI-generated bullet-point suggestions

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    resume = relationship("Resume", back_populates="analyses")
    job_description = relationship("JobDescription", back_populates="analyses")
    score_breakdown = relationship("Score", back_populates="analysis", uselist=False, cascade="all, delete-orphan")
