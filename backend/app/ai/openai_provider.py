"""
OpenAI provider — used only for feedback/summary/suggestions, never for
skill extraction (that stays rule-based per the spec). Uses the prompt
structure from the doc:

    "Analyze this resume. Suggest improvements. Mention missing skills.
     Suggest ATS improvements. Suggest stronger project descriptions."

Requires OPENAI_API_KEY to be set. Any failure (bad key, network error,
rate limit, malformed response) is caught and returns None so
suggestion_service.py can fall back to the mock provider rather than
breaking the analysis pipeline.
"""
import json

from app.ai.base import SuggestionProvider, SuggestionContext
from app.core.config import get_settings

settings = get_settings()

SYSTEM_PROMPT = (
    "You are a career coach reviewing a resume. Analyze the resume. "
    "Suggest improvements. Mention missing skills relevant to the target "
    "role if one is provided. Suggest ATS improvements. Suggest stronger "
    "project descriptions where relevant. "
    "Respond ONLY with valid JSON: "
    '{"feedback": "<2-4 sentence narrative feedback>", '
    '"recommendations": ["<short imperative suggestion>", ...]}'
)


class OpenAISuggestionProvider(SuggestionProvider):
    def generate(self, context: SuggestionContext) -> dict | None:
        if not settings.openai_api_key:
            return None

        try:
            from openai import OpenAI

            client = OpenAI(api_key=settings.openai_api_key)

            user_prompt = self._build_user_prompt(context)

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.4,
                max_tokens=500,
            )

            content = response.choices[0].message.content
            parsed = json.loads(content)

            if "feedback" not in parsed or "recommendations" not in parsed:
                return None

            return {"feedback": parsed["feedback"], "recommendations": parsed["recommendations"]}

        except Exception:
            # Network error, bad key, rate limit, malformed JSON, etc. —
            # let suggestion_service.py fall back to the mock provider.
            return None

    @staticmethod
    def _build_user_prompt(context: SuggestionContext) -> str:
        parts = [f"Resume text:\n{context.resume_text[:3000]}"]
        parts.append(f"Detected skills: {', '.join(context.skills) or 'none detected'}")
        parts.append(f"ATS score: {context.ats_score}/100")

        if context.jd_title:
            parts.append(f"Target role: {context.jd_title}")
            if context.missing_skills:
                parts.append(f"Missing skills for this role: {', '.join(context.missing_skills)}")
            if context.match_score is not None:
                parts.append(f"Match score against this role: {context.match_score}%")

        return "\n\n".join(parts)
