import requests
import os

def generate_cover_letter(api_key: str, resume: str, job_description: str) -> str:
    print("🔍 Starting Gemini Flash generation via REST")

    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": api_key
    }

    prompt = f"""
You are a professional cover letter writing assistant.
Using the resume and job description below, generate a tailored, professional cover letter.

Instructions:
- Tone: confident and professional
- Greeting: start with 'Dear Hiring Manager'
- Focus: align strengths from resume to job description
- Keep it concise and well-formatted.

Resume:
\"\"\"
{resume}
\"\"\"

Job Description:
\"\"\"
{job_description}
\"\"\"
"""

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        data = response.json()
        print("✅ Gemini response received.")

        # Extract and return response text
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        print("❌ ERROR OCCURRED:", str(e))
        raise
