# Rotina de Encerramento e Sincronizacao do Agente

Esta regra e de cumprimento obrigatorio pelo Antigravity ao final de qualquer sessao de trabalho.

---

## Gatilhos de Ativacao
Quando o usuario disser palavras ou frases como:
* "Vou encerrar", "vamos parar por hoje", "fechar a sessao", "vou sair", "ate amanha", "tchau", "pode fechar", ou similar.

---

## Procedimento Obrigatorio

1. **Passagem de Turno e Higienizacao:**
   * Executar o `workspace-janitor` (`python scripts/janitor.py --clean`) para eliminar arquivos temporarios ou caches orfaos.
   * Gerar ou atualizar o `.context/handoff.md` via `session-handoff` (`python scripts/handoff.py --generate`), registrando pendencias e o proximo passo imediato.

2. **Revisar e Salvar Aprendizados:**
   * Garantir que novas decisoes de bancada foram indexadas via `decision-distiller` ou registradas em `skills/` e `rules/`.

3. **Acionar o Sync do Cerebro:**
   * Rodar a sincronizacao em `$HOME\.gemini\config`:
     ```powershell
     cd $HOME\.gemini\config
     git add -A
     git commit -m "Auto-sync ao encerrar sessao ($(Get-Date -Format 'dd/MM/yyyy HH:mm'))"
     git push origin main
     ```

4. **Status de Confirmacao:**
   * Confirmar ao usuario que o repositorio remoto foi atualizado e que o handoff esta pronto para a proxima sessao.
