"""
Matching engine — combines exact keyword matching (the doc's primary,
explainable algorithm) with semantic similarity (the doc's suggested
enhancement) into a single match_score.

Weighting: keyword match is the primary signal (70%) since it's exact
and explainable — recruiters can see precisely which required skills
are present/missing. Semantic similarity (30%) captures overall
contextual fit that pure keyword matching misses (e.g. a resume
describing "built REST services" for a JD requiring "API development").
"""
from app.matcher.keyword_matcher import match_skills
from app.matcher.semantic_matcher import compute_semantic_similarity

KEYWORD_WEIGHT = 0.7
SEMANTIC_WEIGHT = 0.3


def run_match(
    resume_skills: list[str],
    resume_text: str,
    required_skills: list[str],
    jd_text: str,
) -> dict:
    keyword_result = match_skills(resume_skills, required_skills)
    semantic_score, semantic_method = compute_semantic_similarity(resume_text, jd_text)

    combined_score = round(
        keyword_result["match_percentage"] * KEYWORD_WEIGHT + semantic_score * SEMANTIC_WEIGHT,
        1,
    )

    return {
        "match_score": combined_score,
        "matched_skills": keyword_result["matched_skills"],
        "missing_skills": keyword_result["missing_skills"],
        "keyword_match_percentage": keyword_result["match_percentage"],
        "semantic_similarity_score": semantic_score,
        "semantic_method": semantic_method,
    }
