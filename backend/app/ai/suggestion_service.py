"""
Suggestion service — the single entry point analysis_service.py calls.
Picks the configured provider (AI_PROVIDER env var: mock | openai |
gemini) and ALWAYS falls back to the mock provider if the real provider
returns None (missing key, API error, malformed response) — so a
misconfigured or unavailable AI provider never breaks resume analysis.
"""
from app.ai.base import SuggestionContext
from app.ai.mock_provider import MockSuggestionProvider
from app.core.config import get_settings

settings = get_settings()

_mock_provider = MockSuggestionProvider()


def _get_real_provider():
    if settings.ai_provider == "openai":
        from app.ai.openai_provider import OpenAISuggestionProvider
        return OpenAISuggestionProvider()
    elif settings.ai_provider == "gemini":
        from app.ai.gemini_provider import GeminiSuggestionProvider
        return GeminiSuggestionProvider()
    return None


def generate_suggestions(context: SuggestionContext) -> dict:
    """
    Returns {"feedback": str, "recommendations": list[str], "provider_used": str}.
    provider_used is "mock", "openai", or "gemini" — useful for debugging
    and for showing the user which mode generated the feedback.
    """
    real_provider = _get_real_provider()

    if real_provider is not None:
        result = real_provider.generate(context)
        if result is not None:
            return {**result, "provider_used": settings.ai_provider}

    # Fallback: no real provider configured, or it failed.
    result = _mock_provider.generate(context)
    return {**result, "provider_used": "mock"}
