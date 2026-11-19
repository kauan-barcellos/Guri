---
name: tech-doc-writer
description: >-
  Padronizacao de documentacao tecnica, manuais de bancada, guias de montagem e READMEs sem enrolacao.
  Use ao produzir documentacao de engenharia para projetos de hardware, firmware e scripts de aquisicao.
---

# Redator Tecnico de Engenharia (Tech Doc Writer)

Esta skill define as diretrizes estritas para geracao de documentacao tecnica em Markdown de alta clareza. O foco e eliminar o tom generico de assistente de IA, entregando manuais de operacao, especificacoes de conectores, instrucoes de montagem e READMEs orientados a acao imediata na bancada.

---

## 1. Regras Fundamentais de Redacao Tecnica

* **Sem Intros Vazias:** Va direto ao conteudo util. Nada de frases de abertura como "Neste documento exploraremos as intricacies do sistema".
* **Sem Travessao:** Utilize virgulas, pontos, dois-pontos ou parenteses para separar clausulas.
* **Tabelas de Ligacao e Pinagem:** Sempre inclua colunas claras: Pino Fisico, Nome do Sinal, Nivel de Tensao, Sentido (Entrada/Saida) e Cuidados de Hardware.
* **Comandos Copiaveis:** Blocos de codigo devem conter instrucoes reais e prontas para execucao no terminal, sem placeholders genericos quando a informacao puder ser exata.
* **Secao Obrigatoria de Diagnostico:** Todo manual deve ter um bloco "Falhas Tipicas e Solucoes" (Troubleshooting) baseado em sintomas observaveis.

---

## 2. Estrutura Padrao de Documento Tecnico

```markdown
# [Nome do Equipamento / Placa / Firmware]

Breve descricao operacional em 2 linhas.

## 1. Diagrama de Conexoes
Tabela de pinagem e interligacao eletrica.

## 2. Instrucoes de Instalacao e Compilacao
Comandos diretos para configurar e rodar.

## 3. Parametros Operacionais
Limites eletricos, taxas de comunicacao e requisitos de alimentacao.

## 4. Diagnostico de Problemas Frequentes
Tabela de sintoma, provavel causa raiz e acao corretiva.
```
