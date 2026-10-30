
import re


def evaluate_resume(resume_text):
    if not resume_text or not resume_text.strip():
        raise ValueError("Resume text cannot be empty.")

    text = resume_text.lower()

    sections = {
        "Skills": [
            "skills", "technical skills", "key skills",
            "core competencies"
        ],
        "Education": [
            "education", "academic qualification",
            "educational background"
        ],
        "Projects": [
            "projects", "academic projects",
            "personal projects"
        ],
        "Experience": [
            "experience", "work experience",
            "professional experience", "internship"
        ],
        "Certifications": [
            "certifications", "certificates",
            "courses", "licenses"
        ],
        "Achievements": [
            "achievements", "awards",
            "accomplishments"
        ],
    }

    section_weights = {
        "Skills": 25,
        "Education": 20,
        "Projects": 20,
        "Experience": 15,
        "Certifications": 10,
        "Achievements": 10,
    }

    found_sections = []
    missing_sections = []
    section_scores = {}

    total_score = 0

    for section, keywords in sections.items():

        found = any(
            re.search(
                r"(?<!\w)" + re.escape(keyword) + r"(?!\w)",
                text
            )
            for keyword in keywords
        )

        if found:
            found_sections.append(section)
            section_scores[section] = section_weights[section]
            total_score += section_weights[section]
        else:
            missing_sections.append(section)
            section_scores[section] = 0

    if total_score >= 80:
        strength = "Excellent Resume Structure"
    elif total_score >= 60:
        strength = "Good Resume Structure"
    elif total_score >= 40:
        strength = "Average Resume Structure"
    else:
        strength = "Needs Improvement"

    return {
        "resume_strength_score": total_score,
        "strength_level": strength,
        "found_sections": found_sections,
        "missing_sections": missing_sections,
        "section_scores": section_scores,
    }

def generate_section_suggestions(evaluation):
    suggestions = []

    missing_sections = evaluation.get("missing_sections", [])

    suggestion_map = {
        "Skills": (
            "Add a Skills section listing relevant technical skills, "
            "programming languages, tools, and technologies."
        ),
        "Education": (
            "Add your degree, college name, graduation year, "
            "and relevant academic details."
        ),
        "Projects": (
            "Add academic or personal projects. Describe the problem, "
            "technologies used, your contribution, and outcomes."
        ),
        "Experience": (
            "Include internships, freelance work, volunteering, "
            "or practical experience if applicable."
        ),
        "Certifications": (
            "Include relevant certifications and completed courses "
            "with their issuing organizations."
        ),
        "Achievements": (
            "Highlight relevant awards, competitions, academic "
            "achievements, and measurable accomplishments."
        ),
    }

    for section in missing_sections:
        suggestions.append({
            "section": section,
            "suggestion": suggestion_map[section]
        })

    if not suggestions:
        suggestions.append({
            "section": "Overall",
            "suggestion": (
                "All evaluated sections were detected. "
                "Review their content for accuracy, relevance, "
                "and measurable achievements."
            )
        })

    return suggestions
