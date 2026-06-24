@echo off
title Bharat AI School - Key Setup
cls
echo ============================================
echo    🔑 API KEY SETUP
echo    Bharat AI School V6
echo ============================================
echo.
echo Ye file aapki GROQ API key setup karegi.
echo.

:ask
echo Kya aapke paas Groq API key hai?
echo.
echo    [1] Haan, mere paas key hai
echo    [2] Nahi, mujhe nayi key chahiye
echo    [3] Skip (bina AI chat ke app chalegi)
echo.
choice /c 123 /n /m "Option (1/2/3): "

if errorlevel 3 goto skip
if errorlevel 2 goto getkey
if errorlevel 1 goto havekey

:havekey
cls
echo ============================================
echo    🔑 APNI KEY DAALEIN
echo ============================================
echo.
echo API key yahan paste karein (Right-click paste karein)
echo.
set /p USER_KEY="🔑 API Key: "

if "%USER_KEY%"=="" (
    echo ❌ Key blank hai. Dobara daalein.
    pause
    goto havekey
)

REM Save to secret file
echo @echo off > "%~dp0MY_SECRET_KEY.bat"
echo REM 🔐 Bharat AI School - Secret Key >> "%~dp0MY_SECRET_KEY.bat"
echo set GROQ_API_KEY=%USER_KEY%>> "%~dp0MY_SECRET_KEY.bat"
echo set UPI_ID=gurjas@upi>> "%~dp0MY_SECRET_KEY.bat"
echo set UPI_NAME=Dr. Gurjas Singh>> "%~dp0MY_SECRET_KEY.bat"

echo.
echo ✅ Key save ho gayi!
echo ✅ MY_SECRET_KEY.bat file mein safe hai
echo.
echo 🚀 Ab app kholne ke liye START_HERE.bat chalayein
echo    Ya desktop se "Bharat AI School V6" shortcut
echo.
pause
exit /b

:getkey
cls
echo ============================================
echo    🔗 FREE API KEY KAISE LEIN
echo ============================================
echo.
echo Step-by-step:
echo.
echo 1️⃣ Browser khulega: https://console.groq.com
echo.
echo 2️⃣ "Sign Up" karein (Google se login karein)
echo.
echo 3️⃣ Left sidebar mein "API Keys" par click karein
echo.
echo 4️⃣ "Create API Key" button dabayein
echo.
echo 5️⃣ Key copy karein (gsk_... se start hoti hai)
echo.
echo 6️⃣ Yaha wapas aakar STEP1_SETUP_KEY.bat dobara chalayein
echo.
start https://console.groq.com
echo.
pause
goto havekey

:skip
cls
echo.
echo ⏭️ Skip kiya gaya. App bina AI chat ke chalegi.
echo Baad mein key daalni ho to STEP1_SETUP_KEY.bat dobara chalayein.
echo.
echo 🚀 App kholne ke liye START_HERE.bat chalayein
echo.
pause
exit /b
