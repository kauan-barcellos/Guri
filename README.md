<p align="center">
  <img src="assets/banner.png" alt="GURI - A mente que pensa" width="100%">
</p>

<div align="center">

[![Status](https://img.shields.io/badge/Status-%C3%89%20s%C3%B3%20querer!-00C853?style=for-the-badge)](https://github.com/kauan-barcellos/Guri)
[![Language](https://img.shields.io/badge/Idioma-pt--BR-blue?style=for-the-badge)](https://github.com/kauan-barcellos/Guri)
[![Antigravity](https://img.shields.io/badge/Powered%20By-Antigravity%20CLI-blueviolet?style=for-the-badge)](https://antigravity.google)
[![Subagents](https://img.shields.io/badge/Subagentes-85%20Especialistas-orange?style=for-the-badge)](agents/README.md)
[![Skills](https://img.shields.io/badge/Skills-77%20Modulares-success?style=for-the-badge)](skills/README.md)
[![KiCad](https://img.shields.io/badge/CAD-KiCad%2010.0-314CB6?style=for-the-badge&logo=kicad&logoColor=white)](https://kicad.org)
[![Embedded](https://img.shields.io/badge/Firmware-ESP32%20%7C%20STM32%20%7C%20Arduino-00979D?style=for-the-badge)](skills/README.md#firmware-e-sistemas-embarcados-esp32-stm32-e-arduino)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)

</div>

---

# Guri: Assistente Pessoal e Engenheiro de Bancada

O **Guri** é a inteligência central e parceiro operacional para desenvolvimento de hardware (KiCad 10 + JLCPCB), desenvolvimento de firmware para microcontroladores (ESP32, STM32 e Arduino em C/C++), ensaios físicos e aquisição de dados (LabJack T7, HBM Catman), engenharia de software de alta performance, conformidade jurídica (LGPD) e automação de bancada.

---

## 🏛️ Arquitetura do Sistema

```text
┌────────────────────────────────────────────────────────────────────────┐
│                              GURI CORE                                 │
│          Tom de Voz Autêntico • Regras Anti-IA • Engenharia Direta     │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │
         ┌─────────────────────────┼─────────────────────────┐
         ▼                         ▼                         ▼
┌──────────────────┐      ┌──────────────────┐      ┌──────────────────┐
│  ORQUESTRADOR    │      │  CATÁLOGO JIT    │      │ SUÍTE DE TOKENS  │
│  DINÂMICO JIT    │      │  85 SUBAGENTES   │      │   5 FRENTES      │
│  Triagem 3 Níveis│      │  Sob Demanda     │      │ AST/RTK/Headroom │
└──────────────────┘      └──────────────────┘      └──────────────────┘
```

---

## ⚡ Orquestração Dinâmica Just-in-Time (JIT)

O sistema opera com uma régua de complexidade estrita para evitar poluição de contexto e consumo desnecessário de tokens:

* **Nível 1 (Baixa Complexidade):** Respostas rápidas e ajustes pontuais resolvidos imediatamente sem disparar subagentes.
* **Nível 2 (Média Complexidade):** Implementações estruturadas seguindo as [Skills Locais](skills/README.md) (`python-testing`, `git-workflow`, `search-first`).
* **Nível 3 (Alta Complexidade):** Ativação isolada e temporária de especialistas do catálogo em segundo plano via `subagent-orchestrator-jit`.

Consulte o [Catálogo Completo de Subagentes](agents/README.md) para ver todos os 85 especialistas disponíveis.

---

## 🔌 Firmware e Microcontroladores (ESP32, STM32 e Arduino em C/C++)

O Guri incorpora conhecimento formal e padrões de engenharia para desenvolvimento de firmware de alta confiabilidade:

* **Segurança de Memória (Zero Heap):** Proibição de `malloc()` e `free()` no loop principal, adoção de contêineres estáticos via ETL (Embedded Template Library) e filas circulares (Ring Buffers).
* **Multi-Alvo com PlatformIO:** Configuração unificada de compilação em `platformio.ini` para ESP32, STM32 e Arduino com flags estritas do GCC (`-Os -Wall -Wextra -fno-exceptions`).
* **Testes Unitários com Unity:** Execução de testes no computador de desenvolvimento (ambiente `native`) para lógica pura e na placa física via serial/SWD.
* **Especialistas por Plataforma:**
  - **ESP32:** Gestão de tarefas FreeRTOS dual-core (`xTaskCreatePinnedToCore`), NimBLE para economia de RAM, instruções SIMD com `esp-dsp` e respeito aos strapping pins.
  - **STM32:** Transferências contínuas via DMA (ADC, UART, SPI), hierarquia NVIC, configuração de clocks (HSE/PLL) e gravação SWD.
  - **Arduino (AVR/SAMD):** Preservação rigorosa de SRAM, literais na Flash via macro `F()` e `PROGMEM`, `ArduinoJson v7` em stack e multitarefa cooperativa sem bloqueio com `TaskScheduler`.

---

## 🚀 Suíte de Otimização de Tokens em 5 Frentes

Construída em Python nativo sem dependências externas, economiza de 40% a 100% de tokens em todas as entradas:

1. **AST Repo-Map (`repo_map.py`):** Extração sintática de assinaturas de código sem corpos de função (-85%).
2. **Log Filter (`log_filter.py`):** Sanitização e descarte de ruído em saídas de testes e compilação (-70%).
3. **JSON Pruner (`json_pruner.py`):** Poda de nulos e tabularização de dados de MCP (-75%).
4. **Text Compressor (`text_compressor.py`):** Poda semântica de clichês e redundâncias textuais (-50%).
5. **Fact Cache (`fact_cache.py`):** Cache relacional SQLite de especificações fixas (100% - Zero Token).

### Atalhos Rápidos no Terminal:
* `opt.bat --path <pasta>`: Gera Repo-Map comprimido.
* `opt.bat --log <arquivo.log>`: Filtra saídas de erro e testes.
* `opt.bat --cache-get <namespace> <chave>`: Consulta regras em cache com 100% de economia.
* `sync.bat [mensagem]`: Commita e sincroniza automaticamente com o repositório remoto.
