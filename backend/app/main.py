"""
Application entrypoint.

Routers are registered here as each module is built. Currently a bare
skeleton with a health check so the scaffolding can be verified end-to-end
before any feature module lands.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.core.init_db import init_db

from app.core.config import get_settings

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()          # Create all database tables
    yield

app = FastAPI(
    title=settings.app_name,
    lifespan=lifespan
)

# Wide-open CORS for local dev; tighten before production deployment.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    return {"status": "ok", "app": settings.app_name}


from app.api import auth, resume, analysis, jd, dashboard  # noqa: E402

app.include_router(auth.router, prefix=settings.api_v1_prefix)
app.include_router(resume.router, prefix=settings.api_v1_prefix)
app.include_router(analysis.router, prefix=settings.api_v1_prefix)
app.include_router(jd.router, prefix=settings.api_v1_prefix)
app.include_router(dashboard.router, prefix=settings.api_v1_prefix)
