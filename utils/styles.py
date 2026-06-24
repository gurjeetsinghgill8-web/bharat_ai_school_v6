"""
Bharat AI School V6 — UI Style Guidelines & CSS Injection
Premium Light Sky-Blue High Contrast Theme.
"""
import streamlit as st

def inject_custom_styles():
    """Inject custom light sky-blue CSS styles into the Streamlit application."""
    st.markdown(
        """
        <style>
        /* ── Core Font & Typography ── */
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Poppins:wght@400;500;600;700&display=swap');
        
        /* Base Sky-Blue Styles */
        .stApp {
            font-family: 'Outfit', sans-serif;
            background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 50%, #bae6fd 100%) !important;
            color: #0f172a !important;
        }
        
        /* Force dark fonts for readability across standard components */
        h1, h2, h3, h4, h5, h6 {
            font-family: 'Outfit', sans-serif;
            font-weight: 700 !important;
            color: #0f172a !important;
            letter-spacing: -0.02em;
        }
        
        /* Override generic elements text color */
        p, span, li, label, div[data-testid="stMarkdownContainer"] p, div[data-testid="stWidgetLabel"] p {
            color: #0f172a !important;
        }
        
        /* Input box label styling */
        label[data-testid="stWidgetLabel"] {
            color: #0f172a !important;
            font-weight: 600 !important;
        }
        
        /* ── Sidebar Styling ── */
        section[data-testid="stSidebar"] {
            background-color: #f0f9ff !important;
            border-right: 1px solid rgba(14, 165, 233, 0.25) !important;
        }
        
        section[data-testid="stSidebar"] hr {
            border-color: rgba(14, 165, 233, 0.2) !important;
        }
        
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] span,
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3 {
            color: #0f172a !important;
        }
        
        /* ── Glassmorphism Cards ── */
        .glass-card {
            background: rgba(255, 255, 255, 0.85);
            border: 1px solid rgba(14, 165, 233, 0.3);
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 20px;
            box-shadow: 0 10px 25px -5px rgba(14, 165, 233, 0.15);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        .glass-card:hover {
            transform: translateY(-2px);
            border-color: rgba(14, 165, 233, 0.6);
            box-shadow: 0 15px 35px -10px rgba(14, 165, 233, 0.3);
        }
        
        /* Course/Chapter List Items */
        .list-item {
            background: rgba(255, 255, 255, 0.7);
            border: 1px solid rgba(14, 165, 233, 0.25);
            border-radius: 12px;
            padding: 16px;
            margin-bottom: 12px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            transition: background 0.2s;
        }
        
        .list-item:hover {
            background: rgba(224, 242, 254, 0.85);
            border-color: rgba(14, 165, 233, 0.45);
        }
        
        /* ── Modern Buttons ── */
        .stButton>button {
            background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%) !important;
            color: #ffffff !important;
            border: none !important;
            border-radius: 10px !important;
            padding: 10px 24px !important;
            font-weight: 600 !important;
            box-shadow: 0 4px 12px rgba(14, 165, 233, 0.25) !important;
            transition: all 0.2s ease !important;
        }
        
        .stButton>button:hover {
            transform: translateY(-1px) !important;
            box-shadow: 0 6px 20px rgba(14, 165, 233, 0.4) !important;
            background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%) !important;
        }
        
        .stButton>button:active {
            transform: translateY(1px) !important;
        }
        
        /* Secondary or plain buttons inside Streamlit forms */
        div[data-testid="stFormSubmitButton"] button {
            background: linear-gradient(135deg, #10b981 0%, #047857 100%) !important;
            color: #ffffff !important;
            box-shadow: 0 4px 12px rgba(16, 185, 129, 0.35) !important;
        }
        div[data-testid="stFormSubmitButton"] button:hover {
            background: linear-gradient(135deg, #34d399 0%, #059669 100%) !important;
            box-shadow: 0 6px 20px rgba(16, 185, 129, 0.45) !important;
        }
        
        /* ── Streamlit Chat Layout Styling ── */
        div[data-testid="stChatMessage"] {
            background-color: rgba(255, 255, 255, 0.9) !important;
            border: 1px solid rgba(14, 165, 233, 0.25) !important;
            border-radius: 14px !important;
            padding: 16px !important;
            margin-bottom: 12px !important;
            box-shadow: 0 4px 12px rgba(14, 165, 233, 0.08) !important;
            backdrop-filter: blur(8px);
        }
        
        div[data-testid="stChatMessage"] p, div[data-testid="stChatMessage"] span {
            color: #0f172a !important;
        }
        
        div[data-testid="stChatMessage"]:has(span[data-testid="stChatMessageAvatar"]) {
            border-left: 3px solid #0284c7 !important;
        }
        
        div[data-testid="stChatMessage"][data-testid="stChatMessage-user"] {
            background-color: rgba(224, 242, 254, 0.8) !important;
            border-left: 3px solid #10b981 !important;
        }
        
        /* ── Leaderboard Table ── */
        .leaderboard-container {
            background: rgba(255, 255, 255, 0.8);
            border: 1px solid rgba(14, 165, 233, 0.25);
            border-radius: 12px;
            overflow: hidden;
        }
        
        .leaderboard-row {
            display: flex;
            justify-content: space-between;
            padding: 12px 20px;
            border-bottom: 1px solid rgba(14, 165, 233, 0.15);
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
            background: #f0f9ff;
        }
        ::-webkit-scrollbar-thumb {
            background: #bae6fd;
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #0ea5e9;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def card_html(title: str, subtitle: str, body: str = "", footer: str = "") -> str:
    """Return HTML code for a beautiful custom card."""
    body_html = f"<div style='font-size:0.95em;color:#334155;margin:10px 0;'>{body}</div>" if body else ""
    footer_html = f"<div style='font-size:0.85em;color:#1e293b;font-weight:600;'>{footer}</div>" if footer else ""
    return f"""
    <div class="glass-card">
        <div style="font-size:1.25em;font-weight:700;color:#0f172a;line-height:1.2;">{title}</div>
        <div style="font-size:0.85em;color:#0284c7;font-weight:500;margin-top:4px;">{subtitle}</div>
        {body_html}
        {footer_html}
    </div>
    """
