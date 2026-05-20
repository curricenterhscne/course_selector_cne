@echo off
chcp 65001 > nul
cd /d "%~dp0"

echo.
echo  ============================================
echo   충남교육청  편제표 데이터 관리 도구
echo  ============================================
echo.

:: ── Python 확인 ──────────────────────────────
python --version >nul 2>&1
if not errorlevel 1 (
    set PYTHON=python
    goto :server_start
)
python3 --version >nul 2>&1
if not errorlevel 1 (
    set PYTHON=python3
    goto :server_start
)

echo  [오류] Python이 설치되어 있지 않습니다.
echo.
echo  아래 주소에서 Python을 설치한 후 다시 실행하세요.
echo  https://www.python.org/downloads/
echo.
echo  설치 시 "Add Python to PATH" 항목을 반드시 체크하세요.
echo.
pause
exit /b 1

:: ── 서버 시작 ────────────────────────────────
:server_start

:: 포트 8080이 이미 사용 중이면 바로 브라우저만 열기
netstat -an | findstr ":8080 " >nul 2>&1
if not errorlevel 1 (
    echo  [알림] 포트 8080이 이미 실행 중입니다. 브라우저를 엽니다.
    start "" "http://localhost:8080/admin.html"
    echo.
    echo  작업을 마치면 이 창을 닫으세요.
    pause >nul
    exit /b 0
)

:: 백그라운드로 서버 실행
start /min "편제표_관리서버" %PYTHON% -m http.server 8080

:: 서버 준비 대기 후 브라우저 열기
timeout /t 2 /nobreak >nul
start "" "http://localhost:8080/admin.html"

echo  브라우저에서 관리 도구가 열렸습니다.
echo.
echo  브라우저가 열리지 않으면 주소창에 직접 입력하세요:
echo    http://localhost:8080/admin.html
echo.
echo  작업을 마치면 아무 키나 눌러 서버를 종료하세요.
echo.
pause >nul

:: ── 서버 종료 ────────────────────────────────
echo  서버를 종료합니다...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":8080 " 2^>nul') do (
    taskkill /f /pid %%a >nul 2>&1
)
echo  종료 완료.
timeout /t 1 /nobreak >nul
exit /b 0
