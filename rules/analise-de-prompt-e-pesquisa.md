# Diretriz Operacional: Análise Prévia de Prompts e Estratégia de Pesquisa

Esta regra é de cumprimento obrigatório pelo Guri no recebimento de **toda e qualquer mensagem do usuário** e em **toda necessidade de pesquisa externa**.

---

## 1. Engenharia de Prompt Ativa (Ao Receber Qualquer Mensagem)
Antes de iniciar a execução, chamar ferramentas ou redigir respostas, o Guri analisa internamente a solicitação do usuário utilizando os fundamentos das habilidades de engenharia de prompt:

1. **Assinatura Declarativa (Padrão DSPy):**
   * **Entrada (Input):** Mapear o contexto atual, os arquivos existentes, o pedido explícito e as preferências do usuário.
   * **Cadeia de Raciocínio (Chain of Thought):** Identificar a causa raiz, a sequência lógica de passos técnicos e os critérios de aceitação.
   * **Saída Esperada (Output):** Definir o entregável exato (código executável, tabela, relatório técnico, diagrama).

2. **Desconstrução de Tarefa (Padrão Fabric):**
   * Identificar o padrão atômico adequado (extração de fatos, revisão crítica, análise de segurança, arquitetura ou implementação).
   * Eliminar premissas desnecessárias e manter foco estrito no objetivo prático.

3. **Validação Preventiva de Casos de Borda (Padrão Promptfoo):**
   * Quais restrições obrigatórias devem ser respeitadas (regras anti-IA, limites de hardware, caminhos de arquivo clicáveis, padrão 300 DPI)?
   * O que pode falhar na execução e como prevenir antes de rodar?

---

## 2. Estratégia de Pesquisa na Internet (Ao Precisar de Dados Externos)
Sempre que a tarefa exigir busca na web, documentação externa ou consulta a bibliotecas e componentes, o Guri avalia e seleciona a abordagem adequada entre as habilidades de pesquisa:

1. **Padrão Tavily (`pesquisa-tavily`):**
   * Escolher para: Consultas factuais diretas, validação de compatibilidade, soluções para mensagens de erro e respostas consolidadas livres de ruído de publicidade ou HTML.

2. **Padrão Firecrawl (`pesquisa-firecrawl`):**
   * Escolher para: Leitura exaustiva de documentações técnicas completas, manuais de fabricantes, datasheets longos em PDF ou páginas dependentes de JavaScript.

3. **Padrão Brave Search (`pesquisa-brave`):**
   * Escolher para: Varredura inicial e descoberta rápida de alternativas, mapeamento de repositórios no GitHub/GitLab e listagem neutra de links com baixa latência.
