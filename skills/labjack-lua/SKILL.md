---
name: labjack-lua
description: >-
  Guia e regras obrigatórias para desenvolvimento de scripts Lua embarcados na LabJack T7-PRO e T-Series.
  Use sempre que o usuário pedir para criar, modificar, analisar ou otimizar scripts Lua para a LabJack,
  garantindo conformidade com limites de memória RAM, precisão float 32-bit, temporização, interação via USER_RAM
  e boas práticas do manual oficial.
---

# Desenvolvimento Lua para LabJack T7-PRO / T-Series

Este guia define as regras fundamentais e procedimentos obrigatórios para escrever scripts Lua embarcados que rodam diretamente no processador da LabJack T7-PRO.

---

## 🛑 As 7 Regras Críticas de Desenvolvimento

### 1. Limite Severo de Memória RAM (Max ~150 linhas)
* A máquina virtual Lua consome ~25 KB da RAM da placa.
* O código-fonte é compilado em bytecode **dentro da própria LabJack**. Por isso, comentários longos, nomes compridos de funções/variáveis consomem a RAM do processo de compilação.
* **Prática**: Manter scripts enxutos (menos de 150 linhas).
* Chamar `collectgarbage()` periodicamente em loops longos se tabelas forem manipuladas.

### 2. Sempre Usar `local` para Variáveis e Funções
* No interpretador Lua embarcado, acessar variáveis globais leva mais que o dobro do tempo (17.2 µs vs 8.5 µs por iteração).
* **Obrigatório**: Declarar tudo como `local`:
  ```lua
  local x = 0
  local valor_sensor = 0
  ```
* **Obrigatório**: Criar referências locais para funções de hardware:
  ```lua
  local dioWrite = LJ.DIO_S_W
  local mbRead = MB.readTable
  local mbWrite = MB.writeTable
  ```

### 3. Precisão Numérica: Float 32-bit (IEEE 754)
* O interpretador Lua na T7 utiliza float de 32 bits de precisão simples.
* Valores inteiros acima de 24 bits (16.777.216) perdem precisão nos bits menos significativos.
* Para ler números inteiros grandes ou contadores de 32 bits, leia como dois registradores Modbus de 16 bits separados.

### 4. Controle de Tempo com `LJ.IntervalConfig`
* **Nunca** use loops `while true do` ocupando 100% da CPU sem temporizador.
* Use a API nativa de intervalos de alta precisão da LabJack:
  ```lua
  local checkInterval = LJ.CheckInterval
  LJ.IntervalConfig(0, 10) -- Configura intervalo 0 para 10 ms (100 Hz)

  while true do
    if checkInterval(0) then
      -- Executa a cada 10 ms
    end
  end
  ```

### 5. Comunicação com Python/Host via `USER_RAM`
* A troca de dados entre o script Lua (embarcado) e o código Python (no computador) deve ser feita pela memória Modbus compartilhada `USER_RAM`:
  * Registradores float: `USER_RAM_F32_0` até `USER_RAM_F32_19` (Endereço Modbus 46000...)
  * Registradores inteiros: `USER_RAM_U32_0` até `USER_RAM_U32_19`
* O script Lua grava os resultados na `USER_RAM` e o Python lê via `ljm.eReadName(handle, "USER_RAM_F32_0")`.

### 6. Gravação no Cartão SD e RTC (Recursos T7-PRO)
* Para salvar dados de forma autônoma sem computador:
  * A T7-PRO possui relógio RTC com bateria e slot MicroSD.
  * Use as bibliotecas integradas da LabJack para abrir arquivos no SD e salvar em CSV com carimbo de data/hora do RTC.

### 7. Inicialização e Autostart
* Para testar em tempo de execução: `LUA_RUN = 1` (inicia), `LUA_RUN = 0` (para).
* Para rodar de forma autônoma ao ligar a placa: `LUA_RUN = 1` seguido de gravação na memória Flash não-volátil da T7.

---

## 📝 Template Padrão para Novo Script Lua

```lua
-- Script Base Otimizado para T7-PRO
local checkInterval = LJ.CheckInterval
local mbRead = MB.readTable
local mbWrite = MB.writeTable

-- Intervalo de amostragem em ms (ex: 10 ms = 100 Hz)
LJ.IntervalConfig(0, 10)

-- Ajusta fatia de CPU do Lua (padrao = 10 instrucoes/servico)
LJ.setLuaThrottle(10)

local tensao = 0.0
local LIMITE_ALERTA = 0.8

while true do
  if checkInterval(0) then
    -- Le canal diferencial AIN0
    tensao = mbRead(0, 3) -- Endereco Modbus 0 (AIN0), tipo FLOAT32 (3)

    -- Logica de controle ou acionamento instantaneo
    if tensao > LIMITE_ALERTA then
      LJ.DIO_S_W(0, 1) -- Liga FIO0 em microssegundos
    else
      LJ.DIO_S_W(0, 0) -- Desliga FIO0
    end

    -- Exporta valor processado para o Python ler via USER_RAM
    mbWrite(46000, 3, tensao)
  end
end
```
