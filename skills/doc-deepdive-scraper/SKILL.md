---
name: doc-deepdive-scraper
description: >-
  Sintetizador e extrator cirurgico de documentacao tecnica, APIs e datasheets da web sem inchaço de tokens.
  Use ao pesquisar novas bibliotecas, componentes ou documentacoes online para extrair apenas tabelas de pinagem, assinaturas e exemplos praticos.
---

# Sintetizador de Documentacao Tecnica (Doc Deepdive Scraper)

Esta skill resolve o problema de inchar a janela de contexto com paginas web inteiras, documentacoes em HTML poluido ou PDFs pesados. O extrator filtra apenas informacoes tecnicas uteis, salvando o resumo condensado no scratch ou no diretorio `.context/docs/`.

---

## 1. Pipeline de Extracao em 3 Etapas

```
[1. Coleta do Texto Bruto] ──> [2. Poda de Lixo e Filtragem] ──> [3. Destilacao Compacta]
```

### Etapa 1: Coleta Limpa
* Utilizar a ferramenta de busca ou leitura (Firecrawl, Tavily ou download direto de documentacao).
* Nao despejar o conteudo cru no chat do usuario.

### Etapa 2: Poda de Lixo Semantico
O script `scripts/doc_extract.py` remove automaticamente:
* Menus de navegacao, barras laterais e breadcrumbs.
* Avisos de cookies, rodapes de copyright e publicidade.
* Estilos CSS, blocos SVG e scripts embutidos.

### Etapa 3: Destilacao e Salvamento
Extrair exclusivamente os blocos essenciais:
* Tabelas de pinagem, registradores e enderecos I2C/SPI.
* Assinaturas de classes, funcoes, parametros e retornos.
* Exemplos minimos de inicializacao e leitura.
* Limites eletricos absolutos e recomendacoes de circuito.

Salvar o arquivo final em `.context/docs/<nome_modulo>.md`.

---

## 2. Execucao do Script Auxiliar

```bash
# Limpar e estruturar um arquivo bruto salvo no scratch:
python scripts/doc_extract.py --input caminho/para/pagina_bruta.html --output .context/docs/sensor_xyz.md
```
