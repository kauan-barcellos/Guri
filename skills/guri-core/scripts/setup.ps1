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
                git -C "$configPath" log --oneline -n [math]::Min([int]$commitsAtras, 5) HEAD..origin/main | ForEach-Object {
                    Write-Host "    -> $_" -ForegroundColor Cyan
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
