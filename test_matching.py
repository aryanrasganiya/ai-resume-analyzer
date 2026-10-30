
from modules.matching_scorer import (
    calculate_match_score,
    interpret_score,
)

resume = """
Python SQL Pandas Git.
Built a student performance prediction project.
"""

job = """
Junior analyst requiring Python SQL Pandas NumPy
Excel Power BI Git and data visualization.
"""

result = calculate_match_score(resume, job)

print("Overall score:", result["overall_score"])
print("Skill coverage:", result["skill_coverage"])
print("Text similarity:", result["text_similarity"])
print("Matched skills:", result["matched_skills"])
print("Missing skills:", result["missing_skills"])
print("Interpretation:", interpret_score(result["overall_score"]))
