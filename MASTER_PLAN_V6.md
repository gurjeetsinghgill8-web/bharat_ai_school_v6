# 🚀 Bharat AI School V6 — Master Plan
## "₹20/माह — पूरा भारत सीखेगा AI"

---

## 🎯 Vision
एक ऐसा AI शिक्षा प्लेटफ़ॉर्म जो **₹20 प्रति माह** में पूरे भारत को step-by-step Machine Learning, AI, ChatGPT, Gemini, और सॉफ़्टवेयर डेवलपमेंट सिखाए।

## 🏗️ Architecture: Harness Engineering

```
┌─────────────┐     ┌──────────────────┐     ┌─────────────┐
│  app.py     │────▶│ harness/         │────▶│ utils/      │
│  (Streamlit)│     │ llm_harness.py   │     │ groq_client │
│  UI Layer   │◀────│ (Orchestrator)   │◀────│ (LLM API)   │
└─────────────┘     └──────────────────┘     └─────────────┘
                          │
                    ┌─────┴──────┐
                    │            │
              ┌─────▼──┐  ┌─────▼──────┐
              │ db/    │  │ features/  │
              │ schema │  │ curriculum │
              │ ops    │  │ habit      │
              └────────┘  │ payment    │
                          │ youtube    │
                          └────────────┘
```

## 📂 Project Structure

```
bharat_ai_school_v6/
├── app.py                    # Main Streamlit UI
├── harness/                  # 🧠 Harness Engineering Layer
│   ├── __init__.py
│   ├── llm_harness.py        # Central orchestrator
│   ├── system_prompts.py     # Teacher personas
│   └── tools.py              # Tool definitions
├── db/
│   ├── __init__.py
│   ├── schema.py             # SQLite tables
│   └── operations.py         # CRUD functions
├── features/                 # 🧩 Feature modules
│   ├── __init__.py
│   ├── curriculum.py         # Course catalog + syllabus
│   ├── habit_engine.py       # Streak + XP
│   ├── mentor.py             # Project mentor
│   ├── youtube_helper.py     # YouTube links
│   └── payment.py            # ₹20/month subscription
├── utils/
│   ├── __init__.py
│   ├── groq_client.py        # LLM API client
│   ├── pdf_generator.py      # PDF output
│   └── helpers.py            # Utilities
├── requirements.txt
├── .env.example
└── MASTER_PLAN_V6.md
```

## 📊 Database Schema

- `users` — Accounts, login, admin flag
- `courses` — Course catalog (free + paid)
- `modules` — Course modules (ordering)
- `chapters` — Lesson content + code + YouTube search
- `user_progress` — Completion tracking
- `chat_history` — AI teacher conversations
- `user_habits` — Streak, XP, daily goals
- `subscriptions` — ₹20/month payment records
- `youtube_links` — Curated video URLs per chapter

## ✨ Current Features (V6.0 MVP)

### ✅ Done
- Complete DB schema + CRUD operations
- Harness orchestrator (UI ↔ LLM ↔ DB pipeline)
- 4 Teacher personas: Bharat AI Guru, Aryabhatta, Dr. Kalam, Chanakya
- Course catalog (7 built-in courses)
- AI Syllabus generator (personalized)
- Chapter system with progress tracking
- YouTube link suggestions (curated + AI-generated)
- PDF generation (chapter notes + certificates)
- Duolingo-style streak + XP system
- ₹20/month UPI payment system
- Admin dashboard (users, payments, seed data)
- Streamlit UI (Home, Courses, Course View, Chat, Profile, Admin)

### 🔜 Next (V6.1)
- Razorpay auto-payment integration
- Multi-language support (full Hindi, English)
- Mobile-responsive design
- Community leaderboard
- Tiffin defense system concept
- Course marketplace

## 💰 Business Model

| Tier | Price | Features |
|------|-------|----------|
| Free | ₹0 | 3 demo chapters, 1 course preview |
| Monthly | ₹20 | Full curriculum, AI Chat, PDF, Streaks |
| Premium (Future) | ₹99 | Live classes, Certificate, Project review |

## 👨‍🏫 Teacher Personas

| Teacher | Style | Best For |
|---------|-------|----------|
| 🤖 Bharat AI Guru | Friendly, beginner | First-time learners |
| 🧮 Aryabhatta | Mathematical, formula-based | Logic & algorithms |
| 🚀 Dr. Kalam | Inspirational, visionary | Career & motivation |
| 📜 Chanakya | Strategic, money-focused | Freelancing & startups |

## 🛠️ Tech Stack

- **Python 3.10+** — Core language
- **Streamlit** — Web UI framework
- **Groq API (Llama 3.1 8B)** — LLM inference
- **SQLite** — Local database
- **fpdf2** — PDF generation
- **requests** — API calls

## 🚀 How to Run

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Copy env and add your Groq API key
cp .env.example .env
# Edit .env: GROQ_API_KEY=your_key_here

# 3. Run the app
streamlit run app.py
```

## 🌱 Created
**Date:** June 22, 2026
**By:** Dr. Gurjas Singh Gill
**Mission:** AI education for every Indian at ₹20/month
