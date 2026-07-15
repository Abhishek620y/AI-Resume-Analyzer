"""Pydantic schemas for Skill (master list) and dashboard aggregation responses."""
from pydantic import BaseModel, ConfigDict


class SkillOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    category: str | None = None


class DashboardCards(BaseModel):
    total_resumes: int
    average_ats_score: float
    average_match_score: float
    top_skills: list[str]
    top_missing_skills: list[str]


class SkillDistributionItem(BaseModel):
    skill: str
    count: int


class DashboardCharts(BaseModel):
    skill_distribution: list[SkillDistributionItem]
    ats_score_trend: list[dict]   # [{date, average_score}]
    match_score_trend: list[dict]  # [{date, average_score}]
