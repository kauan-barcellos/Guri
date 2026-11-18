"""
Frente 4: Text Compressor (Inspirado no LLMLingua / Selective-Context).
Poda frases de preenchimento, parágrafos repetitivos e jargões vazios,
preservando rigorosamente tabelas, números, blocos de código e fatos técnicos.
"""

import re
from typing import Dict, List

# Expressões de preenchimento e clichês que não agregam valor técnico
FILLER_PATTERNS = [
    re.compile(r"\b(?:com certeza|certamente|com muito prazer|é com grande satisfação|espero que isso ajude)[^.!?\n]*[.!?:]*", re.I),
    re.compile(r"\b(?:como mencionado anteriormente|como você sabe|vale ressaltar que|é importante notar que|cabe destacar que)\s*,?", re.I),
    re.compile(r"\b(?:se você tiver alguma dúvida|fico à disposição|qualquer dúvida estou aqui|conte comigo)[^.!?\n]*[.!?:]*", re.I),
]

def _is_filler_sentence(sent: str) -> bool:
    for pat in FILLER_PATTERNS:
        if pat.search(sent):
            return True
    return False

def compress_text_content(text: str, aggressive: bool = False) -> Dict[str, any]:
    """
    Comprime documentos textuais e relatórios longos.
    Preserva blocos de código, tabelas Markdown e métricas numéricas.
    """
    lines = text.splitlines()
    compressed_lines: List[str] = []
    seen_paragraphs = set()
    in_code_block = False

    for line in lines:
        stripped = line.strip()

        # Blocos de código são preservados integralmente sem alteração
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            compressed_lines.append(line)
            continue
        
        if in_code_block:
            compressed_lines.append(line)
            continue

        # Preserva linhas de tabelas markdown e cabeçalhos intactos
        if stripped.startswith("|") or stripped.startswith("#"):
            compressed_lines.append(line)
            continue

        # Linhas em branco consecutivas são suprimidas
        if not stripped:
            if compressed_lines and compressed_lines[-1] != "":
                compressed_lines.append("")
            continue

        # Deduplicação de parágrafos idênticos
        normalized = re.sub(r"\s+", " ", stripped.lower())
        if len(normalized) > 40:
            if normalized in seen_paragraphs:
                continue
            seen_paragraphs.add(normalized)

        # Remoção de frases de preenchimento
        cleaned_line = line
        for pat in FILLER_PATTERNS:
            cleaned_line = pat.sub("", cleaned_line).strip()

        if cleaned_line:
            # Em modo agressivo, reduz pontuações redundantes e espaços múltiplos
            if aggressive:
                cleaned_line = re.sub(r"\s{2,}", " ", cleaned_line)
            compressed_lines.append(cleaned_line)

    result = "\n".join(compressed_lines).strip()
    orig_tokens = len(text) // 4
    comp_tokens = max(1, len(result) // 4)
    savings_pct = round((1 - (comp_tokens / max(1, orig_tokens))) * 100, 1) if orig_tokens > 0 else 0.0

    return {
        "content": result,
        "original_tokens_est": orig_tokens,
        "compressed_tokens_est": comp_tokens,
        "savings_percentage": max(0.0, savings_pct),
    }
