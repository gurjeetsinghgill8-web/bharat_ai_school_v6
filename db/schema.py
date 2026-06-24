"""
Bharat AI School V6 — Database Schema (SQLite)
Defines all tables: users, courses, chapters, progress, habits, payments, chat history.
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "bharat_ai_school.db")

def get_connection():
    """Get a thread-safe SQLite connection."""
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn

def init_db():
    """Create all tables if they don't exist."""
    conn = get_connection()
    cursor = conn.cursor()

    # ── Users ──
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            full_name TEXT DEFAULT '',
            email TEXT DEFAULT '',
            language TEXT DEFAULT 'hi',
            skill_level TEXT DEFAULT 'Beginner',
            is_admin INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # ── Courses (hardcoded catalog + custom) ──
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT DEFAULT '',
            provider TEXT DEFAULT 'Bharat AI School',
            level TEXT DEFAULT 'Beginner',
            is_free INTEGER DEFAULT 1,
            url TEXT DEFAULT '',
            career_benefit TEXT DEFAULT '',
            tech_stack TEXT DEFAULT '',
            is_custom INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # ── Modules (a course has modules, modules have chapters) ──
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS modules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            description TEXT DEFAULT '',
            module_order INTEGER DEFAULT 0,
            FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE
        )
    """)

    # ── Chapters (the actual lesson content) ──
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chapters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            module_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            content TEXT DEFAULT '',
            code_example TEXT DEFAULT '',
            youtube_search_term TEXT DEFAULT '',
            chapter_order INTEGER DEFAULT 0,
            FOREIGN KEY (module_id) REFERENCES modules(id) ON DELETE CASCADE
        )
    """)

    # ── User Progress (which chapters a user completed) ──
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            course_id INTEGER NOT NULL,
            module_id INTEGER,
            chapter_id INTEGER,
            completed INTEGER DEFAULT 0,
            completed_at TIMESTAMP,
            FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE,
            UNIQUE(username, chapter_id)
        )
    """)

    # ── Chat History (scoped by username + course) ──
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            course_id INTEGER DEFAULT 0,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # ── User Habits (streak, xp) ──
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            current_streak INTEGER DEFAULT 0,
            best_streak INTEGER DEFAULT 0,
            last_activity_date TEXT DEFAULT '',
            total_xp INTEGER DEFAULT 0,
            daily_goal INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # ── Subscriptions (₹20/month) ──
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subscriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            plan_type TEXT DEFAULT 'monthly',
            amount_paid REAL DEFAULT 20.0,
            start_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            end_date TIMESTAMP,
            is_active INTEGER DEFAULT 0,
            payment_method TEXT DEFAULT 'UPI',
            transaction_id TEXT DEFAULT '',
            verified_by_admin INTEGER DEFAULT 0,
            UNIQUE(username, transaction_id)
        )
    """)

    # ── YouTube Links (curated per chapter, manually added) ──
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS youtube_links (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chapter_id INTEGER NOT NULL,
            title TEXT DEFAULT '',
            url TEXT NOT NULL,
            language TEXT DEFAULT 'hi',
            added_by TEXT DEFAULT 'admin',
            FOREIGN KEY (chapter_id) REFERENCES chapters(id) ON DELETE CASCADE
        )
    """)

    conn.commit()
    conn.close()
    print(f"✅ Database initialized at {DB_PATH}")

if __name__ == "__main__":
    init_db()
