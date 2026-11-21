# =====================================================================
# GURI - Script de Instalacao Universal para Novas Maquinas
# Execucao Direta (Web):
#   irm https://raw.githubusercontent.com/kauan-barcellos/Guri/main/instalar_guri.ps1 | iex
# Execucao Local:
#   .\instalar_guri.ps1
# =====================================================================

[CmdletBinding()]
param(
    [string]$RepoUrl = "https://github.com/kauan-barcellos/Guri.git"
)

$ErrorActionPreference = "Stop"

Write-Host "`n=======================================================" -ForegroundColor Cyan
Write-Host "         INSTALADOR AUTOMATICO DO GURI                 " -ForegroundColor Cyan
Write-Host "             >> A mente que pensa <<                   " -ForegroundColor Yellow
Write-Host "=======================================================`n" -ForegroundColor Cyan

# 1. Checagem de Dependencias Essenciais
Write-Host "[1/5] Verificando dependencias essenciais..." -ForegroundColor Yellow

# Git
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "[X] Git nao encontrado no sistema." -ForegroundColor Red
    Write-Host "    Para instalar via terminal, execute: winget install --id Git.Git -e" -ForegroundColor Gray
    throw "Instale o Git e execute este instalador novamente."
}
Write-Host "  [+] Git detectado: $(git --version)" -ForegroundColor Green

# Python
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "[X] Python nao encontrado no sistema." -ForegroundColor Red
    Write-Host "    Para instalar via terminal, execute: winget install --id Python.Python.3.12 -e" -ForegroundColor Gray
    throw "Instale o Python 3.10+ e execute este instalador novamente."
}
Write-Host "  [+] Python detectado: $(python --version 2>&1)" -ForegroundColor Green

# Antigravity CLI (agy)
$agyCmd = Get-Command agy -ErrorAction SilentlyContinue
$agyBinPath = "$HOME\AppData\Local\agy\bin"
if (-not $agyCmd -and -not (Test-Path "$agyBinPath\agy.exe")) {
    Write-Host "  [!] Antigravity CLI (agy) ainda nao localizado no PATH." -ForegroundColor DarkYellow
    Write-Host "      Voce podera instalar ou configurar o Antigravity depois." -ForegroundColor Gray
} else {
    Write-Host "  [+] Antigravity CLI detectado." -ForegroundColor Green
}

# 2. Configuracao do Cerebro (~/.gemini/config)
$configPath = "$HOME\.gemini\config"
Write-Host "`n[2/5] Configurando repositorio do cérebro em $configPath..." -ForegroundColor Yellow

if (-not (Test-Path $configPath)) {
    New-Item -ItemType Directory -Path $configPath -Force | Out-Null
}

$localHostname = $null
if (Test-Path "$configPath\config.json") {
    try {
        $rawConfig = Get-Content "$configPath\config.json" -Raw -ErrorAction SilentlyContinue | ConvertFrom-Json
        if ($rawConfig.userSettings.remoteControlHostname) {
            $localHostname = $rawConfig.userSettings.remoteControlHostname
        }
    } catch {}
}

if (-not $localHostname) {
    $cleanCompName = ($env:COMPUTERNAME -replace '[^a-zA-Z0-9-]', '').ToLower()
    $localHostname = "$cleanCompName-shard"
}

if (Test-Path "$configPath\.git") {
    Write-Host "  [*] Repositorio Git existente detectado. Atualizando via git pull..." -ForegroundColor Gray
    try {
        git -C "$configPath" pull origin main
        Write-Host "  [+] Cerebro atualizado com sucesso!" -ForegroundColor Green
    } catch {
        Write-Host "  [!] Aviso: Nao foi possivel rodar git pull agora (sem conexao ou conflito local)." -ForegroundColor Yellow
    }
} else {
    Write-Host "  [*] Conectando $configPath ao repositorio $RepoUrl..." -ForegroundColor Gray
    git -C "$configPath" init --quiet
    git -C "$configPath" remote add origin $RepoUrl 2>$null
    git -C "$configPath" fetch origin main --quiet
    git -C "$configPath" reset --mixed origin/main --quiet
    git -C "$configPath" checkout -f main --quiet
    Write-Host "  [+] Arquivos sincronizados com a branch main!" -ForegroundColor Green
}

# Preservar o hostname local e ignorar mudancas de config.json no Git
if (Test-Path "$configPath\config.json") {
    try {
        $cfg = Get-Content "$configPath\config.json" -Raw | ConvertFrom-Json
        $cfg.userSettings.remoteControlHostname = $localHostname
        $cfg | ConvertTo-Json -Depth 10 | Set-Content "$configPath\config.json" -Encoding UTF8
        git -C "$configPath" update-index --skip-worktree config.json 2>$null
        Write-Host "  [+] Hostname local configurado: $localHostname (protegido contra sobrescrita)" -ForegroundColor Green
    } catch {
        Write-Host "  [!] Nota: Nao foi possivel ajustar o hostname em config.json." -ForegroundColor Yellow
    }
}

# 3. Instalacao dos Executaveis Globais (guri.cmd e opt.cmd)
Write-Host "`n[3/5] Criando executaveis globais (guri e opt)..." -ForegroundColor Yellow

$targetBinDir = $null
if (Test-Path $agyBinPath) {
    $targetBinDir = $agyBinPath
} elseif (Test-Path "$HOME\.gemini\antigravity-cli\bin") {
    $targetBinDir = "$HOME\.gemini\antigravity-cli\bin"
} else {
    $targetBinDir = "$HOME\bin"
    if (-not (Test-Path $targetBinDir)) {
        New-Item -ItemType Directory -Path $targetBinDir -Force | Out-Null
    }
    $userPath = [Environment]::GetEnvironmentVariable("Path", "User")
    if ($userPath -split ';' -notcontains $targetBinDir) {
        [Environment]::SetEnvironmentVariable("Path", "$userPath;$targetBinDir", "User")
        $env:PATH += ";$targetBinDir"
    }
}

$guriBatContent = @"
@echo off
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
"@

$optBatContent = @"
@echo off
set "PYTHONPATH=%USERPROFILE%\.gemini\config\skills\token-optimization\scripts"
python -m token_optimizer %*
"@

Set-Content -Path "$targetBinDir\guri.cmd" -Value $guriBatContent -Encoding ASCII
Set-Content -Path "$targetBinDir\opt.cmd" -Value $optBatContent -Encoding ASCII
Write-Host "  [+] Executaveis instalados em: $targetBinDir" -ForegroundColor Green

# 4. Configuracao do Perfil do PowerShell
Write-Host "`n[4/5] Configurando integracao com o PowerShell ($PROFILE)..." -ForegroundColor Yellow

$profileDir = Split-Path -Parent $PROFILE
if (-not (Test-Path $profileDir)) {
    New-Item -ItemType Directory -Path $profileDir -Force | Out-Null
}
if (-not (Test-Path $PROFILE)) {
    New-Item -ItemType File -Path $PROFILE -Force | Out-Null
}

$blocoGuri = @'

# =====================================================================
# GURI - Assistente de Engenharia, Codigo e Produtividade
# =====================================================================

function guri {
    <#
    .SYNOPSIS
        Inicia o Guri com comparacao ativa de historico e sincronizacao do GitHub.
    .EXAMPLE
        guri                     # Inicia nova sessao no diretorio atual
        guri -c <session-id>     # Reconecta a uma sessao anterior
    #>
    $configPath = "$HOME\.gemini\config"

    # 1. Compara ativamente com o repositorio remoto se houver Git
    if (Test-Path "$configPath\.git") {
        try {
            git -C "$configPath" fetch origin main --quiet 2>$null

            $commitsAtras = (git -C "$configPath" rev-list --count HEAD..origin/main 2>$null)
            $commitsAfrente = (git -C "$configPath" rev-list --count origin/main..HEAD 2>$null)

            if ($commitsAtras -and [int]$commitsAtras -gt 0) {
                Write-Host "`n[*] Kauan, foram encontradas $commitsAtras atualizacao(oes) no GitHub:" -ForegroundColor Yellow
                $logs = git -C "$configPath" log --oneline -n [math]::Min([int]$commitsAtras, 5) HEAD..origin/main
                foreach ($l in $logs) {
                    Write-Host "    -> $l" -ForegroundColor Cyan
                }
                git -C "$configPath" pull --quiet origin main 2>$null
                Write-Host "[+] Cerebro do Guri sincronizado com sucesso!`n" -ForegroundColor Green
            } elseif ($commitsAfrente -and [int]$commitsAfrente -gt 0) {
                Write-Host "`n[i] Kauan, esta maquina tem $commitsAfrente commit(s) local(is) pendente(s) de envio para o GitHub." -ForegroundColor DarkYellow
                Write-Host "    Use 'guri-salvar' quando quiser subir suas alteracoes.`n" -ForegroundColor Gray
            }
        } catch {}
    }

    # 2. Exibe o banner oficial com a frase do dia
    $bannerScript = "$configPath\skills\guri-core\scripts\banner.py"
    if (Test-Path $bannerScript) {
        python "$bannerScript"
    }

    # 3. Executa o assistente com os argumentos passados
    agy @args
}

function guri-salvar {
    <#
    .SYNOPSIS
        Salva todos os aprendizados e audita se o repositorio remoto esta 100% atualizado.
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

    Write-Host "`n[*] Kauan, iniciando auditoria e sincronizacao com o GitHub..." -ForegroundColor Yellow

    # 1. Fetch para garantir estado atualizado das referencias remotas
    git -C "$configPath" fetch origin main --quiet 2>$null

    # 2. Stage e commit de alteracoes de arquivos locais
    git -C "$configPath" add -A
    $status = git -C "$configPath" status --porcelain
    if ($status) {
        $dataHora = Get-Date -Format "dd/MM/yyyy HH:mm"
        git -C "$configPath" commit -m "$mensagem ($dataHora)" --quiet
        Write-Host "[+] Alteracoes locais commitadas: $mensagem" -ForegroundColor Green
    }

    # 3. Verifica e envia commits locais pendentes
    $pendentes = (git -C "$configPath" rev-list --count origin/main..HEAD 2>$null)
    if ($pendentes -and [int]$pendentes -gt 0) {
        Write-Host "[*] Enviando $pendentes commit(s) pendente(s) para o GitHub..." -ForegroundColor Yellow
        git -C "$configPath" push origin main --quiet
    }

    # 4. Auditoria final de integridade: compara hashes exatos
    $hashLocal = (git -C "$configPath" rev-parse HEAD 2>$null)
    $hashRemoto = (git -C "$configPath" rev-parse origin/main 2>$null)

    if ($hashLocal -and $hashRemoto -and ($hashLocal -eq $hashRemoto)) {
        Write-Host "[OK] Kauan, auditoria confirmada: o GitHub esta 100% espelhado e em dia com esta maquina!" -ForegroundColor Green
        Write-Host "     Hash de sincronia: $($hashLocal.Substring(0, 7))`n" -ForegroundColor DarkGray
    } else {
        Write-Host "[!] Kauan, atencao: foram identificadas divergencias entre local e remoto." -ForegroundColor Yellow
        Write-Host "    Local:  $hashLocal" -ForegroundColor Gray
        Write-Host "    Remoto: $hashRemoto" -ForegroundColor Gray
        Write-Host "    Execute 'git -C `"$configPath`" status' para inspecionar os detalhes.`n" -ForegroundColor Yellow
    }
}
'@

$conteudoPerfil = Get-Content $PROFILE -Raw -ErrorAction SilentlyContinue
if ($null -eq $conteudoPerfil -or $conteudoPerfil -notmatch "function guri\s*\{") {
    Add-Content -Path $PROFILE -Value $blocoGuri
    Write-Host "  [+] Funcoes 'guri' e 'guri-salvar' adicionadas ao perfil!" -ForegroundColor Green
} else {
    $padrao = "(?s)# ===+\s*# GURI - Assistente.*?function guri-salvar\s*\{.*?\n\}"
    if ($conteudoPerfil -match $padrao) {
        $escapedBloco = $blocoGuri.Trim().Replace('$', '$$')
        $conteudoPerfil = $conteudoPerfil -replace $padrao, $escapedBloco
        Set-Content -Path $PROFILE -Value $conteudoPerfil -Force
    } else {
        Add-Content -Path $PROFILE -Value $blocoGuri
    }
    Write-Host "  [+] Funcoes atualizadas no perfil existente!" -ForegroundColor Green
}

# 5. Validacao da Instalacao
Write-Host "`n[5/5] Validando inicializacao..." -ForegroundColor Yellow

$bannerScript = "$configPath\skills\guri-core\scripts\banner.py"
if (Test-Path $bannerScript) {
    python "$bannerScript"
}

Write-Host "-------------------------------------------------------" -ForegroundColor Cyan
Write-Host "Configuracao concluida com sucesso!" -ForegroundColor Green
Write-Host "Comandos disponiveis de qualquer pasta ou terminal:" -ForegroundColor White
Write-Host "  guri                  -> Inicia sessao com auto-sync e banner" -ForegroundColor Cyan
Write-Host "  guri -c <id>          -> Reconecta a sessao anterior" -ForegroundColor Cyan
Write-Host "  guri-salvar           -> Envia alteracoes e aprendizados para o GitHub" -ForegroundColor Cyan
Write-Host "  opt --path <pasta>    -> Comprime tokens via AST Repo-Map" -ForegroundColor Cyan
Write-Host "-------------------------------------------------------`n" -ForegroundColor Cyan
