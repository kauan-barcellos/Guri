---
name: prompt-dspy
description: >-
  Engenharia de prompt programática e declarativa (Stanford DSPy).
  Use para estruturar pedidos complexos em assinaturas formais (Input -> Thought -> Output), encadeamento Chain-of-Thought / ReAct e otimização algorítmica de instruções.
---

# Engenharia de Prompt Programática: Padrão DSPy (Stanford NLP)

Esta habilidade substitui o ajuste empírico de prompts por uma abordagem declarativa, estruturada e mensurável, inspirada no framework DSPy da Universidade de Stanford.

---

## 1. Princípios do DSPy

Em vez de escrever parágrafos soltos e torcer para o modelo interpretar corretamente:
* **Assinaturas Formais (Signatures):** Toda tarefa é modelada com tipos claros de entrada e saída.
  * Formato: `Input(dados, contexto, restrições) -> Thought(critérios e cadeia de raciocínio) -> Output(entregável estruturado)`.
* **Módulos Reutilizáveis:**
  * `Predict`: Execução direta para tarefas mecânicas ou extrações simples.
  * `ChainOfThought`: Separação explícita entre a reflexão analítica prévia e a resposta final.
  * `ReAct`: Encadeamento de Pensamento -> Ação (chamada de ferramenta) -> Observação.
* **Otimização Orientada a Métricas:** O prompt evolui com base em acertos concretos (testes que passam, ausência de erros de sintaxe e conformidade de regras).

---

## 2. Como Aplicar ao Receber uma Mensagem do Usuário

Sempre que o usuário enviar uma solicitação complexa, o Guri processa internamente a assinatura:

```
[Assinatura DSPy Aplicada]
Entrada:
  - Contexto do projeto: Onde estamos trabalhando e o que já foi feito.
  - Solicitação declarada: O que o usuário pediu explicitamente.
  - Restrições implícitas: Regras anti-IA, padrões de hardware, formatos de arquivos.

Raciocínio (Thought):
  - Qual é a real causa raiz ou objetivo final?
  - Quais etapas técnicas são necessárias para garantir a entrega sem erros?
  - Há dependências de ferramentas ou arquivos que precisam ser verificadas antes?

Saída (Output):
  - Código limpo, plano executável ou resposta técnica sem floreios.
```

---

## 3. Benefícios Práticos

* Elimina ambiguidades antes de disparar ferramentas ou editar arquivos.
* Garante consistência de saída mesmo em projetos com centenas de arquivos.
* Permite manter o foco estrito no que foi solicitado sem dispersão de contexto.
