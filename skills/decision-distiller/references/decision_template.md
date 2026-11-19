# Registro de Decisoes de Projeto (.context/decisions.md)

Este documento registra as decisoes tecnicas tomadas durante o desenvolvimento, servindo como guia imutavel para sessoes futuras.

---

### [DEC-001] Exemplo de Registro
* Data: 2026-11-19
* Contexto: Escolha do conversor DC-DC para alimentacao de sensores analogicos.
* Decisao: Utilizar LDO linear dedicado em vez do regulador chaveado principal.
* Justificativa Tecnica: O ripple de chaveamento de 100 kHz interferia na leitura de pontes de strain gauge.
* Regra Pratica: Sensores analogicos de alta sensibilidade devem sempre receber alimentacao filtrada por LDO independente.
