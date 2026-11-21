@echo off
rem Launcher do Guri com comparacao ativa de historico no CMD
if exist "%USERPROFILE%\.gemini\config\.git" (
    git -C "%USERPROFILE%\.gemini\config" fetch origin main --quiet >nul 2>&1
    for /f %%i in ('git -C "%USERPROFILE%\.gemini\config" rev-list --count HEAD..origin/main 2^>nul') do set "BEHIND=%%i"
    if defined BEHIND if not "%BEHIND%"=="0" (
        echo [*] Kauan, sincronizando cerebro com %BEHIND% nova^(s^) alteracao^(oes^) do GitHub...
        git -C "%USERPROFILE%\.gemini\config" pull --quiet origin main >nul 2>&1
    )
)
python "%USERPROFILE%\.gemini\config\skills\guri-core\scripts\banner.py"
agy %*
