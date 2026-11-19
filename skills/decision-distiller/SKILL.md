---
name: decision-distiller
description: >-
  Destilador de decisoes de bancada, preferencias tecnicas do usuario e licoes aprendidas em arquivos vivos de contexto.
  Use apos correcoes de curso do usuario ou ao consolidar escolhas de arquitetura para atualizar a memoria persistente do projeto.
---

# Destilador de Decisoes e Preferencias (Decision Distiller)

Esta skill monitora correcoes de curso, escolhas de design e diretrizes fornecidas pelo usuario durante a execucao dos trabalhos, destilando esses aprendizados em registros atomicos de contexto para evitar repeticao de erros e manter o alinhamento com as preferencias de bancada.

---

## 1. Gatilhos de Ativacao

A destilacao e acionada nos seguintes cenarios:
1. **Correcao Direta:** Quando o usuario corrige uma escolha de componente, biblioteca, padrao de nomenclatura, estilo de codigo ou restricao fisica de hardware.
2. **Definicao de Topologia:** Quando uma decisao de arquitetura ou protocolo de comunicacao e formalizada.
3. **Restricao de Projeto:** Quando um limite operacional e fixado (exemplo: tensao maxima em pino, frequencia de amostragem padrao, margem de seguranca termica).

---

## 2. Destino das Decisoes

Dependendo do alcance, a decisao e gravada no local apropriado:
* **Escopo do Projeto:** Gravada em `.context/decisions.md` no workspace ativo.
* **Escopo Global de Bancada:** Gravada nas regras centrais do usuario ou no `agent-memory`.

---

## 3. Formato do Registro Atomico

Cada entrada no `.context/decisions.md` segue o modelo simplificado abaixo:

```markdown
### [DEC-XXX] Titulo Curto da Decisao
* Data: YYYY-MM-DD
* Contexto: Motivo que levou a discussao ou correcao
* Decisao: Regra adotada de forma clara e prescritiva
* Justificativa Tecnica: Causa fisica, eletrica ou de arquitetura
* Regra Pratica: Como o assistente deve agir a partir de agora
```

---

## 4. Regras Operacionais

1. **Atomicidade:** Cada decisao aborda apenas um ponto especifico.
2. **Sem Ambiguidade:** A regra pratica deve ser direta, dizendo exatamente o que usar e o que evitar.
3. **Confirmacao Rapida:** Apos registrar a decisao, informar ao usuario em uma frase que o aprendizado foi indexado na memoria do projeto.
