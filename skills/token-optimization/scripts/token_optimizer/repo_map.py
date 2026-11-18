"""
Frente 1: AST Repo-Map (Inspirado no Aider).
Extrai a árvore sintática de código Python (classes, métodos, assinaturas e docstrings),
eliminando corpos de funções para reduzir o consumo de tokens em 80% a 90%.
"""

import ast
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple

EXCLUDE_DIRS = {
    ".git",
    "__pycache__",
    ".pytest_cache",
    ".venv",
    "venv",
    "node_modules",
    "dist",
    "build",
    ".idea",
    ".vscode",
}

class ASTSignatureExtractor(ast.NodeVisitor):
    def __init__(self):
        self.lines: List[str] = []
        self.indent = 0

    def _add(self, text: str):
        self.lines.append("    " * self.indent + text)

    def visit_Module(self, node: ast.Module):
        doc = ast.get_docstring(node)
        if doc:
            first_line = doc.strip().split("\n")[0]
            self._add(f'"""{first_line}"""')
        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef):
        bases = [ast.unparse(b) for b in node.bases]
        bases_str = f"({', '.join(bases)})" if bases else ""
        self._add(f"class {node.name}{bases_str}:")
        
        doc = ast.get_docstring(node)
        self.indent += 1
        if doc:
            first_line = doc.strip().split("\n")[0]
            self._add(f'"""{first_line}"""')
        
        # Visita apenas nós filhos que sejam funções ou classes internas
        has_children = False
        for child in node.body:
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                self.visit(child)
                has_children = True
            elif isinstance(child, ast.AnnAssign) and isinstance(child.target, ast.Name):
                # Anotações de atributos de classe (Dataclasses / Pydantic)
                val = f" = {ast.unparse(child.value)}" if child.value else ""
                self._add(f"{child.target.id}: {ast.unparse(child.annotation)}{val}")
                has_children = True
        
        if not has_children and not doc:
            self._add("...")
        self.indent -= 1

    def visit_FunctionDef(self, node: ast.FunctionDef):
        self._format_function(node, is_async=False)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        self._format_function(node, is_async=True)

    def _format_function(self, node, is_async: bool):
        prefix = "async def " if is_async else "def "
        args = ast.unparse(node.args)
        ret = f" -> {ast.unparse(node.returns)}" if node.returns else ""
        self._add(f"{prefix}{node.name}({args}){ret}:")
        
        self.indent += 1
        doc = ast.get_docstring(node)
        if doc:
            first_line = doc.strip().split("\n")[0]
            self._add(f'"""{first_line}"""')
        self._add("...")
        self.indent -= 1


def summarize_python_file(file_path: Path) -> Optional[str]:
    try:
        source = file_path.read_text(encoding="utf-8", errors="ignore")
        parsed = ast.parse(source, filename=str(file_path))
        extractor = ASTSignatureExtractor()
        extractor.visit(parsed)
        return "\n".join(extractor.lines)
    except Exception:
        return None


def generate_repo_map(target_path: str, max_files: int = 50) -> Dict[str, any]:
    """
    Gera o mapa sintático do repositório ou arquivo individual.
    Retorna o mapa condensado e métricas de economia de tokens.
    """
    path = Path(target_path)
    if not path.exists():
        raise FileNotFoundError(f"Caminho não encontrado: {target_path}")

    files_to_process: List[Path] = []
    if path.is_file():
        files_to_process = [path]
    else:
        for root, dirs, files in os.walk(path):
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS and not d.startswith(".")]
            for f in files:
                if f.endswith(".py"):
                    files_to_process.append(Path(root) / f)
                    if len(files_to_process) >= max_files:
                        break
            if len(files_to_process) >= max_files:
                break

    map_lines: List[str] = []
    total_original_chars = 0
    total_compressed_chars = 0
    processed_count = 0

    base_dir = path if path.is_dir() else path.parent

    for f in files_to_process:
        try:
            rel_path = f.relative_to(base_dir)
        except ValueError:
            rel_path = f.name
            
        original_size = f.stat().st_size
        total_original_chars += original_size
        
        summary = summarize_python_file(f)
        if summary and summary.strip():
            map_lines.append(f"### {rel_path}")
            map_lines.append("```python")
            map_lines.append(summary)
            map_lines.append("```\n")
            total_compressed_chars += len(summary)
            processed_count += 1

    content = "\n".join(map_lines)
    orig_tokens = total_original_chars // 4
    comp_tokens = max(1, len(content) // 4)
    savings_pct = round((1 - (comp_tokens / max(1, orig_tokens))) * 100, 1) if orig_tokens > 0 else 0.0

    return {
        "content": content,
        "files_processed": processed_count,
        "original_tokens_est": orig_tokens,
        "compressed_tokens_est": comp_tokens,
        "savings_percentage": max(0.0, savings_pct),
    }
