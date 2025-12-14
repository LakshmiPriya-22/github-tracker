# pdf_generator.py

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from utils import format_iso

def generate_pdf(student_name, regd, username, summary, repo_rows):
    filename = f"{username}_report.pdf"

    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Title
    story.append(Paragraph("GitHub Activity Report", styles["Title"]))
    story.append(Spacer(1, 12))

    # Student Info
    info = f"""
    <b>Student:</b> {student_name or '-'}<br/>
    <b>RegdNo:</b> {regd}<br/>
    <b>GitHub:</b> {username}<br/>
    <b>Total Repos:</b> {summary['total_repos']}<br/>
    <b>Total Commits:</b> {summary['total_commits']}<br/>
    <b>Last Active:</b> {format_iso(summary['last_active'])}<br/>
    """
    story.append(Paragraph(info, styles["Normal"]))
    story.append(Spacer(1, 12))

    # Repo Table
    table_data = [["Repository", "Commits", "Last Commit"]]
    for name, commits, last_commit in repo_rows:
        table_data.append([
            name,
            str(commits),
            format_iso(last_commit)
        ])

    table = Table(table_data, repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.lightgrey),
        ("GRID", (0,0), (-1,-1), 0.4, colors.black),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
    ]))

    story.append(table)
    story.append(Spacer(1, 12))

    doc.build(story)
    return filename
