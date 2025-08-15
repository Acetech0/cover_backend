import requests

def gemini_call(api_key: str, text: str) -> str:
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": api_key
    }
    payload = {"contents": [{"parts": [{"text": text}]}]}
    response = requests.post(url, headers=headers, json=payload)
    data = response.json()
    return data["candidates"][0]["content"]["parts"][0]["text"]

def generate_cover_letter(api_key: str, resume: str, job_description: str) -> str:
    # Step 1: Extract key skills & achievements
    step1_prompt = f"""
    From the following resume, extract the top 5 achievements and 5 skills that are most relevant to the job description.

    Resume:
    {resume}

    Job Description:
    {job_description}
    """
    key_points = gemini_call(api_key, step1_prompt)

    # Step 2: Map to ATS keywords
    step2_prompt = f"""
    Based on these key points:
    {key_points}

    Suggest ATS-friendly keywords that match the job description without sounding forced.
    """
    ats_keywords = gemini_call(api_key, step2_prompt)

    # Step 3: Draft cover letter
    step3_prompt = f"""
    Using the resume, job description, key points, and ATS keywords provided, 
    write a confident, persuasive cover letter.

    Resume:
    {resume}

    Job Description:
    {job_description}

    Key Points:
    {key_points}

    ATS Keywords:
    {ats_keywords}
    """
    first_draft = gemini_call(api_key, step3_prompt)

    # Step 4: Critique & improve
    step4_prompt = f"""
    Critique the following cover letter for persuasiveness, clarity, and alignment with the job description. 
    Then rewrite it to be stronger, without losing professionalism.

    Cover Letter Draft:
    {first_draft}
    """
    final_letter = gemini_call(api_key, step4_prompt)

    return final_letter
