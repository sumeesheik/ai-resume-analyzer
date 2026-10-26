# AI Resume Analyzer and Job Recommendation System

## About the Project

This project helps students understand how well their resume matches different job roles. It analyzes an uploaded resume, identifies skills, recommends suitable jobs, highlights missing skills, and suggests a learning roadmap to improve career opportunities.

## Features

- Upload resumes in PDF and DOCX formats.
- Detect skills mentioned in the resume.
- Recommend suitable job roles with matching scores.
- Identify missing skills for selected roles.
- Generate a personalized learning roadmap.
- Download analysis reports in CSV and TXT formats.

## Technologies Used

- Python
- Streamlit
- Pandas
- Scikit-learn
- Plotly
- PyPDF and python-docx

## How to Run

1. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

2. Start the application:

   ```bash
   python -m streamlit run app.py
   ```

3. Open the local URL shown in the terminal and upload your resume.

## Project Structure

- `app.py` – Main Streamlit application
- `job_matcher.py` – Job matching and scoring
- `resume_parser.py` – Resume text extraction
- `skill_extractor.py` – Skill detection
- `text_cleaner.py` – Text preprocessing
- `roadmap_generator.py` – Learning roadmap generation
- `data/` – Job roles and skill datasets
- `tests/` – Test cases and automated tests

## Note

This project is designed for educational and career guidance purposes. Matching scores are estimates and may not fully represent a person's skills or job suitability.