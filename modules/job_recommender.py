
JOB_ROLES = {
    "Data Analyst": [
        "Python", "SQL", "Excel", "Power BI", "Tableau",
        "Pandas", "NumPy", "Data Visualization", "Data Analysis"
    ],
    "Data Scientist": [
        "Python", "SQL", "Pandas", "NumPy", "Scikit-learn",
        "Machine Learning", "Statistics", "Data Analysis"
    ],
    "Machine Learning Engineer": [
        "Python", "Scikit-learn", "Machine Learning",
        "Deep Learning", "TensorFlow", "PyTorch", "Git", "Docker"
    ],
    "Python Backend Developer": [
        "Python", "Flask", "Django", "FastAPI", "SQL",
        "MySQL", "PostgreSQL", "Git", "Docker"
    ],
    "Frontend Developer": [
        "HTML", "CSS", "JavaScript", "TypeScript", "React"
    ],
    "Data Engineer": [
        "Python", "SQL", "MySQL", "PostgreSQL",
        "MongoDB", "Docker", "AWS", "Linux"
    ],
}


def recommend_job_roles(resume_text, top_n=3):
    from modules.skill_extractor import extract_skills

    resume_skills = set(extract_skills(resume_text))

    if not resume_skills:
        return []

    recommendations = []

    for role, required_skills in JOB_ROLES.items():
        matched = sorted(
            resume_skills.intersection(required_skills),
            key=str.casefold
        )

        score = round(
            len(matched) / len(set(required_skills)) * 100, 2
        )

        recommendations.append({
            "role": role,
            "match_score": score,
            "matched_skills": matched,
            "missing_skills": sorted(
                set(required_skills) - resume_skills,
                key=str.casefold
            ),
        })

    recommendations.sort(
        key=lambda item: item["match_score"],
        reverse=True
    )

    return recommendations[:top_n]
