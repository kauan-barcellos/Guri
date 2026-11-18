---
name: github-ops
description: >-
  Automação de operações no GitHub via linha de comando gh CLI (baseado em affaan-m/ECC).
  Gerenciamento de Pull Requests, triagem de issues, download de artefatos e criação de releases.
---

# GitHub Operations: Automação via CLI Oficial (`gh`)

Este guia padroniza a gestão de repositórios remotos, fluxos de Pull Request, triagem de incidentes e pipelines de CI/CD utilizando a ferramenta oficial de linha de comando do GitHub (`gh`).

---

## 1. Princípios de Execução

* Todas as operações de GitHub são executadas de modo direto e programático via terminal, sem depender de navegação manual na interface web.
* Garanta que o comando `gh auth status` confirme a autenticação ativa antes de disparar comandos em lote.
* Pull Requests devem conter títulos concisos no padrão Conventional Commits (ex: `feat:`, `fix:`, `docs:`, `refactor:`) e descrição técnica das alterações.

---

## 2. Comandos e Padrões Essenciais

### A. Fluxo de Pull Requests (PRs)
* **Criar Pull Request:**
  ```powershell
  gh pr create --title "feat: adicionar driver de comunicacao labjack" --body "## O que foi feito`n- Implementado driver Lua para leitura de canais analógicos.`n- Adicionados testes de integridade." --base main
  ```
* **Verificar Status de Testes e CI do PR Ativo:**
  ```powershell
  gh pr checks
  ```
* **Realizar Merge com Squash (Histórico Limpo):**
  ```powershell
  gh pr merge --squash --delete-branch
  ```

### B. Gestão de Issues
* **Listar Issues Abertas com Tags Específicas:**
  ```powershell
  gh issue list --label "bug" --state open --limit 10
  ```
* **Criar Nova Issue Técnica:**
  ```powershell
  gh issue create --title "Investigar instabilidade de amostragem a 100kHz" --body "Durante ensaios de impacto, observou-se jitter na amostragem." --label "investigacao"
  ```

### C. Monitoramento de Pipelines (GitHub Actions)
* **Visualizar Últimas Execuções de CI:**
  ```powershell
  gh run list --limit 5
  ```
* **Inspecionar Log de Execução que Falhou:**
  ```powershell
  gh run view <RUN_ID> --log-failed
  ```

### D. Criação de Releases Versionadas
* **Publicar Nova Release a partir de Tag:**
  ```powershell
  gh release create v1.2.0 --title "Release v1.2.0" --notes "Notas das alteracoes incluidas nesta versao."
  ```

---

## 3. Checklist de Higiene e Segurança

* [ ] Verifique se todas as alterações locais foram commitadas antes de abrir o PR.
* [ ] Certifique-se de que os testes locais passaram antes de solicitar revisão remota.
* [ ] Ao realizar merge, prefira o modo `squash` para manter o histórico da branch principal limpo e legível.
