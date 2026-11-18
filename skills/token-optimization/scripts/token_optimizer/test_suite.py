"""
Suíte de Testes Automatizados para a Token Optimizer Suite.
Valida rigorosamente o funcionamento das 5 frentes de economia.
"""

import os
import sys
import tempfile
from pathlib import Path

# Adiciona o diretório scripts ao sys.path para importação direta
current_dir = Path(__file__).parent.parent
sys.path.insert(0, str(current_dir))

from token_optimizer import (
    FactCache,
    TokenOptimizer,
    compress_text_content,
    filter_log_output,
    generate_repo_map,
    prune_json_payload,
)

def test_repo_map():
    print("[1/5] Testando AST Repo-Map (Aider)...", end=" ")
    sample_code = '''"""Modulo de teste para calculo de sinais e processamento de ensaios."""

import math
import time

class AnalisadorSinal:
    """Classe para processamento de sinais de ensaio."""
    taxa_amostragem: float = 1000.0
    buffer_limite: int = 50000

    def __init__(self, taxa: float, canal: int = 0):
        self.taxa = taxa
        self.canal = canal
        self.buffer = []
        self.contador = 0
        self.ativo = True

    def calcular_rms(self, dados: list[float]) -> float:
        """Calcula o valor RMS de um vetor de dados."""
        if not dados:
            return 0.0
        soma = 0.0
        for x in dados:
            soma += x * x
        media = soma / len(dados)
        resultado_rms = math.sqrt(media)
        return resultado_rms

    def filtrar_janela_movel(self, dados: list[float], tamanho_janela: int) -> list[float]:
        """Aplica filtro de media movel em todo o vetor de dados."""
        if len(dados) < tamanho_janela:
            return dados
        resultado = []
        for i in range(len(dados) - tamanho_janela + 1):
            janela = dados[i:i + tamanho_janela]
            resultado.append(sum(janela) / tamanho_janela)
        return resultado

    def exportar_estatisticas(self, dados: list[float]) -> dict:
        """Extrai metricas descritivas detalhadas da amostragem."""
        if not dados:
            return {}
        pico_max = max(dados)
        pico_min = min(dados)
        media_val = sum(dados) / len(dados)
        return {
            "max": pico_max,
            "min": pico_min,
            "media": media_val,
            "rms": self.calcular_rms(dados),
            "pontos": len(dados)
        }

async def coletar_dados_stream(canal: int, duracao_s: float) -> list[float]:
    """Coleta dados assincronos do sensor em alta frequencia."""
    amostras = []
    inicio = time.time()
    while time.time() - inicio < duracao_s:
        amostras.append(10.5)
    return amostras
'''
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False, encoding="utf-8") as f:
        f.write(sample_code)
        temp_file = f.name

    try:
        res = generate_repo_map(temp_file)
        assert res["files_processed"] == 1
        assert "class AnalisadorSinal:" in res["content"]
        assert "def calcular_rms(self, dados: list[float]) -> float:" in res["content"]
        assert "def filtrar_janela_movel(self, dados: list[float], tamanho_janela: int) -> list[float]:" in res["content"]
        assert "async def coletar_dados_stream(canal: int, duracao_s: float) -> list[float]:" in res["content"]
        assert "soma += x * x" not in res["content"]  # Corpo da função foi expurgado
        assert "sum(janela) / tamanho_janela" not in res["content"]  # Corpo expurgado
        assert res["savings_percentage"] > 30.0
        print(f"OK (Economia: {res['savings_percentage']}%)")
    finally:
        os.remove(temp_file)

def test_log_filter():
    print("[2/5] Testando Log Filter (RTK)...", end=" ")
    raw_lines = [
        "\x1b[32mStarting pytest run on test_suite.py...\x1b[0m",
        "[===>     ] 10% completed\r",
        "[========>] 50% completed\r",
    ]
    # Simula 40 linhas repetitivas de passagem de teste ou polling
    for i in range(40):
        raw_lines.append(f"test_modulo_calculo.py::test_caso_{i} PASSED [ {i*2}%]")
    for _ in range(15):
        raw_lines.append("DEBUG: Sensor polling alive state OK")
    raw_lines.extend([
        "Traceback (most recent call last):",
        "  File \"src/main.py\", line 42, in processar",
        "    raise ValueError(\"Valor fora dos limites do sensor\")",
        "ValueError: Valor fora dos limites do sensor",
        "=== 1 failed, 55 passed in 1.45s ==="
    ])
    raw_log = "\n".join(raw_lines)
    res = filter_log_output(raw_log, max_lines=30)
    assert "\x1b[32m" not in res["content"]  # ANSI limpo
    assert "[===>" not in res["content"]  # Barra de progresso eliminada
    assert "repetida" in res["content"].lower() or "suprimidos" in res["content"].lower()
    assert "ValueError: Valor fora dos limites do sensor" in res["content"]  # Traceback preservado
    assert "=== 1 failed, 55 passed in 1.45s ===" in res["content"]
    assert res["savings_percentage"] > 20.0
    print(f"OK (Economia: {res['savings_percentage']}%)")

def test_json_pruner():
    print("[3/5] Testando JSON Pruner (Headroom)...", end=" ")
    raw_json = {
        "status": "success",
        "empty_list": [],
        "null_val": None,
        "nested": {"valid": 123, "empty_dict": {}},
        "components": [
            {"ref": "R1", "val": "10k", "footprint": "0805", "desc": None},
            {"ref": "R2", "val": "22k", "footprint": "0805", "desc": None},
            {"ref": "R3", "val": "47k", "footprint": "0805", "desc": None},
        ]
    }
    res = prune_json_payload(raw_json, format_output="compact")
    assert "empty_list" not in res["content"]
    assert "null_val" not in res["content"]
    assert "empty_dict" not in res["content"]
    assert '"valid":123' in res["content"]
    assert res["savings_percentage"] > 20.0
    print(f"OK (Economia: {res['savings_percentage']}%)")

def test_text_compressor():
    print("[4/5] Testando Text Compressor (LLMLingua)...", end=" ")
    raw_text = """
    Certamente! É com grande satisfação que apresento este relatório técnico.
    
    O ensaio de impacto da ferramenta SPG2607 atingiu pico de torque de 1.450 Nm.
    
    O ensaio de impacto da ferramenta SPG2607 atingiu pico de torque de 1.450 Nm.
    
    Vale ressaltar que a corrente máxima medida foi de 18.2 A.
    
    Espero que isso ajude! Se você tiver alguma dúvida, fico à disposição!
    """
    res = compress_text_content(raw_text)
    assert "É com grande satisfação" not in res["content"]
    assert "Espero que isso ajude" not in res["content"]
    assert "1.450 Nm" in res["content"]
    assert "18.2 A" in res["content"]
    # Parágrafo repetido deve aparecer apenas uma vez
    assert res["content"].count("1.450 Nm") == 1
    assert res["savings_percentage"] > 35.0
    print(f"OK (Economia: {res['savings_percentage']}%)")

def test_fact_cache():
    print("[5/5] Testando Fact Cache (GPTCache)...", end=" ")
    with tempfile.NamedTemporaryFile("w", suffix=".db", delete=False) as f:
        temp_db = Path(f.name)

    try:
        cache = FactCache(db_path=temp_db)
        cache.seed_defaults()
        
        # Teste de consulta exata
        rule = cache.get("jlcpcb", "regras dfm 2 camadas")
        assert rule is not None
        assert "Trilha mínima 0.127mm" in rule
        
        # Teste de busca por palavra-chave
        results = cache.search("labjack")
        assert len(results) >= 1
        assert "LabJack T7 Lua" in results[0]["content"]
        print("OK (100% de Economia em consultas cacheadas)")
    finally:
        if temp_db.exists():
            os.remove(temp_db)

def run_all_tests():
    print("==================================================")
    print("Iniciando Validação da Token Optimizer Suite")
    print("==================================================")
    test_repo_map()
    test_log_filter()
    test_json_pruner()
    test_text_compressor()
    test_fact_cache()
    print("==================================================")
    print("TODAS AS 5 FRENTES VALIDADAS COM 100% DE SUCESSO!")
    print("==================================================")

if __name__ == "__main__":
    run_all_tests()
