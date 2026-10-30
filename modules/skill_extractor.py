
import re
from pathlib import Path

import pandas as pd


# Find skills.csv in the project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent
SKILLS_FILE = PROJECT_ROOT / "skills.csv"


def load_skills():
    """Load skills and categories from the CSV dataset."""
    if not SKILLS_FILE.exists():
        raise FileNotFoundError(
            f"Skills dataset not found: {SKILLS_FILE}"
        )

    df = pd.read_csv(SKILLS_FILE)

    required_columns = {"skill", "category"}
    if not required_columns.issubset(df.columns):
        raise ValueError(
            "skills.csv must contain skill and category columns."
        )

    df = df.dropna(subset=["skill", "category"])
    df["skill"] = df["skill"].astype(str).str.strip()
    df["category"] = df["category"].astype(str).str.strip()

    return df


def contains_skill(text, skill):
    """Match a skill without matching it inside larger words."""
    pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"
    return re.search(pattern, text, flags=re.IGNORECASE) is not None


def extract_skills(text):
    """Return skills detected in a block of text."""
    if not text or not text.strip():
        return []

    skills_df = load_skills()
    found = []

    for skill in skills_df["skill"].unique():
        if contains_skill(text, skill):
            found.append(skill)

    return sorted(found, key=str.casefold)


def compare_skills(resume_text, job_description):
    """Compare resume skills against the job description."""
    resume_skills = set(extract_skills(resume_text))
    required_skills = set(extract_skills(job_description))

    matched = sorted(
        resume_skills & required_skills,
        key=str.casefold
    )

    missing = sorted(
        required_skills - resume_skills,
        key=str.casefold
    )

    # Only calculate coverage when the description has known skills.
    coverage = (
        round(len(matched) / len(required_skills) * 100, 2)
        if required_skills
        else None
    )

    return {
        "resume_skills": sorted(resume_skills, key=str.casefold),
        "required_skills": sorted(required_skills, key=str.casefold),
        "matched_skills": matched,
        "missing_skills": missing,
        "skill_coverage": coverage,
    }
