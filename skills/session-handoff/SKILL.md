---
name: session-handoff
description: >-
  Protocolo de passagem de turno e persistencia de estado entre sessoes via .context/handoff.md.
  Use ao encerrar tarefas longas, antes de reiniciar a conversa ou ao iniciar uma nova sessao para recuperar o fio da meada.
---

# Protocolo de Passagem de Turno (Session Handoff)

Esta skill resolve a perda de contexto operacional entre diferentes sessoes de terminal ou reinicios de conversa, garantindo que o assistente retome o trabalho exatamente do ponto em que parou sem exigir que o usuario reexplique o estado do projeto.

---

## 1. O Arquivo Vivo (.context/handoff.md)

Toda passagem de turno e registrada em um arquivo centralizado no projeto em `.context/handoff.md`. Esse arquivo e mantido no workspace e segue a estrutura padrao abaixo:

```markdown
# Session Handoff: [Nome do Projeto / Modulo]

## 1. Metadados da Sessao
* Data/Hora: YYYY-MM-DD HH:MM
* Branch Git: feature/... ou main
* Ultimo Commit: [hash ou mensagem]
* Responsavel: [Usuario / Assistente]

## 2. O que foi Concluido
* [x] Item 1 finalizado e verificado
* [x] Item 2 com testes passando

## 3. Estado Atual e Variaveis Criticas
* Arquivos modificados principais: `caminho/para/arquivo`
* Parametros de configuracao: pinagens, taxas de amostragem, limites eletricos ou regras ativas
* Decisoes tecnicas tomadas no turno

## 4. Bloqueios e Questoes Pendentes
* Duvidas de projeto aguardando validacao
* Testes que falharam ou dependencias externas pendentes

## 5. Proximo Passo Imediato
* Primeira acao concreta a ser executada no inicio do proximo turno
```

---

## 2. Regras de Ativacao

### Ao Iniciar uma Nova Sessao
1. Verificar se existe o arquivo `.context/handoff.md` no workspace.
2. Se existir, ler os itens 3 (Estado Atual) e 5 (Proximo Passo Imediato).
3. Reportar ao usuario em 2 a 3 linhas o estado encontrado e confirmar se prossegue com o proximo passo imediato.

### Ao Finalizar uma Sessao ou Marco
1. Executar o script auxiliar `python scripts/handoff.py --generate` para capturar os arquivos modificados no git.
2. Atualizar o bloco de pendencias e o proximo passo imediato.
3. Salvar o arquivo antes de encerrar o turno ou antes de acionar comandos de compactacao de contexto.

---

## 3. Script Auxiliar de Automacao

O script `scripts/handoff.py` automatiza a geracao e leitura do handoff:

```bash
# Para gerar ou atualizar o handoff com base no git:
python scripts/handoff.py --generate

# Para ler rapidamente o resumo da sessao anterior:
python scripts/handoff.py --read
```
