"""Pydantic schemas for JobDescription."""
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class JobDescriptionCreate(BaseModel):
    title: str
    company: str | None = None
    description: str
    required_skills: list[str] = []


class JobDescriptionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    title: str
    company: str | None
    description: str
    required_skills: list[str] = []
    created_at: datetime
