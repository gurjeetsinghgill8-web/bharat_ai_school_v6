"""
Bharat AI School V6 — Main Streamlit Application
The UI layer. Routes user requests to the Harness orchestrator.
"""
import streamlit as st
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ── Page config (must be first Streamlit command) ──
st.set_page_config(
    page_title="Bharat AI School",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS injection ──
from utils.styles import inject_custom_styles, card_html
inject_custom_styles()

# ── Imports ──
from db.schema import init_db
from db import operations as db_ops
from features.curriculum import seed_courses, get_modules_with_chapters, BUILTIN_COURSES
from features.habit_engine import format_streak_display, get_streak_badge
from features.payment import (
    get_upi_payment_details, generate_upi_url, check_subscription_status,
    record_payment, get_subscription_required_message
)
from features.youtube_helper import get_curated_links, get_chapter_youtube_links
from utils.pdf_generator import generate_chapter_pdf, generate_certificate_pdf
from utils.helpers import get_language_options, get_skill_levels
from harness.llm_harness import LLMHarness

# ── Initialize DB + seed courses ──
if "db_initialized" not in st.session_state:
    init_db()
    seed_courses()
    st.session_state.db_initialized = True

# ── Session state ──
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.persona = "default"
    st.session_state.page = "home"
    st.session_state.current_course_id = 0
    st.session_state.current_chapter_id = 0

# ──────────────────────────────────────────────
#  SIDEBAR
# ──────────────────────────────────────────────

def render_sidebar():
    with st.sidebar:
        st.image("https://img.icons8.com/fluency/96/artificial-intelligence.png", width=60)
        st.markdown("### 🎓 Bharat AI School")
        st.markdown("**₹20/माह — पूरा भारत सीखेगा AI**")
        st.divider()

        if st.session_state.logged_in:
            # User info
            user = db_ops.get_user(st.session_state.username)
            if user:
                st.markdown(f"👤 **{user.get('full_name') or st.session_state.username}**")
                habits = db_ops.get_habits(st.session_state.username)
                if habits:
                    badge = get_streak_badge(habits["current_streak"])
                    st.markdown(f"{badge} Streak: **{habits['current_streak']} days**")
                    st.markdown(f"⭐ XP: **{habits['total_xp']}**")

            # Navigation
            st.divider()
            st.markdown("### 📍 Navigation")
            nav = st.radio(
                "Go to",
                ["🏠 Home", "📚 Courses", "📖 Current Course", "👤 Profile", "🔧 Admin"],
                index=0,
                label_visibility="collapsed",
                key="nav_radio",
            )
            page_map = {
                "🏠 Home": "home",
                "📚 Courses": "courses",
                "📖 Current Course": "course_view",
                "👤 Profile": "profile",
                "🔧 Admin": "admin",
            }
            st.session_state.page = page_map.get(nav, "home")

            # Teacher persona selector
            st.divider()
            st.markdown("### 🧠 AI Teacher")
            persona = st.selectbox(
                "Choose your teacher",
                options=["default", "aryabhatta", "kalam", "chanakya"],
                format_func=lambda x: {
                    "default": "🤖 Bharat AI Guru",
                    "aryabhatta": "🧮 Aryabhatta",
                    "kalam": "🚀 Dr. Kalam",
                    "chanakya": "📜 Chanakya",
                }.get(x, x),
                index=0,
                key="persona_select",
            )
            st.session_state.persona = persona

            # Logout
            st.divider()
            if st.button("🚪 Logout", use_container_width=True):
                st.session_state.logged_in = False
                st.session_state.username = ""
                st.session_state.page = "home"
                st.rerun()
        else:
            st.markdown("### 🔐 Login / Signup")
            st.markdown("खाता बनाएं या लॉगिन करें:")

# ──────────────────────────────────────────────
#  AUTH PAGES
# ──────────────────────────────────────────────

def render_login():
    st.markdown("## 🔐 Login")
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        col1, col2 = st.columns(2)
        with col1:
            login_btn = st.form_submit_button("Login", use_container_width=True)
        with col2:
            signup_btn = st.form_submit_button("Signup", use_container_width=True)

        if login_btn:
            user = db_ops.verify_user(username, password)
            if user:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success(f"Welcome back, {user.get('full_name') or username}!")
                st.rerun()
            else:
                st.error("❌ Invalid username or password")

        if signup_btn:
            # Switch to signup
            st.session_state.show_signup = True
            st.rerun()

def render_signup():
    st.markdown("## 📝 Sign Up")
    st.markdown("**₹20/माह — पूरे भारत को AI सिखाने का मिशन**")
    with st.form("signup_form"):
        username = st.text_input("Choose a username*")
        password = st.text_input("Create a password*", type="password")
        confirm = st.text_input("Confirm password*", type="password")
        full_name = st.text_input("Full name (optional)")
        col1, col2 = st.columns(2)
        with col1:
            language = st.selectbox("Language", options=["hi", "hi-en", "en"],
                                    format_func=lambda x: {"hi": "हिन्दी", "hi-en": "हिंग्लिश", "en": "English"}.get(x, x))
        with col2:
            skill_level = st.selectbox("Your level", get_skill_levels())

        if st.form_submit_button("🚀 Create Account", use_container_width=True):
            if not username or not password:
                st.error("Username and password are required")
            elif password != confirm:
                st.error("Passwords don't match")
            elif len(password) < 4:
                st.error("Password must be at least 4 characters")
            else:
                success = db_ops.create_user(username, password, full_name, "", language, skill_level)
                if success:
                    st.success("✅ Account created! Please login.")
                    st.session_state.show_signup = False
                    st.rerun()
                else:
                    st.error("❌ Username already exists. Try another.")

    if st.button("← Back to Login"):
        st.session_state.show_signup = False
        st.rerun()

# ──────────────────────────────────────────────
#  HOME PAGE
# ──────────────────────────────────────────────

def render_home():
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("""
        # 🚀 Bharat AI School
        ## ₹20/माह — पूरा भारत सीखेगा AI!
        """)

        st.markdown("""
        ### 🤖 क्या सीखेंगे आप?
        | Course | Level |
        |--------|-------|
        | 🧠 Machine Learning Zero to Hero | Beginner |
        | 💬 ChatGPT & Prompt Engineering | Beginner |
        | 🌟 Gemini & Google AI Studio | Beginner |
        | 🏗️ Build Your Own AI Agent | Advanced |
        | 💼 Startup & Freelancing with AI | All Levels |

        ### ✨ Features
        - ✅ **Step-by-step chapters** — छोटे-छोटे logical modules
        - ✅ **AI Teacher** — आर्यभट्ट, डॉ. कलाम, चाणक्य से सीखें
        - ✅ **YouTube Links** — हर chapter के लिए video suggestions
        - ✅ **PDF Download** — Notes को PDF में save करें
        - ✅ **Daily Streak 🔥** — Duolingo-style habit building
        - ✅ **₹20/माह** — सबसे सस्ता AI school in India
        """)

    with col2:
        st.markdown("""
        ### 📊 Live Stats
        """)
        # Top leaderboard
        leaderboard = db_ops.get_leaderboard(5)
        if leaderboard:
            st.markdown("#### 🏆 Top Learners")
            html_rows = []
            for i, entry in enumerate(leaderboard, 1):
                rank_emoji = {1: "🥇", 2: "🥈", 3: "🥉"}.get(i, f" {i} ")
                html_rows.append(f"""
                <div class="leaderboard-row">
                    <div style="display: flex; align-items: center; gap: 10px;">
                        <span class="leaderboard-rank">{rank_emoji}</span>
                        <span style="font-weight: 600; color: #0f172a;">{entry['username']}</span>
                    </div>
                    <div style="display: flex; gap: 8px;">
                        <span class="badge badge-streak">🔥 {entry['current_streak']}d</span>
                        <span class="badge badge-xp">⭐ {entry['total_xp']} XP</span>
                    </div>
                </div>
                """)
            st.markdown(f"""
            <div class="leaderboard-container">
                {"".join(html_rows)}
            </div>
            """, unsafe_allow_html=True)

        st.divider()
        st.markdown("### 🎯 Today's Motivation")
        st.info("🌱 **हर दिन एक chapter पढ़ें।**\n\nएक आदत बनाएं, AI सीखें, अपना future बनाएं।")

        if st.button("🚀 आज ही शुरू करें", use_container_width=True):
            if not st.session_state.logged_in:
                st.session_state.show_signup = True
            else:
                st.session_state.page = "courses"
            st.rerun()

# ──────────────────────────────────────────────
#  COURSES PAGE
# ──────────────────────────────────────────────

def render_courses():
    st.markdown("## 📚 All Courses")

    # Filter by level
    levels = ["All"] + get_skill_levels()
    level_filter = st.selectbox("Filter by level", levels, key="course_level_filter")

    courses = db_ops.get_courses(level_filter if level_filter != "All" else None)

    if not courses:
        st.warning("No courses available yet.")
        return

    for course in courses:
        with st.expander(f"**{course['title']}**  ({course['level']}){' 🔓 Free' if course['is_free'] else ' 🔒 Paid'}", expanded=False):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(course.get("description", ""))
                if course.get("career_benefit"):
                    st.markdown(f"💼 **Career:** {course['career_benefit']}")
                if course.get("tech_stack"):
                    st.markdown(f"🛠️ **Tech:** {course['tech_stack']}")
                if course.get("url"):
                    st.markdown(f"🔗 [External Link]({course['url']})")
            with col2:
                # Check if user can access
                can_access = course["is_free"] or db_ops.has_active_subscription(st.session_state.username)

                if can_access:
                    if st.button(f"📖 Start {course['title'][:20]}", key=f"start_{course['id']}", use_container_width=True):
                        st.session_state.current_course_id = course["id"]
                        st.session_state.page = "course_view"
                        st.rerun()
                else:
                    st.button(f"🔒 ₹20/mo", key=f"locked_{course['id']}", disabled=True, use_container_width=True)
                    st.caption("Subscribe to access")

# ──────────────────────────────────────────────
#  COURSE VIEW PAGE
# ──────────────────────────────────────────────

def render_course_view():
    course_id = st.session_state.current_course_id
    if not course_id:
        st.warning("No course selected. Go to Courses page first.")
        return

    course = db_ops.get_course(course_id)
    if not course:
        st.error("Course not found.")
        return

    # Check access
    if not course["is_free"] and not db_ops.has_active_subscription(st.session_state.username):
        st.warning(get_subscription_required_message())
        if st.button("💳 Subscribe Now"):
            st.session_state.page = "profile"
            st.rerun()
        return

    st.markdown(f"## 📖 {course['title']}")
    st.caption(course.get("description", ""))

    # Progress bar
    done, total, pct = db_ops.get_course_progress_pct(st.session_state.username, course_id)
    st.progress(pct / 100.0)
    st.markdown(f"**Progress:** {done}/{total} chapters ({pct}%)")

    # Tabs
    tab1, tab2 = st.tabs(["📚 Chapters", "💬 Chat with AI Teacher"])

    with tab1:
        modules_data = get_modules_with_chapters(course_id)
        if not modules_data:
            st.info("No content yet. Generate syllabus below!")

            # AI Syllabus Generator
            st.markdown("### 🤖 Generate AI Syllabus")
            with st.form("syllabus_form"):
                goal = st.text_input("What do you want to learn?", "Machine Learning from scratch")
                level = st.selectbox("Your level", get_skill_levels(), index=0)
                if st.form_submit_button("🚀 Generate Syllabus"):
                    with st.spinner("AI is creating your personalized syllabus..."):
                        harness = LLMHarness(st.session_state.username, st.session_state.persona)
                        syllabus = harness.generate_syllabus(goal, level)
                        # Save to DB
                        for mod_order, mod in enumerate(syllabus):
                            mid = db_ops.add_module(course_id, mod.get("title", "Module"), mod.get("description", ""), mod_order)
                            for ch_order, ch in enumerate(mod.get("chapters", [])):
                                db_ops.add_chapter(mid, ch.get("title", "Chapter"), ch.get("content", ""), chapter_order=ch_order)
                        st.success("✅ Syllabus generated! Refresh the page.")
                        st.rerun()
        else:
            for mod_data in modules_data:
                mod = mod_data["module"]
                st.markdown(f"### 📘 {mod['title']}")
                if mod.get("description"):
                    st.caption(mod["description"])

                for ch in mod_data["chapters"]:
                    completed = db_ops.is_chapter_completed(st.session_state.username, ch["id"])
                    status = "✅" if completed else "📄"
                    col_a, col_b = st.columns([4, 1])

                    with col_a:
                        st.markdown(f"{status} **{ch['title']}**")

                    with col_b:
                        if st.button("Read", key=f"read_{ch['id']}", use_container_width=True):
                            st.session_state.current_chapter_id = ch["id"]
                            st.rerun()

                    # Show chapter content if selected
                    if st.session_state.get("current_chapter_id") == ch["id"]:
                        render_chapter_detail(ch)

    with tab2:
        render_chat(course_id)

def render_chapter_detail(chapter):
    """Render a single chapter with full content."""
    with st.container(border=True):
        st.markdown(f"### 📖 {chapter['title']}")

        # Content
        has_content = chapter.get("content") and len(chapter["content"].strip()) > 150
        if has_content:
            st.markdown(chapter["content"])
            
            # Allow regenerating lesson with another persona style
            with st.expander("🔄 Reset & Regenerate Lesson"):
                st.caption(f"आप इस chapter को अपने चुने हुए AI Teacher ({st.session_state.persona.capitalize()}) के स्टाइल में दोबारा तैयार कर सकते हैं।")
                if st.button("✨ Regenerate Lesson", key=f"regen_{chapter['id']}", use_container_width=True):
                    with st.spinner("AI Teacher पाठ को नए तरीके से लिख रहे हैं..."):
                        harness = LLMHarness(st.session_state.username, st.session_state.persona)
                        course_title = "AI Course"
                        course = db_ops.get_course(st.session_state.current_course_id)
                        if course:
                            course_title = course["title"]
                        conn = db_ops.get_connection()
                        mod_row = conn.execute("SELECT title, description FROM modules WHERE id=?", (chapter["module_id"],)).fetchone()
                        conn.close()
                        module_title = mod_row["title"] if mod_row else "Getting Started"
                        module_desc = mod_row["description"] if mod_row and mod_row["description"] else ""
                        
                        lesson = harness.generate_chapter_content(
                            course_title=course_title,
                            module_title=module_title,
                            chapter_title=chapter["title"],
                            chapter_description=module_desc or chapter["title"]
                        )
                        db_ops.update_chapter(
                            chapter["id"],
                            content=lesson.get("content", ""),
                            code_example=lesson.get("code_example", ""),
                            youtube_search_term=lesson.get("youtube_search_term", "")
                        )
                        st.success("✅ पाठ सफलतापूर्वक दोबारा तैयार किया गया!")
                        st.rerun()
        else:
            st.info("इस chapter का विस्तृत पाठ (Detailed Lesson) अभी तैयार नहीं है।")
            if st.button("✨ AI Teacher से पाठ तैयार करवाएं (Generate Lesson)", key=f"gen_{chapter['id']}", use_container_width=True):
                with st.spinner("AI Teacher आपके लिए विस्तृत पाठ तैयार कर रहे हैं... इसमें 15-20 सेकंड लग सकते हैं।"):
                    harness = LLMHarness(st.session_state.username, st.session_state.persona)
                    course_title = "AI Course"
                    course = db_ops.get_course(st.session_state.current_course_id)
                    if course:
                        course_title = course["title"]
                    conn = db_ops.get_connection()
                    mod_row = conn.execute("SELECT title, description FROM modules WHERE id=?", (chapter["module_id"],)).fetchone()
                    conn.close()
                    module_title = mod_row["title"] if mod_row else "Getting Started"
                    module_desc = mod_row["description"] if mod_row and mod_row["description"] else ""
                    
                    lesson = harness.generate_chapter_content(
                        course_title=course_title,
                        module_title=module_title,
                        chapter_title=chapter["title"],
                        chapter_description=chapter.get("content") or module_desc or chapter["title"]
                    )
                    db_ops.update_chapter(
                        chapter["id"],
                        content=lesson.get("content", ""),
                        code_example=lesson.get("code_example", ""),
                        youtube_search_term=lesson.get("youtube_search_term", "")
                    )
                    st.success("✅ विस्तृत पाठ तैयार हो गया है! पेज रीलोड हो रहा है...")
                    st.rerun()

        # Code example
        if chapter.get("code_example"):
            with st.expander("💻 Code Example", expanded=True):
                st.code(chapter["code_example"], language="python")

        # YouTube links
        yt_links = get_chapter_youtube_links(chapter["id"])
        if yt_links:
            st.markdown("### 📺 YouTube Tutorials")
            for link in yt_links:
                st.markdown(f"- [{link['title']}]({link['url']})")
        elif chapter.get("youtube_search_term"):
            st.markdown("### 📺 YouTube Tutorials")
            search_term = chapter["youtube_search_term"]
            from urllib.parse import quote
            query = quote(f"{search_term} tutorial hindi")
            url = f"https://www.youtube.com/results?search_query={query}"
            st.markdown(f"👉 **[YouTube पर '{search_term}' के Tutorials देखें]({url})**")

        # Curated links from helper
        curated = get_curated_links(chapter["title"])
        if curated:
            st.markdown("### 🎯 Recommended Playlists")
            for link in curated:
                st.markdown(f"- [{link['title']}]({link['url']})")

        # Actions
        col_a, col_b = st.columns([1, 1])
        with col_a:
            if st.button("✅ Mark Complete", key=f"complete_{chapter['id']}", use_container_width=True):
                course_id = st.session_state.current_course_id
                module_id = chapter["module_id"]
                db_ops.mark_chapter_complete(st.session_state.username, course_id, module_id, chapter["id"])
                st.success("🎉 Chapter completed! +10 XP")
                st.rerun()

        with col_b:
            # PDF download
            pdf_chapter_data = {
                "title": chapter["title"],
                "content": chapter.get("content", ""),
                "code_example": chapter.get("code_example", ""),
                "youtube_search_term": chapter.get("youtube_search_term", ""),
            }
            pdf_path = generate_chapter_pdf(pdf_chapter_data, st.session_state.username)
            with open(pdf_path, "rb") as f:
                st.download_button(
                    "📥 Download PDF",
                    data=f,
                    file_name=os.path.basename(pdf_path),
                    mime="application/pdf",
                    use_container_width=True,
                )

# ──────────────────────────────────────────────
#  CHAT INTERFACE
# ──────────────────────────────────────────────

def render_chat(course_id=0):
    """Chat with AI Teacher for the current course."""
    st.markdown("### 💬 Ask Your AI Teacher")

    # Check subscription for chat
    course = db_ops.get_course(course_id) if course_id else None
    if course and not course["is_free"] and not db_ops.has_active_subscription(st.session_state.username):
        st.warning("💬 Chat with AI Teacher is a paid feature. Subscribe for ₹20/month!")
        return

    # Show chat history
    chat_history = db_ops.get_chat_history(st.session_state.username, course_id, limit=30)
    for msg in chat_history:
        role = msg["role"]
        content = msg["content"]
        if role == "user":
            st.chat_message("user").markdown(content)
        else:
            st.chat_message("assistant").markdown(content)

    # Chat input
    prompt = st.chat_input("Ask anything about this course...")
    if prompt:
        st.chat_message("user").markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("🧠 Thinking..."):
                harness = LLMHarness(
                    st.session_state.username,
                    st.session_state.persona,
                    language="Hinglish"
                )
                result = harness.process_message(prompt, course_id)

                # Display reply
                st.markdown(result["reply"])

                # Show YouTube links if any
                if result["youtube_links"]:
                    st.markdown("### 📺 YouTube Search Results")
                    for term, url in zip(result["youtube_terms"], result["youtube_links"]):
                        st.markdown(f"- 🎬 [{term}]({url})")

                # Show quiz if any
                if result["quiz_questions"]:
                    st.markdown("### 📝 Quick Quiz")
                    for q in result["quiz_questions"]:
                        st.markdown(f"- {q['question']}")

        st.rerun()

# ──────────────────────────────────────────────
#  PROFILE PAGE
# ──────────────────────────────────────────────

def render_profile():
    st.markdown("## 👤 My Profile")

    user = db_ops.get_user(st.session_state.username)
    habits = db_ops.get_habits(st.session_state.username)

    if not user:
        st.error("User not found")
        return

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("### 📋 Account Info")
        st.markdown(f"**Name:** {user.get('full_name') or '—'}")
        st.markdown(f"**Username:** {st.session_state.username}")
        st.markdown(f"**Level:** {user.get('skill_level', 'Beginner')}")
        st.markdown(f"**Language:** {user.get('language', 'hi')}")

        # Edit profile
        with st.expander("✏️ Edit Profile"):
            with st.form("edit_profile"):
                name = st.text_input("Full name", value=user.get("full_name", ""))
                lang = st.selectbox("Language", ["hi", "hi-en", "en"],
                                    index=["hi", "hi-en", "en"].index(user.get("language", "hi")))
                level = st.selectbox("Skill level", get_skill_levels(),
                                     index=get_skill_levels().index(user.get("skill_level", "Beginner")))
                if st.form_submit_button("Save"):
                    db_ops.update_user(st.session_state.username, full_name=name, language=lang, skill_level=level)
                    st.success("✅ Profile updated!")
                    st.rerun()

    with col2:
        st.markdown("### 🔥 Streak & XP")
        if habits:
            st.markdown(format_streak_display(habits["current_streak"], habits["total_xp"]), unsafe_allow_html=True)

        # Subscription status
        st.divider()
        st.markdown("### 💳 Subscription")
        sub_status = check_subscription_status(st.session_state.username)
        if sub_status["active"]:
            st.success(f"✅ Active! Expires in {sub_status['days_left']} days")
            st.caption(f"Plan: {sub_status['plan']} | Paid: ₹{sub_status['amount_paid']}")
        elif sub_status.get("pending"):
            st.warning("⏳ Verification Pending")
            st.info(f"Payment of ₹{int(sub_status['amount_paid'])} is under review by admin.\n\n**Transaction ID:** `{sub_status['transaction_id']}`\n\nAccess will be granted shortly!")
        else:
            st.warning("🔒 No active subscription")
            render_payment_section()

def render_payment_section():
    """Payment form for ₹20/month subscription."""
    st.markdown("### 🎯 Subscribe for ₹20/month")
    st.markdown("Get access to: All courses, AI Chat, PDF downloads, Streak rewards")

    # UPI details
    upi = get_upi_payment_details()
    upi_url = generate_upi_url()

    col_a, col_b = st.columns([1, 1])
    with col_a:
        st.markdown(f"""
        **UPI ID:** `{upi['upi_id']}`
        **Amount:** ₹{int(upi['amount'])}
        **Name:** {upi['name']}

        Scan QR or use UPI app to pay.
        """)
        st.code(upi_url, language="text")

    with col_b:
        st.markdown("**UPI QR Code**")
        from urllib.parse import quote
        qr_api_url = f"https://api.qrserver.com/v1/create-qr-code/?size=250x250&data={quote(upi_url)}"
        st.image(qr_api_url, width=200, caption="Scan QR using any UPI App (GPay, PhonePe, Paytm)")

    st.divider()
    st.markdown("### ✅ Confirm Payment")
    with st.form("payment_confirm"):
        txn_id = st.text_input("Enter UPI Transaction ID (UTR)")
        if st.form_submit_button("Verify Payment", use_container_width=True):
            if txn_id:
                record_payment(st.session_state.username, 20.0, txn_id)
                st.success("✅ Payment submitted! Admin will verify within 24 hours.")
                st.info("Meanwhile, enjoy your free courses!")
                st.rerun()
            else:
                st.error("Please enter transaction ID")

# ──────────────────────────────────────────────
#  ADMIN PAGE
# ──────────────────────────────────────────────

def render_admin():
    """Admin dashboard for managing users, courses, payments."""
    user = db_ops.get_user(st.session_state.username)
    if not user or not user.get("is_admin"):
        st.error("🔒 Admin access only")
        return

    st.markdown("## 🔧 Admin Dashboard")

    tab1, tab2, tab3, tab4 = st.tabs(["Users", "Payments", "Content", "Seed Data"])

    with tab1:
        st.markdown("### 👥 All Users")
        users = db_ops.get_all_users()
        for u in users:
            st.markdown(f"- {u['username']} ({u.get('full_name', '—')}) — {'Admin' if u['is_admin'] else 'User'} — joined {u.get('created_at', '')[:10]}")

    with tab2:
        st.markdown("### 💳 All Subscriptions")
        subs = db_ops.get_all_subscriptions()
        if subs:
            for s in subs:
                st.markdown(f"- **{s['username']}** — ₹{s['amount_paid']} — {s['payment_method']} — {'✅ Verified' if s['verified_by_admin'] else '⏳ Pending'} — Txn: {s.get('transaction_id', '—')}")
        else:
            st.info("No subscriptions yet.")

        # Verify a payment
        st.divider()
        st.markdown("### ✅ Verify Payment")
        with st.form("verify_payment"):
            txn = st.text_input("Transaction ID to verify")
            if st.form_submit_button("Verify"):
                db_ops.verify_subscription(txn)
                st.success(f"✅ Transaction {txn} verified!")
                st.rerun()

    with tab3:
        st.markdown("### 📝 Manage Content")
        st.info("Content management coming in next version. For now, use DB directly or seed data below.")

    with tab4:
        st.markdown("### 🌱 Seed Demo Content")
        if st.button("Seed Sample Chapters", use_container_width=True):
            # Create sample chapters for first course
            courses = db_ops.get_courses()
            if courses:
                c = courses[0]
                # Add module
                mid = db_ops.add_module(c["id"], "Getting Started", "First steps in AI", 0)
                db_ops.add_chapter(mid, "What is Artificial Intelligence?",
                                   "AI means machines that can think and learn.\n\n**Examples:**\n- Chatbots like ChatGPT\n- Self-driving cars\n- Face recognition on phones\n\nAI is divided into:\n1. **Narrow AI** — one task (e.g., Chess AI)\n2. **General AI** — human-level (still research)",
                                   'print("Hello AI World!")\nprint("AI is the future of technology.")',
                                   "what is artificial intelligence explained simply",
                                   0)
                db_ops.add_chapter(mid, "History of AI",
                                   "1950: Alan Turing asked 'Can machines think?'\n1956: Dartmouth Conference — AI born\n1997: Deep Blue beats Kasparov\n2012: Deep Learning revolution\n2022: ChatGPT changes everything",
                                   "# Key milestones\nyears = [1950, 1956, 1997, 2012, 2022]\nevents = ['Turing Test', 'AI born', 'Chess win', 'Deep Learning', 'ChatGPT']\nfor y, e in zip(years, events):\n    print(f'{y}: {e}')",
                                   "history of artificial intelligence timeline",
                                   1)
                st.success("✅ Sample chapters created!")
                st.rerun()

    # Logout from admin
    if st.button("🔒 Lock Admin", use_container_width=True):
        st.session_state.page = "home"
        st.rerun()

# ──────────────────────────────────────────────
#  MAIN APP ROUTER
# ──────────────────────────────────────────────

def main():
    render_sidebar()

    # If not logged in → show auth pages
    if not st.session_state.logged_in:
        if st.session_state.get("show_signup"):
            render_signup()
        else:
            render_login()
        return

    # Route to the correct page
    page = st.session_state.get("page", "home")

    if page == "home":
        render_home()
    elif page == "courses":
        render_courses()
    elif page == "course_view":
        render_course_view()
    elif page == "profile":
        render_profile()
    elif page == "admin":
        render_admin()
    else:
        render_home()

if __name__ == "__main__":
    main()
