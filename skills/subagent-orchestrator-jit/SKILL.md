---
name: subagent-orchestrator-jit
description: >-
  Orquestrador dinâmico Just-in-Time (JIT) de subagentes. Analisa a complexidade da solicitação em 3 níveis e convoca
  subagentes especializados sob demanda apenas quando a tarefa for complexa ou crítica, preservando a janela de contexto.
---

# Subagent Orchestrator JIT: Orquestração Dinâmica Just-in-Time

Este guia estabelece o protocolo operacional do agente principal como Engenheiro Coordenador, garantindo que subagentes especializados sejam ativados apenas quando estritamente necessários, mantendo a conversa principal rápida, concisa e econômica em tokens.

---

## 1. O Triângulo de Classificação de Complexidade

Antes de iniciar qualquer execução, analise a solicitação do usuário e enquadre-a em um dos três níveis:

```
[ Solicitação do Usuário ]
            │
            ├─► Nível 1: Baixa Complexidade ──► Execução Direta (Sem subagente)
            │
            ├─► Nível 2: Média Complexidade ──► Execução com Skills Locais
            │
            └─► Nível 3: Alta Complexidade ───► Ativação Dinâmica JIT de Subagente
```

### Nível 1: Baixa Complexidade (Execução Direta)
* **Critérios:** Tarefas pontuais, ajustes em uma única função, consultas conceituais, correções de sintaxe ou comandos simples.
* **Ação:** O agente principal resolve imediatamente no chat principal.
* **Proibição:** Não invocar nenhum subagente.

### Nível 2: Média Complexidade (Execução com Skills Locais)
* **Critérios:** Implementação de novas funcionalidades em até 2 arquivos, escrita de testes convencionais, refatorações moderadas ou criação de commits semânticos.
* **Ação:** O agente principal implementa seguindo as diretrizes das Skills carregadas (`python-testing`, `git-workflow`, `search-first`).

### Nível 3: Alta Complexidade e Criticidade (Ativação Dinâmica JIT)
* **Critérios Obrigatórios (pelo menos um deve ser atendido):**
  1. **Volume de Leitura:** A análise exige ler mais de 3 arquivos grandes ou analisar centenas de linhas de traceback/logs.
  2. **Necessidade de Imparcialidade:** Auditoria de segurança, code review adversarial pré-commit ou revisão de regressões lógicas.
  3. **Operação de Alto Risco:** Alteração estrutural em banco de dados em produção, migrações com dados reais ou configurações de rede.
  4. **Falha Persistente:** O compilador ou teste quebrou mais de duas vezes com erros complexos de tipagem ou dependência.

---

## 2. Protocolo de Ciclo de Vida JIT

Quando uma tarefa é classificada como **Nível 3**, o orquestrador executa o seguinte fluxo:

```
1. Localizar Perfil no Catálogo
   (C:\Users\kauam.barcellos\.gemini\config\agents\<agente>.md)
              │
              ▼
2. Validar se Agente já está Registrado
   (Se não estiver, registrar dinamicamente com define_subagent)
              │
              ▼
3. Invocar Subagente com Prompt Delimitado
   (invoke_subagent com dados objetivos e isolamento de escopo)
              │
              ▼
4. Receber Relatório Sintetizado
   (Apenas o parecer técnico conciso entra no contexto principal)
              │
              ▼
5. Liberar Recursos
   (Encerrar o subagente após a entrega para liberar workspaces)
```

---

## 3. Catálogo de Perfis Especializados em Disco

Os perfis de agentes ficam armazenados em `C:\Users\kauam.barcellos\.gemini\config\agents\`. 
O orquestrador consulta o catálogo sob demanda, garantindo custo zero de tokens no cabeçalho durante tarefas rotineiras.

---

## 4. Checklist do Orquestrador

* [ ] Classifiquei o nível de complexidade antes de agir.
* [ ] Se for Nível 1 ou 2, executei diretamente sem abrir subagentes.
* [ ] Se for Nível 3, selecionei o perfil estritamente adequado para a tarefa.
* [ ] O prompt enviado ao subagente contém apenas o contexto necessário (arquivos específicos, logs ou diffs).
* [ ] O parecer final retornado ao usuário é limpo, direto e sem poluição de logs intermediários.


---

## 5. Integração com Fan-Out e MapReduce
Quando a tarefa de Nível 3 envolver varredura massiva de mais de 10 arquivos independentes ou auditoria concorrente de múltiplos repositórios, o orquestrador JIT convoca o padrão [subagent-orchestrator-mapreduce](file:///C:/Users/kauam.barcellos/.gemini/config/skills/subagent-orchestrator-mapreduce/SKILL.md) para processamento distribuído.
