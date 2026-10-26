
import re
from pathlib import Path

import pandas as pd

from text_cleaner import clean_text


DATA_FILE = Path(__file__).parent / "data" / "skill_dictionary.csv"


def load_skill_dictionary() -> pd.DataFrame:
    """Load the project's controlled skill vocabulary."""
    return pd.read_csv(DATA_FILE).fillna("")


def contains_skill(text: str, skill: str) -> bool:
    """Match a skill without accidentally matching it inside another word."""
    normalized_text = clean_text(text)
    normalized_skill = clean_text(skill)

    pattern = (
        r"(?<![a-z0-9])"
        + re.escape(normalized_skill)
        + r"(?![a-z0-9])"
    )

    return re.search(pattern, normalized_text) is not None


def extract_skills(text: str) -> list[str]:
    """Return skills detected in the resume."""
    dictionary = load_skill_dictionary()
    found = []

    for skill in dictionary["skill"].tolist():
        if skill and contains_skill(text, skill):
            found.append(skill)

    return sorted(set(found), key=str.lower)


def extract_skills_by_category(text: str) -> dict[str, list[str]]:
    """Group detected skills by category."""
    dictionary = load_skill_dictionary()
    results = {}

    for _, row in dictionary.iterrows():
        skill = row["skill"]
        category = row["category"]

        if skill and contains_skill(text, skill):
            results.setdefault(category, []).append(skill)

    return results
