---
name: pesquisa-firecrawl
description: >-
  Raspagem avançada e extração profunda da web via Firecrawl.
  Use quando precisar extrair documentações técnicas completas, páginas complexas renderizadas em JavaScript, PDFs ou varrer domínios inteiros em formato Markdown limpo.
---

# Extração Profunda da Web: Padrão Firecrawl (Deep Web Scraping & Crawling)

Esta habilidade orienta o agente na extração exaustiva de conteúdo da internet para situações em que resumos curtos de busca não são suficientes.

---

## 1. Princípios Operacionais do Firecrawl

Diferente de uma pesquisa superficial, o padrão Firecrawl realiza a leitura e digitalização de documentações inteiras:
* **Conversão direta para Markdown:** Transforma a estrutura visual e semântica do site em Markdown limpo (títulos, listas, tabelas e blocos de código preservados).
* **Renderização completa:** Interpreta conteúdo dinâmico baseado em JavaScript (Single Page Applications, portais interativos de documentação).
* **Estruturação de documentos densos:** Extração de datasheets técnicos, manuais em PDF e APIs completas.
* **Mapeamento de subpáginas (Crawl):** Permite navegar recursivamente em tópicos encadeados de uma documentação técnica a partir da URL raiz.

---

## 2. Quando Escolher este Padrão

* Leitura de guias oficiais de ferramentas (documentação do KiCad, manuais da LabJack, APIs de hardware).
* Análise de normas técnicas ou regulamentos completos publicados em sites governamentais (ANPD, INMETRO).
* Extração de tabelas longas de especificações de componentes ou catálogos de fornecedores.
* Quando uma busca simples resulta em trechos truncados ou incompletos.

---

## 3. Protocolo de Extração

1. **Definição da URL Alvo:**
   * Localize a documentação canônica (evite páginas secundárias ou mirrors desatualizados).

2. **Hierarquização do Conteúdo:**
   * Mantenha os níveis de títulos (`#`, `##`, `###`) fiéis à hierarquia do manual original.
   * Preserve blocos de código com a linguagem indicada (ex: `python`, `powershell`, `lua`).

3. **Limpeza de Artefatos:**
   * Remova menus laterais de navegação, breadcrumbs soltos e links de rodapé.
   * Guarde tabelas de pinagem e parâmetros elétricos em formato Markdown com alinhamento correto.
