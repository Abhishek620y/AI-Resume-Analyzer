"""
Mock provider — generates plausible, useful feedback using templates and
the same structured data the ATS/matching engines already computed, with
no external API call. This is the default provider (AI_PROVIDER=mock) so
the app works fully end-to-end before an OpenAI/Gemini key is added, and
it's also the automatic fallback if a real provider call fails.
"""
from app.ai.base import SuggestionProvider, SuggestionContext


class MockSuggestionProvider(SuggestionProvider):
    def generate(self, context: SuggestionContext) -> dict:
        name = context.resume_name or "This candidate"
        feedback_parts = []

        # Opening summary line, tone varies with score band.
        if context.ats_score >= 80:
            feedback_parts.append(
                f"{name}'s resume is strong overall, scoring {context.ats_score}/100 on the ATS scan."
            )
        elif context.ats_score >= 60:
            feedback_parts.append(
                f"{name}'s resume is solid but has room to improve, scoring {context.ats_score}/100 on the ATS scan."
            )
        else:
            feedback_parts.append(
                f"{name}'s resume needs meaningful work, scoring {context.ats_score}/100 on the ATS scan."
            )

        if context.jd_title:
            if context.match_score is not None and context.match_score >= 70:
                feedback_parts.append(
                    f"It's a strong match for the '{context.jd_title}' role at {context.match_score}%."
                )
            elif context.match_score is not None:
                feedback_parts.append(
                    f"It matches the '{context.jd_title}' role at {context.match_score}%, "
                    f"with some gaps worth addressing."
                )

        if context.missing_skills:
            feedback_parts.append(
                f"Consider highlighting or gaining experience in: {', '.join(context.missing_skills)}."
            )

        if context.ats_notes:
            feedback_parts.append(context.ats_notes[0])

        feedback = " ".join(feedback_parts)

        # Short, imperative recommendations — matching the doc's example style
        # ("Improve summary.", "Add Docker.", "Add AWS.").
        recommendations = []
        for skill in context.missing_skills[:5]:
            recommendations.append(f"Add {skill}.")

        recommendations.append("Use strong action verbs at the start of each bullet point.")
        recommendations.append("Quantify achievements with numbers or percentages where possible.")

        if not context.skills:
            recommendations.append("Add a dedicated Skills section listing your key technical skills.")

        return {"feedback": feedback, "recommendations": recommendations}
