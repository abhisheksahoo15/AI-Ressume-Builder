from fastapi.testclient import TestClient

from main import app
from resume_agent import NOT_FOUND, analyze_resume


SAMPLE_RESUME = """
Abhishek Sahoo
abhishek@example.com
+91 9876543210
https://www.linkedin.com/in/abhishek-sahoo
https://github.com/abhisheksahoo15

Education
Master of Computer Applications, Cambridge Institute of Technology

Skills
Python, FastAPI, React, SQL, Docker, AWS, Machine Learning, GitHub Actions

Projects
HireFire AI Resume Builder - Built a FastAPI resume analyzer using Python and Machine Learning.

Experience
Software Engineer Intern - Worked on Docker, CI/CD pipelines, and FastAPI microservices.

Certifications
AWS Cloud Practitioner

Achievements
Final year project selected for department demo.
"""

SAMPLE_JD = """
We are hiring an AI Engineer with Python, FastAPI, AWS, Docker, SQL, Machine Learning,
REST API experience, prompt engineering, and strong communication skills.
"""


def test_resume_agent_extracts_resume_information():
    analysis = analyze_resume(SAMPLE_RESUME, SAMPLE_JD, "AI Engineer")
    extracted = analysis["extracted_information"]

    assert extracted["Name"] == "Abhishek Sahoo"
    assert extracted["Email"] == "abhishek@example.com"
    assert extracted["Phone"] != NOT_FOUND
    assert extracted["LinkedIn"] != NOT_FOUND
    assert "Python" in extracted["Skills"]
    assert "FastAPI" in extracted["Skills"]
    assert analysis["ats_score"]["overall"] > 0
    assert "ResumePilot AI Agent Analysis" in analysis["analysis_markdown"]
    assert "Concise Action Plan" in analysis["analysis_markdown"]


def test_resume_agent_marks_missing_information_as_not_found():
    analysis = analyze_resume("", SAMPLE_JD, "Data Analyst")
    extracted = analysis["extracted_information"]

    assert extracted["Name"] == NOT_FOUND
    assert extracted["Email"] == NOT_FOUND
    assert analysis["ats_score"]["overall"] == 0
    assert "Not Found" in analysis["analysis_markdown"]


def test_resume_agent_api_returns_markdown_report():
    client = TestClient(app)
    response = client.post(
        "/resume-agent/analyze/",
        data={
            "resume_text": SAMPLE_RESUME,
            "job_description": SAMPLE_JD,
            "career_goal": "AI Engineer",
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "success"
    assert payload["analysis"]["ats_score"]["overall"] > 0
    assert "# ResumePilot AI Agent Analysis" in payload["analysis_markdown"]
