---
name: plan-executor
description: >-
  Execucao atomica e rastreavel de planos de engenharia passo a passo com checklists e validacao por portao.
  Use para guiar a implementacao de tarefas complexas mantendo o checklist vivo e validado a cada etapa.
---

# Executor Atomico de Planos (Plan Executor)

Esta skill organiza e executa planos de implementacao tecnicos divididos em etapas atomicas sequenciais. Baseada nos principios de execucao do `obra/superpowers`, ela assegura que cada tarefa seja implementada, testada e validada empiricamente antes do avanco para o proximo passo.

---

## 1. Estrutura do Plano de Acao (TODO.md)

O plano e registrado em `TODO.md` e decomposto em passos de curta duracao (15 a 30 minutos de trabalho cada):

```markdown
# Plano de Implementacao: [Funcionalidade]

Status: Em Andamento

- [x] **Etapa 1: Estrutura Base e Header**
  - Acao: Criar `sensor_driver.hpp` com structs estaticas e definicao de registradores.
  - Verificacao: Compilador compila o header sem erros.
  
- [ ] **Etapa 2: Implementacao da FSM de Leitura**
  - Acao: Criar funcoes de transicao de estado em `sensor_driver.cpp`.
  - Verificacao: Teste de unidade executando ciclo completo de leitura simulada.

- [ ] **Etapa 3: Integracao com Hardware Real / Script de Teste**
  - Acao: Conectar leitura ao barramento I2C e imprimir leituras raw no console serial.
  - Verificacao: Leituras consistentes recebidas por pelo menos 10 segundos contínuos.
```

---

## 2. Regras Estritas de Execucao

1. **Uma Tarefa por Turno:** Nunca execute multiplas etapas simultaneamente sem validar a anterior.
2. **Evidencia Obrigatoria:** Uma caixa de verificacao `[ ]` so e marcada como `[x]` apos a execucao bem sucedida da verificacao empírica correspondente.
3. **Parada Imediata em Falhas:** Se a verificacao falhar, interrompa o plano. Nao prossiga com as etapas seguintes acumulando erros sobre uma base instavel. Aplique o `systematic-debugging`.
4. **Atualizacao Visivel:** Sempre mostre ao usuario o progresso do checklist a cada mudanca de etapa.
