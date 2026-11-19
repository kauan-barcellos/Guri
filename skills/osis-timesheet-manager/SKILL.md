---
name: osis-timesheet-manager
description: >-
  Gestor e auditor automatico de reporte de horas e OSIs na plataforma intranet (Node.js/Express).
  Use sempre que o usuario pedir para checar horas pendentes, auditar dias faltantes no mes, ver saldo de OSIs ou lancar horas de trabalho.
---

# Gestor e Auditor de Horas e OSIs (OSIS Timesheet Manager)

Esta skill formaliza a logica de conexao, extracao, auditoria e apontamento de horas na plataforma interna de Ordens de Servico Internas (OSIs) da intranet (`http://10.1.1.82:1005`), garantindo que o assistente consiga responder com exatidao quais tarefas estao abertas, onde cada hora foi alocada e identificar dias pendentes de reporte no mes.

---

## 1. Arquitetura da Plataforma e Mecanismo de Dados

A plataforma opera em Node.js com Express e gerencia os dados sob as seguintes regras tecnicas:

1. **Autenticacao:** Realizada via `POST /login` com campos `user` e `password`, mantendo o cookie de sessao `osisApp.session`.
2. **Ciclo Contabil Semanal:** A empresa consolida ciclos de 7 dias com inicio nas quartas-feiras, com meta padrao de **42.5 horas semanais** (jornada de 8.5 horas por dia util).
3. **Mapeamento de Atividades Encerradas:**
   * A rota `/get-partial-report-page` filtra apenas tarefas com `Fim Real` em aberto.
   * Quando uma atividade e encerrada, ela sai dessa lista inicial, mas permanece salva na pagina central da ordem (`/cadastro-osi/<id>`), identificada com o simbolo de concluido.
   * O endpoint individual `/get-this-osi-activities/<id>` e o dashboard `/dashboard-executor` preservam todo o historico de dias e horas apontadas, independentemente do status da atividade.

---

## 2. Regras de Auditoria Diaria e Mensal

Ao ser acionado pelo usuario, o assistente deve:

1. **Identificar a Semana Vigente:**
   * Mapear os dias uteis de segunda a sexta da semana atual.
   * Discriminar em cada dia: total de horas, codigo da OSI e nome da atividade.
   * Descartar dias de feriado confirmados pelo usuario (exemplo: 20/11 - Consciencia Negra).

2. **Auditar o Mes Corrente:**
   * Varrer todos os dias uteis do dia 1 ate a data de hoje.
   * Identificar dias com deficit em relacao a meta de 8.5 h/dia.
   * Exibir o saldo acumulado e a diferenca exata a ser regularizada.

3. **Verificar Saldo das Atividades Abertas:**
   * Calcular o saldo disponivel de cada atividade ativa (`Horas Planejadas - Horas Gastas`).
   * Indicar ao usuario onde as horas pendentes podem ser alocadas sem estourar o orcamento da ordem.

---

## 3. Endpoints de Leitura e Escrita

* **Login:** `POST /login` (`user`, `password`)
* **Atividades Abertas:** `GET /get-partial-report-page`
* **Detalhes e Historico da Atividade:** `GET /get-this-osi-activities/:id`
* **Dashboard Semanal:** `GET /dashboard-executor`
* **Lançamento de Horas:** `POST /add-report/:id`
  * Formato: `multipart/form-data`
  * Campo `reported_date`: Timestamp em milissegundos referente a data do apontamento em UTC 06:00 (`new Date('YYYY-MM-DD').setUTCHours(6,0,0,0)`).
  * Campo `total_hours`: Quantidade de horas trabalhadas (float).

---

## 4. Uso do Script Auxiliar

O script `scripts/osis_tracker.py` encapsula toda a comunicacao sem depender de bibliotecas externas (usando apenas a biblioteca padrao do Python):

```bash
# Consultar status geral, dias com horas faltantes e semana vigente:
python scripts/osis_tracker.py

# Consultar o historico das semanas fechadas no dashboard:
python scripts/osis_tracker.py --weekly

# Lancar horas de hoje em uma atividade (exemplo 8.5h no ID 93310):
python scripts/osis_tracker.py --report --act 93310 --hours 8.5

# Lancar horas com data retroativa:
python scripts/osis_tracker.py --report --act 93310 --hours 8.5 --date 2026-11-16
```
