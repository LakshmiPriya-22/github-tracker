# main.py

from student_manager import load_students, get_github_username
from github_api import get_student_summary, get_user_profile
from pdf_generator import generate_pdf

def main():
    students = load_students()

    user_input = input("Enter RegdNo or GitHub username: ").strip()
    username = get_github_username(user_input, students)

    print(f"Fetching data for {username}...")

    # Fetch summary + repos
    summary, repo_rows = get_student_summary(username)

    # Get student's GitHub name
    profile = get_user_profile(username)
    student_name = None
    if profile:
        student_name = profile.get("name") or profile.get("login")

    # Regd no available only when input is regd
    regd = user_input if user_input in students else "-"

    # Generate PDF
    pdf_file = generate_pdf(student_name, regd, username, summary, repo_rows)
    print("PDF generated:", pdf_file)

if __name__ == "__main__":
    main()
