---
name: executive-summary
description: >-
  Geracao de resumos executivos de 1 pagina e relatorios consolidados de ensaios e medicoes de bancada.
  Use apos sessoes de teste (Catman, LabJack, ensaios de torque ou carga) para entregar conclusoes tecnicas diretas para tomada de decisao.
---

# Resumo Executivo e Relatorio de Ensaio (Executive Summary)

Esta skill formata resultados de ensaios fisicos, medicoes em osciloscopio, testes de torque, calibracoes e analises de aquisicao em um relatorio condensado de exatamente uma pagina. O objetivo e fornecer uma conclusao tecnica clara para engenheiros lideres, clientes ou gestores sem perder tempo com prolixidade.

---

## 1. Estrutura Padrao de 1 Pagina

O relatorio e salvo em `relatorios/resumo_ensaio_[data].md` ou entregue no chat seguindo 5 blocos obrigatorios:

### 1. Cabecalho de Ensaio
* Dispositivo Sob Teste (DUT): [Codigo / Modelo]
* Data e Local: YYYY-MM-DD (Bancada de Testes)
* Instrumentacao Utilizada: (ex: HBM Catman, LabJack T7-PRO, Torquimetro)
* Responsavel Tecnico: [Nome]

### 2. Resumo Direto (O Resultado em 3 Linhas)
* Declaracao binaria de aprovacao (Aprovado / Reprovado / Aprovado com Ressalvas).
* Principal valor medido versus limite estipulado.
* Acao recomendada imediata.

### 3. Tabela de Metricas Criticas
| Parametro | Limite Min | Nominal | Limite Max | Medido | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Torque de Pico | 15.0 Nm | 18.0 Nm | 20.0 Nm | 18.4 Nm | CONFORME |
| Ripple de Tensao | - | 50 mV | 100 mV | 62 mV | CONFORME |

### 4. Anomalias e Eventos Fora da Faixa
Listagem em tópicos de qualquer leitura espuria, ruido detectado ou comportamento imprevisto durante o ensaio. Se nao houver anomalias, registrar explicitamente "Nenhuma anomalia observada durante o ciclo de testes".

### 5. Conclusao e Decisao de Engenharia
Decisao tecnica justificada sobre liberar o lote, modificar o circuito ou prosseguir com a proxima etapa de homologacao.
