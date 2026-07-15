"""
Score model — the per-category ATS breakdown for a single Analysis.

Kept as its own table (rather than JSON on Analysis) because the doc calls
out that this breakdown is the whole point of making the score explainable
during a viva — first-class columns make it trivial to query/aggregate for
the dashboard (e.g. "average Skills score across all resumes").
"""
from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


class Score(Base):
    __tablename__ = "scores"

    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(Integer, ForeignKey("analyses.id"), nullable=False, unique=True)

    formatting = Column(Float, default=0)   # max 15
    skills = Column(Float, default=0)        # max 20
    projects = Column(Float, default=0)      # max 20
    experience = Column(Float, default=0)    # max 20
    education = Column(Float, default=0)     # max 10
    grammar = Column(Float, default=0)       # max 15 (keywords/grammar combined)

    total = Column(Float, default=0)         # max 100, sum of the above

    analysis = relationship("Analysis", back_populates="score_breakdown")
