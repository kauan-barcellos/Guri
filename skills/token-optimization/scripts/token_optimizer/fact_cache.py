"""
Frente 5: Fact & Spec Cache (Inspirado no GPTCache).
Cache relacional local em SQLite para regras de hardware, pinagens,
limites de fabricação e especificações estáveis, economizando 100% dos tokens
em consultas recorrentes.
"""

import contextlib
import os
import re
import sqlite3
from pathlib import Path
from typing import Dict, List, Optional

def _get_default_cache_path() -> Path:
    # 1. Prioriza pasta local da própria skill
    skill_cache = Path(__file__).parent.parent / "cache" / "facts_cache.db"
    try:
        skill_cache.parent.mkdir(parents=True, exist_ok=True)
        # Testa permissão de escrita criando/abrindo
        test_file = skill_cache.parent / ".perm_check"
        test_file.touch()
        test_file.unlink()
        return skill_cache
    except Exception:
        pass

    # 2. Fallback resiliente para TEMP do sistema (sempre acessível na sandbox)
    temp_dir = Path(os.environ.get("TEMP", os.environ.get("TMP", "/tmp"))) / "guri_cache"
    temp_dir.mkdir(parents=True, exist_ok=True)
    return temp_dir / "facts_cache.db"

class FactCache:
    def __init__(self, db_path: Optional[Path] = None):
        self.db_path = db_path or _get_default_cache_path()
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    @contextlib.contextmanager
    def _connection(self):
        conn = sqlite3.connect(str(self.db_path))
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    def _normalize_key(self, text: str) -> str:
        # Normaliza chave: minúsculas, sem acentos grosseiros e espaços compactados
        clean = re.sub(r"[^\w\s]", "", text.lower())
        return re.sub(r"\s+", " ", clean).strip()

    def _init_db(self):
        with self._connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS facts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    namespace TEXT NOT NULL,
                    query_key TEXT NOT NULL,
                    normalized_key TEXT NOT NULL,
                    content TEXT NOT NULL,
                    tags TEXT,
                    access_count INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(namespace, normalized_key)
                )
            """)
            conn.execute("CREATE INDEX IF NOT EXISTS idx_norm_key ON facts (normalized_key)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_namespace ON facts (namespace)")

    def set(self, namespace: str, key: str, content: str, tags: str = "") -> bool:
        norm_key = self._normalize_key(key)
        with self._connection() as conn:
            conn.execute("""
                INSERT INTO facts (namespace, query_key, normalized_key, content, tags, access_count, updated_at)
                VALUES (?, ?, ?, ?, ?, 0, CURRENT_TIMESTAMP)
                ON CONFLICT(namespace, normalized_key) DO UPDATE SET
                    content = excluded.content,
                    tags = excluded.tags,
                    updated_at = CURRENT_TIMESTAMP
            """, (namespace, key, norm_key, content, tags))
        return True

    def get(self, namespace: str, key: str) -> Optional[str]:
        norm_key = self._normalize_key(key)
        with self._connection() as conn:
            cursor = conn.execute("""
                SELECT content FROM facts 
                WHERE namespace = ? AND normalized_key = ?
            """, (namespace, norm_key))
            row = cursor.fetchone()
            if row:
                conn.execute("""
                    UPDATE facts SET access_count = access_count + 1 
                    WHERE namespace = ? AND normalized_key = ?
                """, (namespace, norm_key))
                return row[0]
        return None

    def search(self, query: str, namespace: Optional[str] = None) -> List[Dict[str, any]]:
        norm_query = f"%{self._normalize_key(query)}%"
        with self._connection() as conn:
            if namespace:
                cursor = conn.execute("""
                    SELECT namespace, query_key, content, tags, access_count 
                    FROM facts 
                    WHERE namespace = ? AND (normalized_key LIKE ? OR tags LIKE ?)
                    ORDER BY access_count DESC LIMIT 5
                """, (namespace, norm_query, norm_query))
            else:
                cursor = conn.execute("""
                    SELECT namespace, query_key, content, tags, access_count 
                    FROM facts 
                    WHERE normalized_key LIKE ? OR tags LIKE ?
                    ORDER BY access_count DESC LIMIT 5
                """, (norm_query, norm_query))
            
            results = []
            for r in cursor.fetchall():
                results.append({
                    "namespace": r[0],
                    "key": r[1],
                    "content": r[2],
                    "tags": r[3],
                    "access_count": r[4],
                })
            return results

    def seed_defaults(self):
        """Carrega fatos fixos de engenharia para economizar consultas frequentes."""
        defaults = [
            (
                "jlcpcb", 
                "regras dfm 2 camadas", 
                "JLCPCB 2-Layer DFM: Trilha mínima 0.127mm (5mil), Folga mínima 0.127mm (5mil), Via mínima furo 0.3mm / anel 0.6mm, Espessura placa 1.6mm, Cobre 1oz (35um).",
                "dfm,jlcpcb,pcb,clearance"
            ),
            (
                "labjack", 
                "limites lua t7", 
                "LabJack T7 Lua: RAM total 2KB para script, floats 32-bit (sem 64-bit), USER_RAM para troca de registradores, interrupções determinísticas via timers LJ.",
                "labjack,lua,t7,memoria"
            ),
            (
                "kicad",
                "net classes de potencia",
                "Net Classes de Potência: Largura mínima 0.8mm a 1.2mm para correntes até 3A, vias com furo 0.4mm e diâmetro 0.8mm, isolamento mínimo 0.3mm para GND.",
                "kicad,netclass,potencia,largura"
            ),
        ]
        for ns, k, val, tags in defaults:
            self.set(ns, k, val, tags)
