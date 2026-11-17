# 🤖 GURI — A mente que pensa

```text
   ______  __  ______  ____
  / ____/ / / / / __ \/  _/   >> GURI • A mente que pensa
 / / __  / / / / /_/ // /     >> "Vem devagarinho. Qual a boa de hoje?"
/ /_/ / / /_/ / _, _// /      -------------------------------------------------
\____/  \____/_/ |_/___/      [+] Cérebro: Sincronizado via GitHub (Guri)
                              [+] Status:  É só querer!
════════════════════════════════════════════════════════════════════════════════════
```

> **"Vem devagarinho. Qual a boa de hoje?"**
> **Status:** *É só querer!*

Bem-vindo ao repositório central do **Guri**, o assistente pessoal polivalente feito para resolver qualquer parada: engenharia pesada, análise de dados de bancada, código, jurídico/LGPD, redação e automações do dia a dia.

---

## 🧠 Como o Guri é organizado

O cérebro do Guri é 100% modular, direto ao ponto e sem complicação. Ele é dividido em:

### 1. 📜 `rules/` (Como o Guri pensa e fala)
* **`diretrizes-gerais.md`**: Define a voz do Guri. Sempre em português do Brasil (pt-BR), didático, sem termos difíceis ou jargões desnecessários. Gráficos sempre a 300 DPI com grandezas e unidades físicas claras `[ex: Torque (Nm), Corrente (A)]`, tabelas limpas e links clicáveis.
* **`rotina-sync-encerramento.md`**: A regra sagrada: antes de fechar qualquer sessão, o Guri lembra ou executa o sync com este repositório para nunca perder nada.

### 2. ⚡ `skills/` (As especialidades do Guri)
Cada habilidade é uma pasta independente com manual (`SKILL.md`) e scripts prontos para rodar:
* **`guri-core/`**: O coração do Guri — o gerador de banner estiloso em arte ASCII com frases descontraídas.
* **`kicad10-hardware-design/`** & **`kicad10-pcb-designer/`**: Desenvolvimento de hardware no KiCad 10.0 + JLCPCB, regras de módulos COTS, segregação de ruído e automação MCP.
* **`bom-lifecycle-auditor/`** & **`embedded-pinout-planner/`**: Auditoria de componentes JLCPCB e pinagem de MCUs.
* **`hardware-adr/`**: Registros de Decisão de Arquitetura de Hardware (ADRs).
* **`leitor-catman/`**: Leitura de arquivos .BIN e .TST do HBM catman/QuantumX (amostragem a 19.2 kHz), decimação sem ruído (anti-aliasing) e ensaios de impacto.
* **`labjack-lua/`**: Scripts Lua embarcados de alto desempenho para DAQ LabJack T7-PRO.
* **`electrical-panel-analyzer/`**: Leitura e interpretação de diagramas e quadros elétricos.
* **`advogado-especialista/` & `lgpd-*/`**: Conjunto robusto de conformidade com a LGPD e suporte jurídico.
* **`matplotlib/` & `geopandas/`**: Visualização científica de dados em alta resolução e análise geoespacial.
* **`seu-tom-de-voz/`**: Tom de voz autêntico de liderança e regras anti-IA permanentes para e-mails, relatórios, posts e artigos.
* **`humanizer/`**: Refinamento de texto natural.

---

## 🚀 Como usar o Guri em qualquer máquina

### No computador novo (Primeira vez):
Abra o terminal e clone o Guri direto na sua pasta de configurações:
```powershell
git clone https://github.com/kauan-barcellos/Guri.git $HOME\.gemini\config
```

### Para ativar o comando `guri` no PowerShell:
Basta adicionar a função ao seu perfil (`$PROFILE`):
```powershell
function guri {
    python "$HOME\.gemini\config\skills\guri-core\scripts\banner.py"
    agy $args
}
```

### No dia a dia:
* **Antes de começar:**
  ```powershell
  cd $HOME\.gemini\config
  git pull origin main
  ```
* **Antes de fechar a sessão:**
  ```powershell
  cd $HOME\.gemini\config
  git add -A
  git commit -m "Novos aprendizados do Guri"
  git push origin main
  ```