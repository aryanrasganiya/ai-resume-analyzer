
from io import BytesIO
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,)

def generate_pdf_report(results, recommendations, job_recommendations, evaluation, section_suggestions):
    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=0.6 * inch,
        leftMargin=0.6 * inch,
        topMargin=0.6 * inch,
        bottomMargin=0.6 * inch,
    )

    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="ReportTitle",
            parent=styles["Title"],
            alignment=TA_CENTER,
            textColor=colors.HexColor("#17365D"),
            spaceAfter=18,
        )
    )

    story = []

    def add_paragraph(text, style="BodyText"):
        story.append(Paragraph(escape(str(text)), styles[style]))
        story.append(Spacer(1, 6))

    def add_list(items):
        if not items:
            add_paragraph("None detected.")
            return

        for item in items:
            add_paragraph(f"- {item}")

    story.append(
        Paragraph(
            "AI Resume Analyzer for Freshers",
            styles["ReportTitle"],
        )
    )

    add_paragraph("Resume Analysis Report", "Heading2")
    add_paragraph(
        "This report provides a preliminary comparison between "
        "the submitted resume and the supplied job description."
    )

    story.append(Spacer(1, 8))

    score_data = [
        ["Metric", "Result"],
        ["Overall Match Score", f'{results["overall_score"]}%'],
        ["Text Similarity", f'{results["text_similarity"]}%'],
        [
            "Skill Coverage",
            (
                f'{results["skill_coverage"]}%'
                if results["skill_coverage"] is not None
                else "N/A"
            ),
        ],
    ]

    score_table = Table(
        score_data,
        colWidths=[3 * inch, 2 * inch],
    )

    score_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#17365D")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("PADDING", (0, 0), (-1, -1), 7),
        ])
    )

    story.append(score_table)
    story.append(Spacer(1, 14))

    add_paragraph("Matched Skills", "Heading2")
    add_list(results.get("matched_skills", []))

    add_paragraph("Potential Skill Gaps", "Heading2")
    add_list(results.get("missing_skills", []))

    add_paragraph("Detected Resume Skills", "Heading2")
    add_list(results.get("resume_skills", []))

    add_paragraph("Recommended Job Roles", "Heading2")

    for job in job_recommendations:
        add_paragraph(
            f'{job["role"]} — {job["match_score"]}% skill match',
            "Heading3",
        )
        add_paragraph(
            "Matched skills: "
            + (", ".join(job["matched_skills"]) or "None")
        )

    add_paragraph("Personalized Improvement Suggestions", "Heading2")

    for item in recommendations:
        add_paragraph(
            f'{item["priority"]} Priority — {item["category"]}',
            "Heading3",
        )
        add_paragraph(item["suggestion"])

    story.append(Spacer(1, 12))

    add_paragraph("Resume Strength Analysis", "Heading2")

    add_paragraph(
        f'Resume Strength Score: '
        f'{evaluation["resume_strength_score"]}/100'
    )

    add_paragraph(
        f'Strength Level: {evaluation["strength_level"]}'
    )

    add_paragraph("Sections Found", "Heading3")
    add_list(evaluation.get("found_sections", []))

    add_paragraph("Sections Missing", "Heading3")
    add_list(evaluation.get("missing_sections", []))

    add_paragraph("Section-wise Scores", "Heading3")

    for section, score in evaluation.get(
        "section_scores", {}
    ).items():
        add_paragraph(f"{section}: {score}")

    add_paragraph(
        "Resume Section Improvement Suggestions",
        "Heading2"
    )

    for item in section_suggestions:
        add_paragraph(item["section"], "Heading3")
        add_paragraph(item["suggestion"])

    
    add_paragraph("Resume Strength Analysis", "Heading2")

    add_paragraph(
        f'Resume Strength Score: '
        f'{evaluation["resume_strength_score"]}/100'
    )

    add_paragraph(
        f'Strength Level: {evaluation["strength_level"]}'
    )

    add_paragraph("Sections Found", "Heading3")
    add_list(evaluation.get("found_sections", []))

    add_paragraph("Sections Missing", "Heading3")
    add_list(evaluation.get("missing_sections", []))

    add_paragraph("Section-wise Scores", "Heading3")

    for section, score in evaluation.get("section_scores", {}).items():
        add_paragraph(f"{section}: {score}")

    add_paragraph(
        "Resume Section Improvement Suggestions",
        "Heading2"
    )

    for item in section_suggestions:
        add_paragraph(item["section"], "Heading3")
        add_paragraph(item["suggestion"])


    add_paragraph(
        "Note: Scores are heuristic indicators, not an official ATS "
        "score, hiring decision, or guarantee of job suitability."
    )

    document.build(story)
    buffer.seek(0)

    return buffer.getvalue()
