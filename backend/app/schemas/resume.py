"""Pydantic schemas for Resume — used by upload/parsing endpoints."""
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class EducationEntry(BaseModel):
    degree: str | None = None
    institution: str | None = None
    year: str | None = None


class ExperienceEntry(BaseModel):
    title: str | None = None
    company: str | None = None
    duration: str | None = None
    description: str | None = None


class ProjectEntry(BaseModel):
    title: str | None = None
    description: str | None = None
    tech_stack: list[str] = []


class ResumeCreate(BaseModel):
    """Used internally after parsing — not a direct request body (upload uses multipart file)."""
    name: str | None = None
    email: str | None = None
    phone: str | None = None
    education: list[EducationEntry] = []
    experience: list[ExperienceEntry] = []
    projects: list[ProjectEntry] = []
    skills: list[str] = []
    certifications: list[str] = []
    resume_path: str
    raw_text: str | None = None


class ResumeOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    name: str | None
    email: str | None
    phone: str | None
    education: list[dict] = []
    experience: list[dict] = []
    projects: list[dict] = []
    skills: list[str] = []
    certifications: list[str] = []
    resume_path: str
    created_at: datetime


class ResumeListOut(BaseModel):
    """Lighter-weight version for list views (dashboard, history)."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str | None
    email: str | None
    skills: list[str] = []
    created_at: datetime
