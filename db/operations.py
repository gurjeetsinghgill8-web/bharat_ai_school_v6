"""
Bharat AI School V6 — Database Operations
All CRUD functions: users, progress, habits, subscriptions, chat.
"""
import hashlib
from datetime import datetime, timedelta
from .schema import get_connection

# ──────────────────────────────────────────────
#  USER OPERATIONS
# ──────────────────────────────────────────────

def create_user(username, password, full_name="", email="", language="hi", skill_level="Beginner", is_admin=0):
    conn = get_connection()
    try:
        pwd_hash = hashlib.sha256(password.encode()).hexdigest()
        conn.execute(
            "INSERT INTO users (username, password_hash, full_name, email, language, skill_level, is_admin) VALUES (?,?,?,?,?,?,?)",
            (username, pwd_hash, full_name, email, language, skill_level, is_admin)
        )
        conn.commit()
        # auto-create habit row
        conn.execute("INSERT OR IGNORE INTO user_habits (username) VALUES (?)", (username,))
        conn.commit()
        return True
    except Exception as e:
        print(f"User create error: {e}")
        return False
    finally:
        conn.close()

def verify_user(username, password):
    conn = get_connection()
    pwd_hash = hashlib.sha256(password.encode()).hexdigest()
    row = conn.execute("SELECT * FROM users WHERE username=? AND password_hash=?", (username, pwd_hash)).fetchone()
    conn.close()
    return dict(row) if row else None

def get_user(username):
    conn = get_connection()
    row = conn.execute("SELECT * FROM users WHERE username=?", (username,)).fetchone()
    conn.close()
    return dict(row) if row else None

def update_user(username, **kwargs):
    allowed = {"full_name", "email", "language", "skill_level"}
    sets = {k: v for k, v in kwargs.items() if k in allowed}
    if not sets:
        return False
    conn = get_connection()
    sets["username"] = username
    query = "UPDATE users SET " + ", ".join(f"{k}=?" for k in sets if k != "username") + " WHERE username=?"
    vals = [v for k, v in sets.items() if k != "username"] + [username]
    conn.execute(query, vals)
    conn.commit()
    conn.close()
    return True

# ──────────────────────────────────────────────
#  COURSE / MODULE / CHAPTER OPERATIONS
# ──────────────────────────────────────────────

def get_courses(level=None):
    conn = get_connection()
    if level and level != "All":
        rows = conn.execute("SELECT * FROM courses WHERE level=? ORDER BY id", (level,)).fetchall()
    else:
        rows = conn.execute("SELECT * FROM courses ORDER BY id").fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_course(course_id):
    conn = get_connection()
    row = conn.execute("SELECT * FROM courses WHERE id=?", (course_id,)).fetchone()
    conn.close()
    return dict(row) if row else None

def add_course(title, description, level, provider="Bharat AI School", is_free=1, url="", career_benefit="", tech_stack=""):
    conn = get_connection()
    conn.execute(
        "INSERT INTO courses (title, description, provider, level, is_free, url, career_benefit, tech_stack) VALUES (?,?,?,?,?,?,?,?)",
        (title, description, provider, level, is_free, url, career_benefit, tech_stack)
    )
    conn.commit()
    course_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    conn.close()
    return course_id

def get_modules(course_id):
    conn = get_connection()
    rows = conn.execute("SELECT * FROM modules WHERE course_id=? ORDER BY module_order", (course_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def add_module(course_id, title, description="", module_order=0):
    conn = get_connection()
    conn.execute("INSERT INTO modules (course_id, title, description, module_order) VALUES (?,?,?,?)",
                 (course_id, title, description, module_order))
    conn.commit()
    mid = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    conn.close()
    return mid

def get_chapters(module_id):
    conn = get_connection()
    rows = conn.execute("SELECT * FROM chapters WHERE module_id=? ORDER BY chapter_order", (module_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_chapter(chapter_id):
    conn = get_connection()
    row = conn.execute("SELECT * FROM chapters WHERE id=?", (chapter_id,)).fetchone()
    conn.close()
    return dict(row) if row else None

def add_chapter(module_id, title, content="", code_example="", youtube_search_term="", chapter_order=0):
    conn = get_connection()
    conn.execute(
        "INSERT INTO chapters (module_id, title, content, code_example, youtube_search_term, chapter_order) VALUES (?,?,?,?,?,?)",
        (module_id, title, content, code_example, youtube_search_term, chapter_order)
    )
    conn.commit()
    cid = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    conn.close()
    return cid

def update_chapter(chapter_id, **kwargs):
    allowed = {"title", "content", "code_example", "youtube_search_term"}
    sets = {k: v for k, v in kwargs.items() if k in allowed}
    if not sets:
        return False
    conn = get_connection()
    query = "UPDATE chapters SET " + ", ".join(f"{k}=?" for k in sets) + " WHERE id=?"
    vals = list(sets.values()) + [chapter_id]
    conn.execute(query, vals)
    conn.commit()
    conn.close()
    return True

# ──────────────────────────────────────────────
#  USER PROGRESS
# ──────────────────────────────────────────────

def mark_chapter_complete(username, course_id, module_id, chapter_id):
    conn = get_connection()
    conn.execute(
        "INSERT OR REPLACE INTO user_progress (username, course_id, module_id, chapter_id, completed, completed_at) VALUES (?,?,?,?,1,?)",
        (username, course_id, module_id, chapter_id, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()
    # award XP
    add_xp(username, 10)
    # update learning daily streak
    update_streak(username)

def is_chapter_completed(username, chapter_id):
    conn = get_connection()
    row = conn.execute(
        "SELECT completed FROM user_progress WHERE username=? AND chapter_id=? AND completed=1",
        (username, chapter_id)
    ).fetchone()
    conn.close()
    return row is not None

def get_user_progress(username, course_id):
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM user_progress WHERE username=? AND course_id=? AND completed=1",
        (username, course_id)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_course_progress_pct(username, course_id):
    """Returns (completed_chapters, total_chapters, percentage)."""
    conn = get_connection()
    total = conn.execute("""
        SELECT COUNT(*) FROM chapters c
        JOIN modules m ON c.module_id = m.id
        WHERE m.course_id = ?
    """, (course_id,)).fetchone()[0]
    done = conn.execute(
        "SELECT COUNT(*) FROM user_progress WHERE username=? AND course_id=? AND completed=1",
        (username, course_id)
    ).fetchone()[0]
    conn.close()
    pct = round((done / total) * 100, 1) if total > 0 else 0
    return done, total, pct

# ──────────────────────────────────────────────
#  CHAT HISTORY
# ──────────────────────────────────────────────

def save_message(username, role, content, course_id=0):
    conn = get_connection()
    conn.execute("INSERT INTO chat_history (username, course_id, role, content) VALUES (?,?,?,?)",
                 (username, course_id, role, content))
    conn.commit()
    conn.close()

def get_chat_history(username, course_id=0, limit=20):
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM chat_history WHERE username=? AND course_id=? ORDER BY created_at DESC LIMIT ?",
        (username, course_id, limit)
    ).fetchall()
    conn.close()
    return [dict(r) for r in reversed(rows)]

def clear_chat_history(username, course_id=0):
    conn = get_connection()
    conn.execute("DELETE FROM chat_history WHERE username=? AND course_id=?", (username, course_id))
    conn.commit()
    conn.close()

# ──────────────────────────────────────────────
#  HABITS / STREAK / XP
# ──────────────────────────────────────────────

def get_habits(username):
    conn = get_connection()
    row = conn.execute("SELECT * FROM user_habits WHERE username=?", (username,)).fetchone()
    conn.close()
    return dict(row) if row else None

def update_streak(username):
    habits = get_habits(username)
    if not habits:
        return None
    today = datetime.now().strftime("%Y-%m-%d")
    last = habits["last_activity_date"]
    streak = habits["current_streak"]
    best = habits["best_streak"]

    if last == today:
        return habits  # already updated today

    if last:
        last_dt = datetime.strptime(last, "%Y-%m-%d")
        diff = (datetime.now() - last_dt).days
        if diff == 1:
            streak += 1  # consecutive!
        else:
            streak = 1   # reset
    else:
        streak = 1  # first ever

    best = max(best, streak)
    conn = get_connection()
    conn.execute(
        "UPDATE user_habits SET current_streak=?, best_streak=?, last_activity_date=? WHERE username=?",
        (streak, best, today, username)
    )
    conn.commit()
    conn.close()
    habits["current_streak"] = streak
    habits["best_streak"] = best
    habits["last_activity_date"] = today
    return habits

def add_xp(username, points):
    conn = get_connection()
    conn.execute("UPDATE user_habits SET total_xp = total_xp + ? WHERE username=?", (points, username))
    conn.commit()
    conn.close()

def get_leaderboard(limit=10):
    conn = get_connection()
    rows = conn.execute(
        "SELECT username, current_streak, best_streak, total_xp FROM user_habits ORDER BY total_xp DESC LIMIT ?",
        (limit,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]

# ──────────────────────────────────────────────
#  SUBSCRIPTIONS (₹20/month)
# ──────────────────────────────────────────────

def create_subscription(username, amount=20.0, method="UPI", txn_id=""):
    conn = get_connection()
    end_date = (datetime.now() + timedelta(days=30)).isoformat()
    conn.execute(
        "INSERT INTO subscriptions (username, amount_paid, end_date, payment_method, transaction_id, is_active) VALUES (?,?,?,?,?,0)",
        (username, amount, end_date, method, txn_id)
    )
    conn.commit()
    conn.close()

def get_active_subscription(username):
    conn = get_connection()
    row = conn.execute(
        "SELECT * FROM subscriptions WHERE username=? AND is_active=1 AND end_date > datetime('now') ORDER BY end_date DESC LIMIT 1",
        (username,)
    ).fetchone()
    conn.close()
    return dict(row) if row else None

def get_pending_subscription(username):
    conn = get_connection()
    row = conn.execute(
        "SELECT * FROM subscriptions WHERE username=? AND verified_by_admin=0 AND is_active=0 ORDER BY start_date DESC LIMIT 1",
        (username,)
    ).fetchone()
    conn.close()
    return dict(row) if row else None

def has_active_subscription(username):
    sub = get_active_subscription(username)
    return sub is not None

def get_all_subscriptions():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM subscriptions ORDER BY start_date DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]

# ──────────────────────────────────────────────
#  YOUTUBE LINKS
# ──────────────────────────────────────────────

def get_youtube_links(chapter_id):
    conn = get_connection()
    rows = conn.execute("SELECT * FROM youtube_links WHERE chapter_id=?", (chapter_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def add_youtube_link(chapter_id, title, url, language="hi"):
    conn = get_connection()
    conn.execute("INSERT INTO youtube_links (chapter_id, title, url, language) VALUES (?,?,?,?)",
                 (chapter_id, title, url, language))
    conn.commit()
    conn.close()

# ──────────────────────────────────────────────
#  ADMIN HELPERS
# ──────────────────────────────────────────────

def get_all_users():
    conn = get_connection()
    rows = conn.execute("SELECT id, username, full_name, email, language, skill_level, is_admin, created_at FROM users ORDER BY created_at DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]

def verify_subscription(txn_id):
    conn = get_connection()
    start_date = datetime.now().isoformat()
    end_date = (datetime.now() + timedelta(days=30)).isoformat()
    conn.execute(
        "UPDATE subscriptions SET verified_by_admin=1, is_active=1, start_date=?, end_date=? WHERE transaction_id=?",
        (start_date, end_date, txn_id)
    )
    conn.commit()
    conn.close()
