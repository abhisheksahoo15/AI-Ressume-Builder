from __future__ import annotations

import io
import re
import zipfile
from collections import Counter
from typing import Any
from xml.etree import ElementTree


NOT_FOUND = "Not Found"

SECTION_ALIASES = {
    "summary": ["summary", "professional summary", "career summary", "profile", "objective"],
    "education": ["education", "academic details", "academics", "qualification", "qualifications"],
    "skills": ["skills", "technical skills", "core skills", "key skills", "technologies"],
    "projects": ["projects", "academic projects", "personal projects", "project experience"],
    "experience": ["experience", "work experience", "professional experience", "employment", "internship", "internships"],
    "certifications": ["certifications", "certificates", "licenses"],
    "achievements": ["achievements", "awards", "honors", "accomplishments"],
}

STOPWORDS = {
    "the", "and", "for", "with", "that", "this", "from", "your", "you", "are", "will", "have",
    "has", "our", "their", "they", "was", "were", "been", "being", "into", "about", "over",
    "under", "using", "use", "used", "work", "worked", "role", "candidate", "team", "teams",
    "job", "description", "responsibilities", "requirements", "required", "preferred", "ability",
    "skills", "experience", "years", "year", "strong", "good", "must", "should", "plus", "such",
    "etc", "who", "what", "when", "where", "why", "how", "can", "may", "within", "across",
    "including", "based", "knowledge", "understanding", "building", "build", "develop", "developed",
}

SKILL_CATALOG = {
    "Programming Languages": [
        "Python", "Java", "JavaScript", "TypeScript", "C++", "C#", "C", "Go", "Rust", "SQL", "R",
        "Scala", "Bash", "Shell", "HTML", "CSS",
    ],
    "Frameworks": [
        "React", "Next.js", "Node.js", "Express", "Django", "FastAPI", "Flask", "Spring Boot",
        "Angular", "Vue", "Tailwind", "Bootstrap", "REST API", "GraphQL",
    ],
    "Cloud": [
        "AWS", "Azure", "GCP", "Google Cloud", "EC2", "S3", "Lambda", "Cloud Run", "App Service",
        "Cloud Functions",
    ],
    "Databases": [
        "MySQL", "PostgreSQL", "MongoDB", "Redis", "SQLite", "Oracle", "Snowflake", "BigQuery",
        "DynamoDB", "Firebase",
    ],
    "DevOps": [
        "Docker", "Kubernetes", "Git", "GitHub", "GitHub Actions", "Jenkins", "CI/CD", "Terraform",
        "Ansible", "Linux", "Nginx", "Prometheus", "Grafana",
    ],
    "Machine Learning": [
        "Machine Learning", "Deep Learning", "Scikit-learn", "TensorFlow", "PyTorch", "Pandas",
        "NumPy", "Matplotlib", "Seaborn", "Statistics", "NLP", "Computer Vision", "Power BI",
        "Tableau", "Excel",
    ],
    "Generative AI": [
        "Generative AI", "LLM", "RAG", "Prompt Engineering", "LangChain", "LlamaIndex",
        "Vector Database", "Embeddings", "OpenAI API", "Agents", "Fine-tuning",
    ],
}

SOFT_SKILLS = [
    "Communication", "Leadership", "Collaboration", "Teamwork", "Problem Solving", "Ownership",
    "Mentoring", "Agile", "Scrum", "Stakeholder Management", "Analytical Thinking",
]

ROLE_PROFILES = {
    "Software Engineer": [
        "Python", "Java", "JavaScript", "TypeScript", "Data Structures", "Algorithms", "REST API",
        "Git", "SQL", "Testing", "System Design", "OOP",
    ],
    "Data Scientist": [
        "Python", "SQL", "Statistics", "Pandas", "NumPy", "Scikit-learn", "Machine Learning",
        "Data Visualization", "Tableau", "Power BI", "Experimentation",
    ],
    "AI Engineer": [
        "Python", "Machine Learning", "Deep Learning", "LLM", "RAG", "Prompt Engineering",
        "LangChain", "Vector Database", "OpenAI API", "Embeddings", "API",
    ],
    "ML Engineer": [
        "Python", "Machine Learning", "Scikit-learn", "TensorFlow", "PyTorch", "Docker",
        "Kubernetes", "MLOps", "Model Deployment", "CI/CD", "AWS",
    ],
    "Full Stack Developer": [
        "HTML", "CSS", "JavaScript", "TypeScript", "React", "Node.js", "Express", "REST API",
        "SQL", "MongoDB", "Git", "Deployment",
    ],
    "DevOps Engineer": [
        "Linux", "Docker", "Kubernetes", "CI/CD", "Jenkins", "GitHub Actions", "Terraform",
        "AWS", "Azure", "Monitoring", "Nginx",
    ],
    "Cloud Engineer": [
        "AWS", "Azure", "GCP", "EC2", "S3", "Lambda", "Docker", "Kubernetes", "Terraform",
        "Networking", "Linux", "Security",
    ],
    "Data Analyst": [
        "SQL", "Excel", "Power BI", "Tableau", "Python", "Pandas", "Statistics",
        "Data Visualization", "Dashboard", "Reporting", "Business Intelligence",
    ],
}

STRONG_VERBS = [
    "built", "developed", "implemented", "designed", "deployed", "optimized", "automated",
    "created", "led", "improved", "delivered", "integrated", "analyzed", "engineered",
    "launched", "reduced", "increased", "streamlined", "architected",
]

WEAK_VERBS = [
    "worked", "helped", "assisted", "made", "did", "handled", "responsible", "participated",
    "involved", "managed things", "used",
]

GENERIC_PHRASES = [
    "hard working", "team player", "quick learner", "fast learner", "good communication",
    "responsible for", "worked on", "basic knowledge", "self motivated",
]


def analyze_resume(resume_text: str = "", job_description: str = "", career_goal: str = "") -> dict[str, Any]:
    """Return a deterministic ResumePilot analysis without inventing candidate facts."""
    resume_text = clean_text(resume_text)
    job_description = clean_text(job_description)
    career_goal = career_goal.strip()

    sections = extract_sections(resume_text)
    extracted = extract_resume_information(resume_text, sections)
    ats = calculate_ats_breakdown(resume_text, job_description, extracted, sections)
    problems = detect_resume_problems(resume_text, job_description, extracted, sections)
    role_fit = estimate_role_fit(resume_text, extracted, sections)
    best_role = max(role_fit, key=role_fit.get) if role_fit else NOT_FOUND
    target_role = career_goal or best_role or NOT_FOUND
    job_match = compare_with_job(resume_text, job_description, extracted, ats["overall"])
    improvements = build_improvements(extracted, sections, target_role, job_match)
    missing_skills = suggest_missing_skills(extracted, target_role, job_description)
    interview_prep = generate_interview_prep(extracted, target_role, job_description)
    cover_letter = generate_cover_letter(extracted, target_role, job_description)
    roadmap = generate_roadmap(target_role, missing_skills, problems)
    action_plan = build_action_plan(problems, missing_skills, job_match)

    analysis = {
        "extracted_information": extracted,
        "ats_score": ats,
        "problems": problems,
        "role_fit": role_fit,
        "improvements": improvements,
        "missing_skills": missing_skills,
        "job_match": job_match,
        "interview_preparation": interview_prep,
        "cover_letter": cover_letter,
        "roadmap": roadmap,
        "action_plan": action_plan,
    }
    analysis["analysis_markdown"] = to_markdown(analysis, target_role)
    return analysis


def extract_text_from_upload_bytes(raw: bytes, filename: str = "") -> str:
    """Best-effort text extraction using only the standard library."""
    if not raw:
        return ""

    suffix = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    if suffix in {"txt", "md", "csv", "rtf"}:
        return decode_bytes(raw)

    if suffix == "docx":
        return extract_docx_text(raw)

    if suffix == "pdf":
        return extract_pdf_text_best_effort(raw)

    return decode_bytes(raw)


def clean_text(text: str) -> str:
    text = text or ""
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[\t\f\v]+", " ", text)
    text = re.sub(r" +", " ", text)
    return text.strip()


def get_lines(text: str) -> list[str]:
    return [line.strip(" -*\u2022") for line in text.split("\n") if line.strip()]


def normalize_heading(line: str) -> str:
    return re.sub(r"[^a-zA-Z /&-]", "", line).strip().lower()


def detect_heading(line: str) -> str | None:
    normalized = normalize_heading(line)
    if not normalized or len(normalized) > 45:
        return None

    for key, aliases in SECTION_ALIASES.items():
        if normalized in aliases:
            return key
    return None


def extract_sections(text: str) -> dict[str, list[str]]:
    sections = {key: [] for key in SECTION_ALIASES}
    current: str | None = None

    for raw_line in text.split("\n"):
        line = raw_line.strip()
        if not line:
            continue

        key = None
        tail = ""
        if ":" in line:
            head, possible_tail = line.split(":", 1)
            key = detect_heading(head)
            tail = possible_tail.strip()
        else:
            key = detect_heading(line)

        if key:
            current = key
            if tail:
                sections[key].append(tail)
            continue

        if current:
            sections[current].append(line)

    return sections


def extract_resume_information(text: str, sections: dict[str, list[str]]) -> dict[str, Any]:
    lines = get_lines(text)
    email = first_or_not_found(re.findall(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", text, re.I))
    phone = first_or_not_found(re.findall(r"(?:\+?\d[\d\s().-]{7,}\d)", text))
    linkedin = first_or_not_found(re.findall(r"(?:https?://)?(?:www\.)?linkedin\.com/[^\s,)]+", text, re.I))
    github = first_or_not_found(re.findall(r"(?:https?://)?(?:www\.)?github\.com/[^\s,)]+", text, re.I))
    urls = re.findall(r"(?:https?://|www\.)[^\s,)]+", text, re.I)
    portfolio_urls = [
        url for url in urls
        if "linkedin.com" not in url.lower() and "github.com" not in url.lower()
    ]

    skills_by_category = extract_skills_by_category(text)
    skills = [skill for values in skills_by_category.values() for skill in values]

    education = section_or_inferred(
        sections.get("education", []),
        infer_lines(lines, ["b.tech", "bachelor", "master", "mca", "bca", "degree", "university", "college", "institute", "cgpa"]),
    )
    projects = section_or_not_found(sections.get("projects", []))
    experience = section_or_not_found(sections.get("experience", []))
    certifications = section_or_not_found(sections.get("certifications", []))
    achievements = section_or_not_found(sections.get("achievements", []))

    return {
        "Name": extract_name(lines),
        "Email": email,
        "Phone": phone.strip() if phone != NOT_FOUND else NOT_FOUND,
        "LinkedIn": linkedin,
        "GitHub": github,
        "Portfolio": portfolio_urls if portfolio_urls else NOT_FOUND,
        "Education": education,
        "Skills": skills if skills else NOT_FOUND,
        "Skills By Category": skills_by_category,
        "Projects": projects,
        "Experience": experience,
        "Certifications": certifications,
        "Achievements": achievements,
    }


def extract_name(lines: list[str]) -> str:
    heading_words = {alias for aliases in SECTION_ALIASES.values() for alias in aliases}
    for line in lines[:8]:
        lowered = line.lower()
        if any(token in lowered for token in ["@", "linkedin", "github", "http", "www."]):
            continue
        if normalize_heading(line) in heading_words:
            continue
        if re.search(r"\d", line):
            continue
        words = line.split()
        if 1 < len(words) <= 5 and re.fullmatch(r"[A-Za-z][A-Za-z .'-]{1,80}", line):
            return line.title() if line.isupper() else line
    return NOT_FOUND


def section_or_not_found(lines: list[str]) -> list[str] | str:
    cleaned = [line.strip() for line in lines if line.strip()]
    return cleaned if cleaned else NOT_FOUND


def section_or_inferred(section_lines: list[str], inferred: list[str]) -> list[str] | str:
    cleaned = [line.strip() for line in section_lines if line.strip()]
    if cleaned:
        return cleaned
    return inferred if inferred else NOT_FOUND


def infer_lines(lines: list[str], keywords: list[str]) -> list[str]:
    found = []
    for line in lines:
        lowered = line.lower()
        if any(keyword in lowered for keyword in keywords):
            found.append(line)
    return found[:6]


def first_or_not_found(values: list[str]) -> str:
    return values[0].strip() if values else NOT_FOUND


def extract_skills_by_category(text: str) -> dict[str, list[str]]:
    lower = text.lower()
    compact = compact_text(lower)
    found: dict[str, list[str]] = {}

    for category, skills in SKILL_CATALOG.items():
        category_found = []
        for skill in skills:
            if phrase_exists(skill, lower, compact):
                category_found.append(skill)
        if category_found:
            found[category] = category_found

    soft_found = [skill for skill in SOFT_SKILLS if phrase_exists(skill, lower, compact)]
    if soft_found:
        found["Soft Skills"] = soft_found

    return found


def phrase_exists(phrase: str, lower_text: str, compact: str | None = None) -> bool:
    phrase_lower = phrase.lower()
    compact = compact if compact is not None else compact_text(lower_text)

    if re.search(r"[^a-z0-9 ]", phrase_lower):
        return phrase_lower in lower_text or compact_text(phrase_lower) in compact

    return re.search(rf"\b{re.escape(phrase_lower)}\b", lower_text) is not None


def compact_text(text: str) -> str:
    return re.sub(r"[^a-z0-9+#]+", "", text.lower())


def extract_keywords(text: str) -> set[str]:
    lower = text.lower()
    words = re.findall(r"[a-z][a-z0-9+#.-]{2,}", lower)
    keywords = {word.strip(".-") for word in words if word not in STOPWORDS and len(word.strip(".-")) >= 3}
    for values in SKILL_CATALOG.values():
        for skill in values:
            if phrase_exists(skill, lower):
                keywords.add(skill.lower())
    return keywords


def calculate_ats_breakdown(
    resume_text: str,
    job_description: str,
    extracted: dict[str, Any],
    sections: dict[str, list[str]],
) -> dict[str, Any]:
    if not resume_text:
        return {
            "overall": 0,
            "breakdown": {
                "Formatting": {"score": 0, "why": "Resume text was not available for analysis."},
                "Keywords": {"score": 0, "why": "Resume text was not available for keyword comparison."},
                "Technical Skills": {"score": 0, "why": "No technical skills could be extracted."},
                "Soft Skills": {"score": 0, "why": "No soft skills could be extracted."},
                "Experience": {"score": 0, "why": "Experience section was not found."},
                "Education": {"score": 0, "why": "Education section was not found."},
                "Readability": {"score": 0, "why": "Resume text was not available for readability checks."},
                "Project Quality": {"score": 0, "why": "Project section was not found."},
            },
        }

    lines = get_lines(resume_text)
    available_sections = [key for key, value in sections.items() if value]
    contact_count = sum(1 for key in ["Email", "Phone", "LinkedIn", "GitHub"] if extracted.get(key) != NOT_FOUND)
    bullet_like = sum(1 for line in resume_text.splitlines() if line.strip().startswith(("-", "*", "\u2022")))
    long_lines = [line for line in lines if len(line) > 160]
    paragraphs = [part for part in re.split(r"\n\s*\n", resume_text) if len(part.split()) > 80]
    quantified_count = len(re.findall(r"\b\d+(?:\.\d+)?%?|\b\d+x\b", resume_text.lower()))

    formatting_score = clamp(
        25 + len(available_sections) * 8 + contact_count * 5 + min(bullet_like, 6) * 2 - len(long_lines) * 4,
        0,
        100,
    )

    if job_description:
        resume_keywords = extract_keywords(resume_text)
        job_keywords = extract_keywords(job_description)
        overlap = resume_keywords & job_keywords
        keyword_score = int((len(overlap) / max(len(job_keywords), 1)) * 100)
        keyword_why = f"{len(overlap)} of {len(job_keywords)} important job-description keywords were found."
    else:
        keyword_score = 55 if extracted.get("Skills") != NOT_FOUND else 20
        keyword_why = "No job description was provided, so keyword strength is estimated from resume content only."

    technical_skills = [
        skill
        for category, values in extracted.get("Skills By Category", {}).items()
        if category != "Soft Skills"
        for skill in values
    ]
    soft_skills = extracted.get("Skills By Category", {}).get("Soft Skills", [])
    project_lines = safe_list(extracted.get("Projects"))
    experience_lines = safe_list(extracted.get("Experience"))

    technical_score = clamp(len(technical_skills) * 9, 15 if technical_skills else 0, 100)
    soft_score = clamp(len(soft_skills) * 18, 25 if soft_skills else 0, 100)
    experience_score = score_experience(experience_lines, quantified_count)
    education_score = 88 if extracted.get("Education") != NOT_FOUND else 15
    readability_score = clamp(90 - len(long_lines) * 8 - len(paragraphs) * 10, 10, 100)
    project_score = score_projects(project_lines, resume_text)

    breakdown = {
        "Formatting": {
            "score": formatting_score,
            "why": f"{len(available_sections)} resume sections and {contact_count} contact fields were detected.",
        },
        "Keywords": {"score": clamp(keyword_score, 0, 100), "why": keyword_why},
        "Technical Skills": {
            "score": technical_score,
            "why": f"{len(technical_skills)} technical skills were detected.",
        },
        "Soft Skills": {"score": soft_score, "why": f"{len(soft_skills)} soft skills were detected."},
        "Experience": {
            "score": experience_score,
            "why": "Experience is stronger when bullets start with action verbs and include measurable outcomes.",
        },
        "Education": {
            "score": education_score,
            "why": "Education is present and readable." if education_score > 50 else "Education section was not found.",
        },
        "Readability": {
            "score": readability_score,
            "why": "Short lines and bullet-style content are easier for ATS parsing and recruiter scanning.",
        },
        "Project Quality": {
            "score": project_score,
            "why": "Projects score higher when they name the problem, tech stack, action taken, and measurable result.",
        },
    }

    weights = {
        "Formatting": 0.13,
        "Keywords": 0.22,
        "Technical Skills": 0.15,
        "Soft Skills": 0.07,
        "Experience": 0.15,
        "Education": 0.10,
        "Readability": 0.10,
        "Project Quality": 0.08,
    }
    overall = int(sum(breakdown[key]["score"] * weight for key, weight in weights.items()))
    return {"overall": clamp(overall, 0, 100), "breakdown": breakdown}


def score_experience(lines: list[str], quantified_count: int) -> int:
    if not lines:
        return 20
    strong = sum(1 for line in lines if starts_with_any(line, STRONG_VERBS))
    weak = sum(1 for line in lines if any(verb in line.lower() for verb in WEAK_VERBS))
    score = 45 + strong * 12 + min(quantified_count, 5) * 5 - weak * 7
    return clamp(score, 0, 100)


def score_projects(lines: list[str], full_text: str) -> int:
    if not lines:
        return 20
    skills = extract_skills_by_category("\n".join(lines))
    skill_count = sum(len(values) for values in skills.values())
    action_count = sum(1 for line in lines if any(verb in line.lower() for verb in STRONG_VERBS))
    metric_count = len(re.findall(r"\b\d+(?:\.\d+)?%?|\b\d+x\b", "\n".join(lines).lower()))
    score = 35 + min(skill_count, 8) * 6 + action_count * 6 + min(metric_count, 4) * 5
    if "github" in full_text.lower():
        score += 8
    return clamp(score, 0, 100)


def starts_with_any(line: str, verbs: list[str]) -> bool:
    lowered = line.lower().strip(" -*\u2022")
    return any(lowered.startswith(verb) for verb in verbs)


def detect_resume_problems(
    resume_text: str,
    job_description: str,
    extracted: dict[str, Any],
    sections: dict[str, list[str]],
) -> dict[str, list[str]]:
    if not resume_text:
        return {
            "Missing sections": ["Resume text was not found, so all resume sections need review."],
            "Weak action verbs": [NOT_FOUND],
            "Grammar mistakes": [NOT_FOUND],
            "Repeated words": [NOT_FOUND],
            "Poor formatting": ["Resume text could not be parsed from the provided input."],
            "Missing keywords": safe_missing_keywords("", job_description),
            "Generic descriptions": [NOT_FOUND],
            "Long paragraphs": [NOT_FOUND],
            "Weak project explanations": [NOT_FOUND],
        }

    lower = resume_text.lower()
    missing_sections = []
    for section in ["summary", "education", "skills", "projects", "experience", "certifications", "achievements"]:
        if not sections.get(section) and section not in ["summary"]:
            extracted_name = section.capitalize()
            if extracted.get(extracted_name, NOT_FOUND) == NOT_FOUND:
                missing_sections.append(section.title())
        elif section == "summary" and not sections.get("summary"):
            missing_sections.append("Summary")

    weak_action_lines = [
        line for line in get_lines(resume_text)
        if any(verb in line.lower() for verb in WEAK_VERBS)
    ][:8]

    grammar = []
    if re.search(r"\bi\s", resume_text):
        grammar.append("Lowercase standalone 'i' found; capitalize it as 'I'.")
    if re.search(r" {2,}", resume_text):
        grammar.append("Multiple consecutive spaces found.")
    bullet_lines = [
        line.strip() for line in resume_text.splitlines()
        if line.strip().startswith(("-", "*", "\u2022"))
    ]
    lowercase_bullets = [line for line in bullet_lines if re.match(r"[-*\u2022]\s+[a-z]", line)]
    if lowercase_bullets:
        grammar.append("Some bullets start with lowercase letters.")

    repeated = detect_repeated_words(resume_text)
    formatting = []
    if not bullet_lines:
        formatting.append("No bullet-style lines detected; ATS and recruiters prefer short bullet points.")
    if any(len(line) > 160 for line in get_lines(resume_text)):
        formatting.append("Some lines are very long; split them into shorter bullets.")
    if extracted.get("Email") == NOT_FOUND or extracted.get("Phone") == NOT_FOUND:
        formatting.append("Email or phone number is missing from the parsed resume.")

    generic = [phrase for phrase in GENERIC_PHRASES if phrase in lower]
    long_paragraphs = [
        part.strip()[:120] + "..."
        for part in re.split(r"\n\s*\n", resume_text)
        if len(part.split()) > 80
    ][:5]

    project_lines = safe_list(extracted.get("Projects"))
    weak_projects = []
    for line in project_lines:
        has_metric = re.search(r"\b\d+(?:\.\d+)?%?|\b\d+x\b", line)
        has_stack = bool(extract_skills_by_category(line))
        if not has_metric or not has_stack:
            weak_projects.append(
                f"{line} | Why: add tech stack and measurable result so the project proves job-ready ability."
            )

    return {
        "Missing sections": missing_sections or [NOT_FOUND],
        "Weak action verbs": weak_action_lines or [NOT_FOUND],
        "Grammar mistakes": grammar or [NOT_FOUND],
        "Repeated words": repeated or [NOT_FOUND],
        "Poor formatting": formatting or [NOT_FOUND],
        "Missing keywords": safe_missing_keywords(resume_text, job_description),
        "Generic descriptions": generic or [NOT_FOUND],
        "Long paragraphs": long_paragraphs or [NOT_FOUND],
        "Weak project explanations": weak_projects or [NOT_FOUND],
    }


def detect_repeated_words(text: str) -> list[str]:
    repeated = re.findall(r"\b([a-zA-Z]{3,})\s+\1\b", text, re.I)
    high_frequency = [
        word for word, count in Counter(
            word.lower()
            for word in re.findall(r"\b[a-zA-Z]{4,}\b", text)
            if word.lower() not in STOPWORDS
        ).most_common(5)
        if count >= 8
    ]
    results = [f"Repeated adjacent word: {word}" for word in repeated[:5]]
    results.extend(f"Overused word: {word}" for word in high_frequency)
    return results


def safe_missing_keywords(resume_text: str, job_description: str) -> list[str]:
    if not job_description:
        return [NOT_FOUND]
    resume_keywords = extract_keywords(resume_text)
    job_keywords = extract_keywords(job_description)
    missing = sorted(job_keywords - resume_keywords)
    return missing[:20] if missing else [NOT_FOUND]


def estimate_role_fit(
    resume_text: str,
    extracted: dict[str, Any],
    sections: dict[str, list[str]],
) -> dict[str, int]:
    if not resume_text:
        return {role: 0 for role in ROLE_PROFILES}

    lower = resume_text.lower()
    compact = compact_text(lower)
    has_projects = extracted.get("Projects") != NOT_FOUND
    has_experience = extracted.get("Experience") != NOT_FOUND
    fits = {}

    for role, profile in ROLE_PROFILES.items():
        matched = [term for term in profile if phrase_exists(term, lower, compact)]
        score = int((len(matched) / len(profile)) * 78)
        if has_projects:
            score += 9
        if has_experience:
            score += 9
        if sections.get("skills"):
            score += 4
        fits[role] = clamp(score, 0, 100)
    return fits


def compare_with_job(
    resume_text: str,
    job_description: str,
    extracted: dict[str, Any],
    ats_score: int,
) -> dict[str, Any]:
    if not job_description:
        return {
            "Resume Match %": NOT_FOUND,
            "Missing Keywords": [NOT_FOUND],
            "Missing Skills": [NOT_FOUND],
            "Experience Gap": "Job description was not provided.",
            "ATS Prediction": NOT_FOUND,
            "Interview Probability": NOT_FOUND,
        }

    resume_keywords = extract_keywords(resume_text)
    job_keywords = extract_keywords(job_description)
    overlap = resume_keywords & job_keywords
    match = int((len(overlap) / max(len(job_keywords), 1)) * 100)

    job_skills_by_category = extract_skills_by_category(job_description)
    resume_skills = set(safe_list(extracted.get("Skills")))
    missing_skills = [
        skill
        for values in job_skills_by_category.values()
        for skill in values
        if skill not in resume_skills
    ]

    prediction = "High" if match >= 75 and ats_score >= 75 else "Medium" if match >= 50 else "Low"
    interview_probability = clamp(int(match * 0.55 + ats_score * 0.45), 0, 100)

    return {
        "Resume Match %": match,
        "Missing Keywords": safe_missing_keywords(resume_text, job_description),
        "Missing Skills": missing_skills[:20] if missing_skills else [NOT_FOUND],
        "Experience Gap": estimate_experience_gap(resume_text, job_description),
        "ATS Prediction": prediction,
        "Interview Probability": f"{interview_probability}%",
    }


def estimate_experience_gap(resume_text: str, job_description: str) -> str:
    jd_years = [int(num) for num in re.findall(r"(\d+)\+?\s*(?:years|yrs|year)", job_description.lower())]
    resume_years = [int(num) for num in re.findall(r"(\d+)\+?\s*(?:years|yrs|year)", resume_text.lower())]

    if not jd_years:
        return "Not Found in job description."

    required = max(jd_years)
    if not resume_years:
        return f"JD mentions {required}+ years, but resume years of experience were Not Found."

    candidate_years = max(resume_years)
    if candidate_years >= required:
        return f"No obvious gap detected: resume mentions {candidate_years}+ years against JD request of {required}+ years."

    return f"Potential gap: resume mentions {candidate_years}+ years while JD asks for {required}+ years."


def build_improvements(
    extracted: dict[str, Any],
    sections: dict[str, list[str]],
    target_role: str,
    job_match: dict[str, Any],
) -> dict[str, Any]:
    skills = safe_list(extracted.get("Skills"))
    skill_phrase = ", ".join(skills[:6]) if skills else "your strongest verified skills"
    target = target_role if target_role != NOT_FOUND else "the target role"

    if skills:
        summary = (
            f"{target} candidate with hands-on skills in {skill_phrase}. "
            "Add one sentence with your strongest project or internship outcome and a measurable result such as "
            "'improved accuracy by X%' or 'reduced deployment time by X%'."
        )
    else:
        summary = (
            f"{target} candidate. Add 5-8 verified technical skills, one strongest project, and one measurable outcome."
        )

    skill_groups = []
    for category, values in extracted.get("Skills By Category", {}).items():
        skill_groups.append(f"{category}: {', '.join(values)}")

    project_rewrites = []
    for project in safe_list(extracted.get("Projects")):
        project_rewrites.append(
            f"Built {project}; add the exact tech stack, your responsibility, and a metric such as users, accuracy, latency, or deployment impact. "
            "Why: project bullets need proof of scope, not only a project name."
        )

    experience_rewrites = []
    for experience in safe_list(extracted.get("Experience")):
        cleaned = re.sub(r"^(worked on|responsible for|helped with)\s+", "", experience, flags=re.I)
        experience_rewrites.append(
            f"Implemented {cleaned}; add a measurable result such as time saved, defects reduced, or process improved. "
            "Why: action-plus-impact bullets are stronger for recruiters and ATS scoring."
        )

    return {
        "Summary Rewrite": {
            "text": summary,
            "why": "A focused summary gives ATS systems target-role keywords and gives recruiters the candidate's value in the first scan.",
        },
        "Skills Rewrite": {
            "text": skill_groups if skill_groups else [NOT_FOUND],
            "why": "Grouped skills are easier for ATS parsing and help hiring managers quickly verify role fit.",
        },
        "Project Description Rewrites": project_rewrites or [NOT_FOUND],
        "Experience Bullet Rewrites": experience_rewrites or [NOT_FOUND],
        "Job Keyword Note": {
            "text": job_match.get("Missing Keywords", [NOT_FOUND]),
            "why": "Adding truthful missing JD keywords improves match rate only when the candidate can support them in interviews.",
        },
    }


def suggest_missing_skills(
    extracted: dict[str, Any],
    target_role: str,
    job_description: str,
) -> dict[str, dict[str, Any]]:
    current_skills = set(safe_list(extracted.get("Skills")))
    jd_skills = {
        skill
        for values in extract_skills_by_category(job_description).values()
        for skill in values
    } if job_description else set()

    target_terms = set()
    if target_role in ROLE_PROFILES:
        target_terms.update(ROLE_PROFILES[target_role])

    recommendations: dict[str, dict[str, Any]] = {}
    for category, skills in SKILL_CATALOG.items():
        priority = [
            skill for skill in skills
            if skill not in current_skills and (skill in jd_skills or skill in target_terms)
        ]
        if not priority:
            priority = [skill for skill in skills if skill not in current_skills][:3]
        recommendations[category] = {
            "skills": priority[:6] if priority else [NOT_FOUND],
            "why": (
                f"These skills support {target_role} expectations and/or appear in the job description."
                if target_role != NOT_FOUND
                else "Career goal was Not Found, so these are general employability skills for technical resumes."
            ),
        }
    return recommendations


def generate_interview_prep(
    extracted: dict[str, Any],
    target_role: str,
    job_description: str,
) -> dict[str, Any]:
    skills = safe_list(extracted.get("Skills"))
    projects = safe_list(extracted.get("Projects"))
    primary_skill = skills[0] if skills else "your primary programming language"
    target = target_role if target_role != NOT_FOUND else "the target role"

    top_20 = [
        f"Walk me through your resume for {target}.",
        "Which project best proves you are ready for this role?",
        f"Explain the strongest concept you know in {primary_skill}.",
        "How do you debug a production issue?",
        "How do you design a REST API for a real product workflow?",
        "What tradeoffs did you make in your most important project?",
        "How do you test your code before release?",
        "Explain authentication and authorization in a web application.",
        "How do you optimize a slow database query?",
        "What is the difference between horizontal and vertical scaling?",
        "How do you manage Git branches in a team?",
        "Describe one difficult technical problem you solved.",
        "How would you learn a missing skill from this job description?",
        "What metrics would you use to prove your project worked?",
        "Explain object-oriented programming with an example.",
        "How do you handle API failures or timeouts?",
        "What security risks do you check in a web app?",
        "How do you prioritize tasks when deadlines are tight?",
        "Why are you interested in this role?",
        "What would you improve in your resume project if given one more month?",
    ]

    coding = [
        "Solve two-sum and explain time complexity.",
        "Reverse a linked list iteratively and recursively.",
        "Find the first non-repeating character in a string.",
        "Design a simple rate limiter.",
        "Write SQL to find the second-highest salary or score.",
    ]
    behavioral = [
        "Tell me about a time you handled feedback.",
        "Tell me about a time you worked under pressure.",
        "Describe a conflict in a team and how you handled it.",
        "Tell me about a time you had to learn something quickly.",
        "Describe a failure and what you changed afterward.",
    ]
    project_specific = [
        f"Explain the architecture, tech stack, and result of: {project}"
        for project in projects[:5]
    ] or [NOT_FOUND]

    company_specific = [NOT_FOUND]
    if job_description:
        company_specific = [
            "Which requirements in this JD match your resume most strongly?",
            "Which JD requirement is your biggest gap, and how are you closing it?",
            "How would you contribute in the first 30 days based on this JD?",
        ]

    return {
        "Top 20 Interview Questions": top_20,
        "Coding Questions": coding,
        "Behavioral Questions": behavioral,
        "Project-Specific Questions": project_specific,
        "Company-Specific Questions": company_specific,
    }


def generate_cover_letter(
    extracted: dict[str, Any],
    target_role: str,
    job_description: str,
) -> str:
    if not job_description:
        return "Not Found: job description was not provided, so a personalized cover letter cannot be generated safely."

    name = extracted.get("Name", NOT_FOUND)
    skills = safe_list(extracted.get("Skills"))
    projects = safe_list(extracted.get("Projects"))
    target = target_role if target_role != NOT_FOUND else "the open role"
    skill_sentence = ", ".join(skills[:6]) if skills else "the verified skills listed in my resume"
    project_sentence = projects[0] if projects else "my strongest resume project"
    signature = name if name != NOT_FOUND else "[Your Name]"

    return (
        "Dear Hiring Manager,\n\n"
        f"I am applying for {target}. My resume shows hands-on alignment with this role through {skill_sentence}. "
        f"One relevant proof point is {project_sentence}; I would strengthen this further by adding measurable outcomes "
        "such as performance, accuracy, users, or deployment impact.\n\n"
        "I am interested in this opportunity because the job description matches the technical direction shown in my resume. "
        "I can contribute by learning quickly, communicating clearly, and turning project work into production-ready execution.\n\n"
        "Thank you for your time and consideration.\n\n"
        f"Sincerely,\n{signature}"
    )


def generate_roadmap(
    target_role: str,
    missing_skills: dict[str, dict[str, Any]],
    problems: dict[str, list[str]],
) -> list[dict[str, str]]:
    priority_skills = []
    for entry in missing_skills.values():
        for skill in entry.get("skills", []):
            if skill != NOT_FOUND and skill not in priority_skills:
                priority_skills.append(skill)
            if len(priority_skills) >= 6:
                break
        if len(priority_skills) >= 6:
            break

    target = target_role if target_role != NOT_FOUND else "your target role"
    skills_text = ", ".join(priority_skills[:4]) if priority_skills else "the most relevant missing role skills"

    return [
        {
            "period": "Days 1-7",
            "action": f"Rewrite summary, skills, projects, and experience bullets for {target}. Add missing contact/section details.",
            "why": "The resume must first become ATS-readable before applications can convert.",
        },
        {
            "period": "Days 8-14",
            "action": f"Build or upgrade one proof project using {skills_text}.",
            "why": "A focused project turns missing keywords into interview-ready evidence.",
        },
        {
            "period": "Days 15-21",
            "action": "Practice coding, SQL, and role-specific interview questions daily; document answers using STAR format.",
            "why": "Interview probability improves when resume claims can be defended clearly.",
        },
        {
            "period": "Days 22-30",
            "action": "Apply to targeted roles, tailor keywords for each JD, and track callbacks, rejections, and missing patterns.",
            "why": "A feedback loop reveals whether the resume, skills, or targeting strategy needs adjustment.",
        },
    ]


def build_action_plan(
    problems: dict[str, list[str]],
    missing_skills: dict[str, dict[str, Any]],
    job_match: dict[str, Any],
) -> list[str]:
    missing_sections = [item for item in problems.get("Missing sections", []) if item != NOT_FOUND]
    missing_keywords = [item for item in job_match.get("Missing Keywords", []) if item != NOT_FOUND]
    missing_skill_items = []
    for entry in missing_skills.values():
        for skill in entry.get("skills", []):
            if skill != NOT_FOUND and skill not in missing_skill_items:
                missing_skill_items.append(skill)

    return [
        f"Add or improve missing sections: {', '.join(missing_sections[:4]) if missing_sections else 'none detected'}.",
        f"Add truthful JD keywords: {', '.join(missing_keywords[:6]) if missing_keywords else 'none detected'}.",
        f"Build proof for priority skills: {', '.join(missing_skill_items[:5]) if missing_skill_items else 'none detected'}.",
        "Rewrite every weak bullet as Action + Tool/Skill + Measurable Result.",
        "Apply with a tailored resume version for each serious job description.",
    ]


def to_markdown(analysis: dict[str, Any], target_role: str) -> str:
    extracted = analysis["extracted_information"]
    ats = analysis["ats_score"]
    lines = [
        "# ResumePilot AI Agent Analysis",
        "",
        f"Target Role: {target_role if target_role else NOT_FOUND}",
        "",
        "## Step 1: Extracted Resume Information",
        "",
        "| Field | Result |",
        "| --- | --- |",
    ]

    for field in [
        "Name", "Email", "Phone", "LinkedIn", "GitHub", "Portfolio", "Education", "Skills",
        "Projects", "Experience", "Certifications", "Achievements",
    ]:
        lines.append(f"| {field} | {md_cell(extracted.get(field, NOT_FOUND))} |")

    lines.extend([
        "",
        "## Step 2: ATS Score",
        "",
        f"Overall ATS Score: {ats['overall']}/100",
        "",
        "| Category | Score | Why |",
        "| --- | ---: | --- |",
    ])
    for category, data in ats["breakdown"].items():
        lines.append(f"| {category} | {data['score']} | {md_cell(data['why'])} |")

    lines.extend(["", "## Step 3: Detected Problems", ""])
    for category, items in analysis["problems"].items():
        lines.append(f"### {category}")
        lines.extend(format_items(items))
        lines.append("")

    lines.extend([
        "## Step 4: Industry Role Fit",
        "",
        "| Role | Fit % |",
        "| --- | ---: |",
    ])
    for role, score in analysis["role_fit"].items():
        lines.append(f"| {role} | {score}% |")

    improvements = analysis["improvements"]
    lines.extend([
        "",
        "## Step 5: Improvements And Rewrites",
        "",
        "### Summary",
        f"- {improvements['Summary Rewrite']['text']}",
        f"- Why: {improvements['Summary Rewrite']['why']}",
        "",
        "### Skills",
    ])
    lines.extend(format_items(improvements["Skills Rewrite"]["text"]))
    lines.append(f"- Why: {improvements['Skills Rewrite']['why']}")
    lines.extend(["", "### Project Descriptions"])
    lines.extend(format_items(improvements["Project Description Rewrites"]))
    lines.extend(["", "### Experience Bullets"])
    lines.extend(format_items(improvements["Experience Bullet Rewrites"]))
    lines.extend([
        "",
        "### Job Keyword Note",
        f"- Keywords: {md_cell(improvements['Job Keyword Note']['text'])}",
        f"- Why: {improvements['Job Keyword Note']['why']}",
    ])

    lines.extend(["", "## Step 6: Suggested Missing Skills", ""])
    for category, data in analysis["missing_skills"].items():
        lines.append(f"### {category}")
        lines.append(f"- Skills: {md_cell(data['skills'])}")
        lines.append(f"- Why: {data['why']}")
        lines.append("")

    job_match = analysis["job_match"]
    lines.extend([
        "## Step 7: Job Matching",
        "",
        f"- Resume Match %: {job_match['Resume Match %']}",
        f"- Missing Keywords: {md_cell(job_match['Missing Keywords'])}",
        f"- Missing Skills: {md_cell(job_match['Missing Skills'])}",
        f"- Experience Gap: {job_match['Experience Gap']}",
        f"- ATS Prediction: {job_match['ATS Prediction']}",
        f"- Interview Probability: {job_match['Interview Probability']}",
        "",
        "## Step 8: Interview Preparation",
        "",
    ])
    for category, items in analysis["interview_preparation"].items():
        lines.append(f"### {category}")
        lines.extend(format_items(items))
        lines.append("")

    lines.extend([
        "## Step 9: ATS-Friendly Cover Letter",
        "",
        analysis["cover_letter"],
        "",
        "## Step 10: 30-Day Employability Roadmap",
        "",
    ])
    for item in analysis["roadmap"]:
        lines.append(f"### {item['period']}")
        lines.append(f"- Action: {item['action']}")
        lines.append(f"- Why: {item['why']}")
        lines.append("")

    lines.extend(["## Concise Action Plan", ""])
    lines.extend(format_items(analysis["action_plan"]))
    return "\n".join(lines).strip()


def format_items(items: Any) -> list[str]:
    if isinstance(items, str):
        return [f"- {items}"]
    if not items:
        return [f"- {NOT_FOUND}"]
    return [f"- {item}" for item in items]


def md_cell(value: Any) -> str:
    if value is None:
        return NOT_FOUND
    if isinstance(value, list):
        if not value:
            return NOT_FOUND
        return "<br>".join(str(item).replace("|", "\\|") for item in value)
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def safe_list(value: Any) -> list[str]:
    if value == NOT_FOUND or value is None:
        return []
    if isinstance(value, list):
        return [str(item) for item in value if str(item).strip()]
    return [str(value)] if str(value).strip() else []


def clamp(value: int | float, minimum: int, maximum: int) -> int:
    return max(minimum, min(maximum, int(value)))


def decode_bytes(raw: bytes) -> str:
    for encoding in ["utf-8", "utf-16", "latin-1"]:
        try:
            return raw.decode(encoding).strip()
        except UnicodeDecodeError:
            continue
    return raw.decode("latin-1", errors="ignore").strip()


def extract_docx_text(raw: bytes) -> str:
    try:
        with zipfile.ZipFile(io.BytesIO(raw)) as docx:
            xml = docx.read("word/document.xml")
    except Exception:
        return ""

    try:
        root = ElementTree.fromstring(xml)
    except ElementTree.ParseError:
        return ""

    namespace = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    paragraphs = []
    for paragraph in root.findall(".//w:p", namespace):
        text_parts = [
            node.text
            for node in paragraph.findall(".//w:t", namespace)
            if node.text
        ]
        if text_parts:
            paragraphs.append("".join(text_parts))
    return "\n".join(paragraphs).strip()


def extract_pdf_text_best_effort(raw: bytes) -> str:
    decoded = decode_bytes(raw)
    snippets = re.findall(r"\(([^()]{3,120})\)\s*Tj", decoded)
    if snippets:
        return clean_text("\n".join(snippets))

    readable = re.findall(r"[A-Za-z0-9@#%+.,:/() -]{20,}", decoded)
    filtered = [
        part.strip()
        for part in readable
        if not part.strip().startswith(("%PDF", "obj", "endobj", "stream", "endstream"))
    ]
    return clean_text("\n".join(filtered[:80]))
