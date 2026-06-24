"""
Bharat AI School V6 — LLM Harness (Central Orchestrator)
The ENGINE that sits between UI ↔ LLM ↔ Database.

Pipeline per user request:
1. Retrieve Context (user_progress, habits, chat history)
2. Inject System Prompt (teacher persona + harness rules)
3. Tool Selection (YouTube, PDF, Quiz or just reply)
4. Execute LLM Call
5. Update Memory (save chat, update streak)
6. Return structured response
"""
from typing import Optional
from .system_prompts import build_system_prompt
from .tools import extract_youtube_terms, extract_quiz_questions, build_youtube_search_url
from utils.groq_client import call_llm
from db import operations as db_ops
from datetime import datetime


class LLMHarness:
    """The central orchestrator for all AI interactions."""

    def __init__(self, username: str, persona: str = "default", language: str = "Hinglish"):
        self.username = username
        self.persona = persona
        self.language = language

    def process_message(self, user_message: str, course_id: int = 0) -> dict:
        """
        Process a single user message through the full harness pipeline.
        Returns: {
            "reply": str,           # AI response text
            "youtube_links": list,  # [YT: ...] extracted links
            "quiz_questions": list, # [QUIZ] blocks
            "xp_gained": int,       # XP awarded
            "streak_updated": bool, # Was streak updated?
            "current_streak": int,
            "total_xp": int,
        }
        """
        # ── Step 1: Retrieve Context ──
        context = self._retrieve_context(course_id)
        
        # ── Step 2: Build System Prompt ──
        system_prompt = build_system_prompt(self.persona, self.language)
        
        # ── Step 3: Assemble Message List ──
        messages = [
            {"role": "system", "content": system_prompt},
        ]
        
        # Inject context as a system message (not visible to user)
        messages.append({
            "role": "system", 
            "content": f"=== USER CONTEXT ===\n{context['context_summary']}"
        })
        
        # Add recent chat history (last 6 messages)
        for msg in context["history"][-6:]:
            messages.append({"role": msg["role"], "content": msg["content"]})
        
        # Add current user message
        messages.append({"role": "user", "content": user_message})

        # ── Step 4: Execute LLM Call ──
        reply = call_llm(messages)

        # ── Step 5: Process Tools ──
        youtube_terms = extract_youtube_terms(reply)
        youtube_links = [build_youtube_search_url(term) for term in youtube_terms]
        quiz_questions = extract_quiz_questions(reply)

        # Clean reply: remove tool markers from visible text
        clean_reply = reply
        import re
        clean_reply = re.sub(r'\[YT:.*?\]', '', clean_reply)
        clean_reply = re.sub(r'\[QUIZ\].*?\[/QUIZ\]', '', clean_reply, flags=re.DOTALL)
        clean_reply = clean_reply.strip()

        # ── Step 6: Update Memory ──
        db_ops.save_message(self.username, "user", user_message, course_id)
        db_ops.save_message(self.username, "assistant", reply, course_id)

        # Update streak + award XP for asking a question
        habits = db_ops.update_streak(self.username)
        db_ops.add_xp(self.username, 2)  # 2 XP per question
        total_xp = db_ops.get_habits(self.username)["total_xp"] if db_ops.get_habits(self.username) else 0

        # ── Step 7: Return Response ──
        return {
            "reply": clean_reply,
            "youtube_links": youtube_links,
            "youtube_terms": youtube_terms,
            "quiz_questions": quiz_questions,
            "xp_gained": 2,
            "streak_updated": True,
            "current_streak": habits["current_streak"] if habits else 0,
            "total_xp": total_xp,
        }

    def _retrieve_context(self, course_id: int) -> dict:
        """Fetch user data needed for context injection."""
        user = db_ops.get_user(self.username)
        habits = db_ops.get_habits(self.username)
        history = db_ops.get_chat_history(self.username, course_id, limit=10)
        
        # Build a summary string for the LLM
        lines = []
        if user:
            lines.append(f"User Level: {user.get('skill_level', 'Beginner')}")
            lines.append(f"Language: {self.language}")
        if habits:
            lines.append(f"Streak: {habits.get('current_streak', 0)} days")
            lines.append(f"Total XP: {habits.get('total_xp', 0)}")
        
        if course_id:
            course = db_ops.get_course(course_id)
            if course:
                lines.append(f"Current Course: {course['title']}")
                done, total, pct = db_ops.get_course_progress_pct(self.username, course_id)
                lines.append(f"Course Progress: {done}/{total} chapters ({pct}%)")

        return {
            "user": user,
            "habits": habits,
            "history": history,
            "context_summary": "\n".join(lines) if lines else "New user — no context yet."
        }

    def generate_syllabus(self, user_goal: str, skill_level: str = "Beginner") -> list:
        """
        Generate a personalized syllabus using the LLM.
        Returns list of module dicts.
        """
        prompt = f"""Generate a learning syllabus for a student who wants to: {user_goal}
They are at {skill_level} level.

Output EXACTLY in this JSON format (no other text):
[
  {{
    "title": "Module Title",
    "description": "Brief desc",
    "chapters": [
      {{"title": "Chapter Title", "content": "What this chapter covers"}}
    ]
  }}
]
Generate 3-5 modules, each with 2-4 chapters. Keep it practical and project-based.
Response must be valid JSON only, no markdown formatting."""
        
        messages = [
            {"role": "system", "content": "You are a curriculum designer for an Indian AI school. Output only valid JSON."},
            {"role": "user", "content": prompt}
        ]
        
        raw = call_llm(messages, temperature=0.3)
        
        # Parse JSON from response
        import json
        import re
        json_match = re.search(r'\[.*\]', raw, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(), strict=False)
            except json.JSONDecodeError:
                pass
        # Fallback syllabus
        return [
            {"title": "Introduction to AI", "description": "Basic concepts", "chapters": [
                {"title": "What is AI?", "content": "AI basics"},
                {"title": "Types of AI", "content": "Narrow vs General AI"}
            ]}
        ]

    def generate_chapter_content(self, course_title: str, module_title: str, chapter_title: str, chapter_description: str) -> dict:
        """
        Generate detailed lesson, code example, and YouTube search term on-demand.
        Returns a dict with content, code_example, and youtube_search_term.
        """
        from .system_prompts import get_persona
        persona_info = get_persona(self.persona)
        
        prompt = f"""You are teaching a student as your persona: {persona_info['name']}.
Style: {persona_info['tagline']}
System Instructions: {persona_info['system_prompt']}

You need to write a detailed, high-quality lesson for:
- Course: "{course_title}"
- Module: "{module_title}"
- Chapter: "{chapter_title}"
- Chapter Outline: "{chapter_description}"

Generate a complete, engaging, and detailed lesson (written in Hinglish) containing:
1. Clear explanations with simple analogies from daily Indian life.
2. A working Python code example (20-30 lines, well-commented). ALWAYS use single quotes for strings inside python code (e.g., print('text')) to avoid JSON syntax errors.
3. A specific search term to find good tutorials on YouTube.

You MUST output your response EXACTLY in this JSON format (no other text, just valid JSON):
{{
  "content": "Detailed lesson in markdown format. Use bolding, bullet points, and headers. Explain the concept step-by-step.",
  "code_example": "Python code here",
  "youtube_search_term": "YouTube search query"
}}
"""
        messages = [
            {"role": "system", "content": "You are a teacher at an Indian AI school. You output only valid JSON."},
            {"role": "user", "content": prompt}
        ]
        
        raw = call_llm(messages, temperature=0.7)
        
        import json
        import re
        json_match = re.search(r'\{.*\}', raw, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(), strict=False)
            except json.JSONDecodeError:
                pass
        
        return {
            "content": f"### {chapter_title}\n\nLesson generation failed. Please try again to reload the content.",
            "code_example": "print('Lesson generation failed. Please try again.')",
            "youtube_search_term": f"{chapter_title} tutorial"
        }
