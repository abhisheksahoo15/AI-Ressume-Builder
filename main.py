from fastapi import FastAPI, Request, File, UploadFile, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os
import json
import base64
import hashlib
import hmac
import secrets
import time
import requests
from bs4 import BeautifulSoup
import logging
from urllib.parse import quote_plus
from resume_agent import analyze_resume, extract_text_from_upload_bytes

# Load the Pretrained ATS Model



# Initialize FastAPI app
app = FastAPI()

# Setup logging for Azure debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Setting up Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Serve static files (CSS, JS, Images)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Ensure necessary directories exist
os.makedirs("temp", exist_ok=True)
os.makedirs("ml_model", exist_ok=True)

# Load the ATS Score Prediction Model (Bypassed to prevent scikit-learn environment pickling warnings)
ats_model = "simulation"

ADMIN_USERNAME = os.getenv("HIREFIRE_ADMIN_USERNAME", "Abhi@2003")
ADMIN_PASSWORD = os.getenv("HIREFIRE_ADMIN_PASSWORD", "Abhi@2003")
ADMIN_SESSION_SECRET = os.getenv("HIREFIRE_ADMIN_SESSION_SECRET", secrets.token_hex(32))
ADMIN_SESSION_COOKIE = "hirefire_admin_session"
ADMIN_SESSION_TTL = 8 * 60 * 60

ADMIN_SETTINGS_PATH = os.path.join("temp", "admin_settings.json")
DEFAULT_ADMIN_SETTINGS = {
    "profile": {
        "name": "",
        "email": "",
        "phone": "",
        "linkedin": "",
        "education": "",
        "experience": "",
        "projects": "",
        "certifications": "",
    },
    "ats": {
        "target_role": "",
        "minimum_ats_score": 70,
        "analysis_temperature": 0.35,
        "review_notes": "",
    },
}


def load_admin_settings():
    """Load the lightweight local admin configuration."""
    settings = json.loads(json.dumps(DEFAULT_ADMIN_SETTINGS))
    try:
        with open(ADMIN_SETTINGS_PATH, "r", encoding="utf-8") as settings_file:
            saved = json.load(settings_file)
        for key in settings["profile"]:
            if isinstance(saved.get("profile", {}).get(key), str):
                settings["profile"][key] = saved["profile"][key]
        for key in ("target_role", "review_notes"):
            if isinstance(saved.get("ats", {}).get(key), str):
                settings["ats"][key] = saved["ats"][key]
        if isinstance(saved.get("ats", {}).get("minimum_ats_score"), (int, float)):
            settings["ats"]["minimum_ats_score"] = max(0, min(100, int(saved["ats"]["minimum_ats_score"])))
        if isinstance(saved.get("ats", {}).get("analysis_temperature"), (int, float)):
            settings["ats"]["analysis_temperature"] = round(max(0, min(1, float(saved["ats"]["analysis_temperature"]))), 2)
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        pass
    return settings


def save_admin_settings(settings):
    with open(ADMIN_SETTINGS_PATH, "w", encoding="utf-8") as settings_file:
        json.dump(settings, settings_file, indent=2)


def normalize_admin_settings(payload):
    settings = load_admin_settings()
    profile = payload.get("profile", {}) if isinstance(payload, dict) else {}
    ats = payload.get("ats", {}) if isinstance(payload, dict) else {}

    for key in settings["profile"]:
        if key in profile:
            settings["profile"][key] = str(profile[key] or "").strip()
    for key in ("target_role", "review_notes"):
        if key in ats:
            settings["ats"][key] = str(ats[key] or "").strip()
    try:
        settings["ats"]["minimum_ats_score"] = max(0, min(100, int(ats.get("minimum_ats_score", settings["ats"]["minimum_ats_score"]))))
    except (TypeError, ValueError):
        pass
    try:
        settings["ats"]["analysis_temperature"] = round(max(0, min(1, float(ats.get("analysis_temperature", settings["ats"]["analysis_temperature"])))), 2)
    except (TypeError, ValueError):
        pass
    return settings


def create_admin_session(username: str) -> str:
    expires_at = int(time.time()) + ADMIN_SESSION_TTL
    payload = f"{username}:{expires_at}".encode("utf-8")
    signature = hmac.new(ADMIN_SESSION_SECRET.encode("utf-8"), payload, hashlib.sha256).hexdigest()
    encoded_payload = base64.urlsafe_b64encode(payload).decode("ascii").rstrip("=")
    return f"{encoded_payload}.{signature}"


def is_admin_session_valid(session_token: str | None) -> bool:
    if not session_token or "." not in session_token:
        return False
    encoded_payload, signature = session_token.split(".", 1)
    try:
        padded_payload = encoded_payload + "=" * (-len(encoded_payload) % 4)
        payload = base64.urlsafe_b64decode(padded_payload.encode("ascii"))
        expected_signature = hmac.new(ADMIN_SESSION_SECRET.encode("utf-8"), payload, hashlib.sha256).hexdigest()
        username, expires_at = payload.decode("utf-8").rsplit(":", 1)
        return (
            hmac.compare_digest(signature, expected_signature)
            and hmac.compare_digest(username, ADMIN_USERNAME)
            and int(expires_at) > int(time.time())
        )
    except (ValueError, TypeError, UnicodeDecodeError, base64.binascii.Error):
        return False


def require_admin(request: Request):
    if not is_admin_session_valid(request.cookies.get(ADMIN_SESSION_COOKIE)):
        raise HTTPException(status_code=401, detail="Admin authentication required")


@app.get("/")
async def home(request: Request):
    """ Serve the Landing Page """
    try:
        return templates.TemplateResponse(request=request, name="index.html", context={"title": "FastAPI Web Page"})
    except Exception as e:
        logger.error(f"Error loading home page: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")



@app.get("/about/")
async def about(request: Request):
    """ Serve the Landing Page """
    try:
        return templates.TemplateResponse(request=request, name="about.html", context={"title": "About Us"})
    except Exception as e:
        logger.error(f"Error loading home page: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    


@app.get("/contact/")
async def contact(request: Request):
    """ Serve the Landing Page """
    try:
        return templates.TemplateResponse(request=request, name="contact.html", context={"title": "Contact Us"})
    except Exception as e:
        logger.error(f"Error loading home page: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    


# resume builder app
@app.get("/resume-builder/")
async def resume_builder_page(request: Request):
    """ Serve the Resume Builder Page """
    try:
        return templates.TemplateResponse(request=request, name="create_resume.html", context={"title": "Resume Builder"})
    except Exception as e:
        logger.error(f"Error loading resume builder page: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    

@app.get("/ats-score-check/")
async def ats_score_page(request: Request):
    """ Serve the ATS Score Check Page """
    try:
        return templates.TemplateResponse(request=request, name="Ats_score_check.html", context={"title": "ATS Score Check"})
    except Exception as e:
        logger.error(f"Error loading ATS score check page: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/admin/")
async def admin_page(request: Request):
    """Serve the local admin workspace."""
    try:
        authenticated = is_admin_session_valid(request.cookies.get(ADMIN_SESSION_COOKIE))
        return templates.TemplateResponse(
            request=request,
            name="admin.html" if authenticated else "admin_login.html",
            context={"title": "Admin Workspace", "admin_authenticated": authenticated},
        )
    except Exception as e:
        logger.error(f"Error loading admin page: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.post("/api/admin/login/")
async def admin_login(request: Request, payload: dict):
    username = str(payload.get("username", ""))
    password = str(payload.get("password", ""))
    if not (hmac.compare_digest(username, ADMIN_USERNAME) and hmac.compare_digest(password, ADMIN_PASSWORD)):
        raise HTTPException(status_code=401, detail="Invalid admin credentials")

    response = {"status": "success", "message": "Admin session started."}
    from fastapi.responses import JSONResponse
    json_response = JSONResponse(response)
    json_response.set_cookie(
        ADMIN_SESSION_COOKIE,
        create_admin_session(username),
        max_age=ADMIN_SESSION_TTL,
        httponly=True,
        samesite="lax",
        secure=False,
    )
    return json_response


@app.get("/api/admin/session/")
async def admin_session(request: Request):
    if not is_admin_session_valid(request.cookies.get(ADMIN_SESSION_COOKIE)):
        raise HTTPException(status_code=401, detail="Admin authentication required")
    return {"status": "success", "authenticated": True, "username": ADMIN_USERNAME}


@app.post("/api/admin/logout/")
async def admin_logout():
    from fastapi.responses import JSONResponse
    json_response = JSONResponse({"status": "success", "message": "Admin session ended."})
    json_response.delete_cookie(ADMIN_SESSION_COOKIE)
    return json_response


@app.get("/api/admin/settings/")
async def get_admin_settings(request: Request):
    require_admin(request)
    return {"status": "success", "settings": load_admin_settings()}


@app.put("/api/admin/settings/")
async def update_admin_settings(request: Request, payload: dict):
    try:
        require_admin(request)
        settings = normalize_admin_settings(payload)
        save_admin_settings(settings)
        return {"status": "success", "settings": settings}
    except OSError as e:
        logger.error(f"Error saving admin settings: {e}")
        raise HTTPException(status_code=500, detail="Unable to save admin settings")


@app.post("/api/admin/reset/")
async def reset_admin_settings(request: Request):
    try:
        require_admin(request)
        settings = json.loads(json.dumps(DEFAULT_ADMIN_SETTINGS))
        save_admin_settings(settings)
        return {"status": "success", "settings": settings}
    except OSError as e:
        logger.error(f"Error resetting admin settings: {e}")
        raise HTTPException(status_code=500, detail="Unable to reset admin settings")


@app.post("/resume-agent/analyze/")
async def resume_agent_analyze(
    resume_text: str = Form(""),
    job_description: str = Form(""),
    career_goal: str = Form(""),
    analysis_temperature: float | None = Form(None),
    minimum_ats_score: int | None = Form(None),
    resume_file: UploadFile | None = File(None),
):
    """Analyze a resume with the deterministic ResumePilot career-agent workflow."""
    try:
        uploaded_text = ""
        upload_note = "No file uploaded."

        if resume_file and resume_file.filename:
            raw = await resume_file.read()
            uploaded_text = extract_text_from_upload_bytes(raw, resume_file.filename)
            upload_note = (
                "Resume text extracted from uploaded file."
                if uploaded_text
                else "Uploaded file received, but text extraction returned Not Found. Paste resume text for best results."
            )

        final_resume_text = resume_text.strip() or uploaded_text
        saved_ats_settings = load_admin_settings()["ats"]
        temperature = saved_ats_settings["analysis_temperature"] if analysis_temperature is None else max(0, min(1, float(analysis_temperature)))
        minimum_score = saved_ats_settings["minimum_ats_score"] if minimum_ats_score is None else max(0, min(100, int(minimum_ats_score)))
        analysis = analyze_resume(
            resume_text=final_resume_text,
            job_description=job_description,
            career_goal=career_goal,
        )
        analysis["analysis_settings"] = {
            "analysis_temperature": round(temperature, 2),
            "minimum_ats_score": minimum_score,
        }
        analysis["ats_score"]["target_threshold"] = minimum_score
        analysis["ats_score"]["threshold_status"] = "On target" if analysis["ats_score"]["overall"] >= minimum_score else "Needs improvement"
        analysis["source_note"] = upload_note

        return {
            "status": "success",
            "source_note": upload_note,
            "analysis": analysis,
            "analysis_markdown": analysis["analysis_markdown"],
            "analysis_settings": analysis["analysis_settings"],
        }
    except Exception as e:
        logger.error(f"Error running ResumePilot agent analysis: {e}")
        raise HTTPException(status_code=500, detail="Error running ResumePilot agent analysis")

# @app.post("/predict/")
# async def predict_ats_score(file: UploadFile = File(...)):
#     """ Process Resume & Predict ATS Score """
#     try:
#         if not file.filename:
#             raise HTTPException(status_code=400, detail="No file uploaded")

#         # Save uploaded file temporarily
#         file_location = f"temp/{file.filename}"
#         with open(file_location, "wb") as buffer:
#             shutil.copyfileobj(file.file, buffer)

#         # Check if model is loaded
#         if ats_model is None:
#             logger.error("ATS model not loaded")
#             raise HTTPException(status_code=500, detail="ATS model not available")

#         # Convert file data to a format compatible with ML model (Dummy example)
#         resume_data = {"feature1": [1], "feature2": [0], "feature3": [1]}  # Modify as per your model
#         resume_df = pd.DataFrame(resume_data)

#         # Make Prediction
#         score = ats_model.predict(resume_df)[0]

#         return {"status": "success", "score": score}

#     except HTTPException as http_exc:
#         raise http_exc
#     except Exception as e:
#         logger.error(f"Error processing resume: {e}")
#         raise HTTPException(status_code=500, detail="Error processing resume")

# ---------------------- JOB FINDING FEATURE ----------------------



@app.get("/job-find/")
async def job_find_page(request: Request):
    """ Serve the Job Search Page """
    try:
        return templates.TemplateResponse(request=request, name="job_find.html", context={"title": "Job Finder"})
    except Exception as e:
        logger.error(f"Error loading job finder page: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post("/fetch-jobs/")
async def fetch_jobs(role: str = Form(...), location: str = Form(...)):
    """ Fetch job listings from LinkedIn (with fallback to Remotive and Arbeitnow APIs) """
    try:
        if not role or not location:
            raise HTTPException(status_code=400, detail="Role and location are required")

        jobs = []

        # 1. Try LinkedIn scraping
        try:
            url = f"https://www.linkedin.com/jobs/search/?keywords={role}&location={location}"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
                "Accept-Language": "en-US,en;q=0.9",
                "Referer": "https://www.google.com/",
            }
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                job_cards = soup.find_all("div", class_="base-card")
                for job in job_cards[:10]:
                    title_tag = job.find("h3", class_="base-search-card__title")
                    company_tag = job.find("h4", class_="base-search-card__subtitle")
                    link_tag = job.find("a", class_="base-card__full-link")

                    title = title_tag.text.strip() if title_tag else "N/A"
                    company = company_tag.text.strip() if company_tag else "N/A"
                    job_link = link_tag["href"] if link_tag else "N/A"

                    jobs.append({"title": title, "company": company, "link": job_link})
        except Exception as scrape_err:
            logger.error(f"LinkedIn scraping failed: {scrape_err}")

        # 2. Fallback to Remotive API if LinkedIn yields no results
        if not jobs:
            logger.info("No jobs found via LinkedIn scraping. Querying Remotive API...")
            try:
                remotive_url = f"https://remotive.com/api/remote-jobs?search={role}"
                remotive_res = requests.get(remotive_url, timeout=10)
                if remotive_res.status_code == 200:
                    data = remotive_res.json()
                    remotive_jobs = data.get("jobs", [])
                    for job in remotive_jobs[:10]:
                        jobs.append({
                            "title": job.get("title", "N/A"),
                            "company": job.get("company_name", "N/A"),
                            "link": job.get("url", "N/A")
                        })
            except Exception as remotive_err:
                logger.error(f"Remotive API fallback failed: {remotive_err}")

        # 3. Fallback to Arbeitnow API if still no results
        if not jobs:
            logger.info("No jobs found via Remotive API. Querying Arbeitnow API...")
            try:
                arbeitnow_url = "https://www.arbeitnow.com/api/job-board-api"
                arbeitnow_res = requests.get(arbeitnow_url, timeout=10)
                if arbeitnow_res.status_code == 200:
                    data = arbeitnow_res.json()
                    arbeitnow_jobs = data.get("data", [])
                    # Try to filter by keyword first
                    count = 0
                    for job in arbeitnow_jobs:
                        title = job.get("title", "")
                        if role.lower() in title.lower():
                            jobs.append({
                                "title": title,
                                "company": job.get("company_name", "N/A"),
                                "link": job.get("url", "N/A")
                            })
                            count += 1
                            if count >= 10:
                                break
                    # If still empty, just grab the top 10
                    if not jobs:
                        for job in arbeitnow_jobs[:10]:
                            jobs.append({
                                "title": job.get("title", "N/A"),
                                "company": job.get("company_name", "N/A"),
                                "link": job.get("url", "N/A")
                            })
            except Exception as arbeitnow_err:
                logger.error(f"Arbeitnow API fallback failed: {arbeitnow_err}")

        if not jobs:
            logger.info("No external jobs found. Returning local fallback listings.")
            search_url = (
                "https://www.linkedin.com/jobs/search/?keywords="
                f"{quote_plus(role)}&location={quote_plus(location)}"
            )
            jobs = [
                {
                    "title": f"Junior {role}",
                    "company": "HirefireAI Demo Jobs",
                    "link": search_url,
                },
                {
                    "title": f"{role} Intern / Fresher",
                    "company": "CIT Career Starter",
                    "link": search_url,
                },
            ]

        return {"status": "success", "jobs": jobs}

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Error fetching jobs: {e}")
        raise HTTPException(status_code=500, detail="Error fetching jobs")

# ---------------------- ERROR HANDLING ENDPOINT ----------------------

@app.get("/health/")
async def health_check():
    """ Simple health check endpoint to verify if the server is running """
    return {"status": "running", "message": "FastAPI service is up and running"}

# ---------------------- AZURE DEBUGGING ROUTE ----------------------

@app.get("/debug/")
async def debug_info():
    """ Debugging route to check if required files and directories exist """
    debug_data = {
        "temp_dir_exists": os.path.exists("temp"),
        "ml_model_dir_exists": os.path.exists("ml_model"),
        "ats_model_exists": os.path.exists("ml_model/ats_model.pkl"),
        "ats_model_loaded": ats_model is not None,
    }
    return {"status": "debug", "data": debug_data}
