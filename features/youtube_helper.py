"""
Bharat AI School V6 — YouTube Video Helper
Curated YouTube links + AI-suggested search.
"""
from db import operations as db_ops

# ── Curated YouTube playlists (topic → URLs) ──
CURATED_PLAYLISTS = {
    "machine learning": [
        {"title": "Machine Learning Full Course (Hindi)", "url": "https://youtube.com/playlist?list=PLA0e5qI0lmUt9Bv-oMayP6A6CJfaI9d9c", "language": "hi"},
        {"title": "ML with Python (English)", "url": "https://youtube.com/playlist?list=PLQVvvaa0QuDfKTOs3Keq_kaG2P55YRgv3", "language": "en"},
    ],
    "python": [
        {"title": "Python Full Course (Hindi)", "url": "https://youtube.com/playlist?list=PLu0W_9lII9agwh1XjRt242xIpHhPTIllm", "language": "hi"},
        {"title": "Python for Everybody (English)", "url": "https://youtube.com/playlist?list=PLlRFEj9H3Oj7Bp8-DfGpfAfDBiblRfl5p", "language": "en"},
    ],
    "chatgpt": [
        {"title": "ChatGPT Complete Guide (Hindi)", "url": "https://youtube.com/playlist?list=PLA0e5qI0lmUv1WJoLY_GjJKFASf8MvuWY", "language": "hi"},
    ],
    "gemini": [
        {"title": "Gemini AI Tutorial (English)", "url": "https://youtube.com/playlist?list=PLA0e5qI0lmUuIY1w8oJY3GGQJq7hkSJqB", "language": "en"},
    ],
    "deep learning": [
        {"title": "Deep Learning (Hindi)", "url": "https://youtube.com/playlist?list=PLu0W_9lII9ah6DhNYI4w0xVx9Q3e8F2Yk", "language": "hi"},
    ],
}

def get_curated_links(topic: str) -> list:
    """Get curated YouTube links for a topic (case-insensitive)."""
    topic_lower = topic.lower()
    for key, links in CURATED_PLAYLISTS.items():
        if key in topic_lower or topic_lower in key:
            return links
    return []

def get_chapter_youtube_links(chapter_id: int) -> list:
    """Get YouTube links stored in DB for a chapter."""
    return db_ops.get_youtube_links(chapter_id)

def add_youtube_link_to_chapter(chapter_id: int, title: str, url: str, language: str = "hi"):
    """Admin function to add a YouTube link for a chapter."""
    db_ops.add_youtube_link(chapter_id, title, url, language)

def get_youtube_suggestion_html(search_term: str) -> str:
    """Return HTML/markdown for a YouTube search suggestion."""
    from urllib.parse import quote
    query = quote(f"{search_term} tutorial hindi")
    url = f"https://www.youtube.com/results?search_query={query}"
    return f"""
<div style="background:#f0f0f0;padding:10px;border-radius:8px;margin:5px 0;">
    📺 <b>YouTube पर खोजें:</b> 
    <a href="{url}" target="_blank">{search_term}</a>
</div>
"""
