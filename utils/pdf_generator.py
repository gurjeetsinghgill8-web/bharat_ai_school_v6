"""
Bharat AI School V6 — PDF Generator
Generate chapter notes, study materials, and completion certificates.
Unicode-safe: uses fpdf2 with DejaVu font for Hindi/₹ support.
"""
import os
from datetime import datetime

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "pdf_outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Try fpdf2 with Unicode support
PDF_AVAILABLE = False
ChapterPDF = None

def ensure_fonts_exist():
    """Ensure Poppins fonts exist locally or download them from Google Fonts raw repository."""
    fonts_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")
    os.makedirs(fonts_dir, exist_ok=True)
    
    urls = {
        "Poppins-Regular.ttf": "https://github.com/google/fonts/raw/main/ofl/poppins/Poppins-Regular.ttf",
        "Poppins-Bold.ttf": "https://github.com/google/fonts/raw/main/ofl/poppins/Poppins-Bold.ttf",
        "Poppins-Italic.ttf": "https://github.com/google/fonts/raw/main/ofl/poppins/Poppins-Italic.ttf"
    }
    
    local_source_dir = r"C:\Users\pc\Desktop\ani vedio\fonts"
    
    for name, url in urls.items():
        dest = os.path.join(fonts_dir, name)
        if not os.path.exists(dest):
            # Check local Desktop backup first
            local_src = os.path.join(local_source_dir, name)
            if os.path.exists(local_src):
                import shutil
                try:
                    shutil.copy(local_src, dest)
                    continue
                except:
                    pass
            # Download from Google Fonts raw GitHub
            import urllib.request
            try:
                urllib.request.urlretrieve(url, dest)
            except Exception as e:
                print(f"Failed to download font {name}: {e}")

try:
    from fpdf import FPDF
    
    # Pre-download fonts if not present
    ensure_fonts_exist()
    
    fonts_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")
    regular_path = os.path.join(fonts_dir, "Poppins-Regular.ttf")
    bold_path = os.path.join(fonts_dir, "Poppins-Bold.ttf")
    italic_path = os.path.join(fonts_dir, "Poppins-Italic.ttf")

    if os.path.exists(regular_path) and os.path.exists(bold_path) and os.path.exists(italic_path):
        class ChapterPDF(FPDF):
            """Unicode-safe PDF with Poppins font family (registered under DejaVu for compatibility)."""
            
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                # Register under both Poppins and DejaVu for legacy compatibility
                for name in ["Poppins", "DejaVu"]:
                    self.add_font(name, "", regular_path)
                    self.add_font(name, "B", bold_path)
                    self.add_font(name, "I", italic_path)

            def header(self):
                if self.page_no() > 1:
                    self.set_font("Poppins", "B", 9)
                    self.set_text_color(0, 102, 204)
                    self.cell(0, 7, "Bharat AI School - Chapter Notes", align="C", new_x="LMARGIN", new_y="NEXT")
                    self.line(10, self.get_y(), 200, self.get_y())
                    self.ln(3)

            def footer(self):
                self.set_y(-15)
                self.set_font("Poppins", "I", 7)
                self.set_text_color(128, 128, 128)
                self.cell(0, 10, f"Page {self.page_no()}/{{nb}} | Bharat AI School", align="C")

        PDF_AVAILABLE = True
    else:
        PDF_AVAILABLE = False
except Exception as e:
    print(f"PDF library setup error: {e}")
    ChapterPDF = None
    PDF_AVAILABLE = False


def _make_ascii_safe(text: str) -> str:
    """Strip or replace non-latin chars for PDF fallback."""
    return text.encode("ascii", errors="replace").decode("ascii")


def generate_chapter_pdf(chapter_data: dict, username: str = "student") -> str:
    """
    Generate a PDF for a chapter using fpdf2 with Unicode support.
    Falls back to .txt if PDF unavailable.
    """
    if not PDF_AVAILABLE or ChapterPDF is None:
        # Fallback .txt
        safe_title = "".join(c for c in chapter_data.get("title", "notes")[:30] if c.isalnum() or c in " _-").strip() or "notes"
        fallback_path = os.path.join(OUTPUT_DIR, f"chapter_{safe_title}.txt")
        with open(fallback_path, "w", encoding="utf-8") as f:
            f.write(f"# {chapter_data.get('title', 'Chapter')}\n\n")
            f.write(f"{chapter_data.get('content', '')}\n\n")
            if chapter_data.get("code_example"):
                f.write(f"## Code Example:\n{chapter_data['code_example']}\n")
            if chapter_data.get("youtube_search_term"):
                f.write(f"YouTube: {chapter_data['youtube_search_term']}\n")
        return fallback_path

    try:
        pdf = ChapterPDF()
        pdf.alias_nb_pages()
        pdf.add_page()

        # Title
        pdf.set_font("DejaVu", "B", 16)
        pdf.set_text_color(0, 0, 0)
        title = chapter_data.get("title", "Chapter Notes")
        pdf.multi_cell(0, 10, title)
        pdf.ln(5)

        # Metadata
        pdf.set_font("DejaVu", "I", 9)
        pdf.set_text_color(100, 100, 100)
        pdf.cell(0, 6, f"Generated for: {username} | {datetime.now().strftime('%d %b %Y')}", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(5)

        # Content
        pdf.set_font("DejaVu", "", 11)
        pdf.set_text_color(30, 30, 30)
        content = chapter_data.get("content", "No content available.")
        pdf.multi_cell(0, 7, content)
        pdf.ln(3)

        # Code Example
        code = chapter_data.get("code_example", "")
        if code:
            pdf.set_font("DejaVu", "B", 11)
            pdf.cell(0, 8, "Code Example:", new_x="LMARGIN", new_y="NEXT")
            pdf.set_font("Courier", "", 9)
            pdf.set_fill_color(240, 240, 240)
            pdf.multi_cell(0, 5, code, fill=True)
            pdf.ln(3)

        # YouTube
        yt_term = chapter_data.get("youtube_search_term", "")
        if yt_term:
            pdf.set_font("DejaVu", "B", 11)
            pdf.cell(0, 8, f"YouTube: Search for '{yt_term}'", new_x="LMARGIN", new_y="NEXT")

        # Save
        safe_title = "".join(c for c in title[:40] if c.isalnum() or c in " _-").strip() or "notes"
        filename = f"{safe_title}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        filepath = os.path.join(OUTPUT_DIR, filename)
        pdf.output(filepath)
        return filepath
    except Exception:
        # Last resort: .txt fallback
        safe_title = "".join(c for c in chapter_data.get("title", "notes")[:30] if c.isalnum() or c in " _-").strip() or "notes"
        txt_path = os.path.join(OUTPUT_DIR, f"chapter_{safe_title}_fallback.txt")
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(f"# {chapter_data.get('title', 'Chapter')}\n\n{chapter_data.get('content', '')}\n")
        return txt_path


def generate_certificate_pdf(username: str, course_title: str, course_progress: int = 100) -> str:
    """Generate a completion certificate."""
    if not PDF_AVAILABLE or ChapterPDF is None:
        txt_path = os.path.join(OUTPUT_DIR, f"cert_{username}_{datetime.now().strftime('%Y%m%d')}.txt")
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write("CERTIFICATE OF COMPLETION\n")
            f.write(f"Presented to {username}\n")
            f.write(f"For completing {course_title} ({course_progress}%)\n")
            f.write(f"Bharat AI School | {datetime.now().strftime('%d %b %Y')}\n")
        return txt_path

    try:
        pdf = ChapterPDF()
        pdf.add_page()
        pdf.ln(30)
        pdf.set_font("DejaVu", "B", 24)
        pdf.set_text_color(0, 102, 204)
        pdf.cell(0, 15, "CERTIFICATE", align="C", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(5)
        pdf.set_font("DejaVu", "", 14)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 10, "OF COMPLETION", align="C", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(15)
        pdf.set_font("DejaVu", "", 12)
        pdf.cell(0, 8, "This is to certify that", align="C", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("DejaVu", "B", 18)
        pdf.cell(0, 12, username, align="C", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("DejaVu", "", 12)
        pdf.cell(0, 8, "has successfully completed", align="C", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("DejaVu", "B", 14)
        pdf.cell(0, 10, course_title, align="C", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("DejaVu", "", 12)
        pdf.cell(0, 8, f"with {course_progress}% progress", align="C", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(15)
        pdf.set_font("DejaVu", "I", 10)
        pdf.cell(0, 8, f"Date: {datetime.now().strftime('%d %B %Y')}", align="C", new_x="LMARGIN", new_y="NEXT")
        pdf.cell(0, 8, "Bharat AI School", align="C", new_x="LMARGIN", new_y="NEXT")

        filename = f"certificate_{username}_{datetime.now().strftime('%Y%m%d')}.pdf"
        filepath = os.path.join(OUTPUT_DIR, filename)
        pdf.output(filepath)
        return filepath
    except Exception:
        txt_path = os.path.join(OUTPUT_DIR, f"cert_{username}_{datetime.now().strftime('%Y%m%d')}.txt")
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write("CERTIFICATE OF COMPLETION\n")
            f.write(f"Presented to {username}\nFor completing {course_title}\n")
        return txt_path


def cleanup_old_pdfs(days: int = 7):
    """Delete PDFs older than `days` days to save space."""
    import time
    now = time.time()
    for fname in os.listdir(OUTPUT_DIR):
        fpath = os.path.join(OUTPUT_DIR, fname)
        if os.path.isfile(fpath) and (fname.endswith(".pdf") or fname.endswith(".txt")):
            if now - os.path.getmtime(fpath) > days * 86400:
                os.remove(fpath)
