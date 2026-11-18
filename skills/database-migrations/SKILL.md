---
name: database-migrations
description: >-
  Diretrizes de migrações de banco de dados seguras, reversíveis e com zero downtime (baseado em affaan-m/ECC).
  Separação de DDL e DML, padrão expand-contract e criação concorrente de índices.
---

# Database Migrations: Padrão Seguro e Zero Downtime

Este guia define as diretrizes para evolução de esquemas e dados em bancos de dados relacionais, garantindo reversibilidade, integridade e ausência de bloqueios em produção.

---

## 1. Princípios Fundamentais

1. **Separação Rígida entre DDL e DML:**
   * **Migrações DDL (Estrutura):** `CREATE TABLE`, `ALTER TABLE`, `ADD COLUMN`.
   * **Migrações DML (Dados):** `UPDATE`, `INSERT`, `DELETE`, normalização e preenchimento de colunas.
   * *Nunca misture alterações de estrutura e migrações massivas de dados no mesmo script.*

2. **Criação de Índices sem Bloqueio de Tabela:**
   * No PostgreSQL, utilize sempre `CREATE INDEX CONCURRENTLY` para evitar travar leituras e escritas durante a indexação de tabelas volumosas.
   * Índices concorrentes não podem rodar dentro de blocos transacionais normais (`autocommit=True` exigido no gerenciador de migração).

3. **Estratégia Forward-Only em Produção:**
   * Embora toda migração deva ter um script de reversão (`down`), correções em ambientes de produção devem ser tratadas como novas migrações incrementais para frente, preservando a rastreabilidade do histórico.

---

## 2. O Padrão Expand-Contract (Zero Downtime)

Para alterar colunas ou renomear campos sem derrubar a aplicação ativa:

```
Passo 1 (Expand):       Adicionar a nova coluna mantendo a antiga ativa.
Passo 2 (Dual Write):   A aplicação grava em ambas as colunas e lê da antiga.
Passo 3 (Backfill):     Script DML em lotes (chunks) preenche a nova coluna com dados históricos.
Passo 4 (Switch):       A aplicação passa a ler e gravar exclusivamente na nova coluna.
Passo 5 (Contract):     Remoção segura da coluna antiga em uma migração posterior.
```

---

## 3. Diretrizes para Operações Críticas

### A. Adicionar Colunas com Valores Padrão (NOT NULL DEFAULT)
* Em versões modernas do PostgreSQL (>= 11), `ALTER TABLE ... ADD COLUMN ... DEFAULT ...` é uma operação rápida de metadados.
* Em bancos legados, adicione primeiro a coluna como anulável, preencha o valor padrão em lotes pequenos e, por fim, aplique a restrição `SET NOT NULL`.

### B. Remoção de Colunas ou Tabelas
* Antes de rodar um `DROP COLUMN`, garanta que nenhuma versão ativa da aplicação esteja consultando o campo.
* Remova as referências no código, publique a nova versão da aplicação e apenas depois execute a migração de remoção no banco.

### C. Atualizações de Dados em Massa (Backfills)
* Nunca execute `UPDATE tabela SET campo = valor` em tabelas com centenas de milhares de linhas sem paginação.
* Quebre a atualização em lotes delimitados por ID (por exemplo, lotes de 1.000 a 5.000 registros), com pausas de alguns milissegundos entre lotes para não esgotar as conexões nem saturar o I/O do banco.

---

## 4. Checklist Pré-Publicação

* [ ] A migração DDL está isolada de qualquer script DML.
* [ ] Índices foram configurados com execução concorrente (`CONCURRENTLY`).
* [ ] Nenhuma tabela de alta volumetria sofrerá lock exclusivo prolongado.
* [ ] Existe script de reversão validado localmente.
* [ ] O código da aplicação é retrocompatível com o banco durante o momento da migração.
