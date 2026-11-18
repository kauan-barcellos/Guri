"""
Frente 3: JSON & MCP Payload Pruner (Inspirado no Headroom).
Compacta estruturas de dados JSON e retornos de ferramentas/MCPs,
removendo valores nulos, chaves vazias e tabularizando coleções repetitivas.
"""

import json
from typing import Any, Dict, List, Union

def _prune_recursive(obj: Any) -> Any:
    """Remove recursivamente valores nulos, listas e dicionários vazios."""
    if isinstance(obj, dict):
        pruned = {}
        for k, v in obj.items():
            cleaned_v = _prune_recursive(v)
            if cleaned_v not in (None, "", {}, []):
                pruned[k] = cleaned_v
        return pruned
    elif isinstance(obj, list):
        pruned = []
        for item in obj:
            cleaned_item = _prune_recursive(item)
            if cleaned_item not in (None, "", {}, []):
                pruned.append(cleaned_item)
        return pruned
    return obj

def _can_tabularize(lst: List[Any]) -> bool:
    """Verifica se uma lista consiste em dicionários homogêneos adequados para tabela."""
    if not lst or len(lst) < 2:
        return False
    if not all(isinstance(item, dict) for item in lst):
        return False
    # Verifica se os primeiros itens compartilham a maioria das chaves
    keys_sample = set(lst[0].keys())
    if not keys_sample or len(keys_sample) > 15:
        return False
    for item in lst[1:5]:
        if set(item.keys()) != keys_sample:
            return False
    return True

def _tabularize(lst: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Converte lista de dicionários uniformes em formato columnar compacto."""
    headers = list(lst[0].keys())
    rows = []
    for item in lst:
        row = [item.get(h, "") for h in headers]
        rows.append(row)
    return {"_format": "tabular", "headers": headers, "rows": rows}

def prune_json_payload(
    json_input: Union[str, Dict, List], 
    format_output: str = "compact"
) -> Dict[str, any]:
    """
    Compacta payload JSON.
    format_output pode ser 'compact' (JSON sem espaços) ou 'markdown' (tabela quando aplicável).
    """
    if isinstance(json_input, str):
        original_raw = json_input
        try:
            parsed = json.loads(json_input)
        except json.JSONDecodeError:
            return {
                "content": json_input,
                "error": "Input não é um JSON válido.",
                "savings_percentage": 0.0,
            }
    else:
        parsed = json_input
        original_raw = json.dumps(json_input, indent=2)

    # 1. Poda de valores nulos e vazios
    pruned = _prune_recursive(parsed)

    # 2. Tabularização de coleções homogêneas
    if isinstance(pruned, list) and _can_tabularize(pruned):
        pruned = _tabularize(pruned)
    elif isinstance(pruned, dict):
        for k, v in list(pruned.items()):
            if isinstance(v, list) and _can_tabularize(v):
                pruned[k] = _tabularize(v)

    # 3. Formatação
    if format_output == "markdown" and isinstance(pruned, dict) and pruned.get("_format") == "tabular":
        headers = pruned["headers"]
        rows = pruned["rows"]
        md_lines = ["| " + " | ".join(str(h) for h in headers) + " |"]
        md_lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
        for r in rows:
            md_lines.append("| " + " | ".join(str(val) for val in r) + " |")
        final_str = "\n".join(md_lines)
    else:
        # JSON denso sem espaços
        final_str = json.dumps(pruned, separators=(",", ":"), ensure_ascii=False)

    orig_tokens = len(original_raw) // 4
    comp_tokens = max(1, len(final_str) // 4)
    savings_pct = round((1 - (comp_tokens / max(1, orig_tokens))) * 100, 1) if orig_tokens > 0 else 0.0

    return {
        "content": final_str,
        "original_tokens_est": orig_tokens,
        "compressed_tokens_est": comp_tokens,
        "savings_percentage": max(0.0, savings_pct),
    }
