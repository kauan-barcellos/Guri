---
name: brainstorm-to-spec
description: >-
  Refinamento socratico de ideias e congelamento de requisitos em SPEC.md antes da escrita de codigo ou layout.
  Use ao iniciar qualquer nova funcionalidade ou circuito para fazer perguntas cirurgicas e evitar retrabalho.
---

# Refinamento Socratico e Especificacao (Brainstorm to Spec)

Esta skill impede o erro de iniciar a implementacao de codigo ou desenho de hardware com requisitos vagos ou premissas nao confirmadas. Inspirada no protocolo de `brainstorming` do `obra/superpowers` e nas praticas de especificacao do `addyosmani/agent-skills`, a regra e direta: nenhuma linha de producao e gerada antes do congelamento do `SPEC.md`.

---

## 1. Protocolo Socratico (3 a 5 Perguntas de Bancada)

Ao receber um pedido complexo ou novo bloco de desenvolvimento, faca uma pausa deliberada e apresente ao usuario apenas de 3 a 5 perguntas cirurgicas abordando:

1. **Escopo e Limites:** Qual e o limite exato do que este modulo deve e nao deve fazer?
2. **Entradas e Saidas:** Quais sao os sinais fisicos, formatos de dados, tensoes nominais e protocolos de comunicacao?
3. **Restricoes Fisicas e de Tempo:** Quais sao as taxas de amostragem minimas, tempos maximos de resposta ou limitacoes de memoria RAM/Flash?
4. **Tratamento de Falha:** Como o sistema deve se comportar caso o sensor desconecte, a alimentacao caia ou ocorra timeout?

---

## 2. A Estrutura do SPEC.md

Apos as respostas do usuario, formalize o arquivo `SPEC.md` na raiz do projeto ou na pasta `.context/`:

```markdown
# Especificacao Tecnica: [Nome do Modulo]

## 1. Objetivo Operacional
Descricao concisa do que a entrega resolve no mundo real.

## 2. Requisitos de Hardware e Firmware
* Microcontrolador / Dispositivo:
* Pinos e Barramentos Utilizados:
* Niveis Logicos e Tensoes:
* Restricoes de Memoria ou Temporizacao:

## 3. Arquitetura Proposta
Diagrama em blocos ou fluxo logico em texto simples.

## 4. Criterios Binarios de Aceitacao (Passou / Falhou)
* [ ] Criterio 1: Comunicacao com sensor estabelecida e confirmada via ID de registro.
* [ ] Criterio 2: Taxa de leitura mantida em 100 Hz sem estouro de buffer.
* [ ] Criterio 3: Testes de unidade em C++ aprovados sem alocacao dinamica.
```

---

## 3. Portao de Aprovacao

Apenas prossiga para a construcao do plano de acao (`plan-executor`) apos o usuario ler o `SPEC.md` e dar o aval explicito.
