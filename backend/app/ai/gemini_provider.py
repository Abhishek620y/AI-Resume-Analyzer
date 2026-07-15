"""
Gemini provider — same role as the OpenAI provider (doc lists Gemini as
the cheaper alternative). Requires GEMINI_API_KEY. Any failure falls back
to None so suggestion_service.py switches to the mock provider.
"""
import json
import re

from app.ai.base import SuggestionProvider, SuggestionContext
from app.ai.openai_provider import SYSTEM_PROMPT
from app.core.config import get_settings

settings = get_settings()


class GeminiSuggestionProvider(SuggestionProvider):
    def generate(self, context: SuggestionContext) -> dict | None:
        if not settings.gemini_api_key:
            return None

        try:
            import google.generativeai as genai

            genai.configure(api_key=settings.gemini_api_key)
            model = genai.GenerativeModel("gemini-1.5-flash")

            user_prompt = self._build_user_prompt(context)
            response = model.generate_content(f"{SYSTEM_PROMPT}\n\n{user_prompt}")

            text = response.text.strip()
            # Gemini sometimes wraps JSON in markdown code fences despite instructions.
            text = re.sub(r"^```(?:json)?|```$", "", text, flags=re.MULTILINE).strip()

            parsed = json.loads(text)
            if "feedback" not in parsed or "recommendations" not in parsed:
                return None

            return {"feedback": parsed["feedback"], "recommendations": parsed["recommendations"]}

        except Exception:
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
