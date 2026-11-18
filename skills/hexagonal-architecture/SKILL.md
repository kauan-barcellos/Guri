---
name: hexagonal-architecture
description: >-
  Padrão arquitetural Ports and Adapters para desacoplamento de software (baseado em affaan-m/ECC).
  Isola a lógica de negócio central de bancos de dados, transportes HTTP, filas e ferramentas externas.
---

# Hexagonal Architecture: Padrão Ports and Adapters

Este guia estabelece os princípios de arquitetura de software para isolar a lógica de negócio central (domínio) de frameworks, bancos de dados, interfaces de usuário e protocolos externos.

---

## 1. Princípio Fundamental e Regra de Ouro

Na Arquitetura Hexagonal, **o fluxo de dependências aponta sempre para o centro**. 
O código de negócio puro nunca importa bibliotecas de infraestrutura (como SQLAlchemy, FastAPI, Pandas, boto3 ou drivers de hardware). Em vez disso, o domínio declara interfaces abstratas (Portas), e os módulos externos fornecem implementações concretas (Adaptadores).

```
+---------------------------------------------------------------+
|                       ADAPTADORES DE ENTRADA                  |
|               (CLI, API REST, Mensageria, Scripts)             |
|                                                               |
|        +---------------------------------------------+        |
|        |                PORTAS DE ENTRADA            |        |
|        |                   (Use Cases)               |        |
|        |                                             |        |
|        |        +---------------------------+        |        |
|        |        |      DOMÍNIO CENTRAL      |        |        |
|        |        |   (Entidades e Regras)    |        |        |
|        |        +---------------------------+        |        |
|        |                                             |        |
|        |                PORTAS DE SAÍDA              |        |
|        |             (Interfaces de Repos)           |        |
|        +---------------------------------------------+        |
|                                                               |
|                       ADAPTADORES DE SAÍDA                    |
|             (PostgreSQL, Sistema de Arquivos, S3)             |
+---------------------------------------------------------------+
```

---

## 2. As Camadas do Sistema

### 1. Domínio Central (Domain Core)
* **Conteúdo:** Entidades, objetos de valor e validações de regras de negócio puras.
* **Restrição:** Dependências externas são estritamente proibidas (apenas tipos nativos da linguagem ou bibliotecas de tipos básicos).

### 2. Portas (Ports)
* **Portas de Entrada (Driving Ports):** Casos de uso e serviços da aplicação que definem as operações disponibilizadas ao mundo exterior.
* **Portas de Saída (Driven Ports):** Interfaces e classes abstratas que definem o que a aplicação precisa para persistir dados, emitir notificações ou consultar serviços externos.

### 3. Adaptadores (Adapters)
* **Adaptadores de Entrada (Primary/Driving):** Controladores de API (FastAPI, Flask, Express), comandos de terminal (CLI) ou receptores de eventos.
* **Adaptadores de Saída (Secondary/Driven):** Repositórios SQL/NoSQL, clientes HTTP externos, adaptadores de armazenamento em disco ou conexões com hardware.

---

## 3. Estrutura de Diretórios Recomendada (Exemplo Python)

```text
src/
├── domain/                      # Camada 1: Regras Puras
│   ├── models/                  # Entidades (ex: Ensaio, Dispositivo)
│   └── exceptions.py            # Erros específicos do domínio
│
├── application/                 # Camada 2: Casos de Uso e Portas
│   ├── ports/
│   │   ├── input/               # Interfaces dos Casos de Uso
│   │   └── output/              # Interfaces de Repositórios e Serviços Externos
│   └── use_cases/               # Implementação do fluxo de negócio
│
└── infrastructure/              # Camada 3: Adaptadores Concretos
    ├── adapters/
    │   ├── primary/             # FastAPI / CLI / Scripts
    │   └── secondary/           # PostgresRepo / ArquivoCSV / LabJackDriver
    └── config/                  # Injeção de dependências e variáveis de ambiente
```

---

## 4. Diretrizes de Implementação

1. **Testabilidade Isolada:** A camada de domínio e os casos de uso devem ser 100% testáveis com testes unitários puros, usando mocks ou stubs em memória para as portas de saída, sem precisar subir bancos de dados ou servidores.
2. **Substituição sem Atrito:** A troca de um banco SQLite por PostgreSQL ou de uma API REST por CLI deve exigir alterações exclusivamente na pasta `infrastructure/`, sem modificar nenhuma linha de código em `domain/` ou `application/`.
3. **Injeção de Dependências:** Instancie adaptadores concretos no ponto de entrada da aplicação (ex: `main.py`) e passe-os para os casos de uso através de seus construtores.
