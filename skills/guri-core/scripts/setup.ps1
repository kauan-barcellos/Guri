# =====================================================================
# Script de Instalacao e Configuracao do GURI no PowerShell
# Uso:
#   & "$HOME\.gemini\config\skills\guri-core\scripts\setup.ps1"
# =====================================================================

$ErrorActionPreference = "Stop"

Write-Host "`n=======================================================" -ForegroundColor Cyan
Write-Host "         INSTALACAO DO GURI - A MENTE QUE PENSA        " -ForegroundColor Cyan
Write-Host "=======================================================`n" -ForegroundColor Cyan

# 1. Localizacao do perfil do PowerShell
$profileDir = Split-Path -Parent $PROFILE
if (-not (Test-Path $profileDir)) {
    New-Item -ItemType Directory -Path $profileDir -Force | Out-Null
}
if (-not (Test-Path $PROFILE)) {
    New-Item -ItemType File -Path $PROFILE -Force | Out-Null
}

# 2. Definicao das funcoes de inicializacao e sincronizacao
$blocoGuri = @'

# =====================================================================
# GURI - Assistente de Engenharia, Codigo e Produtividade
# =====================================================================

function guri {
    <#
    .SYNOPSIS
        Inicia o Guri com sincronizacao automatica da nuvem.
    .EXAMPLE
        guri                     # Inicia nova sessao no diretorio atual
        guri -c <session-id>     # Reconecta a uma sessao anterior
    #>
    $configPath = "$HOME\.gemini\config"

    # Sincroniza silenciosamente com o GitHub se houver internet
    if (Test-Path "$configPath\.git") {
        try {
            git -C "$configPath" pull --quiet origin main 2>$null
        } catch {}
    }

    # Exibe o banner oficial com a frase do dia
    $bannerScript = "$configPath\skills\guri-core\scripts\banner.py"
    if (Test-Path $bannerScript) {
        python "$bannerScript"
    }

    # Executa o assistente com os argumentos passados
    agy @args
}

function guri-salvar {
    <#
    .SYNOPSIS
        Salva todos os aprendizados e regras do Guri no GitHub.
    .EXAMPLE
        guri-salvar
        guri-salvar "adicionado modulo de calibracao"
    #>
    param(
        [string]$mensagem = "Sincronizacao de aprendizados do Guri"
    )

    $configPath = "$HOME\.gemini\config"
    if (-not (Test-Path "$configPath\.git")) {
        Write-Host "`n[!] Repositorio Git nao encontrado em $configPath" -ForegroundColor Red
        return
    }

    Write-Host "`n[*] Sincronizando cérebro do Guri com o GitHub..." -ForegroundColor Yellow
    git -C "$configPath" add -A
    $status = git -C "$configPath" status --porcelain
    if (-not $status) {
        Write-Host "[OK] Nada para salvar. O Guri ja esta 100% atualizado com o GitHub!`n" -ForegroundColor Green
        return
    }

    $dataHora = Get-Date -Format "dd/MM/yyyy HH:mm"
    git -C "$configPath" commit -m "$mensagem ($dataHora)"
    git -C "$configPath" push origin main
    Write-Host "[OK] Tudo salvo com sucesso no GitHub!`n" -ForegroundColor Green
}
'@

# 3. Atualizar o profile sem duplicar
$conteudoPerfil = Get-Content $PROFILE -Raw -ErrorAction SilentlyContinue
if ($null -eq $conteudoPerfil -or $conteudoPerfil -notmatch "function guri\s*\{") {
    Add-Content -Path $PROFILE -Value $blocoGuri
    Write-Host "[+] Funcoes 'guri' e 'guri-salvar' adicionadas ao perfil do PowerShell!" -ForegroundColor Green
} else {
    # Substitui bloco existente caso ja tenha sido instalado
    Write-Host "[*] Atualizando funcoes do Guri no seu perfil do PowerShell..." -ForegroundColor Yellow
    # Remove qualquer versao antiga do bloco
    $padrao = "(?s)# ===+\s*# GURI - Assistente.*?function guri-salvar\s*\{.*?\n\}"
    if ($conteudoPerfil -match $padrao) {
        $conteudoPerfil = $conteudoPerfil -replace $padrao, $blocoGuri.Trim()
        Set-Content -Path $PROFILE -Value $conteudoPerfil -Force
    } else {
        Add-Content -Path $PROFILE -Value $blocoGuri
    }
    Write-Host "[+] Perfil atualizado com sucesso!" -ForegroundColor Green
}

Write-Host "`n-------------------------------------------------------" -ForegroundColor Cyan
Write-Host "Configuracao concluida com sucesso!" -ForegroundColor Green
Write-Host "Como usar:" -ForegroundColor White
Write-Host "  1. Digite 'guri' para iniciar qualquer sessao com auto-sync" -ForegroundColor Cyan
Write-Host "  2. Digite 'guri -c <id>' para reconectar a uma sessao" -ForegroundColor Cyan
Write-Host "  3. Digite 'guri-salvar' se quiser forcar o salvamento no GitHub" -ForegroundColor Cyan
Write-Host "-------------------------------------------------------`n" -ForegroundColor Cyan
