# student_manager.py

import json

def load_students(path="students.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def get_github_username(regd_or_username, student_data):
    """
    If input matches regd no → return mapped GitHub username
    Otherwise treat input as a direct GitHub username
    """
    return student_data.get(regd_or_username, regd_or_username)
