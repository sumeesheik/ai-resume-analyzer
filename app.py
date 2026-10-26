
import pandas as pd
import plotly.express as px
import streamlit as st

from job_matcher import analyze_resume
from roadmap_generator import generate_roadmap
from resume_parser import extract_resume_text
from skill_extractor import (
    extract_skills,
    extract_skills_by_category,
)
from text_cleaner import clean_text


# ---------------- PAGE CONFIGURATION ----------------

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide",
)

st.title("AI Resume Analyzer & Job Recommendation System")
st.caption(
    "Analyze your resume, discover matching jobs, identify missing skills, "
    "and generate a personalized learning roadmap."
)


# ---------------- SIDEBAR ----------------

with st.sidebar:
    st.header("About This Project")

    st.write(
        "Upload your resume to discover suitable job roles "
        "and understand which skills you need to improve."
    )

    st.info(
        "Match scores are estimates based on the project's job dataset. "
        "They are not probabilities of getting hired."
    )

    st.markdown("### Supported formats")
    st.write("PDF and DOCX")

    st.markdown("### Analysis")
    st.write("• Resume text extraction")
    st.write("• Skill detection")
    st.write("• Job role recommendations")
    st.write("• Learning roadmap")
    st.write("• Downloadable reports")


# ---------------- RESUME UPLOAD ----------------

st.subheader("Upload Your Resume")

uploaded_file = st.file_uploader(
    "Choose a PDF or DOCX file",
    type=["pdf", "docx"],
    help="Upload a text-based PDF or DOCX resume.",
)

# Stop safely if no file has been uploaded.
if uploaded_file is None:
    st.info("Please upload your resume to begin the analysis.")
    st.stop()

# Check file size: 5 MB maximum.
MAX_FILE_SIZE = 5 * 1024 * 1024

if uploaded_file.size > MAX_FILE_SIZE:
    st.error("File is too large. Please upload a file smaller than 5 MB.")
    st.stop()


# ---------------- EXTRACT RESUME TEXT ----------------

try:
    resume_text = extract_resume_text(
        uploaded_file.getvalue(),
        uploaded_file.name,
    )

except (ValueError, FileNotFoundError) as exc:
    st.error(f"Could not read the resume: {exc}")
    st.stop()

except Exception as exc:
    st.error(
        "An unexpected error occurred while reading the resume. "
        "Please check that the file is valid."
    )
    st.exception(exc)
    st.stop()


# ---------------- CLEAN RESUME TEXT ----------------

try:
    cleaned_text = clean_text(resume_text)

except Exception as exc:
    st.error(f"Could not clean the resume text: {exc}")
    st.stop()

if not cleaned_text or not cleaned_text.strip():
    st.error(
        "The resume contains no usable text. "
        "Try a text-based PDF or DOCX file."
    )
    st.stop()


# ---------------- ANALYZE RESUME ----------------

try:
    with st.spinner("Analyzing your resume... Please wait."):
        results = analyze_resume(cleaned_text)

        detected_skills = extract_skills(cleaned_text)

        categorized_skills = extract_skills_by_category(cleaned_text)

except Exception as exc:
    st.error("Resume analysis failed.")
    st.write(
        "Check that job_roles.csv and skill_dictionary.csv exist "
        "inside your data folder, and that the required packages are installed."
    )
    st.exception(exc)
    st.stop()


# ---------------- VALIDATE ANALYSIS RESULTS ----------------

if results is None or results.empty:
    st.error(
        "No job recommendations were generated. "
        "Check your job_roles.csv file and job_matcher.py."
    )
    st.stop()

required_columns = [
    "role",
    "skill_score",
    "tfidf_score",
    "match_score",
    "description",
    "matched_skills",
    "missing_skills",
]

missing_columns = [
    column for column in required_columns
    if column not in results.columns
]

if missing_columns:
    st.error(
        "The job analysis results are missing required columns: "
        + ", ".join(missing_columns)
    )
    st.write("Please check the output columns in job_matcher.py.")
    st.stop()

results = results.sort_values(
    "match_score",
    ascending=False,
).reset_index(drop=True)

st.success(f"Successfully analyzed: {uploaded_file.name}")


# ---------------- SUMMARY METRICS ----------------

best_role = results.iloc[0]

col1, col2, col3 = st.columns(3)

col1.metric(
    "Detected Skills",
    len(detected_skills),
)

col2.metric(
    "Best Matching Role",
    str(best_role["role"]),
)

col3.metric(
    "Best Match Score",
    f"{float(best_role['match_score']):.1f}%",
)

st.caption(
    "Combined score = 70% required-skill coverage + "
    "30% TF-IDF text similarity. This is an estimate, not a hiring probability."
)


# ---------------- MAIN TABS ----------------

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "Job Recommendations",
        "Skills Analysis",
        "Learning Roadmap",
        "Resume Text",
    ]
)


# ==================================================
# TAB 1: JOB RECOMMENDATIONS
# ==================================================

with tab1:
    st.subheader("Top Recommended Job Roles")

    top_three = results.head(3)

    for index, (_, row) in enumerate(
        top_three.iterrows(),
        start=1,
    ):
        with st.container(border=True):
            st.markdown(f"### {index}. {row['role']}")

            score = float(row["match_score"])

            st.progress(
                min(max(score / 100, 0.0), 1.0),
                text=f"Estimated Match: {score:.1f}%",
            )

            st.write(row["description"])

            st.caption(
                f"Skill Coverage: {float(row['skill_score']):.1f}% | "
                f"Text Similarity: {float(row['tfidf_score']):.1f}%"
            )

    st.divider()

    st.subheader("Compare All Job Roles")

    chart_data = results.sort_values(
        "match_score",
        ascending=True,
    )

    fig = px.bar(
        chart_data,
        x="match_score",
        y="role",
        orientation="h",
        range_x=[0, 100],
        labels={
            "match_score": "Estimated Match Score (%)",
            "role": "Job Role",
        },
        title="Resume-to-Job Matching Results",
        hover_data=["skill_score", "tfidf_score"],
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

    display_results = results[
        ["role", "skill_score", "tfidf_score", "match_score"]
    ].rename(
        columns={
            "role": "Job Role",
            "skill_score": "Skill Score (%)",
            "tfidf_score": "TF-IDF Score (%)",
            "match_score": "Combined Score (%)",
        }
    )

    st.subheader("Detailed Comparison")

    st.dataframe(
        display_results,
        hide_index=True,
        use_container_width=True,
    )


# ==================================================
# TAB 2: SKILLS ANALYSIS
# ==================================================

with tab2:
    st.subheader("Detected Skills")

    if detected_skills:
        st.write(", ".join(detected_skills))
    else:
        st.warning(
            "No skills were detected. Check the extracted resume text "
            "or add more skills to skill_dictionary.csv."
        )

    st.divider()

    st.subheader("Skills by Category")

    if categorized_skills:
        for category, skills in sorted(categorized_skills.items()):
            st.markdown(f"**{category}**")
            st.write(", ".join(skills))
    else:
        st.info("No skill categories were identified.")

    st.divider()

    st.subheader("Required Skills Comparison")

    target_role = st.selectbox(
        "Select a job role",
        options=results["role"].tolist(),
        key="skills_target_role",
    )

    selected = results.loc[
        results["role"] == target_role
    ].iloc[0]

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Required Skills Detected**")

        matched_skills = selected["matched_skills"]

        if matched_skills:
            for skill in matched_skills:
                st.write(f"✓ {skill}")
        else:
            st.write("No matching skills detected.")

    with col2:
        st.markdown("**Skills to Improve**")

        missing_skills = selected["missing_skills"]

        if missing_skills:
            for skill in missing_skills:
                st.write(f"• {skill}")
        else:
            st.success("All listed required skills were detected.")

    st.caption(
        "A skill may be missing from the analysis simply because it was "
        "not mentioned clearly in the resume."
    )


# ==================================================
# TAB 3: LEARNING ROADMAP
# ==================================================

with tab3:
    st.subheader("Personalized Learning Roadmap")

    roadmap_role = st.selectbox(
        "Choose your target job role",
        options=results["role"].tolist(),
        key="roadmap_target_role",
    )

    role_result = results.loc[
        results["role"] == roadmap_role
    ].iloc[0]

    missing_skills = role_result["missing_skills"]

    try:
        roadmap = generate_roadmap(missing_skills)

        if roadmap:
            for item in roadmap:
                with st.container(border=True):
                    st.markdown(f"### {item['week']}")

                    if item["skills"]:
                        st.write(
                            "**Focus Skills:** "
                            + ", ".join(item["skills"])
                        )

                    st.write(item["task"])
        else:
            st.success(
                "No missing skills were identified for this role. "
                "Keep practicing and building projects!"
            )

    except Exception as exc:
        st.error("Could not generate the learning roadmap.")
        st.exception(exc)


# ==================================================
# TAB 4: EXTRACTED RESUME TEXT
# ==================================================

with tab4:
    st.subheader("Extracted Resume Text")

    st.text_area(
        "Review the text extracted from your resume",
        value=resume_text,
        height=350,
    )

    st.caption(
        "PDF text extraction may be imperfect for scanned documents, "
        "multiple columns, or unusual layouts."
    )


# ==================================================
# DOWNLOAD REPORTS
# ==================================================

st.divider()

st.subheader("Download Your Analysis")

report_rows = []

for _, row in results.iterrows():
    report_rows.append(
        {
            "job_role": row["role"],
            "skill_score_percent": row["skill_score"],
            "tfidf_score_percent": row["tfidf_score"],
            "combined_score_percent": row["match_score"],
            "matched_skills": ", ".join(
                row["matched_skills"]
            ),
            "missing_skills": ", ".join(
                row["missing_skills"]
            ),
        }
    )

report_df = pd.DataFrame(report_rows)

csv_bytes = report_df.to_csv(
    index=False
).encode("utf-8-sig")

col1, col2 = st.columns(2)

with col1:
    st.download_button(
        label="Download Job Analysis (CSV)",
        data=csv_bytes,
        file_name="resume_analysis.csv",
        mime="text/csv",
        use_container_width=True,
    )

with col2:
    report_text = (
        "AI Resume Analyzer - Educational Report\n\n"
        f"File analyzed: {uploaded_file.name}\n"
        f"Detected skills: {', '.join(detected_skills)}\n\n"
        + report_df.to_string(index=False)
        + "\n\nScores are estimates, not hiring decisions."
    )

    st.download_button(
        label="Download Text Report",
        data=report_text.encode("utf-8"),
        file_name="resume_analysis.txt",
        mime="text/plain",
        use_container_width=True,
    )


# ---------------- FOOTER ----------------

st.divider()

st.caption(
    "Privacy: this application does not intentionally save uploaded "
    "resumes to a database. Uploaded files are processed by the application. "
    "Avoid uploading sensitive personal information to untrusted deployments."
)
