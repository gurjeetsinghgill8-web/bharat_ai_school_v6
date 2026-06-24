"""
Bharat AI School V6 — UI Style Guidelines & CSS Injection
Premium Dark/Glassmorphism theme system.
"""
import streamlit as st

def inject_custom_styles():
    """Inject custom CSS styles into the Streamlit application."""
    st.markdown(
        """
        <style>
        /* ── Core Font & Typography ── */
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Poppins:wght@400;500;600;700&display=swap');
        
        /* Base styles */
        .stApp {
            font-family: 'Outfit', sans-serif;
            background: radial-gradient(circle at 50% 50%, #111827 0%, #030712 100%) !important;
            color: #f3f4f6 !important;
        }
        
        h1, h2, h3, h4, h5, h6 {
            font-family: 'Outfit', sans-serif;
            font-weight: 700 !important;
            color: #ffffff !important;
            letter-spacing: -0.02em;
        }
        
        /* ── Sidebar Styling ── */
        section[data-testid="stSidebar"] {
            background-color: #0b0f19 !important;
            border-right: 1px solid rgba(255, 255, 255, 0.05) !important;
        }
        
        section[data-testid="stSidebar"] hr {
            border-color: rgba(255, 255, 255, 0.08) !important;
        }
        
        /* ── Glassmorphism Cards ── */
        .glass-card {
            background: rgba(17, 24, 39, 0.7);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 20px;
            box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.7);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        .glass-card:hover {
            transform: translateY(-2px);
            border-color: rgba(99, 102, 241, 0.4);
            box-shadow: 0 20px 40px -15px rgba(99, 102, 241, 0.15);
        }
        
        /* Course/Chapter List Items */
        .list-item {
            background: rgba(31, 41, 55, 0.4);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 12px;
            padding: 16px;
            margin-bottom: 12px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            transition: background 0.2s;
        }
        
        .list-item:hover {
            background: rgba(31, 41, 55, 0.6);
            border-color: rgba(255, 255, 255, 0.1);
        }
        
        /* ── Modern Buttons ── */
        .stButton>button {
            background: linear-gradient(135deg, #4f46e5 0%, #3730a3 100%) !important;
            color: #ffffff !important;
            border: none !important;
            border-radius: 10px !important;
            padding: 10px 24px !important;
            font-weight: 600 !important;
            box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3) !important;
            transition: all 0.2s ease !important;
        }
        
        .stButton>button:hover {
            transform: translateY(-1px) !important;
            box-shadow: 0 6px 20px rgba(79, 70, 229, 0.4) !important;
            background: linear-gradient(135deg, #6366f1 0%, #4338ca 100%) !important;
        }
        
        .stButton>button:active {
            transform: translateY(1px) !important;
        }
        
        /* Secondary or plain buttons inside Streamlit forms */
        div[data-testid="stFormSubmitButton"] button {
            background: linear-gradient(135deg, #10b981 0%, #047857 100%) !important;
            box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3) !important;
        }
        div[data-testid="stFormSubmitButton"] button:hover {
            background: linear-gradient(135deg, #34d399 0%, #059669 100%) !important;
            box-shadow: 0 6px 20px rgba(16, 185, 129, 0.4) !important;
        }
        
        /* ── Streamlit Chat Layout Styling ── */
        div[data-testid="stChatMessage"] {
            background-color: rgba(17, 24, 39, 0.6) !important;
            border: 1px solid rgba(255, 255, 255, 0.05) !important;
            border-radius: 14px !important;
            padding: 16px !important;
            margin-bottom: 12px !important;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2) !important;
            backdrop-filter: blur(8px);
        }
        
        div[data-testid="stChatMessage"]:has(span[data-testid="stChatMessageAvatar"]) {
            border-left: 3px solid #6366f1 !important;
        }
        
        div[data-testid="stChatMessage"][data-testid="stChatMessage-user"] {
            background-color: rgba(31, 41, 55, 0.6) !important;
            border-left: 3px solid #10b981 !important;
        }
        
        /* ── Leaderboard Table ── */
        .leaderboard-container {
            background: rgba(17, 24, 39, 0.5);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 12px;
            overflow: hidden;
        }
        
        .leaderboard-row {
            display: flex;
            justify-content: space-between;
            padding: 12px 20px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            align-items: center;
        }
        
        .leaderboard-row:last-child {
            border-bottom: none;
        }
        
        .leaderboard-rank {
            font-size: 1.1em;
            font-weight: 700;
            width: 30px;
        }
        
        /* ── Badges ── */
        .badge {
            display: inline-flex;
            align-items: center;
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 600;
            color: #ffffff;
            margin-right: 6px;
        }
        .badge-streak {
            background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
            box-shadow: 0 2px 8px rgba(249, 115, 22, 0.3);
        }
        .badge-xp {
            background: linear-gradient(135deg, #a855f7 0%, #7e22ce 100%);
            box-shadow: 0 2px 8px rgba(168, 85, 247, 0.3);
        }
        
        /* ── Custom Scrollbar ── */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        ::-webkit-scrollbar-track {
            background: #030712;
        }
        ::-webkit-scrollbar-thumb {
            background: #1f2937;
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #374151;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def card_html(title: str, subtitle: str, body: str = "", footer: str = "") -> str:
    """Return HTML code for a beautiful custom card."""
    body_html = f"<div style='font-size:0.95em;color:#9ca3af;margin:10px 0;'>{body}</div>" if body else ""
    footer_html = f"<div style='font-size:0.85em;color:#cbd5e1;font-weight:600;'>{footer}</div>" if footer else ""
    return f"""
    <div class="glass-card">
        <div style="font-size:1.25em;font-weight:700;color:#ffffff;line-height:1.2;">{title}</div>
        <div style="font-size:0.85em;color:#818cf8;font-weight:500;margin-top:4px;">{subtitle}</div>
        {body_html}
        {footer_html}
    </div>
    """
