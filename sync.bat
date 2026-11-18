@echo off
setlocal EnableDelayedExpansion
cd /d %~dp0
echo [Guri Sync] Verificando alteracoes locais...
git status --short
echo.
git add -A
set "COMMIT_MSG=%~1"
if not defined COMMIT_MSG (
    set "COMMIT_MSG=chore(sync): sincronizacao automatica da base Guri"
)
echo [Guri Sync] Commitando: !COMMIT_MSG!
git commit -m "!COMMIT_MSG!"
echo [Guri Sync] Enviando para origin main...
git push origin main
echo [Guri Sync] Concluido com sucesso!
endlocal
