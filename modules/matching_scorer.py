
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from modules.skill_extractor import compare_skills


def calculate_text_similarity(resume_text, job_description):
    """Calculate similarity between resume and job description."""

    if not resume_text.strip() or not job_description.strip():
        return 0.0

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
        sublinear_tf=True
    )

    try:
        vectors = vectorizer.fit_transform(
            [resume_text, job_description]
        )
    except ValueError:
        # For example, both inputs may contain only stop words.
        return 0.0

    similarity = cosine_similarity(
        vectors[0:1],
        vectors[1:2]
    )[0][0]

    return round(float(similarity) * 100, 2)


def calculate_match_score(resume_text, job_description):
    """Combine skill coverage and text similarity."""

    if not resume_text.strip() or not job_description.strip():
        raise ValueError(
            "Resume text and job description cannot be empty."
        )

    skill_results = compare_skills(
        resume_text,
        job_description
    )

    text_similarity = calculate_text_similarity(
        resume_text,
        job_description
    )

    skill_coverage = skill_results["skill_coverage"]

    if skill_coverage is not None:
        # Weighted score: 60% skill coverage, 40% text similarity.
        overall_score = (
            0.60 * skill_coverage
            + 0.40 * text_similarity
        )
        scoring_method = "Skill coverage + text similarity"
    else:
        # If no known skills were found in the job description,
        # avoid inventing a skill coverage score.
        overall_score = text_similarity
        scoring_method = "Text similarity only"

    overall_score = round(
        max(0.0, min(100.0, overall_score)),
        2
    )

    return {
        **skill_results,
        "text_similarity": text_similarity,
        "overall_score": overall_score,
        "scoring_method": scoring_method,
    }


def interpret_score(score):
    """Provide a descriptive label, not a hiring prediction."""

    if score >= 75:
        return "Strong textual match"
    elif score >= 50:
        return "Moderate textual match"
    elif score >= 25:
        return "Limited textual match"
    else:
        return "Low textual match"
