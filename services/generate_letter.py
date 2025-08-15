import os
from .gemini import gemini_call, GeminiAPIError

# Optional: allow model override via ENV
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

# ===== Prompt Templates =====
DRAFT_PROMPT = """
You are a professional cover letter writer. Using the resume and job description below,
write a concise, tailored, and persuasive cover letter.

Rules:
- Start with: "Dear Hiring Manager," (unless the hiring manager's name is provided in the inputs — if not, default to this)
- Tone: professional, confident, and enthusiastic.
- Structure: 2–3 short paragraphs max.
- Focus on measurable impact, leadership, and alignment with the job description.
- Subtly incorporate relevant keywords for ATS without sounding forced.
- Output only the final letter text (no commentary).

Resume:
"""

CRITIQUE_PROMPT = """
You are an expert hiring manager and business writing coach. Critique the following cover letter for:
1) Opening hook strength, 2) Story/narrative flow, 3) Quantified achievements, 4) Keyword alignment with the job description,
5) Strength of the close and call to action. Be concise, but specific. Then list concrete revision directives.

Job Description (for alignment):
"""

REWRITE_PROMPT = """
You are an elite copywriter. Rewrite the cover letter below, addressing all weaknesses from the critique.
Improve the hook, narrative flow, quantify impact where possible, ensure keyword alignment, and craft a strong close with a clear CTA.
Keep it professional and under 180 words. Output only the improved letter.

Critique:
"""

POLISH_PROMPT = """
Act as a senior editor. Polish the following letter for clarity, cadence, and brevity without changing meaning.
Remove filler, tighten sentences, and ensure the tone remains confident and warm. Output only the polished letter.

Letter:
"""


def _join_blocks(*blocks: str) -> str:
    return "\n\n".join([b.strip() for b in blocks if b and b.strip()])


def generate_cover_letter(api_key: str, resume: str, job_description: str, *, enable_polish: bool = True) -> str:
    """
    Multi-pass chain: Draft -> Critique -> Rewrite -> (optional) Polish
    Returns the final letter text.
    """
    # Step 1: Draft
    draft_prompt = _join_blocks(
        DRAFT_PROMPT,
        resume.strip(),
        "\nJob Description:\n\n" + job_description.strip(),
    )
    draft = gemini_call(api_key, draft_prompt, model=GEMINI_MODEL)

    # Step 2: Critique
    critique_prompt = _join_blocks(
        CRITIQUE_PROMPT,
        job_description.strip(),
        "\nCover Letter:\n\n" + draft,
    )
    critique = gemini_call(api_key, critique_prompt, model=GEMINI_MODEL)

    # Step 3: Rewrite
    rewrite_prompt = _join_blocks(
        REWRITE_PROMPT,
        critique,
        "\nOriginal Letter:\n\n" + draft,
    )
    rewritten = gemini_call(api_key, rewrite_prompt, model=GEMINI_MODEL)

    # Step 4: Optional polish
    if enable_polish:
        polish_prompt = _join_blocks(
            POLISH_PROMPT,
            rewritten,
        )
        final_letter = gemini_call(api_key, polish_prompt, model=GEMINI_MODEL)
    else:
        final_letter = rewritten

    return final_letter