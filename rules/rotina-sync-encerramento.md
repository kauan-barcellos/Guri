# Rotina de Encerramento e Sincronização do Agente

Esta regra é de cumprimento obrigatório pelo Antigravity ao final de qualquer sessão de trabalho.

---

## Gatilhos de Ativação
Quando o usuário disser palavras ou frases como:
* "Vou encerrar", "vamos parar por hoje", "fechar a sessão", "vou sair", "até amanhã", "tchau", "pode fechar", ou similar.

---

## Procedimento Obrigatório

1. **Revisar e Salvar Aprendizados:**
   * Garantir que novos procedimentos, fórmulas ou scripts de sucesso foram documentados em `skills/` ou `rules/`.

2. **Acionar o Sync do Cérebro:**
   * Rodar ou orientar a execução do `sync_brain.ps1` localizado no diretório de trabalho ou executar a sincronização em `$HOME\.gemini\config`:
     ```powershell
     cd $HOME\.gemini\config
     git add -A
     git commit -m "Auto-sync ao encerrar sessao ($(Get-Date -Format 'dd/MM/yyyy HH:mm'))"
     git push origin main
     ```

3. **Status de Confirmação:**
   * Confirmar ao usuário que o repositório remoto foi atualizado com sucesso e que a próxima máquina poderá carregar os conhecimentos com `git pull`.
