---
name: gateguard
description: >-
  Trava determinística de pré-execução e verificação de fatos (Fact-Forcing Gate, baseado em affaan-m/ECC).
  Bloqueia edições e comandos arriscados até que premissas, escopos e dependências sejam explicitamente confirmados.
---

# GateGuard: Validação e Forçamento de Fatos Pré-Execução

Este guia estabelece um mecanismo de portão de qualidade (Fact-Forcing Gate) para impedir execuções cegas, operações destrutivas ou edições precipitadas em ambientes de desenvolvimento e produção.

---

## 1. O Modelo dos Três Estágios (Deny -> Force -> Allow)

Qualquer operação que altere arquivos de configuração, banco de dados ou execute comandos de sistema com potencial destrutivo deve passar pelas seguintes etapas:

```
[ Ação Arriscada ]
       |
       v
+--------------+     Faltam Fatos?     +-------------------------+
| Estágio 1:   | --------------------> | Estágio 2:              |
| Negar (Deny) |                       | Forçar Fatos (Force)    |
+--------------+                       +-------------------------+
       |                                            |
       | Fatos Consolidados                         | Fatos Declarados
       v                                            v
+----------------------------------------------------------------+
| Estágio 3: Liberar Execução (Allow)                            |
+----------------------------------------------------------------+
```

1. **Estágio 1: Negar (Deny):**
   Interrompe o impulso imediato de rodar comandos perigosos ou alterar código crítico quando o contexto estiver incompleto.
2. **Estágio 2: Forçar Fatos (Force Facts):**
   Exige a declaração explícita dos 4 fatos fundamentais da operação:
   * **Fato A (Alvo):** Qual é o arquivo ou componente exato a ser alterado?
   * **Fato B (Causa):** Qual evidência empírica ou erro fundamenta essa intervenção?
   * **Fato C (Impacto):** Quais módulos ou serviços dependem desse componente?
   * **Fato D (Reversibilidade):** Como reverter a ação caso o resultado seja adverso?
3. **Estágio 3: Liberar (Allow):**
   Executar a operação de maneira contida, cirúrgica e com registro explícito.

---

## 2. Comandos e Ações Sujeitos ao GateGuard

As seguintes operações exigem passagem obrigatória pelo GateGuard:

* **Manipulação de Sistema de Arquivos e Git:**
  * Comandos de exclusão recursiva ou forçada (`rm -rf`, `Remove-Item -Recurse -Force`).
  * Comandos destrutivos de Git (`git reset --hard`, `git clean -fd`, `git push --force`).
* **Bancos de Dados e Migrações:**
  * Comandos DDL diretos que descartam estruturas (`DROP TABLE`, `DROP COLUMN`, `TRUNCATE`).
  * Atualizações em massa sem cláusula `WHERE` explícita ou sem transação (`BEGIN ... ROLLBACK`).
* **Ambiente e Dependências:**
  * Alterações em manifestos de produção sem validação de lockfiles.
  * Execução de instalações globais que possam conflitar com ambientes virtuais ativos.

---

## 3. Protocolo de Aplicação

Ao planejar uma das ações da lista sujeita ao GateGuard:
1. Declare os 4 fatos de validação no raciocínio antes de invocar a ferramenta.
2. Certifique-se de que cópias de segurança ou snapshots do estado anterior estejam preservados.
3. Execute o comando com parâmetros defensivos (modo dry-run, verbose ou dentro de uma transação).
4. Verifique o resultado imediatamente após a execução para confirmar a integridade do sistema.
