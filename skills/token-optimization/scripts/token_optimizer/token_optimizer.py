"""
Token Optimizer Orchestrator: Fachada unificada para orquestração dinâmica das 5 frentes.
Detecta automaticamente o tipo de dado de entrada e aplica a técnica de compactação
ótima com métricas imediatas de economia de tokens.
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, Optional

from .fact_cache import FactCache
from .json_pruner import prune_json_payload
from .log_filter import filter_log_output
from .repo_map import generate_repo_map
from .text_compressor import compress_text_content

class TokenOptimizer:
    def __init__(self):
        self.cache = FactCache()

    def optimize(
        self, 
        data: Any, 
        hint_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Orquestra a compactação dinâmica.
        hint_type pode ser: 'code', 'log', 'json', 'text', 'cache' ou None (auto-detecção).
        """
        # 1. Se for caminho em disco existente
        if isinstance(data, str) and (os.path.exists(data) or data.startswith(".")):
            p = Path(data)
            if p.is_dir() or p.suffix == ".py":
                res = generate_repo_map(str(p))
                res["strategy"] = "AST Repo-Map (Aider)"
                return res

        # 2. Se for JSON ou dicionário Python
        if isinstance(data, (dict, list)):
            res = prune_json_payload(data)
            res["strategy"] = "JSON Pruner (Headroom)"
            return res

        if isinstance(data, str):
            trimmed = data.strip()
            
            # Testa se é JSON válido
            if (trimmed.startswith("{") and trimmed.endswith("}")) or (trimmed.startswith("[") and trimmed.endswith("]")):
                try:
                    res = prune_json_payload(trimmed)
                    res["strategy"] = "JSON Pruner (Headroom)"
                    return res
                except Exception:
                    pass

            # Testa se é log de terminal (pytest, traceback, compiler)
            if any(term in trimmed.lower() for term in [
                "traceback (most recent call last)", "pytest", "passed in", "failed in", 
                "error:", "warning:", "\x1b[", "=== failed"
            ]):
                res = filter_log_output(trimmed)
                res["strategy"] = "Log Filter (RTK)"
                return res

            # Caso padrão: compressão de texto/relatório
            res = compress_text_content(trimmed)
            res["strategy"] = "Text Paring (LLMLingua)"
            return res

        return {
            "content": str(data),
            "strategy": "Passthrough",
            "savings_percentage": 0.0,
        }

def main():
    parser = argparse.ArgumentParser(description="Token Optimizer Suite - Compactação Dinâmica Multi-Frentes")
    parser.add_argument("--path", help="Gera Repo-Map para caminho de arquivo ou pasta")
    parser.add_argument("--json", help="Compacta string JSON")
    parser.add_argument("--log", help="Filtra arquivo de log")
    parser.add_argument("--text", help="Comprime arquivo de texto")
    parser.add_argument("--cache-get", nargs=2, metavar=("NAMESPACE", "KEY"), help="Busca fato em cache")
    parser.add_argument("--cache-set", nargs=3, metavar=("NAMESPACE", "KEY", "CONTENT"), help="Salva fato em cache")
    parser.add_argument("--seed-cache", action="store_true", help="Alimenta cache com regras padrões")

    args = parser.parse_args()
    optimizer = TokenOptimizer()

    if args.seed_cache:
        optimizer.cache.seed_defaults()
        print("Cache alimentado com regras padrões de engenharia.")
        return

    if args.cache_get:
        ns, key = args.cache_get
        val = optimizer.cache.get(ns, key)
        if val:
            print(f"[CACHE HIT 100% Economia]\n{val}")
        else:
            print("[CACHE MISS]")
        return

    if args.cache_set:
        ns, key, val = args.cache_set
        optimizer.cache.set(ns, key, val)
        print(f"Fato registrado em '{ns}::{key}'.")
        return

    if args.path:
        res = optimizer.optimize(args.path)
        print(f"=== {res['strategy']} | Economia: {res['savings_percentage']}% ===")
        print(res["content"])
        return

    if args.log:
        p = Path(args.log)
        content = p.read_text(encoding="utf-8") if p.exists() else args.log
        res = optimizer.optimize(content, hint_type="log")
        print(f"=== {res['strategy']} | Economia: {res['savings_percentage']}% ===")
        print(res["content"])
        return

    if args.json:
        res = optimizer.optimize(args.json, hint_type="json")
        print(f"=== {res['strategy']} | Economia: {res['savings_percentage']}% ===")
        print(res["content"])
        return

    parser.print_help()

if __name__ == "__main__":
    main()
