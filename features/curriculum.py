"""
Bharat AI School V6 — Curriculum Engine
Hardcoded course catalog + AI-powered syllabus generator.
"""
from db import operations as db_ops
from harness.llm_harness import LLMHarness

# ── Built-in Course Catalog ──
BUILTIN_COURSES = [
    {
        "title": "Machine Learning Zero to Hero",
        "description": "ML algorithms from scratch: Linear Regression to Neural Networks. Python + practical projects.",
        "provider": "Bharat AI School",
        "level": "Beginner",
        "is_free": 1,
        "url": "",
        "career_benefit": "Data Scientist, ₹5-15 LPA starting salary",
        "tech_stack": "Python, scikit-learn, TensorFlow, Pandas",
    },
    {
        "title": "ChatGPT & Prompt Engineering",
        "description": "Master ChatGPT, Gemini, Claude. Learn prompt engineering, API integration, and build AI apps.",
        "provider": "Bharat AI School",
        "level": "Beginner",
        "is_free": 1,
        "url": "",
        "career_benefit": "AI Engineer, Prompt Engineer, Freelancer — ₹3-8 LPA",
        "tech_stack": "OpenAI API, LangChain, Streamlit",
    },
    {
        "title": "Gemini & Google AI Studio",
        "description": "Use Gemini 1.5 Flash/Pro, multimodal prompts, Google AI Studio for no-code AI.",
        "provider": "Bharat AI School",
        "level": "Beginner",
        "is_free": 1,
        "url": "",
        "career_benefit": "AI Product Builder, ₹4-10 LPA",
        "tech_stack": "Gemini API, Google AI Studio, Python",
    },
    {
        "title": "Claude & Advanced LLM Ops",
        "description": "Anthropic Claude, safety, tool use, and multi-agent systems. Production-grade LLM deployment.",
        "provider": "Bharat AI School",
        "level": "Intermediate",
        "is_free": 0,
        "url": "",
        "career_benefit": "LLM Ops Engineer, ₹8-20 LPA",
        "tech_stack": "Claude API, MCP, LangGraph",
    },
    {
        "title": "Python for AI (Absolute Beginner)",
        "description": "Python from zero: variables, loops, functions, NumPy, Pandas — all with AI context.",
        "provider": "Bharat AI School",
        "level": "Beginner",
        "is_free": 1,
        "url": "",
        "career_benefit": "Foundation for any AI/ML role",
        "tech_stack": "Python, Jupyter, Colab",
    },
    {
        "title": "Build Your Own AI Agent",
        "description": "Create autonomous AI agents: tools, memory, multi-step reasoning. Harness Engineering approach.",
        "provider": "Bharat AI School",
        "level": "Advanced",
        "is_free": 0,
        "url": "",
        "career_benefit": "AI Agent Developer, ₹10-25 LPA",
        "tech_stack": "LangChain, Groq, Streamlit, SQLite",
    },
    {
        "title": "Startup & Freelancing with AI",
        "description": "How to use AI to build startups, get freelancing gigs, and earn money. Chanakya-style strategy.",
        "provider": "Bharat AI School",
        "level": "All",
        "is_free": 0,
        "url": "",
        "career_benefit": "Startup Founder, Freelancer — unlimited earning potential",
        "tech_stack": "Any — focus is on monetization",
    },
]

def seed_courses():
    """Insert built-in courses into DB if not already present."""
    existing = db_ops.get_courses()
    if len(existing) >= len(BUILTIN_COURSES):
        return  # already seeded
    
    for course in BUILTIN_COURSES:
        db_ops.add_course(
            title=course["title"],
            description=course["description"],
            level=course["level"],
            provider=course["provider"],
            is_free=course["is_free"],
            url=course["url"],
            career_benefit=course["career_benefit"],
            tech_stack=course["tech_stack"],
        )
    print(f"✅ Seeded {len(BUILTIN_COURSES)} courses")

def get_modules_with_chapters(course_id):
    """Get all modules + their chapters for a course."""
    modules = db_ops.get_modules(course_id)
    result = []
    for mod in modules:
        chapters = db_ops.get_chapters(mod["id"])
        result.append({
            "module": mod,
            "chapters": chapters,
        })
    return result

def generate_and_save_syllabus(username, course_id, course_title, user_goal, skill_level):
    """
    Use AI to generate a syllabus for an existing course.
    The syllabus is saved as modules + chapters in DB.
    """
    harness = LLMHarness(username)
    syllabus = harness.generate_syllabus(user_goal, skill_level)
    
    for mod_order, mod in enumerate(syllabus):
        module_id = db_ops.add_module(
            course_id=course_id,
            title=mod.get("title", "Module"),
            description=mod.get("description", ""),
            module_order=mod_order,
        )
        for ch_order, ch in enumerate(mod.get("chapters", [])):
            db_ops.add_chapter(
                module_id=module_id,
                title=ch.get("title", "Chapter"),
                content=ch.get("content", ""),
                chapter_order=ch_order,
            )
    return syllabus
