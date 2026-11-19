---
name: github-repo-inspector
description: >-
  Inspecao e dissecação rapida de repositorios do GitHub com extracao direcionada de codigo sem queimar contexto.
  Use para analisar bibliotecas abertas, clonar referencias em pasta temporaria e extrair apenas assinaturas de funcoes e exemplos essenciais.
---

# Inspecao e Extracao Direcionada de Repositorios (GitHub Repo Inspector)

Esta skill permite inspecionar repositorios remotos no GitHub para reaproveitar solucoes, drivers de sensores, bibliotecas C/C++ ou algoritmos Python sem clonar o projeto inteiro para o workspace de trabalho nem queimar a janela de contexto.

---

## 1. Fluxo de Execucao em 4 Etapas

```
[1. Clone Raso / Shallow] ──> [2. Mapeamento da Arvore] ──> [3. Extracao Seletiva] ──> [4. Descarte do Clone]
```

### Etapa 1: Clone Superficial
* O script `scripts/inspect_repo.py` clona apenas o ultimo commit (`--depth 1`) em uma pasta temporaria segura no diretorio temporario do sistema.
* Nao polui o repositorio atual.

### Etapa 2: Mapeamento de Estrutura
* Lista arquivos chave: `README.md`, headers `.h`/`.hpp`, arquivos de configuracao (`platformio.ini`, `setup.py`, `CMakeLists.txt`) e pastas de exemplos (`examples/`, `samples/`).

### Etapa 3: Extracao de Assinaturas e Exemplos
* Extrai apenas os blocos necessarios: definicao de pinos, funcoes principais de inicializacao e leitura, e loops de teste.
* Salva os trechos destilados em `.context/references/<nome_repo>.md` ou no scratch.

### Etapa 4: Limpeza Imediata
* Remove a pasta clonada automaticamente ao concluir a extracao.

---

## 2. Comandos do Script Auxiliar

```bash
# Inspecionar arvore e extrair exemplos de um repositorio remoto:
python scripts/inspect_repo.py --url https://github.com/autor/repo --extract "examples,src" --output .context/references/repo_resumo.md
```
