# -*- coding: utf-8 -*-
"""
Script utilitário para inspeção e processamento de dados do catman (.BIN)
"""
import os
import sys
import numpy as np
from apread import APReader
from scipy.signal import find_peaks

def inspecionar_arquivo(caminho_bin):
    """Exibe um resumo completo dos canais e duração do arquivo."""
    if not os.path.isfile(caminho_bin):
        print(f"[!] Arquivo não encontrado: {caminho_bin}")
        return None
    
    leitor = APReader(caminho_bin)
    print("\n" + "=" * 60)
    print(f"  ARQUIVO: {os.path.basename(caminho_bin)}")
    print("=" * 60)
    
    for idx, grupo in enumerate(leitor.Groups, 1):
        t_dados = grupo.Channels[0].data
        dt = (t_dados[-1] - t_dados[0]) / max(1, len(t_dados) - 1)
        fs = 1.0 / dt if dt > 0 else 0
        duracao = t_dados[-1] - t_dados[0]
        
        print(f"\nGrupo {idx}: '{grupo.Name}'")
        print(f"  * Taxa de amostragem : {fs:.1f} Hz")
        print(f"  * Duração total      : {duracao:.2f} s ({duracao/60:.2f} min)")
        print(f"  * Total de pontos    : {len(t_dados):,}")
        print("  * Canais disponíveis:")
        
        for ch in grupo.Channels[1:]:
            unid = ch.extHeader.get('PhysUnit', '').strip()
            rotulo = f"{ch.Name} ({unid})" if unid else ch.Name
            print(f"      - {rotulo}")
    print("=" * 60 + "\n")
    return leitor

def extrair_metricas_impacto(tempo, torque, altura_minima=20.0, dist_ms=15.0, fs=19200.0):
    """Calcula picos, média e cadência (IPM) de uma rajada de impacto."""
    dist_pontos = int(fs * (dist_ms / 1000.0))
    picos_idx, _ = find_peaks(torque, height=altura_minima, distance=dist_pontos)
    
    if len(picos_idx) == 0:
        return {"pico_max": torque.max(), "pico_min": torque.min(), "ipm": 0, "media": 0}
    
    picos_val = torque[picos_idx]
    pico_max = picos_val.max()
    pico_min = torque.min()
    media_impactos = np.mean(picos_val)
    
    # Frequência de golpes
    if len(picos_idx) > 1:
        dt_medio = np.mean(np.diff(tempo[picos_idx]))
        freq_hz = 1.0 / dt_medio if dt_medio > 0 else 0
    else:
        freq_hz = 0
    
    return {
        "pico_max": pico_max,
        "pico_min": pico_min,
        "media_impactos": media_impactos,
        "freq_hz": freq_hz,
        "ipm": freq_hz * 60,
        "total_golpes": len(picos_idx)
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        inspecionar_arquivo(sys.argv[1])
    else:
        print("Uso: python analisador_catman.py <caminho_do_arquivo.bin>")
