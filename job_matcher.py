
from pathlib import Path
import re

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Locate the dataset relative to this Python file.
BASE_DIR = Path(__file__).resolve().parent
JOB_ROLES_FILE = BASE_DIR / "data" / "job_roles.csv"


def load_job_roles():
    """Load and validate job roles from the CSV file."""

    if not JOB_ROLES_FILE.exists():
        raise FileNotFoundError(
            f"Job roles dataset not found: {JOB_ROLES_FILE}"
        )

    jobs = pd.read_csv(JOB_ROLES_FILE)
    jobs.columns = jobs.columns.str.strip()

    # The CSV uses 'job_role', not 'role'.
    if "job_role" not in jobs.columns:
        raise ValueError(
            "job_roles.csv must contain a 'job_role' column."
        )

    required_columns = ["required_skills", "description"]

    for column in required_columns:
        if column not in jobs.columns:
            raise ValueError(
                f"job_roles.csv is missing the '{column}' column."
            )

    jobs = jobs.dropna(subset=["job_role"]).copy()

    jobs["job_role"] = jobs["job_role"].astype(str).str.strip()
    jobs["required_skills"] = jobs["required_skills"].fillna("").astype(str)
    jobs["description"] = jobs["description"].fillna("").astype(str)

    jobs = jobs[jobs["job_role"] != ""]

    if jobs.empty:
        raise ValueError("No valid job roles were found in job_roles.csv.")

    return jobs


def skill_is_present(skill, resume_text):
    """Check whether a skill appears in the resume text."""

    skill = str(skill).strip().lower()
    resume_text = str(resume_text).lower()

    if not skill:
        return False

    # Match the skill as a phrase rather than part of a longer word.
    pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"

    return re.search(pattern, resume_text) is not None


def analyze_resume(resume_text):
    """Compare a resume against every job role and rank the results."""

    if not isinstance(resume_text, str) or not resume_text.strip():
        raise ValueError("Resume text is empty.")

    jobs = load_job_roles()
    resume_text = resume_text.strip()

    # Store the skills required for each role.
    all_required_skills = []
    role_documents = []

    for _, job in jobs.iterrows():
        skills = [
            skill.strip().lower()
            for skill in job["required_skills"].split(",")
            if skill.strip()
        ]

        all_required_skills.append(skills)

        # Combine role name, required skills and description for comparison.
        role_document = " ".join(
            [
                str(job["job_role"]),
                " ".join(skills),
                str(job["description"]),
            ]
        )

        role_documents.append(role_document)

    # Calculate TF-IDF similarity between the resume and each job role.
    documents = [resume_text] + role_documents

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
    )

    try:
        tfidf_matrix = vectorizer.fit_transform(documents)

        similarities = cosine_similarity(
            tfidf_matrix[0:1],
            tfidf_matrix[1:],
        ).flatten()

    except ValueError:
        # Handle text that contains no usable TF-IDF features.
        similarities = [0.0] * len(jobs)

    results = []

    for index, (_, job) in enumerate(jobs.iterrows()):
        required_skills = all_required_skills[index]

        matched_skills = [
            skill
            for skill in required_skills
            if skill_is_present(skill, resume_text)
        ]

        missing_skills = [
            skill
            for skill in required_skills
            if skill not in matched_skills
        ]

        # Required-skill coverage score.
        if required_skills:
            skill_score = (
                len(matched_skills) / len(required_skills)
            ) * 100
        else:
            skill_score = 0.0

        # Convert cosine similarity into a percentage.
        tfidf_score = float(similarities[index]) * 100

        # Combined score: 70% skill coverage + 30% text similarity.
        match_score = (
            0.70 * skill_score
            + 0.30 * tfidf_score
        )

        results.append(
            {
                # 'role' is the output name expected by app.py.
                "role": job["job_role"],
                "description": job["description"],
                "skill_score": round(skill_score, 2),
                "tfidf_score": round(tfidf_score, 2),
                "match_score": round(match_score, 2),
                "matched_skills": matched_skills,
                "missing_skills": missing_skills,
            }
        )

    results_df = pd.DataFrame(results)

    # Show the best matching role first.
    results_df = results_df.sort_values(
        by="match_score",
        ascending=False,
    ).reset_index(drop=True)

    return results_df
