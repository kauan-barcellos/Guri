---
name: token-optimization
description: >-
  Suíte multi-frentes de economia e otimização dinâmica de tokens (baseada em Aider, RTK, Headroom, LLMLingua e GPTCache).
  Contém scripts para extração AST Repo-Map, filtragem de logs/testes, poda de JSON/MCP, compressão textual e cache de fatos em SQLite.
---

# Token Optimization Suite: Economia Dinâmica Multi-Frentes

Este guia e conjunto de ferramentas implementam uma abordagem em 5 frentes ativas para reduzir o consumo de tokens, acelerar respostas e impedir a degradação da janela de contexto.

---

## 1. As 5 Frentes de Economia Implementadas

A suíte está implementada em Python nativo dentro da pasta `scripts/token_optimizer/` sem dependências externas:

```
[ Entrada Bruta ] ──► [ TokenOptimizer (Auto-Detecção) ]
                             │
                             ├─► Código/Diretório: AST Repo-Map (Aider)    [-80% a -90%]
                             ├─► Logs/Terminal:    Log Filter (RTK)        [-60% a -85%]
                             ├─► JSON/MCPs:        JSON Pruner (Headroom)  [-60% a -95%]
                             ├─► Textos Longos:    Text Paring (LLMLingua) [-40% a -60%]
                             └─► Consultas Fixas:  Fact Cache (GPTCache)   [-100% Zero Token]
```

### Frente 1: AST Repo-Map (`repo_map.py`)
* **Inspirado no:** Aider (50k estrelas).
* **Mecanismo:** Analisa arquivos Python usando a biblioteca nativa `ast`, extrai assinaturas de classes, métodos, parâmetros, retornos e docstrings de cabeçalho, descartando o corpo das funções.
* **Uso:** Navegação inicial em novos repositórios sem ler todos os arquivos na íntegra.

### Frente 2: Filtro Ativo de Logs e Terminal (`log_filter.py`)
* **Inspirado no:** RTK (86k estrelas).
* **Mecanismo:** Remove sequências de escape ANSI, barras de progresso e compacta linhas consecutivas idênticas, preservando integralmente tracebacks, exceções e o resumo de execução do `pytest`.
* **Uso:** Sanitização de saídas de testes e compilação antes de entrar no contexto.

### Frente 3: Poda e Tabularização de JSON/MCP (`json_pruner.py`)
* **Inspirado no:** Headroom (80k estrelas).
* **Mecanismo:** Remove recursivamente chaves com valores nulos, dicionários vazios e listas vazias. Converte automaticamente coleções de dicionários homogêneos em tabelas colunares densas.
* **Uso:** Compactação de respostas volumosas de servidores MCP (KiCad, metadados de pinos).

### Frente 4: Poda Textual de Redundâncias (`text_compressor.py`)
* **Inspirado no:** LLMLingua (7k estrelas).
* **Mecanismo:** Deduplicação de parágrafos idênticos e remoção de clichês e preenchimentos conversacionais, preservando tabelas, números e blocos de código.
* **Uso:** Compactação de relatórios densos e transcrições de ensaios.

### Frente 5: Cache Local de Fatos e Regras (`fact_cache.py`)
* **Inspirado no:** GPTCache (8k estrelas).
* **Mecanismo:** Banco relacional SQLite local que armazena regras imutáveis de engenharia (limites DFM JLCPCB, especificações de componentes, limites de pinos do LabJack).
* **Uso:** Zero consumo de tokens em perguntas conceituais repetitivas.

---

## 2. Como Utilizar a Suíte

### Via Linha de Comando (CLI):
```powershell
# Configurar PYTHONPATH temporário apontando para scripts
$env:PYTHONPATH="C:\Users\kauam.barcellos\.gemini\config\skills\token-optimization\scripts"

# 1. Gerar Repo-Map condensado de uma pasta ou arquivo
python -m token_optimizer --path "C:\Projetos\MeuProjeto"

# 2. Filtrar arquivo de log verboso
python -m token_optimizer --log "caminho\output.log"

# 3. Compactar payload JSON bruto
python -m token_optimizer --json "{'status': 'ok', 'vazio': null, 'itens': [{'id': 1}, {'id': 2}]}"

# 4. Consultar fato em cache (100% de economia)
python -m token_optimizer --cache-get jlcpcb "regras dfm 2 camadas"
```

### Via Código Python:
```python
import sys
sys.path.insert(0, r"C:\Users\kauam.barcellos\.gemini\config\skills\token-optimization\scripts")

from token_optimizer import TokenOptimizer

optimizer = TokenOptimizer()
resultado = optimizer.optimize(dados_brutos)
print(f"Estratégia: {resultado['strategy']} | Economia: {resultado['savings_percentage']}%")
print(resultado["content"])
```

---

## 3. Checklist de Eficiência do Agente

* [ ] Ao inspecionar estrutura de pastas pela primeira vez, utilizar `repo_map` antes de ler arquivos inteiros.
* [ ] Em saídas longas de testes ou compilador, rodar o `log_filter` antes de exibir o erro.
* [ ] Em retornos volumosos de ferramentas/MCP, podar chaves nulas com `json_pruner`.
* [ ] Consultas sobre DFM e especificações fixas devem consultar o `fact_cache`.
