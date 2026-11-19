import os
import sys
import math

def parse_data(file_path):
    headers = []
    rows = []
    delimiter = ','
    
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if not headers:
                if ';' in line:
                    delimiter = ';'
                elif '\t' in line:
                    delimiter = '\t'
                headers = [h.strip().strip('"') for h in line.split(delimiter)]
                continue
            parts = line.split(delimiter)
            if len(parts) == len(headers):
                try:
                    vals = [float(p.strip().strip('"').replace(',', '.')) for p in parts]
                    rows.append(vals)
                except ValueError:
                    pass
    return headers, rows

def calc_stats(series):
    if not series:
        return {}
    n = len(series)
    v_min = min(series)
    v_max = max(series)
    v_pk_pk = v_max - v_min
    v_mean = sum(series) / n
    variance = sum((x - v_mean) ** 2 for x in series) / n
    v_std = math.sqrt(variance)
    v_rms = math.sqrt(sum(x ** 2 for x in series) / n)
    return {
        'count': n,
        'min': v_min,
        'max': v_max,
        'pk_pk': v_pk_pk,
        'mean': v_mean,
        'std': v_std,
        'rms': v_rms
    }

def quicklook(file_path, plot_col=None, time_col=None, out_plot=None):
    if not os.path.exists(file_path):
        print(f"[data-quicklook] Arquivo nao encontrado: {file_path}")
        return

    headers, rows = parse_data(file_path)
    if not rows:
        print("[data-quicklook] Nao foi possivel extrair dados numericos do arquivo.")
        return

    print(f"=== [data-quicklook] Analise: {os.path.basename(file_path)} ===")
    print(f"Total de registros: {len(rows)} | Total de colunas: {len(headers)}\n")

    cols_data = {h: [r[i] for r in rows] for i, h in enumerate(headers)}

    for h in headers:
        st = calc_stats(cols_data[h])
        print(f"Coluna: {h}")
        print(f"  Min: {st['min']:.4f} | Max: {st['max']:.4f} | Pk-Pk: {st['pk_pk']:.4f}")
        print(f"  Media: {st['mean']:.4f} | RMS: {st['rms']:.4f} | Desvio: {st['std']:.4f}\n")

    if plot_col and plot_col in cols_data:
        try:
            import matplotlib
            matplotlib.use('Agg')
            import matplotlib.pyplot as plt

            plt.figure(figsize=(10, 4), dpi=150)
            x_data = cols_data[time_col] if time_col and time_col in cols_data else list(range(len(rows)))
            x_label = time_col if time_col else "Amostras"

            plt.plot(x_data, cols_data[plot_col], color='#0066cc', linewidth=1.2, label=plot_col)
            plt.title(f"Sinal: {plot_col} - {os.path.basename(file_path)}", fontsize=11, fontweight='bold')
            plt.xlabel(x_label, fontsize=10)
            plt.ylabel(plot_col, fontsize=10)
            plt.grid(True, linestyle='--', alpha=0.6)
            plt.legend(loc='upper right')
            plt.tight_layout()

            dest_plot = out_plot if out_plot else f"{plot_col}_plot.png"
            os.makedirs(os.path.dirname(os.path.abspath(dest_plot)), exist_ok=True)
            plt.savefig(dest_plot)
            plt.close()
            print(f"[data-quicklook] Grafico gerado com sucesso em: {dest_plot}")
        except Exception as e:
            print(f"[data-quicklook] Erro ao renderizar grafico via matplotlib: {e}")

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="Inspecao rapida de dados tabulares de bancada")
    parser.add_argument('--input', required=True, help="Caminho do arquivo CSV ou TXT")
    parser.add_argument('--plot', help="Nome da coluna a ser plotada")
    parser.add_argument('--time', help="Nome da coluna de tempo (eixo X)")
    parser.add_argument('--output', help="Caminho de saida do grafico PNG")
    args = parser.parse_args()

    quicklook(args.input, args.plot, args.time, args.output)
