**[Guri](../README.md)** > **Skills**

# Catálogo de Habilidades Modulares (Skills)

> [!NOTE]
> Todas as habilidades abaixo seguem o padrão operacional `SKILL.md`, contendo instruções determinísticas, parâmetros e regras acionadas autonomamente pelo assistente ou via orquestrador.

---

## Engenharia de Hardware e PCB

| Habilidade | Manual de Operação | Descrição e Propósito |
| :--- | :--- | :--- |
| **`kicad10-pcb-designer`** | [SKILL.md](kicad10-pcb-designer/SKILL.md) | Especialista em desenvolvimento de esquemáticos e layout de PCB no KiCad 10.0 integrado com o KiCad MCP Server. Use quando for adicionar componentes, conectar pinos, definir net classes, rotear trilhas, gerenciar planos de terra, executar validações ERC/DRC e preparar dados de fabricação para JLCPCB. |
| **`kicad10-hardware-design`** | [SKILL.md](kicad10-hardware-design/SKILL.md) | Metodologia, regras DFM e ferramentas para desenvolvimento de placas de circuito impresso (PCB) no KiCad 10.0 com JLCPCB. Use sempre que for criar, modificar, rotear ou auditar projetos de hardware, garantindo módulos prontos (COTS), ergonomia de montagem, segregação de ruído (potência vs sinais) e regras de fabricação da JLCPCB. |
| **`kicad-regime-classifier`** | [SKILL.md](kicad-regime-classifier/SKILL.md) | Classificador de regimes físicos e elétricos de trilhas no KiCad 10.0 (IPC-2152, alta velocidade, analógico e potência). Use antes de rotear qualquer circuito para garantir larguras corretas, folgas 3W e integridade de retorno de terra. |
| **`bom-lifecycle-auditor`** | [SKILL.md](bom-lifecycle-auditor/SKILL.md) | Auditor de ciclo de vida e estoque de componentes na JLCPCB / LCSC utilizando banco local offline de 513k peças. Use ao selecionar componentes e antes de gerar a BOM para evitar custos extras de montagem ($3/linha) ou peças em falta. |
| **`embedded-pinout-planner`** | [SKILL.md](embedded-pinout-planner/SKILL.md) | Planejador e validador de pinagem e multiplexação de microcontroladores (STM32, ESP32, RP2040). Use antes de ligar fios de MCU no esquemático para evitar colisões de periféricos, strapping pins e incompatibilidades de firmware. |
| **`hardware-adr`** | [SKILL.md](hardware-adr/SKILL.md) | Gerador e mantenedor de Registros de Decisao de Arquitetura de Hardware (Hardware Architecture Decision Records). Use ao tomar decisoes criticas de topologia, escolha de componentes ou protecao para documentar justificativas tecnicas. |

---

## Ensaios Físicos e Aquisição de Dados (DAQ)

| Habilidade | Manual de Operação | Descrição e Propósito |
| :--- | :--- | :--- |
| **`labjack-lua`** | [SKILL.md](labjack-lua/SKILL.md) | Guia e regras obrigatórias para desenvolvimento de scripts Lua embarcados na LabJack T7-PRO e T-Series. Use sempre que o usuário pedir para criar, modificar, analisar ou otimizar scripts Lua para a LabJack, garantindo conformidade com limites de memória RAM, precisão float 32-bit, temporização, interação via USER_RAM e boas práticas do manual oficial. |
| **`leitor-catman`** | [SKILL.md](leitor-catman/SKILL.md) | Guia e scripts para leitura, processamento e análise de arquivos de aquisição de dados do software HBM catman (.BIN e .TST). Use sempre que precisar inspecionar canais, ler sinais de alta frequência (DAQ), filtrar/decimar dados sem ruído, ou calcular parâmetros de ensaios de torque e ferramentas de impacto (picos, frequência de golpes IPM e relação com corrente). |
| **`electrical-panel-analyzer`** | [SKILL.md](electrical-panel-analyzer/SKILL.md) | Guides the agent in systematically analyzing visual PDFs and images of electrical panel diagrams. Extracts dimensions, internal/external layouts, and component TAGs without hallucination, outputting a professional Markdown report. |
| **`data-quicklook`** | [SKILL.md](data-quicklook/SKILL.md) | Inspecao estatistica e visualizacao rapida de arquivos de aquisicao de dados e sinais de bancada (CSV, BIN, TXT). Use para carregar medicoes de DAQ, calcular picos, medias, RMS e gerar graficos limpos de verificacao imediata no terminal. |
| **`executive-summary`** | [SKILL.md](executive-summary/SKILL.md) | Geracao de resumos executivos de 1 pagina e relatorios consolidados de ensaios e medicoes de bancada. Use apos sessoes de teste (Catman, LabJack, ensaios de torque ou carga) para entregar conclusoes tecnicas diretas para tomada de decisao. |
| **`osis-timesheet-manager`** | [SKILL.md](osis-timesheet-manager/SKILL.md) | Gestor e auditor automatico de reporte de horas e OSIs na plataforma intranet (Node.js/Express). Use sempre que o usuario pedir para checar horas pendentes, auditar dias faltantes no mes, ver saldo de OSIs ou lancar horas de trabalho. |

---

## Firmware e Sistemas Embarcados (ESP32, STM32 e Arduino)

| Habilidade | Manual de Operação | Descrição e Propósito |
| :--- | :--- | :--- |
| **`embedded-c-cpp-patterns`** | [SKILL.md](embedded-c-cpp-patterns/SKILL.md) | Padrões de desenvolvimento em C e C++ para microcontroladores (ESP32, STM32 e Arduino). Guia de segurança de memória sem heap, rotinas de interrupção determinísticas (ISR), filas circulares (Ring Buffers), máquinas de estado (FSM) e uso da biblioteca ETL sem alocação dinâmica. |
| **`platformio-workflow`** | [SKILL.md](platformio-workflow/SKILL.md) | Fluxo de trabalho de engenharia de firmware com PlatformIO para ESP32, STM32 e Arduino. Configuração multi-alvo em platformio.ini, testes unitários com Unity (tanto nativos no computador quanto físicos na placa), compilação com GCC e gerenciamento estrito de dependências. |

---

## Padrões de Engenharia de Software

| Habilidade | Manual de Operação | Descrição e Propósito |
| :--- | :--- | :--- |
| **`python-testing`** | [SKILL.md](python-testing/SKILL.md) | Padrões avançados de testes em Python com Pytest (baseado em affaan-m/ECC). Fixtures idiomáticas, parametrização cirúrgica de casos de borda, mocks seguros e testes assíncronos. |
| **`git-workflow`** | [SKILL.md](git-workflow/SKILL.md) | Padrões de fluxo de trabalho Git limpo e commits semânticos (baseado em affaan-m/ECC). Conventional Commits, atomicidade de alterações, isolamento de branches e higiene de repositório. |
| **`hexagonal-architecture`** | [SKILL.md](hexagonal-architecture/SKILL.md) | Padrão arquitetural Ports and Adapters para desacoplamento de software (baseado em affaan-m/ECC). Isola a lógica de negócio central de bancos de dados, transportes HTTP, filas e ferramentas externas. |
| **`docker-patterns`** | [SKILL.md](docker-patterns/SKILL.md) | Padrões de engenharia para empacotamento em Docker e containers otimizados (baseado em affaan-m/ECC). Multi-stage builds, execução não-root, isolamento de segredos e cache em camadas. |
| **`database-migrations`** | [SKILL.md](database-migrations/SKILL.md) | Diretrizes de migrações de banco de dados seguras, reversíveis e com zero downtime (baseado em affaan-m/ECC). Separação de DDL e DML, padrão expand-contract e criação concorrente de índices. |
| **`mle-workflow`** | [SKILL.md](mle-workflow/SKILL.md) | Protocolo para conversão de notebooks experimentais em pipelines de machine learning reprodutíveis para produção (baseado em affaan-m/ECC). Contratos de dados, validação estrita, modularização e reprodutibilidade. |
| **`tdd-cycle-orchestrator`** | [SKILL.md](tdd-cycle-orchestrator/SKILL.md) | Orquestrador de desenvolvimento orientado a testes (TDD - Test-Driven Development). Use ao implementar modulos, scripts e logica de negocio para assegurar o ciclo Red-Green-Refactor e cobertura empirica. |
| **`systematic-debugging`** | [SKILL.md](systematic-debugging/SKILL.md) | Protocolo de depuração sistemática em 4 fases para erros de ERC, DRC, montagem e scripts. Use sempre que encontrar um erro de projeto ou falha de ferramenta para diagnosticar a causa raiz antes de modificar arquivos. |
| **`search-first`** | [SKILL.md](search-first/SKILL.md) | Protocolo de pesquisa e leitura obrigatória de contexto antes de implementar ou modificar código (baseado em affaan-m/ECC). Impede suposições e reinvenção de roda forçando varredura de pacotes, APIs e código existente. |
| **`systematic-code-reviewer`** | [SKILL.md](systematic-code-reviewer/SKILL.md) | Revisor critico adversarial de codigo, scripts e configuracoes antes do commit. Use ao finalizar qualquer implementacao para auditar casos de borda, complexidade, vazamento de recursos e seguranca. |
| **`github-ops`** | [SKILL.md](github-ops/SKILL.md) | Automação de operações no GitHub via linha de comando gh CLI (baseado em affaan-m/ECC). Gerenciamento de Pull Requests, triagem de issues, download de artefatos e criação de releases. |
| **`brainstorm-to-spec`** | [SKILL.md](brainstorm-to-spec/SKILL.md) | Refinamento socratico de ideias e congelamento de requisitos em SPEC.md antes da escrita de codigo ou layout. Use ao iniciar qualquer nova funcionalidade ou circuito para fazer perguntas cirurgicas e evitar retrabalho. |
| **`github-repo-inspector`** | [SKILL.md](github-repo-inspector/SKILL.md) | Inspecao e dissecação rapida de repositorios do GitHub com extracao direcionada de codigo sem queimar contexto. Use para analisar bibliotecas abertas, clonar referencias em pasta temporaria e extrair apenas assinaturas de funcoes e exemplos essenciais. |
| **`git-worktree-helper`** | [SKILL.md](git-worktree-helper/SKILL.md) | Gerenciamento de git worktrees para testes arriscados, spikes de arquitetura e validacoes em diretorios isolados. Use para criar branches de teste isoladas sem alterar a arvore de trabalho principal do projeto. |
| **`workspace-janitor`** | [SKILL.md](workspace-janitor/SKILL.md) | Higienizacao e faxina sistematica do diretorio de trabalho contra arquivos orfaos, backups de CAD e caches temporarios. Use periodicamente ou antes de commits para identificar lixo de compilacao, logs residuais e relatorios descartaveis. |

---

## Otimização Dinâmica de Tokens e Contexto

| Habilidade | Manual de Operação | Descrição e Propósito |
| :--- | :--- | :--- |
| **`token-optimization`** | [SKILL.md](token-optimization/SKILL.md) | Suíte multi-frentes de economia e otimização dinâmica de tokens (baseada em Aider, RTK, Headroom, LLMLingua e GPTCache). Contém scripts para extração AST Repo-Map, filtragem de logs/testes, poda de JSON/MCP, compressão textual e cache de fatos em SQLite. |

---

## Metasistema, Orquestração e Memória

| Habilidade | Manual de Operação | Descrição e Propósito |
| :--- | :--- | :--- |
| **`subagent-orchestrator-jit`** | [SKILL.md](subagent-orchestrator-jit/SKILL.md) | Orquestrador dinâmico Just-in-Time (JIT) de subagentes. Analisa a complexidade da solicitação em 3 níveis e convoca subagentes especializados sob demanda apenas quando a tarefa for complexa ou crítica, preservando a janela de contexto. |
| **`subagent-orchestrator-mapreduce`** | [SKILL.md](subagent-orchestrator-mapreduce/SKILL.md) | Orquestracao de tarefas volumosas via subagentes efemeros e agregacao Map-Reduce. Use quando a tarefa exigir leitura de muitos arquivos, analise extensiva de logs ou pesquisas pesadas sem queimar contexto. |
| **`continuous-learning-v2`** | [SKILL.md](continuous-learning-v2/SKILL.md) | Motor de instintos e aprendizado contínuo (baseado em affaan-m/ECC). Observa correções do usuário, extrai instintos atômicos com pontuação de confiança e evolui lições validadas em regras permanentes. |
| **`agent-memory`** | [SKILL.md](agent-memory/SKILL.md) | Padrão de arquitetura de memória persistente validado (baseado em sunnyvempati/agent-memory-skill e memodb-io/Acontext). Use para registrar decisões de hardware, pinouts, escolhas de componentes e preferências do usuário em arquivos de estado vivos. |
| **`task-decomposition-and-tracking`** | [SKILL.md](task-decomposition-and-tracking/SKILL.md) | Decomposicao atomica de tarefas e rastreamento persistente de progresso via checklist vivo. Use em solicitacoes de multiplos passos para estruturar o roadmap, evitar esquecimento de etapas e reportar status claro. |
| **`guri-core`** | [SKILL.md](guri-core/SKILL.md) | Núcleo de inicialização, identidade visual e banner do assistente Guri. Contém o script de inicialização do terminal (banner.py), as frases descontraídas de boas-vindas e os comandos de inicialização para qualquer máquina. |
| **`project-architect`** | [SKILL.md](project-architect/SKILL.md) | Engenharia guiada por especificacao e planejamento arquitetural formal (Spec-Driven Development). Use antes de iniciar qualquer funcionalidade ou projeto complexo para congelar requisitos no SPEC.md e evitar retrabalho. |
| **`session-handoff`** | [SKILL.md](session-handoff/SKILL.md) | Protocolo de passagem de turno e persistencia de estado entre sessoes via .context/handoff.md. Use ao encerrar tarefas longas, antes de reiniciar a conversa ou ao iniciar uma nova sessao para recuperar o fio da meada. |
| **`decision-distiller`** | [SKILL.md](decision-distiller/SKILL.md) | Destilador de decisoes de bancada, preferencias tecnicas do usuario e licoes aprendidas em arquivos vivos de contexto. Use apos correcoes de curso do usuario ou ao consolidar escolhas de arquitetura para atualizar a memoria persistente do projeto. |
| **`plan-executor`** | [SKILL.md](plan-executor/SKILL.md) | Execucao atomica e rastreavel de planos de engenharia passo a passo com checklists e validacao por portao. Use para guiar a implementacao de tarefas complexas mantendo o checklist vivo e validado a cada etapa. |

---

## Segurança, Salvaguardas e Conformidade LGPD

| Habilidade | Manual de Operação | Descrição e Propósito |
| :--- | :--- | :--- |
| **`agent-shield`** | [SKILL.md](agent-shield/SKILL.md) | Auditoria estática e salvaguardas de segurança para servidores MCP, credenciais e ferramentas de agente (baseado em affaan-m/ECC). Protege contra vazamento de variáveis de ambiente, injeções de prompt indiretas e chamadas de ferramentas vulneráveis. |
| **`gateguard`** | [SKILL.md](gateguard/SKILL.md) | Trava determinística de pré-execução e verificação de fatos (Fact-Forcing Gate, baseado em affaan-m/ECC). Bloqueia edições e comandos arriscados até que premissas, escopos e dependências sejam explicitamente confirmados. |
| **`secret-sanitizer-and-privacy`** | [SKILL.md](secret-sanitizer-and-privacy/SKILL.md) | Filtro ativo de sanitizacao de segredos, tokens de API, senhas e caminhos sensiveis. Use ao manipular arquivos de configuracao, logs e commits para impedir vazamento de credenciais privadas. |
| **`git-hygiene-and-secrets`** | [SKILL.md](git-hygiene-and-secrets/SKILL.md) | Auditor de higiene de repositorio Git e prevencao de vazamento de segredos e arquivos temporarios do KiCad. Use antes de cada commit e push para garantir que nenhuma chave de API, arquivo de lock ou backup polua o historico. |
| **`shell-safety-and-guardrails`** | [SKILL.md](shell-safety-and-guardrails/SKILL.md) | Diretrizes de execucao deterministica, segura e estritamente headless de comandos no terminal. Use ao formular comandos de shell para evitar travamentos por prompts interativos, loops infinitos ou comandos destrutivos. |
| **`lgpd-audit`** | [SKILL.md](lgpd-audit/SKILL.md) | Orquestrador maestro de conformidade com a LGPD (Lei 13.709/2018). Use para "como estamos de LGPD", "audite LGPD", "compliance LGPD", "gap analysis LGPD" ou qualquer solicitação para avaliar e implementar conformidade de privacidade no projeto. |
| **`lgpd-ropa`** | [SKILL.md](lgpd-ropa/SKILL.md) | Registro das Operações de Tratamento de Dados Pessoais (ROPA - Art. 37 da LGPD). |
| **`lgpd-ripd`** | [SKILL.md](lgpd-ripd/SKILL.md) | Relatório de Impacto à Proteção de Dados Pessoais (RIPD / DPIA - Art. 38 da LGPD). |
| **`lgpd-data-mapping`** | [SKILL.md](lgpd-data-mapping/SKILL.md) | Mapeamento de fluxo de dados pessoais (Data Mapping) e inventário de dados em conformidade com o Art. 37 da LGPD. Use para identificar onde dados pessoais são armazenados e processados. |
| **`lgpd-legal-basis`** | [SKILL.md](lgpd-legal-basis/SKILL.md) | Enquadramento e validação de bases legais de tratamento de dados pessoais (Art. 7º e 11 da LGPD). |
| **`lgpd-consent-schema`** | [SKILL.md](lgpd-consent-schema/SKILL.md) | Modelagem e especificação técnica de consentimento (Consent Ledger) para LGPD (Art. 8º). Use para implementar opt-in, gestão de consentimento de cookies e registro de termos aceitos. |
| **`lgpd-dsar`** | [SKILL.md](lgpd-dsar/SKILL.md) | Atendimento às solicitações de Direitos dos Titulares (Data Subject Access Requests - DSAR) em conformidade com o Art. 18 da LGPD. Use para criar workflows de exportação e exclusão de dados de usuários. |
| **`lgpd-privacy-policy`** | [SKILL.md](lgpd-privacy-policy/SKILL.md) | Criação e atualização de Política de Privacidade e Avisos de Privacidade em conformidade com o Art. 9º da LGPD. Use para criar termo de privacidade, politica de privacidade ou avisos aos titulares. |
| **`lgpd-incident-response`** | [SKILL.md](lgpd-incident-response/SKILL.md) | Plano de resposta a incidentes de segurança e vazamento de dados pessoais (Art. 48 da LGPD). |
| **`lgpd-vendor-audit`** | [SKILL.md](lgpd-vendor-audit/SKILL.md) | Avaliação de conformidade e gestão de risco de fornecedores e operadores de dados pessoais (Art. 39 da LGPD). |
| **`lgpd-dpa`** | [SKILL.md](lgpd-dpa/SKILL.md) | Elaboração e revisão de Data Processing Agreements (DPA) e contratos entre Controlador e Operador. |
| **`lgpd-dpo-encarregado`** | [SKILL.md](lgpd-dpo-encarregado/SKILL.md) | Governança, canal de contato e obrigações do Encarregado de Proteção de Dados (DPO - Art. 41 da LGPD). |
| **`lgpd-anonymization`** | [SKILL.md](lgpd-anonymization/SKILL.md) | Técnicas de anonimização e pseudonimização de dados pessoais de acordo com o Art. 12 da LGPD. |
| **`lgpd-encryption-keys`** | [SKILL.md](lgpd-encryption-keys/SKILL.md) | Criptografia em repouso e em trânsito e gestão de chaves para proteção de dados pessoais (Art. 46 da LGPD). |
| **`lgpd-audit-logging`** | [SKILL.md](lgpd-audit-logging/SKILL.md) | Padrões de registro de logs de acesso e auditoria para rastreabilidade de dados pessoais (Art. 37 da LGPD). |
| **`lgpd-retention-erasure`** | [SKILL.md](lgpd-retention-erasure/SKILL.md) | Definição de prazos de guarda e regras de expiração e eliminação de dados (Art. 15 e 16 da LGPD). |
| **`lgpd-international-transfer`** | [SKILL.md](lgpd-international-transfer/SKILL.md) | Requisitos e cláusulas padrão para transferência internacional de dados pessoais (Art. 33 da LGPD e Res. ANPD 19/2024). |
| **`lgpd-legacy-retrofit`** | [SKILL.md](lgpd-legacy-retrofit/SKILL.md) | Estratégias e arquitetura para adequação retroativa de sistemas legados à LGPD. |
| **`lgpd-eca-digital-minors`** | [SKILL.md](lgpd-eca-digital-minors/SKILL.md) | Requisitos específicos para tratamento de dados pessoais de crianças e adolescentes (Art. 14 da LGPD e ECA Digital / Lei 15.211/2025). |

---

## Pesquisa, RAG e Engenharia de Prompt

| Habilidade | Manual de Operação | Descrição e Propósito |
| :--- | :--- | :--- |
| **`pesquisa-brave`** | [SKILL.md](pesquisa-brave/SKILL.md) | Consultas rápidas e de alto volume em índice global independente via Brave Search. Use para varredura multi-link, descoberta rápida de URLs e dados brutos em JSON sem viés de mecanismos tradicionais. |
| **`pesquisa-firecrawl`** | [SKILL.md](pesquisa-firecrawl/SKILL.md) | Raspagem avançada e extração profunda da web via Firecrawl. Use quando precisar extrair documentações técnicas completas, páginas complexas renderizadas em JavaScript, PDFs ou varrer domínios inteiros em formato Markdown limpo. |
| **`pesquisa-tavily`** | [SKILL.md](pesquisa-tavily/SKILL.md) | Especialista em pesquisa rápida e contextual na internet via Tavily / RAG. Use quando precisar de respostas diretas, fatos consolidados, fontes citadas e contexto limpo sem ruído de HTML. |
| **`doc-deepdive-scraper`** | [SKILL.md](doc-deepdive-scraper/SKILL.md) | Sintetizador e extrator cirurgico de documentacao tecnica, APIs e datasheets da web sem inchaço de tokens. Use ao pesquisar novas bibliotecas, componentes ou documentacoes online para extrair apenas tabelas de pinagem, assinaturas e exemplos praticos. |
| **`prompt-dspy`** | [SKILL.md](prompt-dspy/SKILL.md) | Engenharia de prompt programática e declarativa (Stanford DSPy). Use para estruturar pedidos complexos em assinaturas formais (Input -> Thought -> Output), encadeamento Chain-of-Thought / ReAct e otimização algorítmica de instruções. |
| **`prompt-fabric`** | [SKILL.md](prompt-fabric/SKILL.md) | Padrões modulares de prompt (Fabric Patterns) para estruturação atômica de tarefas. Use para decompor pedidos do usuário em etapas cirúrgicas (extrair sabedoria, analisar argumentos, gerar resumos técnicos, auditar código). |
| **`prompt-promptfoo`** | [SKILL.md](prompt-promptfoo/SKILL.md) | Auditoria, testes de regressão e segurança de prompts (Promptfoo). Use para criar matrizes de avaliação em YAML, comparar modelos e testar resiliência contra injeção de prompt e casos de borda. |
| **`humanizer`** | [SKILL.md](humanizer/SKILL.md) | | Use when editing or reviewing text to remove AI-generated traces and make it sound more natural and human-like. For detecting and fixing: AI vocabulary (delve, leverage, tapestry), promotional tone, superficial -ing analyses, vague attributions, formatting artifacts (curly quotes, excessive bold), and injecting authentic voice. Based on Wikipedia's "Signs of AI writing" guide maintained by WikiProject AI Cleanup. |
| **`seu-tom-de-voz`** | [SKILL.md](seu-tom-de-voz/SKILL.md) | Faz o Claude escrever, revisar e avaliar textos com o tom de voz de quem lidera (coordenadores, gerentes, diretores, heads e CEOs), para que soem como a própria pessoa no trabalho e não como texto genérico de IA. Use SEMPRE que o pedido envolver um texto em primeira pessoa que sairá em nome de alguém em cargo de liderança no mundo corporativo (e-mail para a diretoria, cliente ou parceiro, status de projeto, feedback ou comunicado para o time, mensagem no Teams ou Slack, relatório, apresentação, post de LinkedIn, artigo, newsletter, bio, roteiro de vídeo, palestra, legenda de Instagram, carta ao conselho), quando a pessoa disser "escreve no meu tom", "deixa com a minha cara", "isso parece IA", "revisa meu texto", "melhora esse rascunho", "o que acha desse e-mail", ou pedir para calibrar, montar ou atualizar o perfil de voz. Use também quando alguém escrever em nome de um líder (assistente, marketing, comunicação), mesmo que ninguém mencione voz ou tom. |

---

## Especialidades e Bibliotecas

| Habilidade | Manual de Operação | Descrição e Propósito |
| :--- | :--- | :--- |
| **`matplotlib`** | [SKILL.md](matplotlib/SKILL.md) | Low-level plotting library for full customization. Use when you need fine-grained control over every plot element, creating novel plot types, or integrating with specific scientific workflows. Export to PNG/PDF/SVG for publication. For quick statistical plots use seaborn; for interactive plots use plotly; for publication-ready multi-panel figures with journal styling, use scientific-visualization. |
| **`geopandas`** | [SKILL.md](geopandas/SKILL.md) | Guidance and local audit tools for Python workflows that directly use GeoPandas GeoSeries, GeoDataFrame, spatial operations, or vector-data I/O. |
| **`advogado-especialista`** | [SKILL.md](advogado-especialista/SKILL.md) | 'Advogado especialista em todas as areas do Direito brasileiro: familia, criminal, trabalhista, tributario, consumidor, imobiliario, empresarial, civil e constitucional.' |

---

## Outras Habilidades Especializadas

| Habilidade | Manual de Operação | Descrição e Propósito |
| :--- | :--- | :--- |
| **`evidence-backed-verification`** | [SKILL.md](evidence-backed-verification/SKILL.md) | Protocolo de verificacao empírica obrigatoria ("Deployed is not verified") para entregas de hardware e software. Use ao concluir qualquer bloco de circuito ou layout antes de declarar a tarefa como finalizada ao usuario. |
| **`tech-doc-writer`** | [SKILL.md](tech-doc-writer/SKILL.md) | Padronizacao de documentacao tecnica, manuais de bancada, guias de montagem e READMEs sem enrolacao. Use ao produzir documentacao de engenharia para projetos de hardware, firmware e scripts de aquisicao. |

---
