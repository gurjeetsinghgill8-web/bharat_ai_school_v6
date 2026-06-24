@echo off
title Bharat AI School V6
cls
echo ============================================
echo    🚀 Bharat AI School V6 — ₹20/माह
echo    पूरा भारत सीखेगा AI!
echo ============================================
echo.

cd /d "%~dp0"

REM 🗝️ Python se check karo key hai ya nahi
python -c "import sys,os; sys.path.insert(0,'.'); from utils.groq_client import get_api_key; k=get_api_key(); exit(0 if k and k not in('YOUR_API_KEY_HERE','YOUR_KEY_HERE','') else 1)" >nul 2>&1

if %errorlevel% neq 0 (
    echo ⚠️  API key nahi mili!
    echo.
    echo ============================================
    echo    🔑 KEY SETUP
    echo ============================================
    echo.
    echo  1️⃣  Neeche diya button dabayein
    echo  2️⃣  Notepad khulega
    echo  3️⃣  YOUR_KEY_HERE ki jagah apni GROQ key daalein
    echo  4️⃣  Ctrl+S daba ke save karein
    echo  5️⃣  Notepad band karein
    echo  6️⃣  Yeh wala baba phir se dabayein
    echo.
    echo  🔑 Key nahi hai? https://console.groq.com
    echo.
    echo  ✅  Key daalne ke liye 1 dabayein
    echo  🔜  Skip (bina AI chat ke chalega) — 2 dabayein
    echo.
    choice /c 12 /n /m "Option (1/2): "

    if errorlevel 2 goto skip
    if errorlevel 1 (
        notepad MY_SECRET_KEY.txt
        echo.
        echo 👍 Key daal di? Toh dobara file chalayein!
        pause
        exit /b
    )
)

:skip
echo ✅ App start ho rahi hai...
echo.

pip show streamlit >nul 2>&1
if %errorlevel% neq 0 (
    pip install -r requirements.txt -q
)

echo.
start "" http://localhost:8501
streamlit run app.py --server.port 8501
pause
