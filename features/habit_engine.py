"""
Bharat AI School V6 — Habit & Streak Engine
Duolingo-style daily learning habit system.
"""
from db import operations as db_ops

def get_streak_badge(days: int) -> str:
    """Return emoji badge based on streak length."""
    if days >= 365:
        return "👑"  # King
    elif days >= 180:
        return "🎖️"  # Medal
    elif days >= 90:
        return "🏆"  # Trophy
    elif days >= 30:
        return "⭐"  # Star
    elif days >= 14:
        return "🔥🔥"  # Double fire
    elif days >= 7:
        return "🔥"  # Fire
    elif days >= 3:
        return "💪"  # Strength
    else:
        return "🌱"  # Seed

def get_streak_message(streak: int) -> str:
    """Encouraging message based on streak."""
    if streak == 0:
        return "आज शुरू करें! पहला chapter पढ़ें। 📖"
    elif streak == 1:
        return "पहला दिन! कल फिर आना। 🔥"
    elif streak == 3:
        return "लगातार 3 दिन! जबरदस्त शुरुआत! 💪"
    elif streak == 7:
        return "7 दिन की streak! आप रुकने वाले नहीं हो! 🔥"
    elif streak == 14:
        return "14 दिन! आधा महीना लगातार सीख रहे हो! 🔥🔥"
    elif streak == 30:
        return "30 दिन! आपने एक आदत बना ली है! ⭐"
    elif streak >= 100:
        return f"{streak} दिन! आप एक PRO learner हो! 🏆"
    else:
        return f"लगातार {streak} दिन! शानदार! 💪"

def get_xp_level(total_xp: int) -> dict:
    """Calculate level based on total XP."""
    level = total_xp // 100 + 1
    xp_in_level = total_xp % 100
    return {
        "level": level,
        "xp_in_level": xp_in_level,
        "xp_to_next": 100 - xp_in_level,
        "total_xp": total_xp,
    }

def format_streak_display(streak: int, total_xp: int) -> str:
    """Return a formatted HTML streak and XP display card."""
    badge = get_streak_badge(streak)
    level_info = get_xp_level(total_xp)
    progress_pct = level_info['xp_in_level']
    message = get_streak_message(streak)
    
    return f"""
    <div style="padding: 20px; border-radius: 12px; background: rgba(31, 41, 55, 0.4); border: 1px solid rgba(255, 255, 255, 0.05); margin-bottom: 20px;">
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px;">
            <div style="display: flex; align-items: center; gap: 8px;">
                <span style="font-size: 1.5em;">{badge}</span>
                <span style="font-weight: 700; font-size: 1.1em; color: #ffffff;">{streak} दिन की Streak</span>
            </div>
            <span class="badge badge-xp">Level {level_info['level']}</span>
        </div>
        <div style="font-size: 0.9em; color: #9ca3af; margin-bottom: 8px;">
            XP Progress: {progress_pct}/100 XP (Next Level in {level_info['xp_to_next']} XP)
        </div>
        <div style="background: rgba(255, 255, 255, 0.05); height: 8px; border-radius: 4px; overflow: hidden; margin-bottom: 14px;">
            <div style="background: linear-gradient(90deg, #6366f1, #a855f7); width: {progress_pct}%; height: 100%; border-radius: 4px;"></div>
        </div>
        <div style="font-size: 0.95em; color: #cbd5e1; font-weight: 500; font-style: italic;">
            {message}
        </div>
    </div>
    """
