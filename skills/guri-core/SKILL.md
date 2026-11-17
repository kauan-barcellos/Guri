---
name: guri-core
description: >-
  Núcleo de inicialização, identidade visual e banner do assistente Guri.
  Contém o script de inicialização do terminal (banner.py), as frases descontraídas de boas-vindas
  e os comandos de inicialização para qualquer máquina.
---

# Guri Core: Inicialização e Identidade

Este módulo é o coração do assistente **Guri**, responsável pela sua inicialização descontraída, exibição do banner no terminal e sincronização entre máquinas.

---

## 🎨 O Banner do Terminal (`scripts/banner.py`)
Ao ser chamado, imprime o banner em arte ASCII estilizado em azul/ciano e verde, com o subtítulo **"GURI • A mente que pensa"**, o status **"É só querer!"** e frases descontraídas sorteadas:
* *"Vem devagarinho. Qual a boa de hoje?"*
* *"Fala comigo! Em que posso ajudar hoje?"*
* *"Bora resolver uns problemas?"*
* *"Tudo em ordem por aqui. Qual é a missão de hoje?"*

---

## 🚀 Como Executar em Qualquer Máquina

Basta chamar o launcher:
* No Windows PowerShell:
  ```powershell
  python "$HOME\.gemini\config\skills\guri-core\scripts\banner.py"; agy
  ```
* Ou usar o atalho `guri` após instalar com `.\instalar_guri.ps1`.
