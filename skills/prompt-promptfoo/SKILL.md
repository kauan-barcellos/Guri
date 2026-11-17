---
name: prompt-promptfoo
description: >-
  Auditoria, testes de regressão e segurança de prompts (Promptfoo).
  Use para criar matrizes de avaliação em YAML, comparar modelos e testar resiliência contra injeção de prompt e casos de borda.
---

# Auditoria e Testes de Prompts: Padrão Promptfoo

Esta habilidade traz a disciplina de testes automatizados de software (CI/CD) para o universo dos prompts e agentes de IA, inspirada no Promptfoo.

---

## 1. Princípios do Promptfoo

* **Test-Driven Prompting:** Prompts e instruções de regras devem ser tratados como código, com casos de teste automatizados que verificam entradas esperadas e saídas reais.
* **Detecção de Regressões:** Uma melhoria feita para um cenário não pode estragar um caso que já funcionava anteriormente.
* **Segurança e Red-Teaming:** Teste ativo contra injeção de prompt, vazamento de credenciais privadas ou desvio de diretrizes operacionais.
* **Asserções Objetivas:** Validação com critérios mensuráveis:
  * Contém/não contém palavras proibidas (regras anti-IA).
  * Código compila sem warnings.
  * Estrutura de dados segue o schema JSON/YAML exigido.

---

## 2. Como Aplicar ao Receber uma Mensagem do Usuário

Ao planejar a resposta para o usuário, o agente antecipa mentalmente a matriz de asserções:

1. **Asserção de Restrições:**
   * O texto gerado respeita o tom de voz do Guri (sem travessões artificiais, sem oposições correlativas e em pt-BR)?
   * As figuras têm 300 DPI e grandezas com unidades nos eixos?
   * Os caminhos de arquivos estão no formato de link markdown clicável (`file://`)?

2. **Asserção de Casos de Borda:**
   * O que acontece se o arquivo não existir?
   * O script roda em Windows com PowerShell sem travar em comandos interativos?
   * As variáveis e bibliotecas foram importadas antes de serem chamadas?

---

## 3. Matriz de Avaliação Rápida (Template)

Para validar novas regras ou prompts internos do Guri:

```yaml
# Exemplo de matriz mental de teste (Promptfoo)
description: "Validacao de resposta técnica"
prompts:
  - "Instrucao do Guri"
providers:
  - "Antigravity Agent"
tests:
  - vars:
      requisito: "Análise de arquivo de dados"
    assert:
      - type: not-contains
        value: "Certamente!"
      - type: not-contains
        value: "—"
      - type: contains
        value: "file://"
      - type: javascript
        value: "output.length > 50"
```
