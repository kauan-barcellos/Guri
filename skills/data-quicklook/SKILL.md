---
name: data-quicklook
description: >-
  Inspecao estatistica e visualizacao rapida de arquivos de aquisicao de dados e sinais de bancada (CSV, BIN, TXT).
  Use para carregar medicoes de DAQ, calcular picos, medias, RMS e gerar graficos limpos de verificacao imediata no terminal.
---

# Inspecao Rapida de Sinais e Dados (Data Quicklook)

Esta skill automatiza a analise preliminar de arquivos de medicao gerados na bancada (adquiridos via LabJack, HBM Catman, osciloscopios ou logs seriais). Ela calcula parametros estatisticos fundamentais e gera graficos de verificacao rapida em formato PNG limpo.

---

## 1. Metricas Calculadas Automaticamente

O script `scripts/quicklook.py` processa o arquivo tabular e reporta:
* Total de amostras e duracao temporal estimada.
* Frequencia media de amostragem (taxa em Hz).
* Minimo, Maximo e Amplitude Pico a Pico (Pk-Pk).
* Media aritmetica e Nivel DC.
* Valor Eficaz (RMS) e Desvio Padrao (sigma).

---

## 2. Execucao pelo Terminal

```bash
# Inspecionar estatisticas de todas as colunas:
python scripts/quicklook.py --input medicoes/ensaio_torque.csv

# Gerar grafico PNG de uma coluna especifica com relacao ao tempo:
python scripts/quicklook.py --input medicoes/ensaio_torque.csv --plot "Torque_Nm" --time "Time_s" --output relatorios/torque_plot.png
```

---

## 3. Regras de Apresentacao

* Apresentar os resultados sempre com as unidades fisicas correspondentes.
* Destacar imediatamente se o valor medio estiver deslocado (offset DC inesperado) ou se houver picos anomalos fora de 3 desvios padrao (3-sigma).
