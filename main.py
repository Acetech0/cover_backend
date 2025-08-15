from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv

# Local imports
from services.generate_letter import generate_cover_letter

# Load API Key from .env
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

app = FastAPI(
    title="CoverCraft AI",
    description="AI-powered multi-prompt cover letter generator (Assassin Mode)",
    version="2.0.0",
)

# CORS config (Allow frontend calls from anywhere in dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CoverLetterRequest(BaseModel):
    resume: str
    job_description: str

@app.get("/")
def root():
    return {"ok": True, "service": "CoverCraft AI V2", "mode": "Assassin"}

@app.post("/api/generate")
def generate(request: CoverLetterRequest):
    if not GEMINI_API_KEY:
        raise HTTPException(status_code=500, detail="Gemini API key not found")

    try:
        letter = generate_cover_letter(
            api_key=GEMINI_API_KEY,
            resume=request.resume,
            job_description=request.job_description,
        )
        return {"cover_letter": letter}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))