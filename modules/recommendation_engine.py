
def generate_recommendations(results, resume_text):
    """Generate personalized resume improvement suggestions."""

    recommendations = []
    resume_lower = resume_text.lower()

    missing_skills = results.get("missing_skills", [])
    matched_skills = results.get("matched_skills", [])

    # Skill-based recommendations
    if missing_skills:
        recommendations.append({
            "category": "Skill Development",
            "priority": "High",
            "suggestion": (
                "Review these job-required skills that were not "
                "detected in your resume: "
                + ", ".join(missing_skills)
                + ". Learn relevant skills and add them only when "
                  "you have the knowledge or experience."
            )
        })

    # Project recommendations
    if "project" not in resume_lower:
        recommendations.append({
            "category": "Projects",
            "priority": "Medium",
            "suggestion": (
                "Add a Projects section describing your academic, "
                "personal, or internship projects. Explain the "
                "problem, tools used, and outcome."
            )
        })

    # Education recommendations
    if "education" not in resume_lower:
        recommendations.append({
            "category": "Education",
            "priority": "Medium",
            "suggestion": (
                "Add an Education section with your degree, "
                "institution, and graduation year."
            )
        })

    # Experience recommendations
    experience_terms = [
        "internship", "work experience", "professional experience"
    ]

    if not any(term in resume_lower for term in experience_terms):
        recommendations.append({
            "category": "Experience",
            "priority": "Low",
            "suggestion": (
                "If applicable, include internships, volunteering, "
                "freelance work, or relevant practical experience. "
                "If you have none, emphasize projects instead."
            )
        })

    # Evidence-based writing recommendation
    if matched_skills:
        recommendations.append({
            "category": "Resume Writing",
            "priority": "Medium",
            "suggestion": (
                "Connect relevant skills such as "
                + ", ".join(matched_skills)
                + " to specific projects or achievements. "
                  "Use measurable results where you can substantiate them."
            )
        })

    # General recommendation based on score
    score = results.get("overall_score", 0)

    if score < 50:
        recommendations.append({
            "category": "Job Alignment",
            "priority": "High",
            "suggestion": (
                "Review the job description and tailor your resume "
                "to the requirements you genuinely meet. Include "
                "relevant projects and use accurate terminology."
            )
        })
    else:
        recommendations.append({
            "category": "Job Alignment",
            "priority": "Medium",
            "suggestion": (
                "Review the job description for important requirements "
                "that may be missing from your resume. Make sure your "
                "relevant experience is easy to identify."
            )
        })

    return recommendations
