---
name: workspace-janitor
description: >-
  Higienizacao e faxina sistematica do diretorio de trabalho contra arquivos orfaos, backups de CAD e caches temporarios.
  Use periodicamente ou antes de commits para identificar lixo de compilacao, logs residuais e relatorios descartaveis.
---

# Higienizador de Workspace (Workspace Janitor)

Esta skill mantem o diretorio do projeto limpo, seguro e organizado. Ela rastreia e remove lixo gerado durante compilacoes, backups automaticos de programas de CAD, dumps de depuracao e arquivos temporarios que nao devem poluir o repositorio nem confundir a analise de contexto.

---

## 1. Categorias de Lixo Rastreadas

* **Caches de Compilacao e Interpretadores:** `__pycache__`, `*.pyc`, `.pytest_cache`, `.pio/build`, `.pio/libdeps`.
* **Backups Automaticos de CAD e Editores:** `*-bak`, `*.kicad_pcb-bak`, `*.kicad_sch-bak`, `*.autosave`, `*~`.
* **Arquivos de Sistema e Ocultos:** `Thumbs.db`, `.DS_Store`, `desktop.ini`.
* **Logs Temporarios e Relatorios Descartaveis:** `*.log`, `*.dmp`, `*.tmp`, relatorios de teste orfaos.

---

## 2. Modo Seguro de Operacao

A limpeza opera em duas etapas deterministicas:
1. **Varredura (Dry-Run):** Executa o script `scripts/janitor.py --scan` e lista todos os arquivos encontrados, o espaco ocupado e as extensoes, sem apagar nada.
2. **Confirmacao e Limpeza:** Executa `python scripts/janitor.py --clean` para remover os arquivos confirmados.

---

## 3. Uso do Script

```bash
# Somente inspecionar o que e lixo no diretorio atual:
python scripts/janitor.py --scan

# Limpar com seguranca:
python scripts/janitor.py --clean
```
