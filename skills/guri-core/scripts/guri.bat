@echo off
rem Launcher do Guri com auto-sync no CMD
if exist "%USERPROFILE%\.gemini\config\.git" (
    git -C "%USERPROFILE%\.gemini\config" pull --quiet origin main >nul 2>&1
)
python "%USERPROFILE%\.gemini\config\skills\guri-core\scripts\banner.py"
agy %*
