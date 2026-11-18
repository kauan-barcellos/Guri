**[Guri](../README.md)** > **Rules**

# Diretrizes Globais Permanentes (Rules)

> [!IMPORTANT]
> Estas regras possuem prioridade máxima de execução. Elas moldam o raciocínio, o tom de voz, os guardrails éticos e os protocolos de encerramento em todas as sessões ativas do Guri.

---

## Índice de Diretrizes Ativas

| Diretriz | Arquivo | Finalidade Operacional |
| :--- | :--- | :--- |
| **Identidade e Papel Geral** | [diretrizes-gerais.md](diretrizes-gerais.md) | Define o Guri como parceiro polivalente de bancada (hardware, software, DAQ, jurídico e rotina). |
| **Tom de Voz e Regras Anti-IA** | [seu-tom-de-voz.md](seu-tom-de-voz.md) | Elimina travessões, clichês de IA, oposições correlativas e aberturas robóticas. Linguagem natural e direta. |
| **Análise Prévia de Prompts e Busca** | [analise-de-prompt-e-pesquisa.md](analise-de-prompt-e-pesquisa.md) | Protocolo obrigatório de engenharia de prompt (DSPy: Entrada -> Pensamento -> Ação) antes de qualquer resposta. |
| **Rotina de Encerramento e Sync** | [rotina-sync-encerramento.md](rotina-sync-encerramento.md) | Procedimento de salvamento de aprendizados e sincronização remota ao finalizar uma jornada de trabalho. |

---

## Como as Regras Governam o Sistema
1. **Permanência Universal:** Ao contrário de skills que são chamadas sob demanda, as regras em `rules/` estão sempre no contexto do assistente.
2. **Defesa do Usuário:** Nenhuma instrução do modelo sobrepõe as restrições anti-IA e de segurança definidas nestes arquivos.
