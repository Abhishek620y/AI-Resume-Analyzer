"""
Semantic similarity matcher — compares resume text against a job
description using sentence embeddings, per the doc's suggestion:
"improve this using sentence embeddings (sentence-transformers) to
compare not just exact keywords but also semantic similarity."

sentence-transformers downloads its model from Hugging Face Hub on
first use. If that's unavailable (offline environment, no HF access,
model not pre-cached), this degrades gracefully to a TF-IDF cosine
similarity — still a legitimate, deterministic NLP technique, not AI —
so the matching pipeline keeps working end-to-end either way. Once a
sentence-transformers model is available, it's used automatically with
zero code changes.
"""
import re

_model = None
_model_load_attempted = False


def _get_sentence_transformer():
    global _model, _model_load_attempted
    if _model_load_attempted:
        return _model
    _model_load_attempted = True
    try:
        from sentence_transformers import SentenceTransformer
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    except Exception:
        _model = None
    return _model


def _tfidf_similarity(text_a: str, text_b: str) -> float:
    """Fallback: TF-IDF + cosine similarity. Returns 0-100."""
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity

    if not text_a.strip() or not text_b.strip():
        return 0.0

    vectorizer = TfidfVectorizer(stop_words="english")
    try:
        tfidf_matrix = vectorizer.fit_transform([text_a, text_b])
    except ValueError:
        # Happens if both texts are entirely stop-words/empty after cleaning.
        return 0.0

    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    return round(float(similarity) * 100, 1)


def _embedding_similarity(text_a: str, text_b: str, model) -> float:
    from sentence_transformers import util

    embeddings = model.encode([text_a, text_b], convert_to_tensor=True)
    similarity = util.cos_sim(embeddings[0], embeddings[1]).item()
    # Cosine similarity is -1..1; clamp to 0..1 before scaling to a 0-100 score.
    return round(max(0.0, similarity) * 100, 1)


def compute_semantic_similarity(resume_text: str, jd_text: str) -> tuple[float, str]:
    """
    Returns (score_0_to_100, method_used) where method_used is
    "sentence-transformers" or "tfidf" — surfaced so it's clear in
    testing/logs which path was taken.
    """
    resume_text = re.sub(r"\s+", " ", resume_text or "").strip()
    jd_text = re.sub(r"\s+", " ", jd_text or "").strip()

    model = _get_sentence_transformer()
    if model is not None:
        return _embedding_similarity(resume_text, jd_text, model), "sentence-transformers"

    return _tfidf_similarity(resume_text, jd_text), "tfidf"
