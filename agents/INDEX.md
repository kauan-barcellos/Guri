# Catálogo de Subagentes Especializados (JIT)

Este catálogo reúne as especificações de subagentes do ecossistema ECC adaptadas para orquestração dinâmica Just-in-Time. O agente coordenador consulta este catálogo e ativa os especialistas sob demanda quando uma tarefa Nível 3 for identificada.

---

## Índice de Perfis Disponíveis

| Perfil | Arquivo de Definição | Área de Atuação | Modo Padrão |
| :--- | :--- | :--- | :--- |
| **Planner Architect** | [planner-architect.md](file:///C:/Users/kauam.barcellos/.gemini/config/agents/planner-architect.md) | Decomposição de tarefas complexas, arquitetura e contratos | Read-Only |
| **Test Engineer** | [test-engineer.md](file:///C:/Users/kauam.barcellos/.gemini/config/agents/test-engineer.md) | Suítes de testes unitários e integração com Pytest | Read-Only |
| **Build Error Resolver** | [build-error-resolver.md](file:///C:/Users/kauam.barcellos/.gemini/config/agents/build-error-resolver.md) | Diagnóstico e correção mínima de falhas de compilação e bundler | Read-Only |
| **Code Simplifier** | [code-simplifier.md](file:///C:/Users/kauam.barcellos/.gemini/config/agents/code-simplifier.md) | Redução de nós condicionais e clareza cognitiva de código | Read-Only |
| **Code Reviewer** | [code-reviewer.md](file:///C:/Users/kauam.barcellos/.gemini/config/agents/code-reviewer.md) | Revisão adversarial de diffs com filtro de alta confiança (>80%) | Read-Only |
| **Database Reviewer** | [database-reviewer.md](file:///C:/Users/kauam.barcellos/.gemini/config/agents/database-reviewer.md) | Auditoria de esquemas relacionais, índices, N+1 e migrações | Read-Only |
| **Security Auditor** | [security-auditor.md](file:///C:/Users/kauam.barcellos/.gemini/config/agents/security-auditor.md) | Varredura de vulnerabilidades OWASP Top 10 e segredos | Read-Only |
| **Doc Updater** | [doc-updater.md](file:///C:/Users/kauam.barcellos/.gemini/config/agents/doc-updater.md) | Documentação técnica, referências de API e codemaps | Read-Only |
| **DevOps Engineer** | [devops-engineer.md](file:///C:/Users/kauam.barcellos/.gemini/config/agents/devops-engineer.md) | Dockerfiles, Compose, pipelines de CI/CD e GitHub Actions | Read-Only |
| **Performance Optimizer** | [performance-optimizer.md](file:///C:/Users/kauam.barcellos/.gemini/config/agents/performance-optimizer.md) | Análise de gargalos de CPU/RAM, async e profiling | Read-Only |
| **API Specialist** | [api-specialist.md](file:///C:/Users/kauam.barcellos/.gemini/config/agents/api-specialist.md) | Contratos RESTful, envelopes de erro, OpenAPI e paginação | Read-Only |
| **Data Engineer** | [data-engineer.md](file:///C:/Users/kauam.barcellos/.gemini/config/agents/data-engineer.md) | Pipelines de processamento de dados, séries temporais e streaming | Read-Only |
| **Embedded Firmware** | [embedded-firmware.md](file:///C:/Users/kauam.barcellos/.gemini/config/agents/embedded-firmware.md) | Firmware C/C++, scripts Lua para LabJack e protocolos seriais | Read-Only |
| **Migration Specialist** | [migration-specialist.md](file:///C:/Users/kauam.barcellos/.gemini/config/agents/migration-specialist.md) | Atualização de dependências, refatoração de código legado | Read-Only |
| **Network Security** | [network-security.md](file:///C:/Users/kauam.barcellos/.gemini/config/agents/network-security.md) | Proxies reversos, certificados SSL/TLS, CORS e firewalls | Read-Only |
| **Frontend Specialist** | [frontend-specialist.md](file:///C:/Users/kauam.barcellos/.gemini/config/agents/frontend-specialist.md) | Interfaces Web, TypeScript, gerenciamento de estado e acessibilidade | Read-Only |
