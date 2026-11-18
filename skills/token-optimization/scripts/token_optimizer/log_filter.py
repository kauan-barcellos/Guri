"""
Frente 2: Log Filter (Inspirado no RTK).
Sanitiza e compacta saídas de terminal, pytest, compiladores e git,
removendo sequências ANSI, barras de progresso e repetições inúteis,
preservando integralmente tracebacks, erros e sumários.
"""

import re
from typing import Dict, List

# Regex para limpar sequências de escape ANSI (cores e controle de terminal)
ANSI_ESCAPE = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")

# Padrões comuns de linhas de progresso ou spinners
PROGRESS_PATTERNS = [
    re.compile(r"^\s*\[[=\->\s]+\]\s*\d+%.*"),
    re.compile(r"^\s*\d+%\s*\|[#\-\s]+\|\s*.*"),
    re.compile(r"^Fetching.*?\r"),
    re.compile(r"^Downloading.*?\r"),
]

def clean_ansi(text: str) -> str:
    return ANSI_ESCAPE.sub("", text)

def is_progress_line(line: str) -> bool:
    for pattern in PROGRESS_PATTERNS:
        if pattern.match(line):
            return True
    return False

def filter_log_output(log_text: str, max_lines: int = 120) -> Dict[str, any]:
    """
    Filtra e condensa saídas de log do terminal.
    Preserva tracebacks, mensagens de erro e resumo final.
    """
    clean_text = clean_ansi(log_text)
    raw_lines = [l.rstrip() for l in clean_text.splitlines()]
    
    filtered_lines: List[str] = []
    prev_line = None
    repeat_count = 0

    # Fase 1: Remoção de progresso e repetições consecutivas
    for line in raw_lines:
        if is_progress_line(line):
            continue
        
        # Agrupamento de linhas idênticas consecutivas
        if line == prev_line:
            repeat_count += 1
            continue
        else:
            if repeat_count > 1:
                filtered_lines.append(f"    ... [Linha anterior repetida {repeat_count} vezes] ...")
            repeat_count = 0
            filtered_lines.append(line)
            prev_line = line

    if repeat_count > 1:
        filtered_lines.append(f"    ... [Linha anterior repetida {repeat_count} vezes] ...")

    # Fase 2: Identificação de linhas críticas (Tracebacks, Errors, FAILED, Summary)
    critical_indices = set()
    in_traceback = False

    for idx, line in enumerate(filtered_lines):
        line_lower = line.lower()
        if "traceback (most recent call last)" in line_lower:
            in_traceback = True
        
        if in_traceback:
            critical_indices.add(idx)
            # Fim do traceback geralmente é a linha da exceção
            if re.match(r"^[A-Za-z0-9_.]+(?:Error|Exception|Failed):", line):
                in_traceback = False
                continue

        if any(term in line_lower for term in [
            "error:", "failed:", "failure:", "fatal:", "exception:", 
            "syntaxerror", "importerror", "assertionerror", "warning:",
            "=== failed", "=== error", "=== passed", "=== summary"
        ]):
            # Adiciona a linha crítica e um pouco de contexto adjacente
            for c in range(max(0, idx - 1), min(len(filtered_lines), idx + 2)):
                critical_indices.add(c)

    # Fase 3: Poda inteligente caso exceda max_lines
    if len(filtered_lines) > max_lines:
        output_lines: List[str] = []
        # Mantém primeiras 15 linhas (cabeçalho/comando)
        head_count = 15
        for i in range(min(head_count, len(filtered_lines))):
            output_lines.append(filtered_lines[i])

        # Linhas críticas do meio
        middle_lines = []
        for i in range(head_count, len(filtered_lines) - 20):
            if i in critical_indices:
                middle_lines.append(filtered_lines[i])

        if middle_lines:
            output_lines.append("\n--- [Erros e Alertas Extraídos] ---")
            output_lines.extend(middle_lines[: max_lines - 40])

        output_lines.append(f"\n--- [Logs intermediários suprimidos ({len(filtered_lines) - max_lines} linhas)] ---")

        # Mantém últimas 20 linhas (resumo do teste / status de saída)
        tail_start = max(head_count, len(filtered_lines) - 20)
        output_lines.extend(filtered_lines[tail_start:])
        final_result = "\n".join(output_lines)
    else:
        final_result = "\n".join(filtered_lines)

    orig_tokens = len(log_text) // 4
    comp_tokens = max(1, len(final_result) // 4)
    savings_pct = round((1 - (comp_tokens / max(1, orig_tokens))) * 100, 1) if orig_tokens > 0 else 0.0

    return {
        "content": final_result,
        "original_lines": len(raw_lines),
        "compressed_lines": len(final_result.splitlines()),
        "original_tokens_est": orig_tokens,
        "compressed_tokens_est": comp_tokens,
        "savings_percentage": max(0.0, savings_pct),
    }
