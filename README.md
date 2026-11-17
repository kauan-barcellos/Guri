<p align="center">
  <img src="assets/banner.png" alt="GURI - A mente que pensa" width="100%">
</p>

<div align="center">

[![Status](https://img.shields.io/badge/Status-%C3%89%20s%C3%B3%20querer!-00C853?style=for-the-badge)](https://github.com/kauan-barcellos/Guri)
[![Language](https://img.shields.io/badge/Idioma-pt--BR-blue?style=for-the-badge)](https://github.com/kauan-barcellos/Guri)
[![Antigravity](https://img.shields.io/badge/Powered%20By-Antigravity%20CLI-blueviolet?style=for-the-badge)](https://antigravity.google)
[![KiCad](https://img.shields.io/badge/CAD-KiCad%2010.0-314CB6?style=for-the-badge&logo=kicad&logoColor=white)](https://kicad.org)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)

</div>

# Guri

Repositório central de configurações, habilidades e regras de trabalho do assistente Guri. Este diretório funciona como a memória persistente do agente no Antigravity CLI e pode ser clonado em qualquer máquina para manter o mesmo padrão de trabalho.

---

## O que está configurado aqui

O conteúdo é organizado em três pastas principais:

### 1. Regras permanentes (`rules/`)
Diretrizes ativas em todas as conversas e projetos:
* **`diretrizes-gerais.md`**: Linguagem direta em português do Brasil, sem termos rebuscados. Gráficos com 300 DPI, unidades físicas nos eixos e escalas comparáveis.
* **`seu-tom-de-voz.md`**: Regras anti-IA para textos e conversas (sem travessões artificiais, sem oposições correlativas, sem clichês corporativos e com autoridade baseada em fatos).
* **`rotina-sync-encerramento.md`**: Rotina de verificação e envio automático das alterações para o GitHub antes de fechar a sessão.

### 2. Habilidades de trabalho (`skills/`)
Módulos carregados sob demanda pelo agente:
* **Hardware e PCB (KiCad 10):**
  * `kicad10-hardware-design` e `kicad10-pcb-designer`: Criação de placas, roteamento e geração de arquivos para fabricação na JLCPCB.
  * `bom-lifecycle-auditor`: Consulta ao banco de 513 mil componentes da JLCPCB para escolher peças de linha básica e evitar custos extras de montagem.
  * `embedded-pinout-planner`: Planejamento de pinagem para microcontroladores (STM32, ESP32, RP2040).
  * `hardware-adr`: Modelos e registros de decisões de arquitetura de circuito.
* **Aquisição de Dados e Testes (DAQ):**
  * `leitor-catman`: Leitura de arquivos .BIN e .TST do software HBM catmanAP (amostragens a 19.200 Hz), decimação com média de bloco e cálculo de torque, impactos por minuto (IPM) e rebote.
  * `labjack-lua`: Scripts embarcados em Lua para a placa LabJack T7-PRO com controle de memória e registradores Modbus.
  * `electrical-panel-analyzer`: Leitura e extração de dados de diagramas e quadros elétricos.
* **Jurídico e Proteção de Dados:**
  * `advogado-especialista`: Suporte em direito civil, empresarial, trabalhista e contratos.
  * `lgpd-*`: Conjunto de 18 módulos para auditoria, mapeamento de dados (ROPA), relatórios de impacto (RIPD) e atendimento a titulares.
* **Visualização e Qualidade de Código:**
  * `matplotlib` e `geopandas`: Geração de gráficos técnicos em alta resolução e análise de dados espaciais.
  * `tdd-cycle-orchestrator` e `systematic-debugging`: Desenvolvimento orientado a testes e diagnóstico metódico de erros.
  * `guri-core`: Script de inicialização e banner do terminal com frases do dia.

---

## As 3 regras de hardware

Em qualquer projeto de circuito impresso, o Guri segue três critérios práticos:
1. **Módulos prontos:** Usar placas prontas comerciais (conversores DC-DC, transceivers RS485, ESP32) conectadas por barras de pinos. Evitar circuitos discretos complexos ao redor de chips avulsos.
2. **Ergonomia de montagem:** Bornes voltados para as bordas externas da placa, furos de fixação M3 nos quatro cantos, pontos de teste acessíveis para multímetro e serigrafia legível.
3. **Segregação de ruído:** Separar fisicamente a área de potência (alimentação, relés, motores) da área lógica e dos barramentos de comunicação (I2C, SPI, UART).

---

## Como usar em outra máquina

### 1. Clonar na pasta de configuração
No PowerShell de um computador novo:
```powershell
git clone https://github.com/kauan-barcellos/Guri.git $HOME\.gemini\config
```

### 2. Ativar o comando guri no terminal
Abra o arquivo de perfil do PowerShell (`notepad $PROFILE`) e adicione:
```powershell
function guri {
    python "$HOME\.gemini\config\skills\guri-core\scripts\banner.py"
    agy $args
}
```

### 3. Rotina de sincronização
* Ao começar o trabalho no dia:
  ```powershell
  cd $HOME\.gemini\config; git pull origin main
  ```
* Ao terminar a sessão:
  ```powershell
  cd $HOME\.gemini\config; git add -A; git commit -m "Atualização de habilidades"; git push origin main
  ```