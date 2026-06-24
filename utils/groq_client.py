"""
Bharat AI School V6 — Groq LLM API Client
Model-agnostic harness. Swap model/provider by changing env vars.
"""
import os
import json
import requests
from typing import Optional

# Default endpoint / model — Groq Llama 3.1 8B (fast + cheap)
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
DEFAULT_MODEL = "llama-3.1-8b-instant"        # 8B ~ 8K context, cheap
FALLBACK_MODEL = "llama3-70b-8192"             # If we need more reasoning

def get_api_key() -> Optional[str]:
    """Read GROQ_API_KEY from (in order):
    1. Environment variable (set by MY_SECRET_KEY.bat if called with 'call')
    2. MY_SECRET_KEY.bat file directly (secret file)
    3. .env file (legacy fallback)
    """
    # 1. Check environment variable
    key = os.environ.get("GROQ_API_KEY")
    if key:
        return key

    # get path of THIS file: e.g. .../bharat_ai_school_v6/utils/groq_client.py
    this_file = os.path.abspath(__file__)
    # project_root is grandparent dir (.../bharat_ai_school_v6/)
    project_root = os.path.dirname(os.path.dirname(this_file))

    # 2. Try MY_SECRET_KEY.txt (the secret file — opens easily in Notepad)
    for secret_name in ["MY_SECRET_KEY.txt", "MY_SECRET_KEY.bat"]:
        secret_path = os.path.join(project_root, secret_name)
        if os.path.exists(secret_path):
            with open(secret_path, encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    # Support both formats: "GROQ_API_KEY=..." and "set GROQ_API_KEY=..."
                    if line.startswith("GROQ_API_KEY=") or line.startswith("set GROQ_API_KEY="):
                        val = line.split("=", 1)[1].strip()
                        if val and val not in ("YOUR_API_KEY_HERE", "YOUR_KEY_HERE", ""):
                            return val

    # 3. Try .env (legacy)
    env_path = os.path.join(project_root, ".env")
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line.startswith("GROQ_API_KEY="):
                    return line.split("=", 1)[1].strip().strip("\"'")
    return None

def call_llm(
    messages: list,
    model: str = DEFAULT_MODEL,
    temperature: float = 0.7,
    max_tokens: int = 2048,
    stream: bool = False,
) -> str:
    """
    Universal LLM call function.
    - messages: list of {"role": "system"/"user"/"assistant", "content": "..."}
    - Returns the assistant reply text.
    """
    api_key = get_api_key()
    if not api_key:
        return "❌ API Key missing. Please set GROQ_API_KEY in .env file."

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": stream,
    }

    try:
        resp = requests.post(GROQ_API_URL, headers=headers, json=payload, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"]
    except requests.exceptions.Timeout:
        return "⏱️ Request timed out. Please try again."
    except requests.exceptions.HTTPError as e:
        if resp.status_code == 429:
            return "⏳ Rate limited. Please wait a moment and retry."
        return f"❌ API Error: {resp.status_code} - {resp.text[:200]}"
    except Exception as e:
        return f"❌ Error: {str(e)}"
