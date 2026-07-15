"""
Dashboard service — aggregates Resume/Analysis data into the cards and
charts the frontend dashboard needs. Scoped the same way as everywhere
else: recruiters see only their own data, admins see everything (pass
user_id=None for the admin/global view).

Aggregation is done in Python rather than SQL because skills/missing_skills
are stored as JSON list columns (per our agreed simplified design) — at
this project's scale (a college/portfolio project, not high-volume
production), this is simpler and perfectly adequate.
"""
from collections import Counter, defaultdict
from statistics import mean

from sqlalchemy.orm import Session

from app.models.resume import Resume
from app.models.analysis import Analysis
from app.schemas.dashboard import DashboardCards, DashboardCharts, SkillDistributionItem

TOP_N_SKILLS = 5
TOP_N_SKILLS_CHART = 15


def _scoped_resumes(db: Session, user_id: int | None) -> list[Resume]:
    query = db.query(Resume)
    if user_id is not None:
        query = query.filter(Resume.user_id == user_id)
    return query.all()


def _scoped_analyses(db: Session, resume_ids: list[int]) -> list[Analysis]:
    if not resume_ids:
        return []
    return db.query(Analysis).filter(Analysis.resume_id.in_(resume_ids)).all()


def get_dashboard_cards(db: Session, user_id: int | None = None) -> DashboardCards:
    resumes = _scoped_resumes(db, user_id)
    resume_ids = [r.id for r in resumes]
    analyses = _scoped_analyses(db, resume_ids)

    ats_scores = [a.ats_score for a in analyses if a.ats_score is not None]
    match_scores = [a.match_score for a in analyses if a.match_score is not None]

    skill_counter = Counter()
    for r in resumes:
        skill_counter.update(r.skills or [])

    missing_counter = Counter()
    for a in analyses:
        missing_counter.update(a.missing_skills or [])

    return DashboardCards(
        total_resumes=len(resumes),
        average_ats_score=round(mean(ats_scores), 1) if ats_scores else 0.0,
        average_match_score=round(mean(match_scores), 1) if match_scores else 0.0,
        top_skills=[skill for skill, _ in skill_counter.most_common(TOP_N_SKILLS)],
        top_missing_skills=[skill for skill, _ in missing_counter.most_common(TOP_N_SKILLS)],
    )


def get_dashboard_charts(db: Session, user_id: int | None = None) -> DashboardCharts:
    resumes = _scoped_resumes(db, user_id)
    resume_ids = [r.id for r in resumes]
    analyses = _scoped_analyses(db, resume_ids)

    skill_counter = Counter()
    for r in resumes:
        skill_counter.update(r.skills or [])
    skill_distribution = [
        SkillDistributionItem(skill=skill, count=count)
        for skill, count in skill_counter.most_common(TOP_N_SKILLS_CHART)
    ]

    ats_by_date: dict[str, list[float]] = defaultdict(list)
    match_by_date: dict[str, list[float]] = defaultdict(list)

    for a in analyses:
        date_key = a.created_at.date().isoformat()
        if a.ats_score is not None:
            ats_by_date[date_key].append(a.ats_score)
        if a.match_score is not None:
            match_by_date[date_key].append(a.match_score)

    ats_score_trend = [
        {"date": date, "average_score": round(mean(scores), 1)}
        for date, scores in sorted(ats_by_date.items())
    ]
    match_score_trend = [
        {"date": date, "average_score": round(mean(scores), 1)}
        for date, scores in sorted(match_by_date.items())
    ]

    return DashboardCharts(
        skill_distribution=skill_distribution,
        ats_score_trend=ats_score_trend,
        match_score_trend=match_score_trend,
    )
