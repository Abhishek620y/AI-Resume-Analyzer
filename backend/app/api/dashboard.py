"""
Dashboard endpoints — not explicitly named in the doc's API Design section
(which only covers Resume/JD/Analysis), but required to power the Dashboard
UI page described elsewhere in the spec (Cards + Charts). Scoped the same
way as Resume/JD: recruiters see their own data, admins see everything.

GET /api/dashboard/cards  — Total Resumes, Average ATS, Average Match %, Top Skills, Top Missing Skills
GET /api/dashboard/charts — Skill Distribution, ATS Score Trend, Match Score Trend
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User, UserRole
from app.schemas.dashboard import DashboardCards, DashboardCharts
from app.api.deps import get_current_user
from app.services import dashboard_service

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


def _scope_for(current_user: User) -> int | None:
    return None if current_user.role == UserRole.ADMIN else current_user.id


@router.get("/cards", response_model=DashboardCards)
def get_cards(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return dashboard_service.get_dashboard_cards(db, user_id=_scope_for(current_user))


@router.get("/charts", response_model=DashboardCharts)
def get_charts(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return dashboard_service.get_dashboard_charts(db, user_id=_scope_for(current_user))
