"""
Centralized application configuration.

All environment-driven settings live here so the rest of the codebase
never touches os.environ directly. This is also what makes the AI
provider swappable (mock -> openai -> gemini) with zero code changes
elsewhere.
"""
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # --- App ---
    app_name: str = "AI Resume Analyzer"
    api_v1_prefix: str = "/api"

    # --- Database ---
    database_url: str = "sqlite:///./database/app.db"

    # --- Auth ---
    jwt_secret_key: str = "change-this-to-a-long-random-string"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    # --- AI provider ---
    ai_provider: str = "mock"  # mock | openai | gemini
    openai_api_key: str = ""
    gemini_api_key: str = ""

    # --- File storage ---
    upload_dir: str = "../uploads"
    max_upload_size_mb: int = 10

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache
def get_settings() -> Settings:
    """Cached settings instance — import and call this, don't instantiate Settings() directly."""
    return Settings()
