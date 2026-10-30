# AI Resume Analyzer

## Project Overview

AI Resume Analyzer for Freshers is a Python-based application developed using Streamlit. It analyzes resumes, extracts relevant skills, compares them against job descriptions, and provides career recommendations and resume improvement suggestions.

## Features

- PDF and DOCX resume text extraction
- Automated skill extraction
- Resume and job description matching
- Skill coverage and text similarity calculation
- Matched and missing skill identification
- Personalized resume improvement recommendations
- Job role recommendation engine
- Resume strength evaluation
- Interactive analysis dashboard
- Downloadable PDF analysis reports

## Technologies Used

- Python
- Streamlit
- Pandas
- Scikit-learn
- PyMuPDF
- python-docx
- ReportLab
- Matplotlib

## Installation

1. Clone the repository.
2. Navigate to the project folder.
3. Create and activate a virtual environment.
4. Install dependencies:

```bash
pip install -r requirements.txt
```

5. Run the application:

```bash
streamlit run app.py
```

## Project Structure

```text
AI_Resume_Analyzer/
├── app.py
├── skills.csv
├── requirements.txt
├── README.md
└── modules/
```

## How It Works

1. Upload a resume in PDF or DOCX format.
2. Enter the target job description.
3. Extract and analyze resume information.
4. Identify relevant and missing skills.
5. Calculate a heuristic resume matching score.
6. Recommend relevant job roles.
7. Generate resume improvement suggestions.
8. Download the analysis report as a PDF.

## Disclaimer

The matching and strength scores are heuristic indicators for guidance and are not official ATS scores or hiring predictions.