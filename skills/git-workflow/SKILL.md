---
name: git-workflow
description: >-
  Padrões de fluxo de trabalho Git limpo e commits semânticos (baseado em affaan-m/ECC).
  Conventional Commits, atomicidade de alterações, isolamento de branches e higiene de repositório.
---

# Git Workflow: Práticas de Rastreabilidade e Histórico Semântico

Este guia estabelece os padrões para controle de versão, mensagens de commit estruturadas, fluxo de trabalho em branches e higiene de repositório, garantindo um histórico limpo e auditável.

---

## 1. Padrão Conventional Commits

Todas as mensagens de commit devem seguir a estrutura padronizada:

```
<tipo>(<escopo opcional>): <descrição clara no imperativo>

[corpo opcional detalhando o motivo e contexto da alteração]
```

### Tipos Permitidos:
* **`feat`:** Introdução de uma nova funcionalidade ou capacidade no projeto.
* **`fix`:** Correção de um bug, falha de cálculo ou regressão identificada.
* **`refactor`:** Reorganização de código sem alterar seu comportamento observável externo.
* **`test`:** Adição, correção ou refatoração de testes automatizados.
* **`docs`:** Alterações exclusivas em documentações, esquemáticos conceituais ou manuais.
* **`perf`:** Modificação de código voltada especificamente para melhoria de desempenho.
* **`chore`:** Atualização de dependências, configuração de linters ou ajustes de build.

### Exemplo de Mensagens Corretas:
* `feat(daq): implementar decimação de dados do ensaio de impacto`
* `fix(parser): corrigir leitura de ponto flutuante no arquivo catman bin`
* `refactor(repositorio): desacoplar adaptador postgres da porta de dominio`
* `test(calculos): adicionar casos de borda para frequencia de golpes`

---

## 2. Princípio da Atomicidade

Cada commit deve representar uma única unidade lógica de trabalho:
1. **Comitável e Compilável:** O projeto deve continuar compilando e passando nos testes a cada commit intermediário.
2. **Separação de Preocupações:** Nunca misture correções de formatação/linting com mudanças de regras de negócio no mesmo commit.
3. **Diffs Contidos:** Commits menores facilitam o code review, aceleram a identificação de regressões via `git bisect` e evitam conflitos de merge.

---

## 3. Estratégia de Branches

* **`main`:** Branch principal sempre estável e pronta para implantação.
* **Branches Temporárias:**
  * `feature/<nome-curto>`: Para desenvolvimento de novas capacidades.
  * `bugfix/<nome-curto>`: Para correção de falhas em ambiente de desenvolvimento.
  * `hotfix/<nome-curto>`: Para correções emergenciais aplicadas diretamente sobre a versão estável.
* **Ciclo de Vida Curto:** Branches devem ser fundidas e removidas logo após a conclusão da tarefa para evitar desvios prolongados em relação à branch principal.

---

## 4. Higiene do Repositório e Auditoria Pré-Commit

Antes de executar `git commit`, realize as checagens:
1. **Verificar Estado com Concisão:**
   ```powershell
   git status --short
   ```
2. **Revisar o Diff das Alterações Selecionadas:**
   ```powershell
   git diff --staged
   ```
3. **Bloqueio de Arquivos Indesejados:** Certifique-se de que arquivos de lock temporários, caches locais (`__pycache__`, `.pytest_cache`), pastas virtuais (`.venv`) e arquivos de segredos (`.env`) nunca sejam adicionados ao commit.

---

## 5. Integração com Histórico Linear

* **Rebase Local:** Antes de abrir um Pull Request, atualize sua branch com a base mais recente utilizando rebase (`git pull --rebase origin main`) para manter uma linha do tempo clara sem commits de merge redundantes.
* **Squash no Merge:** Ao concluir um PR com vários commits intermediários de ajuste ("wip", "ajustes no teste"), utilize a opção squash merge para condensar as alterações em uma única entrada semântica no histórico principal.
