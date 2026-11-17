---
name: pesquisa-brave
description: >-
  Consultas rápidas e de alto volume em índice global independente via Brave Search.
  Use para varredura multi-link, descoberta rápida de URLs e dados brutos em JSON sem viés de mecanismos tradicionais.
---

# Pesquisa Independente: Padrão Brave Search (Fast & Neutral Global Index)

Esta habilidade orienta o agente na execução de consultas velozes e neutras contra um índice independente da web mundial.

---

## 1. Princípios Operacionais do Brave Search

* **Independência total de índice:** Não depende do ecossistema de dados do Google ou da Microsoft/Bing, oferecendo resultados sem filtros de personalização ou viés de histórico.
* **Saída direta em JSON estruturado:** Entrega títulos, URLs canônicas, trechos limpos e datas de publicação para consumo imediato por scripts ou agentes.
* **Velocidade e baixo consumo de recursos:** Latência mínima por requisição, ideal para checagens preliminares de existência de ferramentas ou pacotes.
* **Cobertura neutra da comunidade técnica:** Forte indexação de repositórios open-source, fóruns de desenvolvedores e portais alternativos.

---

## 2. Quando Escolher este Padrão

* Mapeamento inicial de quais ferramentas ou bibliotecas existem para resolver um problema.
* Busca por links de repositórios no GitHub, GitLab ou registros do PyPI/npm.
* Obtenção de listas de URLs candidatas para posterior aprofundamento (usando Firecrawl nas mais relevantes).
* Verificação de tendências e discussões recentes em fóruns especializados.

---

## 3. Protocolo de Descoberta

1. **Consulta Ampla para Mapeamento:**
   * Use operadores lógicos simples para listar alternativas viáveis.
   * Exemplo: `"catman" OR "APReader" alternative python library`.

2. **Triagem de Relevância:**
   * Avalie data de atualização, número de estrelas no repositório e consistência da documentação.
   * Filtre resultados repetidos ou sites agregadores de baixa qualidade.

3. **Encaminhamento de Fluxo:**
   * Se os dados do snippet forem conclusivos, responda diretamente.
   * Se o tópico exigir estudo minucioso de código ou arquitetura, encadeie com a leitura da documentação completa.
