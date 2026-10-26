
import csv
import sys
import unittest
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_DIR))


class TestProjectFiles(unittest.TestCase):

    def test_job_roles_file_exists(self):
        file_path = PROJECT_DIR / "data" / "job_roles.csv"
        self.assertTrue(file_path.exists())

    def test_skill_dictionary_file_exists(self):
        file_path = PROJECT_DIR / "data" / "skill_dictionary.csv"
        self.assertTrue(file_path.exists())

    def test_job_roles_columns(self):
        file_path = PROJECT_DIR / "data" / "job_roles.csv"

        with open(file_path, encoding="utf-8", newline="") as file:
            reader = csv.DictReader(file)
            self.assertEqual(
                reader.fieldnames,
                ["job_role", "required_skills", "description"]
            )
            rows = list(reader)

        self.assertGreaterEqual(len(rows), 5)

    def test_skill_dictionary_columns(self):
        file_path = PROJECT_DIR / "data" / "skill_dictionary.csv"

        with open(file_path, encoding="utf-8", newline="") as file:
            reader = csv.DictReader(file)
            self.assertEqual(
                reader.fieldnames,
                ["skill", "category"]
            )
            rows = list(reader)

        self.assertGreaterEqual(len(rows), 20)

    def test_job_roles_have_no_empty_values(self):
        file_path = PROJECT_DIR / "data" / "job_roles.csv"

        with open(file_path, encoding="utf-8", newline="") as file:
            rows = list(csv.DictReader(file))

        for row in rows:
            self.assertTrue(row["job_role"].strip())
            self.assertTrue(row["required_skills"].strip())
            self.assertTrue(row["description"].strip())

    def test_skills_have_no_empty_values(self):
        file_path = PROJECT_DIR / "data" / "skill_dictionary.csv"

        with open(file_path, encoding="utf-8", newline="") as file:
            rows = list(csv.DictReader(file))

        for row in rows:
            self.assertTrue(row["skill"].strip())
            self.assertTrue(row["category"].strip())

    def test_job_roles_are_unique(self):
        file_path = PROJECT_DIR / "data" / "job_roles.csv"

        with open(file_path, encoding="utf-8", newline="") as file:
            rows = list(csv.DictReader(file))

        role_names = [row["job_role"].strip().lower() for row in rows]
        self.assertEqual(len(role_names), len(set(role_names)))

    def test_skills_are_unique(self):
        file_path = PROJECT_DIR / "data" / "skill_dictionary.csv"

        with open(file_path, encoding="utf-8", newline="") as file:
            rows = list(csv.DictReader(file))

        skill_names = [row["skill"].strip().lower() for row in rows]
        self.assertEqual(len(skill_names), len(set(skill_names)))


if __name__ == "__main__":
    unittest.main()
