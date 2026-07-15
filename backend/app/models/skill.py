"""
Skill model — a master reference list of known skills used by the NLP
extraction engine (app/parser) and the matching engine (app/matcher) to
recognize and normalize skill mentions in resumes/JDs.

This is intentionally NOT a join table to Resume/JobDescription — those
keep their own JSON skill lists (per the agreed simplified design). This
table exists purely as a controlled vocabulary / lookup so extraction is
consistent (e.g. "ReactJS", "React.js", "React" all normalize to "React").
"""
from sqlalchemy import Column, Integer, String

from app.core.database import Base


class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    category = Column(String, nullable=True)  # e.g. "language", "framework", "cloud", "tool"
