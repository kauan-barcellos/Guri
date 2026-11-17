---
name: prompt-fabric
description: >-
  Padrões modulares de prompt (Fabric Patterns) para estruturação atômica de tarefas.
  Use para decompor pedidos do usuário em etapas cirúrgicas (extrair sabedoria, analisar argumentos, gerar resumos técnicos, auditar código).
---

# Padrões Modulares de Prompt: Padrão Fabric (Daniel Miessler)

Esta habilidade aplica a filosofia do projeto Fabric para desconstruir problemas complexos em padrões atômicos reutilizáveis e altamente objetivos.

---

## 1. Princípios do Fabric

* **Micro-especialização:** Em vez de pedir para o modelo "pensar sobre tudo", aplica-se um padrão cirúrgico projetado para uma única intenção cognitiva.
* **Seções Padronizadas:** Todo padrão opera com divisões claras:
  * `IDENTITY and GOALS`: Quem é o agente e o que ele deve alcançar.
  * `INPUT FORMAT`: O formato esperado dos dados recebidos.
  * `STEPS`: Sequência numerada e determinística de raciocínio.
  * `OUTPUT INSTRUCTIONS`: Regras estritas de formatação (tabelas, listas, Markdown, sem enrolação).
* **Componibilidade via Terminal:** Padrões pensados para serem encadeados como pipes do Unix (`cat dados | extrair_ideias | resumir`).

---

## 2. Padrões Mais Usados no Guri

1. **`extract_wisdom` (Extração de Sabedoria):**
   * Identifica ideias centrais, fatos, recomendações práticas e lições aprendidas de textos extensos ou transcrições de reuniões.
2. **`analyze_claims` (Análise Crítica de Afirmações):**
   * Avalia a solidez de argumentos técnicos, verificando se há respaldo empírico ou se são apenas suposições.
3. **`code_review_security` (Revisão de Código e Segurança):**
   * Varredura minuciosa de scripts para encontrar brechas, caminhos codificados com dados sensíveis e vazamento de recursos.
4. **`create_summary_technical` (Resumo Técnico para Decisão):**
   * Transforma relatórios longos de ensaio ou medição em resumos executivos com tabelas comparativas e recomendações de projeto.

---

## 3. Aplicação no Início de Toda Mensagem

Quando o usuário faz um pedido:
1. O Guri identifica qual padrão do Fabric melhor se encaixa na necessidade imediata.
2. Aplica a estrutura mental do padrão antes de redigir qualquer linha de código ou texto.
3. Entrega a resposta final de forma enxuta, mantendo apenas a substância técnica.
