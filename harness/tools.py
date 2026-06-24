"""
Bharat AI School V6 — Harness Tool Definitions
Tools that the LLM can trigger: YouTube search, PDF generation, etc.
"""
from typing import Optional

# ── YouTube Tool ──

def extract_youtube_terms(text: str) -> list:
    """
    Parse [YT: search term] patterns from LLM output.
    Returns list of search terms.
    """
    import re
    pattern = r'\[YT:\s*(.*?)\]'
    matches = re.findall(pattern, text)
    return [m.strip() for m in matches]

def build_youtube_search_url(search_term: str, language: str = "hi") -> str:
    """Build a YouTube search URL from a search term."""
    from urllib.parse import quote
    query = quote(f"{search_term} tutorial {language}")
    return f"https://www.youtube.com/results?search_query={query}"

def get_youtube_suggestions(chapter_title: str, chapter_content: str = "") -> str:
    """
    Generate YouTube search suggestions based on chapter content.
    Returns a formatted string for the UI.
    """
    search_term = f"{chapter_title} explained simply"
    url = build_youtube_search_url(search_term)
    return f"""
📺 **YouTube पर खोजें:**
- **"{chapter_title}"** — [YouTube पर देखें]({url})
- **"टिप:** Video देखने के बाद वापस आकर कोड प्रैक्टिस करें!"
"""

# ── PDF Tool ──

def format_for_pdf(chapter_data: dict) -> str:
    """
    Format chapter content into a clean markdown string ready for PDF generation.
    chapter_data should have: title, content, code_example, youtube_search_term
    """
    lines = []
    lines.append(f"# {chapter_data.get('title', 'Chapter')}")
    lines.append("")
    lines.append(f"## 📖 सारांश (Summary)")
    lines.append(chapter_data.get("content", ""))
    if chapter_data.get("code_example"):
        lines.append("")
        lines.append("## 💻 कोड उदाहरण (Code Example)")
        lines.append("```python")
        lines.append(chapter_data["code_example"])
        lines.append("```")
    if chapter_data.get("youtube_search_term"):
        lines.append("")
        lines.append(f"## 📺 YouTube: {chapter_data['youtube_search_term']}")
    return "\n".join(lines)

def extract_quiz_questions(text: str) -> list:
    """
    Parse [QUIZ]...[/QUIZ] blocks from LLM output.
    Returns list of question dicts.
    """
    import re
    pattern = r'\[QUIZ\](.*?)\[/QUIZ\]'
    matches = re.findall(pattern, text, re.DOTALL)
    questions = []
    for block in matches:
        lines = block.strip().split("\n")
        for line in lines:
            line = line.strip()
            if line and not line.startswith("["):
                questions.append({"question": line.strip("Q: ").strip("?")})
    return questions
