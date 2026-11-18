---
name: platformio-workflow
description: >-
  Fluxo de trabalho de engenharia de firmware com PlatformIO para ESP32, STM32 e Arduino.
  Use para configurar projetos multi-alvo em platformio.ini, executar testes unitarios com o framework Unity (tanto nativos no computador quanto fisicos na placa), compilar com flags de otimizacao GCC e gerenciar dependencias.
---

# PlatformIO Multi-Target Workflow & Unity Testing

Esta skill padroniza o ciclo de vida de desenvolvimento, compilacao, teste e gravacao de firmware profissional para microcontroladores (ESP32, STM32 e Arduino) utilizando o ecossistema PlatformIO Core.

---

## 1. Arquitetura Multi-Alvo (`platformio.ini`)

Um unico repositorio de firmware pode compilar para multiplos microcontroladores mantendo o nucleo da logica de negocio desacoplado da camada de abstracao de hardware (HAL).

### Exemplo de Configuracao Profissional:

```ini
[platformio]
default_envs = esp32dev

[common]
build_flags = 
    -Os
    -Wall
    -Wextra
    -fno-exceptions
    -fno-rtti
lib_deps_builtin = 
    bblanchon/ArduinoJson @ ^7.0.0
    etlcpp/Embedded Template Library @ ^20.35.0

; ====================================================================
; ESP32 (Espressif ESP32-WROOM-32)
; ====================================================================
[env:esp32dev]
platform = espressif32 @ ^6.5.0
board = esp32dev
framework = arduino
build_flags = 
    ${common.build_flags}
    -D CORE_DEBUG_LEVEL=0
monitor_speed = 115200
monitor_filters = esp32_exception_decoder, time, colorize
lib_deps = 
    ${common.lib_deps_builtin}
    h2zero/NimBLE-Arduino @ ^1.4.1

; ====================================================================
; STM32 (Blue Pill - STM32F103C8T6)
; ====================================================================
[env:bluepill_f103c8]
platform = ststm32 @ ^17.2.0
board = bluepill_f103c8
framework = arduino
upload_protocol = stlink
debug_tool = stlink
build_flags = 
    ${common.build_flags}
    -D PIO_FRAMEWORK_ARDUINO_ENABLE_CDC
monitor_speed = 115200
lib_deps = 
    ${common.lib_deps_builtin}

; ====================================================================
; Arduino AVR (Uno / Nano - ATmega328P)
; ====================================================================
[env:uno]
platform = atmelavr @ ^5.0.0
board = uno
framework = arduino
build_flags = 
    ${common.build_flags}
monitor_speed = 115200
lib_deps = 
    ${common.lib_deps_builtin}

; ====================================================================
; Ambiente Nativo de Testes no Computador (Host x86/x64)
; ====================================================================
[env:native]
platform = native
test_framework = unity
build_flags = 
    -std=c++17
    -D UNIT_TEST
lib_deps = 
    ${common.lib_deps_builtin}
```

---

## 2. Testes Unitarios com Framework Unity

O PlatformIO integra nativamente o framework Unity (C puro), permitindo validar logica de negocio, calculos de filtros, algoritmos de CRC e maquinas de estado em duas frentes complementares:

### Frente A: Testes Nativos no PC (`pio test -e native`)
- Nao depende de placa fisica conectada na bancada.
- Compilacao e execucao quase instantaneas usando o compilador GCC local (MinGW ou Linux/WSL).
- Ideal para validar funcoes matematicas, buffers circulares e parsers de pacotes seriais.

### Frente B: Testes On-Target (`pio test -e esp32dev` ou `pio test -e bluepill_f103c8`)
- Compila o firmware de teste e grava no microcontrolador via USB/SWD.
- Executa os testes no hardware real com comunicacao serial reportando os resultados para o terminal do PlatformIO.
- Ideal para validar amostragem de ADC, pulsos de PWM e interrupcoes de hardware.

### Estrutura de Arquivo de Teste (`test/test_ring_buffer/test_main.cpp`):

```cpp
#include <unity.h>
#include "ring_buffer.h"

void setUp(void) {
    // Inicializacao antes de cada teste
}

void tearDown(void) {
    // Limpeza apos cada teste
}

void test_ring_buffer_push_pop(void) {
    RingBuffer<uint8_t, 8> rb;
    TEST_ASSERT_TRUE(rb.isEmpty());
    TEST_ASSERT_TRUE(rb.push(0xAB));
    TEST_ASSERT_FALSE(rb.isEmpty());

    uint8_t val = 0;
    TEST_ASSERT_TRUE(rb.pop(val));
    TEST_ASSERT_EQUAL_HEX8(0xAB, val);
    TEST_ASSERT_TRUE(rb.isEmpty());
}

void test_ring_buffer_overflow_prevention(void) {
    RingBuffer<int, 4> rb;
    TEST_ASSERT_TRUE(rb.push(1));
    TEST_ASSERT_TRUE(rb.push(2));
    TEST_ASSERT_TRUE(rb.push(3));
    TEST_ASSERT_TRUE(rb.isFull());
    TEST_ASSERT_FALSE(rb.push(4)); // Nao pode aceitar alem da capacidade
}

int main(int argc, char **argv) {
    UNITY_BEGIN();
    RUN_TEST(test_ring_buffer_push_pop);
    RUN_TEST(test_ring_buffer_overflow_prevention);
    return UNITY_END();
}
```

---

## 3. Comandos de Linha de Comando (CLI)

Ao operar pelo terminal ou scripts de automacao:
- **Compilacao:** `pio run -e esp32dev` (ou `-e bluepill_f103c8`, `-e uno`).
- **Gravacao:** `pio run -t upload -e esp32dev`.
- **Monitor Serial:** `pio device monitor -e esp32dev`.
- **Execucao de Testes Unitarios Nativos:** `pio test -e native`.
- **Limpeza de Build:** `pio run -t clean`.
- **Inspecao de Memoria e Simbolos:** `pio check` e `pio run -t size`.
