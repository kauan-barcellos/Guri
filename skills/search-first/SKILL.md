---
name: search-first
description: >-
  Protocolo de pesquisa e leitura obrigatória de contexto antes de implementar ou modificar código (baseado em affaan-m/ECC).
  Impede suposições e reinvenção de roda forçando varredura de pacotes, APIs e código existente.
---

# Search-First: Protocolo de Pesquisa Prévia à Implementação

Este guia estabelece a obrigatoriedade de investigação sistemática antes de qualquer escrita de código, criação de funções utilitárias ou refatoração, impedindo retrabalho e inconsistências arquiteturais.

---

## 1. Princípio Fundamental

Nenhum arquivo deve ser criado ou substancialmente alterado sem que o agente tenha inspecionado ativamente o contexto do repositório. O objetivo é responder a três perguntas críticas:
1. Essa funcionalidade ou utilitário já existe no projeto?
2. As dependências já instaladas (`requirements.txt`, `pyproject.toml`, `package.json`) já fornecem uma solução padrão?
3. Quais são as convenções exatas de nomes, tratamento de erros e tipagem utilizadas nos módulos vizinhos?

---

## 2. As Três Fases de Investigação Obrigatória

Antes de apresentar ou implementar uma solução técnica, siga o roteiro:

### Fase 1: Varredura de Código Existente
* Localizar arquivos correlatos no workspace antes de propor novos módulos.
* Inspecionar classes base, interfaces ou helpers utilitários já declarados na base de código.
* Verificar se já existem testes cobrindo funcionalidades parecidas para entender os requisitos esperados.

### Fase 2: Inspeção do Manifesto de Dependências
* Checar as bibliotecas já disponíveis no ambiente para não reescrever parsers, manipuladores de arquivos, clientes HTTP ou ferramentas de cálculo matemático que já estão instaladas.
* Se uma nova biblioteca externa for necessária, justificar tecnicamente o motivo da adição antes de incluí-la.

### Fase 3: Validação de Assinaturas e Tipos
* Inspecionar os tipos exatos dos argumentos das funções consumidoras.
* Garantir conformidade com os modelos de dados e evitar divergências de parâmetros (por exemplo: strings versus paths, listas versus iteradores, tipos numéricos de ponto flutuante).

---

## 3. Checklist de Liberação para Edição

Antes de invocar ferramentas de escrita ou edição de código, valide os seguintes pontos:

* [ ] Li os arquivos de destino e os módulos diretamente afetados.
* [ ] Confirmei que a função utilitária planejada não existe em nenhum arquivo do projeto.
* [ ] Verifiquei as bibliotecas já instaladas no ambiente antes de sugerir dependências novas.
* [ ] Conheço o formato exato das entradas e saídas esperadas pelas funções chamadoras.
* [ ] Mantive o estilo, tipagem e convenções já adotados no restante da aplicação.
