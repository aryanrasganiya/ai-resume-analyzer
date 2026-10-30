
import streamlit as st
import fitz  # PyMuPDF
from docx import Document
from io import BytesIO
from modules.skill_extractor import (extract_skills,compare_skills)

from modules.matching_scorer import (calculate_match_score,interpret_score)

from modules.recommendation_engine import generate_recommendations
from modules.job_recommender import recommend_job_roles
from modules.report_generator import generate_pdf_report
from modules.resume_evaluator import (evaluate_resume,generate_section_suggestions)

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main {
        background-color: #0E1117;
    }

    h1 {
        color: #4DA8DA;
        font-weight: 800;
    }

    h2, h3 {
        color: #8ECAE6;
    }

    div.stButton > button {
        background-color: #0077B6;
        color: white;
        border-radius: 10px;
        border: none;
        padding: 10px 22px;
        font-weight: bold;
    }

    div.stButton > button:hover {
        background-color: #023E8A;
        color: white;
        border: 1px solid #90E0EF;
    }

    div[data-testid="stMetric"] {
        background-color: #1B263B;
        border: 1px solid #415A77;
        padding: 15px;
        border-radius: 12px;
    }

    div[data-testid="stExpander"] {
        border: 1px solid #415A77;
        border-radius: 10px;
    }

    footer {
        visibility: hidden;
    }
</style>
""", unsafe_allow_html=True)


def extract_pdf_text(file_bytes):
    """Extract selectable text from a PDF resume."""
    text_parts = []

    with fitz.open(stream=file_bytes, filetype="pdf") as pdf:
        for page_number, page in enumerate(pdf, start=1):
            page_text = page.get_text("text")
            if page_text.strip():
                text_parts.append(
                    f"--- Page {page_number} ---\n{page_text}"
                )

    return "\n\n".join(text_parts)


def extract_docx_text(file_bytes):
    """Extract text from DOCX paragraphs and tables."""
    document = Document(BytesIO(file_bytes))
    text_parts = []

    # Extract paragraphs
    for paragraph in document.paragraphs:
        if paragraph.text.strip():
            text_parts.append(paragraph.text)

    # Extract text from tables
    for table in document.tables:
        for row in table.rows:
            row_text = [
                cell.text.strip() for cell in row.cells
            ]
            if any(row_text):
                text_parts.append(" | ".join(row_text))

    return "\n".join(text_parts)


def extract_resume_text(uploaded_file):
    """Choose the appropriate parser for the uploaded file."""
    file_bytes = uploaded_file.getvalue()
    file_name = uploaded_file.name.lower()

    if file_name.endswith(".pdf"):
        return extract_pdf_text(file_bytes)

    if file_name.endswith(".docx"):
        return extract_docx_text(file_bytes)

    raise ValueError("Unsupported file type.")

# -------------------------------
# Streamlit User Interface
# -------------------------------

st.title("📄 AI Resume Analyzer ")

st.markdown(
    """
    ### Smart Resume Analysis & Career Recommendation Platform

    Upload your resume, compare it with a job description,
    identify skill gaps, and discover suitable career opportunities.
    """
)

st.divider()

st.write(
    "Upload your resume to extract its content. "
    "We'll use this text for skills analysis and job matching."
)

st.divider()

st.subheader("1. Upload Your Resume")

uploaded_file = st.file_uploader(
    "Choose a PDF or DOCX resume",
    type=["pdf", "docx"]
)

resume_text = ""

if uploaded_file is not None:
    st.caption(
        f"File: {uploaded_file.name} | "
        f"Size: {uploaded_file.size / 1024:.2f} KB"
    )

    try:
        with st.spinner("Extracting resume text..."):
            resume_text = extract_resume_text(uploaded_file)

        if resume_text.strip():
            st.success("Resume text extracted successfully!")

            col1, col2 = st.columns(2)
            col1.metric("Characters extracted", f"{len(resume_text):,}")
            col2.metric(
                "Words extracted",
                f"{len(resume_text.split()):,}"
            )

            with st.expander("View extracted resume text", expanded=True):
                st.text_area(
                    "Extracted content",
                    value=resume_text,
                    height=350,
                    disabled=True
                )

        else:
            st.warning(
                "No selectable text was found. "
                "If this is a scanned PDF, OCR may be required."
            )

    except Exception as error:
        st.error(
            "Unable to read this file. Please check that it is a "
            "valid, unencrypted PDF or DOCX document."
        )
        st.caption(f"Technical details: {error}")

st.divider()

st.subheader("2. Job Description")

job_description = st.text_area(
    "Paste the job description",
    placeholder="Paste the role requirements here...",
    height=180
)



if st.button("Analyze Resume", type="primary"):
    if uploaded_file is None:
        st.warning("Please upload your resume first.")

    elif not resume_text.strip():
        st.warning("No resume text is available to analyze.")

    elif not job_description.strip():
        st.warning("Please enter a job description.")

    else:
        try:
            results = calculate_match_score(
                resume_text,
                job_description
            )

            st.divider()
            st.header("Resume–Job Match Analysis")

            # Main score
            st.metric(
                "Overall Match Score",
                f'{results["overall_score"]:.1f}%'
            )

            st.progress(
                int(round(results["overall_score"]))
            )

            st.info(
                interpret_score(results["overall_score"])
            )

            st.caption(
                f'Scoring method: {results["scoring_method"]}. '
                "This is an estimated matching indicator, "
                "not an official ATS score."
            )

            # Supporting scores
            col1, col2 = st.columns(2)

            with col1:
                if results["skill_coverage"] is not None:
                    st.metric(
                        "Required Skill Coverage",
                        f'{results["skill_coverage"]:.1f}%'
                    )
                else:
                    st.metric(
                        "Required Skill Coverage",
                        "Unavailable"
                    )

            with col2:
                st.metric(
                    "Text Similarity",
                    f'{results["text_similarity"]:.1f}%'
                )

            st.divider()

            # Skills found in the resume
            st.subheader("Skills Found in Your Resume")

            if results["resume_skills"]:
                st.write(", ".join(results["resume_skills"]))
            else:
                st.warning("No recognized skills detected.")

            # Matched and missing skills
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Matched Skills")

                if results["matched_skills"]:
                    for skill in results["matched_skills"]:
                        st.write(f"✅ {skill}")
                else:
                    st.info("No matching skills found.")

            with col2:
                st.subheader("Potential Skill Gaps")

                if results["missing_skills"]:
                    for skill in results["missing_skills"]:
                        st.write(f"📌 {skill}")
                else:
                    st.success(
                        "No gaps detected among recognized skills."
                    )

            
            st.divider()
            st.header("Personalized Resume Recommendations")

            recommendations = generate_recommendations(
                results,
                resume_text
            )

            for item in recommendations:
                with st.expander(
                    f'{item["priority"]} Priority — {item["category"]}'
                ):
                    st.write(item["suggestion"])

            
            st.divider()
            st.header("Recommended Job Roles")

            job_recommendations = recommend_job_roles(resume_text)

            if job_recommendations:
                for job in job_recommendations:
                    with st.expander(
                        f'{job["role"]} — {job["match_score"]}% skill match'
                    ):
                        st.write("**Matched Skills**")
                        if job["matched_skills"]:
                            st.write(", ".join(job["matched_skills"]))
                        else:
                            st.write("No matching skills detected.")

                        st.write("**Skills to Develop**")
                        if job["missing_skills"]:
                            st.write(", ".join(job["missing_skills"]))
                        else:
                            st.write("All listed skills were detected.")

            else:
                st.info(
                    "No recognized skills were found. "
                    "Try a resume containing technical or professional skills."
                )

            
            st.divider()
            st.header("Resume Analysis Dashboard")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Overall Match Score",
                    f'{results["overall_score"]}%'
                )

            with col2:
                st.metric(
                    "Text Similarity",
                    f'{results["text_similarity"]}%'
                )

            with col3:
                coverage = results["skill_coverage"]
                coverage_display = (
                    f"{coverage}%"
                    if coverage is not None
                    else "N/A"
                )
                st.metric("Skill Coverage", coverage_display)

            col4, col5 = st.columns(2)

            with col4:
                st.metric(
                    "Matched Skills",
                    len(results["matched_skills"])
                )

            with col5:
                st.metric(
                    "Missing Skills",
                    len(results["missing_skills"])
                )

            matched_count = len(results["matched_skills"])
            missing_count = len(results["missing_skills"])

            if matched_count + missing_count > 0:
                import pandas as pd

                chart_data = pd.DataFrame({
                    "Skill Status": ["Matched", "Missing"],
                    "Count": [matched_count, missing_count]
                })

                st.subheader("Skill Gap Overview")
                st.bar_chart(
                    chart_data.set_index("Skill Status")
                )
            else:
                st.info(
                    "No job-description skills were detected "
                    "for the skill gap chart."
                )

            evaluation = evaluate_resume(resume_text)

            section_suggestions = generate_section_suggestions(
               evaluation
            )

            st.divider()
            st.header("Download Analysis Report")

            pdf_bytes = generate_pdf_report(results,recommendations,job_recommendations,evaluation,section_suggestions)

            st.download_button(
            label="Download PDF Report",
            data=pdf_bytes,
            file_name="resume_analysis_report.pdf",
            mime="application/pdf",
            )

            
            st.divider()
            st.header("Resume Strength Analysis")

            evaluation = evaluate_resume(resume_text)

            st.metric(
                "Resume Strength Score",
                f'{evaluation["resume_strength_score"]}/100'
            )

            st.subheader(evaluation["strength_level"])

            st.progress(
                evaluation["resume_strength_score"] / 100
            )

            col1, col2 = st.columns(2)

            with col1:
                st.write("**Sections Found**")
                for section in evaluation["found_sections"]:
                    st.success(section)

            with col2:
                st.write("**Sections Missing**")
                for section in evaluation["missing_sections"]:
                    st.warning(section)

            st.subheader("Section-wise Score")

            import pandas as pd

            section_data = pd.DataFrame({
                "Section": list(evaluation["section_scores"].keys()),
                "Score": list(evaluation["section_scores"].values())
            })

            st.bar_chart(
                section_data.set_index("Section")
            )

            st.divider()
            st.subheader("Resume Section Improvement Suggestions")

            section_suggestions = generate_section_suggestions(
                evaluation
            )

            for item in section_suggestions:
                with st.expander(item["section"]):
                    st.write(item["suggestion"])


        except Exception as error:
            st.error("The resume analysis could not be completed.")
            st.exception(error)

