---
name: pesquisa-tavily
description: >-
  Especialista em pesquisa rápida e contextual na internet via Tavily / RAG.
  Use quando precisar de respostas diretas, fatos consolidados, fontes citadas e contexto limpo sem ruído de HTML.
---

# Pesquisa na Internet: Padrão Tavily (Search & RAG Aggregator)

Esta habilidade orienta o agente na execução de pesquisas na web otimizadas para modelos de linguagem e pipelines de RAG (Retrieval-Augmented Generation).

---

## 1. Princípios Operacionais do Tavily

O buscador tradicional devolve links azuis e trechos desconexos. O padrão Tavily opera de forma diferente:
* **Remoção de ruído:** Elimina cabeçalhos, rodapés de navegação, banners de cookies e propagandas antes de processar o texto.
* **Agregação multi-fonte:** Não confia em um único resultado. Cruza dados de 3 a 5 fontes para validar números e versões.
* **Citação explícita:** Toda afirmação factual deve vir acompanhada da fonte ou URL de origem.
* **Foco em síntese:** Entrega o dado pronto para raciocínio, sem forçar o agente a baixar dezenas de páginas HTML brutas.

---

## 2. Quando Escolher este Padrão

* Validação de versões de bibliotecas, compatibilidade de ferramentas e comandos de terminal.
* Levantamento de especificações elétricas e pinagens de módulos comerciais.
* Busca de soluções para mensagens de erro em fóruns técnicos (Stack Overflow, GitHub Issues).
* Resumo rápido de notícias de tecnologia ou atualizações regulatórias.

---

## 3. Protocolo de Consulta

1. **Formulação da Query:**
   * Evite buscas vagas. Use palavras-chave técnicas e nomes exatos de pacotes ou ferramentas.
   * Exemplo: `"APReader" python catman "sampling rate"` em vez de `"como ler arquivo catman"`.

2. **Extração e Filtragem:**
   * Isole o trecho exato que responde à pergunta do usuário.
   * Descarte seções opinativas ou introduções prolixas de blogs.

3. **Validação Cruzada:**
   * Se houver divergência entre fontes (ex: versões mínimas de Python suportadas), aponte a divergência claramente.
