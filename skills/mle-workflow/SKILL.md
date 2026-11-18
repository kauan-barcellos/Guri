---
name: mle-workflow
description: >-
  Protocolo para conversão de notebooks experimentais em pipelines de machine learning reprodutíveis para produção (baseado em affaan-m/ECC).
  Contratos de dados, validação estrita, modularização e reprodutibilidade.
---

# Machine Learning Engineering Workflow: Do Notebook à Produção

Este guia define as etapas técnicas para transformar scripts de exploração e Jupyter Notebooks em pacotes de software de aprendizado de máquina e processamento de dados robustos, tipados e reprodutíveis.

---

## 1. O Problema do Notebook em Produção

Notebooks são ferramentas excelentes para análise exploratória, testes visuais de hipóteses e prototipagem rápida. No entanto, carregam armadilhas críticas quando levados para produção:
* Dependência de ordem oculta de execução de células.
* Poluição do namespace global com variáveis intermediárias.
* Ausência de validação de schemas de entrada e saída.
* Dificuldade de testes automatizados e integração contínua (CI/CD).

---

## 2. As Quatro Etapas de Migração para Produção

```
[ Notebook Exploratório ]
            |
            v
+------------------------------------------+
| 1. Linearização e Expurgos de Estado     |
+------------------------------------------+
            |
            v
+------------------------------------------+
| 2. Criação de Contratos de Dados         | (Schemas Pydantic / Dataclasses)
+------------------------------------------+
            |
            v
+------------------------------------------+
| 3. Decomposição Modular em Funções Puras | (Ingestão -> Features -> Modelo)
+------------------------------------------+
            |
            v
+------------------------------------------+
| 4. Testes de Regressão e Reprodutibilidade | (Seeds fixadas, logs estruturados)
+------------------------------------------+
```

### Etapa 1: Linearização e Expurgos de Estado
* Garantir que o pipeline possa ser executado do início ao fim de forma estritamente sequencial, sem dependências circulares.
* Substituir variáveis globais por parâmetros explícitos passados entre funções.

### Etapa 2: Contratos de Dados Formais
* Toda entrada de dados (tabelas, tensores, sinais temporais ou matrizes) deve ser validada por um contrato explícito (ex: usando Pydantic, Marshmallow ou Dataclasses com tipagem estrita).
* Rejeitar dados faltantes ou fora de escala logo na borda de ingestão antes de iniciar o processamento pesado.

### Etapa 3: Decomposição Modular
Separe o código em módulos atômicos com responsabilidades delimitadas:
* `data_loader.py`: Ingestão, leitura de bancos, arquivos ou sensores.
* `features.py`: Pré-processamento, filtragem e engenharia de variáveis.
* `model.py`: Instanciação, carregamento de pesos e inferência.
* `metrics.py`: Cálculo de métricas de avaliação e detecção de drift.

### Etapa 4: Reprodutibilidade Estrita
* Fixar sementes aleatórias (random seeds em NumPy, PyTorch, Scikit-Learn) sempre que houver amostragem estocástica.
* Versionar artefatos e hiperparâmetros de treinamento juntamente com o código.

---

## 3. Estrutura Padrão de Repositório de Engenharia de ML

```text
projeto_ml/
├── data/
│   ├── raw/                     # Dados brutos originais (somente leitura)
│   └── processed/               # Dados tratados prontos para o pipeline
│
├── models/                      # Arquivos serializados de pesos e modelos (.onnx, .pkl)
│
├── src/
│   ├── contracts/               # Schemas de dados de entrada e saída
│   ├── pipeline/
│   │   ├── preprocessing.py     # Limpeza e transformações
│   │   └── inference.py         # Carregamento e predição
│   └── utils/
│       └── logging.py           # Logs estruturados e métricas
│
├── tests/                       # Testes automatizados de regressão
└── requirements.txt             # Dependências com versões exatas fixadas
```

---

## 4. Checklist de Homologação para Produção

* [ ] O código roda de ponta a ponta sem qualquer dependência de ambiente de notebook.
* [ ] As entradas de dados possuem validação estrita de tipos e dimensões.
* [ ] Não há números mágicos nem caminhos de arquivos gravados de forma fixa no código (uso de arquivos de configuração ou variáveis de ambiente).
* [ ] Foram implementados testes unitários para a etapa de transformação de dados e inferência do modelo.
* [ ] O consumo de memória RAM e tempo de processamento foram auditados em lotes representativos.
