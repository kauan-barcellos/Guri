---
name: embedded-c-cpp-patterns
description: >-
  Padroes de desenvolvimento em C e C++ para microcontroladores (ESP32, STM32 e Arduino).
  Use para implementar firmware seguro sem fragmentacao de heap, rotinas de interrupcao deterministacas (ISR), filas circulares (Ring Buffers), maquinas de estado (FSM) e conteineres ETL sem alocacao dinamica.
---

# Embedded C/C++ Patterns & Memory Safety

Esta skill estabelece diretrizes de arquitetura e codificacao segura em C e C++ para sistemas embarcados e microcontroladores (ESP32, STM32 e Arduino), prevenindo travamentos por exaustao de memoria, corrupcao de pilha e condicoes de corrida em interrupcoes.

---

## 1. Seguranca de Memoria e Alocacao Estatica

Microcontroladores operam com limites rigidos de memoria SRAM (2KB no ATmega328P, 20KB a 128KB no STM32F1/F4, 320KB a 512KB no ESP32). A fragmentacao de heap e uma das principais causas de travamento intermitente em operacao continua.

### Regras Mandatorias:
1. **Zero Heap em Operacao Continua:** Proibido o uso de `malloc()`, `free()`, `new` e `delete` dentro do loop principal (`void loop()`, tarefas FreeRTOS recorrentes ou interrupcoes).
2. **Substituicao da STL por ETL (Embedded Template Library):**
   - Nao use `std::vector`, `std::string` ou `std::map` (usam alocacao dinamica e disparam excecoes).
   - Use os conteineres da ETL (`etl::vector<T, N>`, `etl::string<N>`, `etl::queue<T, N>`, `etl::map<K, V, N>`). O tamanho maximo $N$ e alocado estaticamente ou na stack em tempo de compilacao.
3. **Strings e Literais na Memoria Flash:**
   - **AVR / Arduino:** Use sempre a macro `F("texto")` para literais seriais e `PROGMEM` para tabelas de consulta e constantes, mantendo a SRAM livre.
   - **ESP32 / STM32:** Use ponteiros constantes `const char* const` mapeados diretamente na memoria Flash/ROM pelo compilador.
4. **Serializacao JSON sem Fragmentacao:**
   - Empregue `ArduinoJson v7` com objeto local na stack `JsonDocument doc;`. Evite versoes legadas que demandavam alocacao dinamica ou calculo manual de pool.

---

## 2. Rotinas de Servico de Interrupcao (ISR)

Interrupcoes de temporizadores, pinos GPIO ou perifricos seriais operam em contexto de alta prioridade e exigem regras deterministas.

### Protocolo de Seguranca em ISR:
1. **Qualificador `volatile`:** Toda variavel compartilhada entre a ISR e o codigo principal deve ser declarada como `volatile` para impedir que o compilador otimize leituras mantendo valores em registradores.
2. **Execucao Ultrarrapida:** A ISR deve apenas sinalizar uma flag booleana, incrementar um contador ou empilhar bytes em um buffer circular. O processamento pesado deve ocorrer na tarefa principal ou loop de controle.
3. **Operacoes Atomicas e Secoes Criticas:** Leituras e escritas em variaveis maiores que a palavra nativa do microcontrolador (ex: inteiros de 32 bits no AVR de 8 bits) devem ser protegidas desativando temporariamente as interrupcoes:
   - AVR: `noInterrupts(); ... interrupts();` ou bloco `ATOMIC_BLOCK`.
   - ARM Cortex-M (STM32): `__disable_irq(); ... __enable_irq();` ou mascaramento por prioridade via BASEPRI.
   - ESP32: Port mux com `taskENTER_CRITICAL()` e `taskEXIT_CRITICAL()`.
4. **Chamadas Proibidas em ISR:**
   - Nunca execute delays (`delay()`, `vTaskDelay()`).
   - Nunca faca chamadas de I/O bloqueante (como `Serial.print()` ou escritas em barramento I2C).
   - Nunca invoque funcoes que alocam memoria ou chamam mutexes bloqueantes.

---

## 3. Estruturas de Dados Deterministicas

### Fila Circular (Lock-Free Ring Buffer)
Ideal para recepcao serial (UART) e comunicacao entre ISR e consumidor principal:

```cpp
template <typename T, size_t Capacity>
class RingBuffer {
public:
    bool push(const T& item) {
        size_t next = (head_ + 1) % Capacity;
        if (next == tail_) return false; // Buffer cheio
        buffer_[head_] = item;
        head_ = next;
        return true;
    }

    bool pop(T& item) {
        if (head_ == tail_) return false; // Buffer vazio
        item = buffer_[tail_];
        tail_ = (tail_ + 1) % Capacity;
        return true;
    }

    bool isEmpty() const { return head_ == tail_; }
    bool isFull() const { return ((head_ + 1) % Capacity) == tail_; }

private:
    volatile size_t head_ = 0;
    volatile size_t tail_ = 0;
    T buffer_[Capacity];
};
```

### Maquina de Estados Finitos (FSM)
Controle deterministico de atuadores, sequenciamento de testes e protocolos de comunicacao:
- Defina os estados com `enum class State : uint8_t { IDLE, RUNNING, FAULT, COMPLETED };`.
- Mantenha transicoes em `switch-case` com clausula `default` explicita.
- Utilize temporizadores de guarda (watchdogs de estado) para impedir que a maquina fique presa indefinidamente em estados intermediarios.

---

## 4. Diretrizes Especifcas por Plataforma

### ESP32 (ESP-IDF / Arduino-ESP32)
- **Pinagem de Tarefas:** Use `xTaskCreatePinnedToCore()` destinando Core 0 para tarefas de rede (Wi-Fi, BLE) e Core 1 para processamento de controle e amostragem.
- **Stack das Tarefas:** Monitore o consumo de stack com `uxTaskGetStackHighWaterMark()`. Ajuste o tamanho da pilha para evitar estouro (Stack Overflow).
- **NimBLE:** Prefira a biblioteca `NimBLE-Arduino` sobre a biblioteca Bluetooth nativa para economizar ate 50% de memoria RAM e flash.
- **Aceleracao Matematica:** Empregue `esp-dsp` para calculos vetoriais, filtros digitais FIR/IIR e transformadas FFT com instrucoes SIMD.

### STM32 (STM32Duino / Cube HAL / libopencm3)
- **Descarregamento via DMA:** Configure canais de DMA (Direct Memory Access) para transmissao UART e leituras ADC continuas em modo circular, liberando a CPU para calculos.
- **Prioridades NVIC:** Defina prioridades numericas coerentes (0 e a prioridade maxima). Interrupcoes de seguranca (sobrecorrente, paradas de emergencia) devem ter prioridade superior a leituras de sensores periodicos.
- **Clocks:** Configure o oscilador externo HSE com multiplicador PLL para obter estabilidade de barramento e frequencia nominal do SYSCLK.

### Arduino (AVR / SAMD)
- **Multitarefa Cooperativa:** Proibido o uso de `delay()`. Use comparacoes com `millis()` ou a biblioteca `TaskScheduler` com callbacks periodicos.
- **Economia Extrema de SRAM:** Em chips ATmega328P, mantenha o uso estatico de SRAM abaixo de 70% (indicado na compilacao) para reservar espaco seguro para a stack de execucao.
