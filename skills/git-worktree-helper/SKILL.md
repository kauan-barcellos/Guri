---
name: git-worktree-helper
description: >-
  Gerenciamento de git worktrees para testes arriscados, spikes de arquitetura e validacoes em diretorios isolados.
  Use para criar branches de teste isoladas sem alterar a arvore de trabalho principal do projeto.
---

# Isolamento Experimental com Git Worktrees (Git Worktree Helper)

Esta skill permite criar ambientes de trabalho isolados em pastas separadas utilizando o recurso nativo de worktrees do Git. Ela e recomendada para experimentos arriscados, testes de refatoracao de grandes dimensoes, spikes de arquitetura ou testes de novas bibliotecas sem colocar em risco a branch de trabalho atual.

---

## 1. Por que Usar Worktrees em Vez de Branch Comum?

1. **Zero Impacto no Workspace Atual:** A pasta atual permanece intocada, preservando arquivos abertos e estados de build.
2. **Comparacao Lado a Lado:** Permite rodar testes em duas branches diferentes em paralelo no mesmo computador.
3. **Descarte Imediato:** Se o teste der errado, a pasta temporaria e removida com um comando sem deixar sujeira no historico principal.

---

## 2. Fluxo Operacional

```
[1. Criar Worktree Isolado] ──> [2. Executar Experimento] ──> [3. Validar Resultado] ──> [4. Merge ou Descarte]
```

### Criar um Spike Isolado
```bash
python scripts/worktree_helper.py --create spike-novo-sensor
```
Isso cria um diretorio paralelo `../worktree-spike-novo-sensor` apontando para uma nova branch `spike/novo-sensor`.

### Descartar o Experimento
```bash
python scripts/worktree_helper.py --remove spike-novo-sensor
```
Remove com seguranca a pasta e o registro da worktree sem afetar o repositorio principal.

### Listar Worktrees Ativas
```bash
python scripts/worktree_helper.py --list
```
