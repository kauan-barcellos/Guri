---
name: lgpd-consent-schema
description: Modelagem e especificação técnica de consentimento (Consent Ledger) para LGPD (Art. 8º). Use para implementar opt-in, gestão de consentimento de cookies e registro de termos aceitos.
---

# LGPD Consent Schema & Ledger

## Objetivo
Implementar o registro técnico inalterável de consentimento do titular de dados pessoais (Art. 8º da LGPD), permitindo comprovação e fácil revogação.

## Estrutura do Consent Record
- `userId` / `userIdentifier`: Identificador único do titular.
- `consentType`: Tipo de tratamento (ex: `marketing_emails`, `analytics_cookies`).
- `status`: `GRANTED` ou `REVOKED`.
- `timestamp`: Data/hora em ISO 8601 UTC.
- `policyVersion`: Versão dos termos aceitos (ex: `v1.2`).
- `ipAddress` / `userAgent`: Prova técnica de captura.
