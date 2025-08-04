from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from services.generate_letter import generate_cover_letter
import os
from dotenv import load_dotenv

# Load API Key from .env
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize FastAPI app
app = FastAPI()

# CORS config (Allow frontend calls from anywhere in dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic model for request body
class CoverLetterRequest(BaseModel):
    resume: str
    job_description: str

# Route: POST /api/generate
@app.post("/api/generate")
def generate(request: CoverLetterRequest):
    if not GEMINI_API_KEY:
        raise HTTPException(status_code=500, detail="Gemini API key not found")

    try:
        letter = generate_cover_letter(
            api_key=GEMINI_API_KEY,
            resume=request.resume,
            job_description=request.job_description
        )
        return {"cover_letter": letter}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
