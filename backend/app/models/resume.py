"""
Resume model.

Multi-value fields (education, experience, projects, skills, certifications)
are stored as JSON per the agreed simplified approach — fast to build now,
can be normalized into separate tables later without touching the API layer
if needed, since Pydantic schemas would absorb that change.
"""
from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship

from app.core.database import Base


class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    name = Column(String, nullable=True)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)

    education = Column(JSON, default=list)       # list of {degree, institution, year, ...}
    experience = Column(JSON, default=list)       # list of {title, company, duration, description}
    projects = Column(JSON, default=list)         # list of {title, description, tech_stack}
    skills = Column(JSON, default=list)            # list of strings
    certifications = Column(JSON, default=list)    # list of strings

    resume_path = Column(String, nullable=False)   # path to stored file in /uploads
    raw_text = Column(String, nullable=True)        # extracted raw text, useful for re-parsing/matching

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    owner = relationship("User", back_populates="resumes")
    analyses = relationship("Analysis", back_populates="resume", cascade="all, delete-orphan")
