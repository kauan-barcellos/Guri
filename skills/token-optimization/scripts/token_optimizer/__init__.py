"""
Token Optimizer Suite - Motor dinâmico de otimização e compressão de contexto.
Inspirado nas melhores práticas de Aider (AST Repo-Map), RTK (Log Filter),
Headroom (JSON/MCP Pruner), LLMLingua (Text Paring) e GPTCache (Fact Cache).
"""

from .repo_map import generate_repo_map
from .log_filter import filter_log_output
from .json_pruner import prune_json_payload
from .text_compressor import compress_text_content
from .fact_cache import FactCache
from .token_optimizer import TokenOptimizer

__all__ = [
    "generate_repo_map",
    "filter_log_output",
    "prune_json_payload",
    "compress_text_content",
    "FactCache",
    "TokenOptimizer",
]
