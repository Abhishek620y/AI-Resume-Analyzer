"""
Abstract interface all AI suggestion providers implement, so the rest of
the app (suggestion_service, analysis_service) never needs to know
whether it's talking to OpenAI, Gemini, or the mock fallback.
"""
from abc import ABC, abstractmethod


class SuggestionContext:
    """Bundles everything a provider might want to reason about."""

    def __init__(
        self,
        resume_name: str | None,
        resume_text: str,
        skills: list[str],
        ats_score: float,
        ats_notes: list[str],
        jd_title: str | None = None,
        jd_description: str | None = None,
        missing_skills: list[str] | None = None,
        match_score: float | None = None,
    ):
        self.resume_name = resume_name
        self.resume_text = resume_text
        self.skills = skills
        self.ats_score = ats_score
        self.ats_notes = ats_notes
        self.jd_title = jd_title
        self.jd_description = jd_description
        self.missing_skills = missing_skills or []
        self.match_score = match_score


class SuggestionProvider(ABC):
    @abstractmethod
    def generate(self, context: SuggestionContext) -> dict:
        """
        Returns:
            {"feedback": str, "recommendations": list[str]}
        Must never raise — providers should catch their own errors and
        let suggestion_service.py handle fallback to mock.
        """
        raise NotImplementedError
