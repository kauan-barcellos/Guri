---
name: electrical-panel-analyzer
description: >-
  Guides the agent in systematically analyzing visual PDFs and images of electrical panel diagrams. Extracts dimensions, internal/external layouts, and component TAGs without hallucination, outputting a professional Markdown report.
---

# Electrical Panel Analyzer

## Overview
This skill forces the agent to use a structured, page-by-page visual scanning methodology to analyze electrical control panel assembly diagrams (like chillers, heating systems, and pump centers). It ensures no components are missed and organizes the findings into a clean Markdown report.

## Dependencies
This skill leverages the following installed skills for enhanced accuracy:
- `computer-vision-expert`: Used for advanced spatial OCR to prevent mixing up TAGs and components that are visually close together (e.g., on DIN rails).
- `agent-memory-systems`: Used to retain the context and dimensions of panels from early pages while scanning later pages of extensive PDFs.
- `documentation-templates`: Used to format the final output into a professional, table-driven Markdown report.

## Quick Start
Provide a PDF or image of an electrical panel diagram and ask the agent:
"Analise este diagrama elétrico usando a skill electrical-panel-analyzer."

## Workflow

### 1. Setup & Memory Initialization
- **Action**: Invoke `agent-memory-systems` to start tracking the state.
- **Details**: Create a temporary memory structure to hold Dimensions, External Layout, Internal Layout, and Exceptions for each panel found in the document.

### 2. Structured Visual Scanning
- **Action**: Invoke `computer-vision-expert` techniques.
- **Details**: Scan the document page by page or section by section. Pay special attention to spatial positioning to correctly associate text TAGs (e.g., L1, B3.1, PT100) with their physical components (buttons, contactors, PLCs).

### 3. Data Extraction per Panel
- **Action**: Map the following for EACH panel:
  - **Identification**: Name/Function and Physical Dimensions (e.g., 500x600x200).
  - **General Requirements**: Textual instructions (e.g., wiring rules, terminal types).
  - **External Layout**: Door components, signals, HMIs, and their relative positions.
  - **Internal Layout**: Backplate components, DIN rails, circuit breakers.
  - **Connections & Wiring**: Detailed point-to-point connections (source to destination).
  - **Cable Specifications**: Extract cable gauges (bitola in mm² or AWG), colors, types, and shielding.

### 4. Exception Handling
- **Action**: Record unreadable items.
- **Details**: If any TAG or component is blurry or missing, DO NOT hallucinate or guess. Explicitly record it as `[ILEGÍVEL - Componente na posição X]` ou `[NÃO ENCONTRADO]`. Do not stop the analysis; continue to the next item.

### 5. Report Generation
- **Action**: Invoke `documentation-templates`.
- **Details**: Consolidate the memory state into a final Markdown report. Use clear tables for component lists (Component | TAG | Location), and separate tables for Wiring Schedules (From | To | Gauge | Color). Separate each panel into its own section.

## Common Mistakes
- Trying to summarize the entire PDF in one go instead of analyzing panel by panel.
- Hallucinating TAGs that are cut off or blurry. Always use the exception handling rule.
- Failing to use tables for the final output, resulting in a hard-to-read wall of text.
