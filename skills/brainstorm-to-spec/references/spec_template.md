# Template: Especificacao Tecnica (SPEC.md)

## 1. Identificacao
* Projeto: 
* Modulo: 
* Data: 
* Versao: 1.0

## 2. Escopo
* Escopo Incluido:
* Fora do Escopo:

## 3. Interfaces Fisicas e Eletricas
| Sinal | Pino / Conector | Tipo | Nivel Eletrico | Notas |
| :--- | :--- | :--- | :--- | :--- |
| SDA | GPIO 21 | Bidirecional | 3.3V | Pull-up 4.7k ohm |
| SCL | GPIO 22 | Saida Clock | 3.3V | Pull-up 4.7k ohm |

## 4. Requisitos de Firmware / Software
* Sem alocacao de heap (memoria estatica garantida).
* Timeout de comunicacao fixado em 50 ms.

## 5. Criterios de Aceite
* [ ] Compilacao sem avisos (warnings) do GCC.
* [ ] Medicao real em osciloscopio ou log confirmando frequencia esperada.
