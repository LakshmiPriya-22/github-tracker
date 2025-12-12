# config.py

import os

# GitHub API endpoint
GITHUB_API = "https://api.github.com"

# Load GitHub Personal Access Token (optional but recommended)
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# Common headers
HEADERS = {
    "Accept": "application/vnd.github.v3+json"
}

if GITHUB_TOKEN:
    HEADERS["Authorization"] = f"token {GITHUB_TOKEN}"
