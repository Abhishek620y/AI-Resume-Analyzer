"""
Import all models here so Base.metadata is aware of every table when
Base.metadata.create_all(engine) is called (see app/core/init_db.py),
and so Alembic autogenerate can discover them later if we add migrations.
"""
from app.models.user import User, UserRole
from app.models.resume import Resume
from app.models.job_description import JobDescription
from app.models.analysis import Analysis
from app.models.score import Score
from app.models.skill import Skill

__all__ = [
    "User",
    "UserRole",
    "Resume",
    "JobDescription",
    "Analysis",
    "Score",
    "Skill",
]
