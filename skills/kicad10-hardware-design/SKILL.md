---
name: kicad10-hardware-design
description: >-
  Metodologia, regras DFM e ferramentas para desenvolvimento de placas de circuito impresso (PCB) no KiCad 10.0 com JLCPCB.
  Use sempre que for criar, modificar, rotear ou auditar projetos de hardware, garantindo módulos prontos (COTS),
  ergonomia de montagem, segregação de ruído (potência vs sinais) e regras de fabricação da JLCPCB.
---

# Desenvolvimento de Hardware e PCBs (KiCad 10.0 + JLCPCB)

Este guia prático reúne todo o método de desenvolvimento de placas de circuito impresso adotado pelo Guri, focado em agilidade, confiabilidade industrial e facilidade de montagem na bancada.

---

## 🛑 As 3 Regras de Ouro de Hardware

Em qualquer circuito desenhado pelo Guri, estas 3 regras têm prioridade máxima:

### 1. Arquitetura com Módulos Prontos (COTS - Commercial Off-The-Shelf)
* **Nunca reinventar a roda:** Não desenhe circuitos discretos complexos em volta de chips crus (como fontes chaveadas cheias de indutores e diodos, ou transceivers isolados manuais) quando existir um módulo pronto comercial no mercado (ex: conversores DC-DC tipo LM2596, MP1584, módulos ESP32, módulos RS485).
* **Vantagem:** Reduz drásticamente o tempo de projeto, diminui risco de superaquecimento e simplifica muito a manutenção na bancada.
* **Como fazer na PCB:** Desenhe soquetes, barras de pinos (headers) ou pads de encaixe para conectar o módulo pronto diretamente na placa-mãe (*carrier board*).

### 2. Ergonomia, Visibilidade e Facilidade de Montagem
* **Bornes e conectores para fora:** Todos os bornes de parafuso e conectores externos devem ficar voltados para as bordas externas da placa, para que a chave de fenda e os fios não esbarrem em nenhum componente alto.
* **Furos de fixação:** Toda placa deve ter pelo menos 4 furos de montagem nos cantos (M3 / furo 3.2 mm) com folga livre de trilhas ao redor.
* **Pontos de Teste (Test Points):** Adicione pads acessíveis para multímetro e osciloscópio (VCC, 3.3V, 5V, 12V, GND e linhas de sinal).
* **Serigrafia clara:** Nomeie claramente cada pino de borne com texto legível (+24V, GND, IN1, OUT1, TX, RX).

### 3. Segregação Física: Potência vs. Sinais Lógicos
* **Separação espacial:** Separe fisicamente a placa em duas zonas distintas:
  * **Lado de Potência:** Alimentação principal, relés, conversores de tensão e acionamentos indutivos.
  * **Lado Lógico/Sinais:** Microcontroladores, barramentos de comunicação (I2C, SPI, UART, RS485) e sensores sensíveis.
* **Objetivo:** Evitar que ruído elétrico e transientes de chaveamento travem o microcontrolador ou interfiram nas medições.

---

## 📏 Tabela DFM JLCPCB (2 Camadas / 1 oz / 1.6 mm)

Configurações numéricas recomendadas para o KiCad 10:

| Parâmetro | Mínimo Recomendado | Observações |
| :--- | :--- | :--- |
| **Largura de trilha (Sinais lógicos)** | **0.15 mm a 0.20 mm** | Seguro para corrosão química padrão. |
| **Largura de trilha (Alimentação até 0.5A)** | **0.50 mm** (20 mil) | Baixa resistência e queda de tensão mínima. |
| **Largura de trilha (Potência 1A a 2A)** | **1.00 mm a 1.50 mm** | Elevação térmica segura (< 10°C). |
| **Folga de isolamento (Clearance Cu-Cu)** | **0.15 mm a 0.20 mm** | Trilha-trilha, trilha-pad e pad-pad. |
| **Distância do cobre à borda da placa** | **0.50 mm** | Previne curto-circuito no corte mecânico. |
| **Vias padrão (Broca / Anel de Cobre)** | **Drill 0.30 mm / Pad 0.60 mm** | Menor custo, sem taxa de furação fina. |
| **Vias de potência (Reforçadas)** | **Drill 0.40 mm / Pad 0.80 mm** | Suporta ~1.5A contínuos por via; usar em paralelo. |
| **Texto de Serigrafia (Silkscreen)** | **Largura 0.15 mm / Altura 1.0 mm** | Garante leitura nítida sem borrar. |

---

## 🛠️ Ferramentas Locais Disponíveis

* **Criador de Novos Projetos:** `C:\Projetos_PCB\novo_projeto.bat <Nome_Do_Projeto>`
* **Repositório Modelo:** `C:\Projetos_PCB\Template_Projeto_PCB`
* **Banco Local JLCPCB:** SQLite com 513 mil componentes em `~/.kicad-mcp/data/jlcpcb_parts.db`.
* **Autoroteador FreeRouting:** Integrado em `~/.kicad-mcp/freerouting.jar`.
* **Servidor KiCad MCP:** Ativo via `kicad-cli.exe` e Node.js para inspeção e automação de placas direto pelo chat.
