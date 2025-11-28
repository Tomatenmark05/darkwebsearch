"""
AI adapter for analyzing content with OpenAI (new >=1.0.0 client or legacy <1.0),
falling back to a heuristic analyzer if unavailable or if an error occurs.

Environment variables:
- OPENAI_API_KEY : API key for OpenAI.
- MODEL_NAME     : Optional. Defaults to 'gpt-3.5-turbo'.
"""

import os
import json
import re
from typing import Dict, Any
import openai  # noqa: F401


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-3.5-turbo")

# ---------------- JSON Parsing Helpers ---------------- #

def safe_parse_json(text: str) -> Dict[str, Any]:
    """
    Attempt to parse JSON from a string. Tries direct load, then the first {...} block.
    Raises ValueError if unable.
    """
    if not text:
        raise ValueError("Empty response text")

    # Direct attempt
    try:
        return json.loads(text)
    except Exception:
        pass

    # Extract first JSON object block
    match = re.search(r'(\{.*\})', text, re.S)
    if match:
        block = match.group(1)
        try:
            return json.loads(block)
        except Exception:
            pass

    raise ValueError("Could not parse JSON from model response")


# ---------------- Heuristic Fallback ---------------- #

def analyze_fallback(content: str) -> Dict[str, Any]:
    """
    Simple deterministic heuristic: picks frequent words as tags, infers legality
    based on presence of high-risk keywords, extracts first line as title, etc.
    """
    stopwords = {
        "the","and","a","an","of","to","in","for","on","with","by","is","this","that","it","be","are","was","were"
    }
    words = re.findall(r"[A-Za-z]{3,}", content.lower())
    freq = {}
    for w in words:
        if w in stopwords:
            continue
        freq[w] = freq.get(w, 0) + 1
    tags = sorted(freq.keys(), key=lambda k: (-freq[k], k))[:6]

    first_line = next((ln.strip() for ln in content.splitlines() if ln.strip()), "") or "Untitled"
    illegal_keywords = {"exploit", "bomb", "weapon", "carding", "fraud", "malware", "ddos", "phish", "ransomware"}
    legality = not any(k in content.lower() for k in illegal_keywords)

    description = re.sub(r"\s+", " ", content).strip()[:300]  # crude summary
    url = None
    m = re.search(r"https?://[^\s'\"]+", content)
    if m:
        url = m.group(0)

    return {
        "tags": tags,
        "title": first_line,
        "legality": legality,
        "description": description,
        "url": url,
    }


# ---------------- OpenAI Integrations ---------------- #

def _format_system_prompt() -> str:
    return (
        "You are an analysis assistant. Given website/text content, return ONLY a JSON object with keys:\n"
        "tags: array of short tag strings\n"
        "title: short title summarizing content\n"
        "legality: boolean true if legal, false if likely illegal or illicit\n"
        "description: concise description\n"
        "url: optional string or null\n"
        "Return strictly valid JSON. No prose."
    )


def _new_client_completion(content: str) -> Dict[str, Any]:

    from openai import OpenAI  # type: ignore
    client = OpenAI(api_key=OPENAI_API_KEY)

    system_prompt = _format_system_prompt()
    user_prompt = f"Content:\n{content}\n\nReturn JSON."

    # Use structured JSON response if model supports it (gpt-4.1 / newer); for gpt-3.5 it may ignore.
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.0,
        max_tokens=512,
        response_format={"type": "json_object"},
    )

    text = response.choices[0].message.content
    parsed = safe_parse_json(text)
    return {
        "tags": parsed.get("tags", []) if isinstance(parsed.get("tags"), list) else [],
        "title": parsed.get("title"),
        "legality": bool(parsed.get("legality")),
        "description": parsed.get("description"),
        "url": parsed.get("url"),
    }


def analyze_with_openai(content: str) -> Dict[str, Any]:
    """
    Dispatch between new and legacy APIs depending on installed version.
    """
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY not set")



    return _new_client_completion(content)


# ---------------- Public Entry Point ---------------- #

def analyze_content_sync(content: str) -> Dict[str, Any]:
    """
    Main entry used by API endpoint. Attempts OpenAI analysis, falls back if anything fails.
    """
    if OPENAI_API_KEY:
        try:
            return analyze_with_openai(content)
        except Exception as exc:
            # Log or print if desired; fallback ensures endpoint still succeeds.
            print(f"[ai_client] OpenAI analysis failed, using fallback: {exc}")
            return analyze_fallback(content)
    else:
        return analyze_fallback(content)


