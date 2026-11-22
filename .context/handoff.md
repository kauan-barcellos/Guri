# Session Handoff

## 1. Metadados da Sessao
* Data/Hora: 2026-11-21 22:05
* Branch Git: main
* Ultimo Commit: 03913bb feat(cad): automatizar instalacao do FreeCAD MCP, ritmo de 2.5s e regras de modelagem passo a passo

## 2. O que foi Concluido
* [x] Configuracao do FreeCAD 1.1.4: estilo de navegacao Gesture (otimizado para touchpad/notebook), tela inicial Start, tema claro e integracao no PATH.
* [x] Instalacao e ativacao do servidor FreeCAD MCP (porta 9875) com auto-start via `freecad_mcp_settings.json`.
* [x] Resolucao dinamica de caminhos no `mcp_config.json` para eliminar caminhos absolutos do usuario antigo (`kauam.barcellos` -> `kauan` / `uvx`).
* [x] Criacao do cliente orquestrador `tools/guri_cad.py` com suporte a execucao ao vivo via RPC (porta 9875) e fallback headless via FreeCADCmd.
* [x] Ajuste do ritmo de modelagem passo a passo para ~2.5s por etapa para permitir visualizacao e rotacao confortaveis pelo usuario.
* [x] Adicao das 3 regras fundamentais de CAD em `AGENTS.md` e `rules/diretrizes-gerais.md`:
  1. Multi-pecas (cada peca modelada e exportada em `.step` individual alem do `conjunto.step`).
  2. Nomes curtos e intuitivos em pt-BR (ex: haste, cabeca, base, colar, eixo, tampa).
  3. Organizacao por pastas de projeto (`projetos/<nome_do_projeto>/`).
* [x] Automacao completa no instalador universal `instalar_guri.ps1` (etapa 5/6 dedicada a configurar FreeCAD, Mod FreeCADMCP bundled em `assets/`, auto-start e mcp_config.json em qualquer nova maquina).
* [x] Criacao de dois projetos de teste funcionais com modelagem validada: `projetos/parafuso_allen` e `projetos/mancal_flange`.

## 3. Estado Atual e Variaveis Criticas
* FreeCAD conectado e respondendo em `http://127.0.0.1:9875`.
* Pacotes do FreeCAD MCP cacheados no `uv`.
* Repositorio pronto para replicar em qualquer outra maquina via `instalar_guri.ps1`.

## 4. Bloqueios e Questoes Pendentes
* Nenhum bloqueio ativo.

## 5. Proximo Passo Imediato
* Seguir com as modelagens e desenhos sob demanda de acordo com as necessidades de bancada do Kauan.
