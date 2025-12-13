# github_api.py

from utils import request_json, extract_last_page
from config import GITHUB_API

def get_user_profile(username):
    url = f"{GITHUB_API}/users/{username}" #make a link where github keeps user info
    data, _ = request_json(url) #ask github for the user's info
    return data if isinstance(data, dict) else None


def get_user_repos(username):
    repos = []
    page = 1
    per_page = 100

    while True:
        url = f"{GITHUB_API}/users/{username}/repos"
        params = {"per_page": per_page, "page": page, "type": "owner"}

        data, _ = request_json(url, params=params)
        if not isinstance(data, list):
            break

        repos.extend(data)
        if len(data) < per_page: #if git hub send fewer than 100 repos it means no more pages
            break
        page += 1 #otherwise go to next page

    return repos


def get_commit_details(username, repo_name, branch):
    """
    Efficient commit counting using per_page=1 + Link header.
    """
    url = f"{GITHUB_API}/repos/{username}/{repo_name}/commits"
    params = {"per_page": 1, "sha": branch} # ask github 1 commit per page

    data, resp = request_json(url, params=params)
    if resp is None:
        return 0, None

    # Last commit date
    last_commit_date = None
    if isinstance(data, list) and data:
        try:
            last_commit_date = data[0]["commit"]["author"]["date"]
        except:
            last_commit_date = None

    # Check Link header for total pages
    link = resp.headers.get("Link")
    last_page = extract_last_page(link)

    if last_page:
        return last_page, last_commit_date

    # Fallback: count commits if small repo (per_page=100)
    params_100 = {"per_page": 100}
    data2, _ = request_json(url, params_100)

    if isinstance(data2, list):
        return len(data2), last_commit_date

    return 0, last_commit_date


def get_student_summary(username):
    repos = get_user_repos(username)
    repo_rows = []
    total_commits = 0
    last_active = None

    for repo in repos:
        name = repo.get("name")
        branch = repo.get("default_branch")

        commits, last_commit = get_commit_details(username, name, branch)
        total_commits += commits

        if last_commit and (not last_active or last_commit > last_active):
            last_active = last_commit

        repo_rows.append((name, commits, last_commit))

    summary = {
        "total_repos": len(repos),
        "total_commits": total_commits,
        "last_active": last_active,
        "note": "Commit counts might be approximate due to GitHub API pagination."
    }

    return summary, repo_rows
