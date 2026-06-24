"""
Bharat AI School V6 — General Utilities
"""
import os
import json
import hashlib
from datetime import datetime

def sanitize_filename(name: str) -> str:
    """Remove unsafe characters from a filename."""
    return "".join(c for c in name if c.isalnum() or c in " _-").rstrip().strip()

def format_date(date_str: str) -> str:
    """Format ISO date string to readable format."""
    try:
        dt = datetime.fromisoformat(date_str)
        return dt.strftime("%d %b %Y, %I:%M %p")
    except:
        return date_str

def get_project_root() -> str:
    """Get absolute path to the project root."""
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def truncate_text(text: str, max_chars: int = 100) -> str:
    """Truncate text to max_chars and add '...' if truncated."""
    if len(text) <= max_chars:
        return text
    return text[:max_chars-3] + "..."

def get_language_options() -> list:
    """Return supported languages."""
    return [
        {"code": "hi", "name": "हिन्दी (Hindi)", "display": "हिन्दी"},
        {"code": "en", "name": "English", "display": "English"},
        {"code": "hi-en", "name": "Hinglish (हिन्दी + English)", "display": "हिंग्लिश"},
    ]

def get_skill_levels() -> list:
    return ["Beginner", "Intermediate", "Advanced", "All"]

def generate_user_id() -> str:
    """Generate a short unique user ID."""
    import uuid
    return uuid.uuid4().hex[:8]
