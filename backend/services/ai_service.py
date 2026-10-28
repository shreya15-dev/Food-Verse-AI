import os
import json
import base64
import requests
from config import GEMINI_API_KEY, IS_AI_CONFIGURED

def encode_image_to_base64(image_path: str) -> tuple[str, str]:
    """Encodes an image file into base64 and detects mime type."""
    ext = image_path.rsplit(".", 1)[-1].lower()
    mime = "image/jpeg"
    if ext == "png":
        mime = "image/png"
    elif ext == "webp":
        mime = "image/webp"

    with open(image_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")
    return encoded, mime

from config import get_ai_api_key

GEMINI_MODELS = ["gemini-1.5-flash", "gemini-2.0-flash", "gemini-1.5-pro"]

def call_gemini_vision(image_path: str, prompt: str) -> dict:
    """
    Calls Google Gemini multimodal API if GEMINI_API_KEY is configured.
    Falls back gracefully across multiple model versions before returning failure.
    """
    api_key = get_ai_api_key()
    if not api_key:
        return {"success": False, "error": "No API key configured", "is_demo": True}

    base64_data, mime_type = encode_image_to_base64(image_path)
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt + "\n\nCRITICAL: Respond ONLY with a valid JSON object matching the requested schema. Do not enclose in markdown backticks."},
                    {
                        "inline_data": {
                            "mime_type": mime_type,
                            "data": base64_data
                        }
                    }
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.2,
            "response_mime_type": "application/json"
        }
    }

    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": api_key
    }

    last_error = ""
    for model_name in GEMINI_MODELS:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=25)
            if response.status_code == 200:
                res_json = response.json()
                candidates = res_json.get("candidates", [])
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    raw_text = parts[0].get("text", "") if parts else ""
                    raw_text = raw_text.strip()
                    if raw_text.startswith("```json"):
                        raw_text = raw_text[7:]
                    if raw_text.startswith("```"):
                        raw_text = raw_text[3:]
                    if raw_text.endswith("```"):
                        raw_text = raw_text[:-3]

                    parsed = json.loads(raw_text.strip())
                    return {
                        "success": True,
                        "result": parsed,
                        "is_demo": False,
                        "provider": f"Google Gemini Vision API ({model_name})"
                    }
            elif response.status_code in [400, 403, 404]:
                last_error = f"{response.status_code}: {response.text[:200]}"
                continue
            else:
                last_error = f"API error {response.status_code}: {response.text[:200]}"
        except Exception as e:
            last_error = str(e)
            continue

    return {"success": False, "error": last_error or "All vision models failed", "is_demo": True}

def call_gemini_text(prompt: str, system_instruction: str = "", conversation_history: list = None) -> dict:
    """
    Calls Google Gemini text model if GEMINI_API_KEY is configured.
    Supports multi-turn conversation history and system instructions.
    """
    api_key = get_ai_api_key()
    if not api_key:
        return {"success": False, "error": "No API key configured", "is_demo": True}

    # Format and sanitize multi-turn conversation contents for Gemini API:
    # 1. Must start with role 'user' (strip leading welcome/assistant messages)
    # 2. Must strictly alternate: user -> model -> user -> model
    # 3. Must end with role 'user' (the current prompt)
    contents = []
    if conversation_history:
        sanitized_history = []
        for m in conversation_history:
            if not isinstance(m, dict):
                continue
            text = str(m.get("text", "")).strip()
            if not text:
                continue
            role = "model" if m.get("role") in ("assistant", "model") else "user"

            # Gemini requires the conversation to begin with a 'user' turn
            if not sanitized_history and role != "user":
                continue

            # Ensure strict alternation (collapse consecutive turns of the same role)
            if sanitized_history and sanitized_history[-1]["role"] == role:
                sanitized_history[-1]["parts"][0]["text"] += f"\n\n{text}"
            else:
                sanitized_history.append({
                    "role": role,
                    "parts": [{"text": text}]
                })

        # If sanitized history ends with a 'user' turn, merge current prompt into it
        # Otherwise, append the current prompt as the final 'user' turn
        if sanitized_history and sanitized_history[-1]["role"] == "user":
            sanitized_history[-1]["parts"][0]["text"] += f"\n\n{prompt}"
            contents = sanitized_history
        else:
            contents = sanitized_history
            contents.append({
                "role": "user",
                "parts": [{"text": prompt}]
            })
    else:
        contents.append({
            "role": "user",
            "parts": [{"text": prompt}]
        })

    payload = {
        "contents": contents,
        "generationConfig": {
            "temperature": 0.4
        }
    }
    if system_instruction:
        payload["system_instruction"] = {
            "parts": [{"text": system_instruction}]
        }

    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": api_key
    }

    last_error = ""
    for model_name in GEMINI_MODELS:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=25)
            if response.status_code == 200:
                res_json = response.json()
                candidates = res_json.get("candidates", [])
                if candidates:
                    parts_res = candidates[0].get("content", {}).get("parts", [])
                    raw_text = parts_res[0].get("text", "") if parts_res else ""
                    if raw_text.strip():
                        return {
                            "success": True,
                            "text": raw_text.strip(),
                            "is_demo": False,
                            "provider": f"Google Gemini ({model_name})"
                        }
            elif response.status_code == 429:
                last_error = f"Rate limit or quota exceeded (HTTP 429) for model {model_name}."
                continue
            elif response.status_code in [400, 403]:
                last_error = f"HTTP {response.status_code}: {response.text[:200]}"
                # Fall back to payload without system_instruction if 400
                if "system_instruction" in payload and response.status_code == 400:
                    fallback_contents = [
                        {"role": "user", "parts": [{"text": f"System Instruction: {system_instruction}\n\n{prompt}"}]}
                    ]
                    fallback_payload = {"contents": fallback_contents, "generationConfig": {"temperature": 0.4}}
                    fb_res = requests.post(url, json=fallback_payload, headers=headers, timeout=25)
                    if fb_res.status_code == 200:
                        fb_candidates = fb_res.json().get("candidates", [])
                        if fb_candidates:
                            fb_text = fb_candidates[0].get("content", {}).get("parts", [{}])[0].get("text", "")
                            if fb_text.strip():
                                return {
                                    "success": True,
                                    "text": fb_text.strip(),
                                    "is_demo": False,
                                    "provider": f"Google Gemini ({model_name})"
                                }
                continue
            else:
                last_error = f"API error {response.status_code}: {response.text[:200]}"
        except Exception as e:
            last_error = str(e)
            continue

    return {"success": False, "error": last_error or "All text generation models failed", "is_demo": False}
