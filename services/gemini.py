import requests
from typing import Dict, Any

GEMINI_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"

class GeminiAPIError(Exception):
    pass


def gemini_call(api_key: str, prompt: str, model: str = "gemini-1.5-flash", safety_settings: Dict[str, Any] | None = None) -> str:
    """
    Minimal wrapper for Gemini REST 'generateContent'. Returns the first candidate text or raises.
    """
    url = GEMINI_ENDPOINT.format(model=model)
    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": api_key,
    }
    payload: Dict[str, Any] = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    if safety_settings:
        payload["safetySettings"] = safety_settings

    resp = requests.post(url, headers=headers, json=payload, timeout=60)
    try:
        data = resp.json()
    except Exception as ex:
        raise GeminiAPIError(f"Non-JSON response from Gemini: {ex}")

    if resp.status_code >= 400:
        # Gemini often returns detailed error JSON
        message = data.get("error", {}).get("message") if isinstance(data, dict) else None
        raise GeminiAPIError(message or f"Gemini HTTP {resp.status_code}")

    try:
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as ex:
        raise GeminiAPIError(f"Unexpected Gemini payload structure: {ex}")