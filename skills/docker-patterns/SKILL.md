---
name: docker-patterns
description: >-
  Padrões de engenharia para empacotamento em Docker e containers otimizados (baseado em affaan-m/ECC).
  Multi-stage builds, execução não-root, isolamento de segredos e cache em camadas.
---

# Docker Patterns: Práticas de Empacotamento Seguro e Otimizado

Este guia estabelece os padrões para construção de imagens Docker eficientes, seguras, com tempo de compilação reduzido e prontas para operação em produção.

---

## 1. As Cinco Regras de Ouro do Dockerfile

1. **Multi-Stage Build Obrigatório:**
   * Separe o estágio de compilação e instalação de ferramentas (compiladores C, linters, pacotes de desenvolvimento) da imagem final de execução.
   * A imagem final deve conter estritamente o executável e as dependências mínimas de runtime.

2. **Execução sem Privilégios de Root (Non-Root User):**
   * Imagens nunca devem rodar como usuário `root` em produção.
   * Crie um usuário de sistema dedicado (`appuser`) e conceda permissões apenas nas pastas necessárias.

3. **Ordem Estratégica de Camadas para Cache:**
   * Copie manifestos de dependências (`requirements.txt`, `pyproject.toml`, `package.json`) e instale dependências antes de copiar o código fonte da aplicação.
   * Mudanças de código não devem invalidar o cache de download de pacotes.

4. **Uso Rigoroso do `.dockerignore`:**
   * Todo projeto com Dockerfile deve possuir um `.dockerignore` bloqueando pastas locais (`.git`, `node_modules`, `__pycache__`, `.venv`, arquivos `.env`, logs e arquivos temporários).

5. **Tratamento Adequado de Sinais do Sistema (SIGTERM):**
   * Utilize sempre a sintaxe em formato de lista `["executavel", "parametro1"]` na instrução `ENTRYPOINT` ou `CMD`.
   * Evite a sintaxe de shell (`CMD python main.py`), pois ela encapsula o processo em `/bin/sh`, impedindo que a aplicação receba o sinal de encerramento limpo (`SIGTERM`).

---

## 2. Modelo de Referência para Aplicações Python

```dockerfile
# -------------------------------------------------------------
# Estágio 1: Compilação e Construção das Dependências (Builder)
# -------------------------------------------------------------
FROM python:3.12-slim AS builder

WORKDIR /build

# Instala ferramentas de compilação se houver pacotes com extensões C
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# -------------------------------------------------------------
# Estágio 2: Imagem Final de Produção (Runtime Mínimo)
# -------------------------------------------------------------
FROM python:3.12-slim AS runtime

# Criação de usuário sem privilégios de root
RUN groupadd -r appgroup && useradd -r -g appgroup -u 1000 appuser

WORKDIR /app

# Copia pacotes instalados do estágio builder
COPY --from=builder /root/.local /home/appuser/.local
ENV PATH=/home/appuser/.local/bin:$PATH

# Copia código fonte da aplicação
COPY --chown=appuser:appgroup src/ ./src/

USER appuser

EXPOSE 8000

# Execução direta com formato de array (permite recepção de SIGTERM)
ENTRYPOINT ["python", "-m", "src.main"]
```

---

## 3. Diretrizes de Segurança

* **Nunca injetar segredos no `Dockerfile`:** Jamais inclua senhas, chaves de API ou arquivos `.env` dentro da imagem. Injeções de segredos devem ocorrer no momento de execução via variáveis de ambiente ou montagem de volumes seguros.
* **Imagens Base Específicas:** Fixe sempre tags precisas de versão (ex: `python:3.12-slim`), evitando o uso da tag `latest`, que introduz instabilidade e quebras imprevisíveis no build.
* **Limpeza de Cache do Gerenciador de Pacotes:** Ao rodar `apt-get`, execute sempre `rm -rf /var/lib/apt/lists/*` na mesma instrução `RUN` para não acumular camadas inúteis no disco.
