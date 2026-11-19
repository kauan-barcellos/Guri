#!/usr/bin/env python3
"""
GURI STATS - Telemetria e Monitor de Tokens e Contexto
Lê o transcript da sessão ativa do Antigravity CLI e gera um relatório detalhado
de consumo de tokens, eficiência de cache, uso da janela de contexto e chamadas de ferramentas.
"""

import os
import sys
import glob
import json
import argparse
from datetime import datetime

# Cores ANSI
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"

# Modelos conhecidos e suas capacidades de contexto
MODEL_CAPACITIES = {
    "gemini-3.8-flash-high": 1_000_000,
    "gemini-2.5-pro": 2_000_000,
    "gemini-2.5-flash": 1_000_000,
    "gemini-1.5-pro": 2_000_000,
    "gemini-1.5-flash": 1_000_000,
    "claude-3-5-sonnet": 200_000,
    "claude-3-7-sonnet": 200_000,
}
DEFAULT_CAPACITY = 1_000_000

def find_active_transcript(explicit_id=None, explicit_path=None):
    if explicit_path and os.path.exists(explicit_path):
        return explicit_path

    brain_dir = os.path.expanduser("~/.gemini/antigravity-cli/brain")
    if not os.path.exists(brain_dir):
        return None

    if explicit_id:
        target = os.path.join(brain_dir, explicit_id, ".system_generated", "logs", "transcript.jsonl")
        if os.path.exists(target):
            return target
        return None

    pattern = os.path.join(brain_dir, "*", ".system_generated", "logs", "transcript.jsonl")
    candidates = glob.glob(pattern)
    if not candidates:
        return None

    candidates.sort(key=os.path.getmtime, reverse=True)
    return candidates[0]

def render_bar(percentage, width=28):
    filled = int(round(width * (percentage / 100.0)))
    filled = max(0, min(width, filled))
    empty = width - filled
    return "█" * filled + "░" * empty

def analyze_transcript(transcript_path):
    stats = {
        "path": transcript_path,
        "conversation_id": os.path.basename(os.path.dirname(os.path.dirname(os.path.dirname(transcript_path)))),
        "total_steps": 0,
        "user_messages": 0,
        "model_turns": 0,
        "tool_steps": 0,
        "errors": 0,
        "models": {},
        "tool_calls": {},
        "total_input_tokens": 0,
        "total_cache_tokens": 0,
        "total_output_tokens": 0,
        "last_step": None,
        "first_timestamp": None,
        "last_timestamp": None,
    }

    with open(transcript_path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            try:
                item = json.loads(line)
            except Exception:
                continue

            stats["total_steps"] += 1
            stype = item.get("type", "")
            source = item.get("source", "")
            status = item.get("status", "")
            created_at = item.get("created_at")

            if created_at:
                if not stats["first_timestamp"]:
                    stats["first_timestamp"] = created_at
                stats["last_timestamp"] = created_at

            if status == "ERROR":
                stats["errors"] += 1

            if stype == "USER_INPUT":
                stats["user_messages"] += 1

            elif stype == "PLANNER_RESPONSE":
                stats["model_turns"] += 1
                model = item.get("model", "desconhecido")
                stats["models"][model] = stats["models"].get(model, 0) + 1

                inp = item.get("input_tokens", 0)
                cache = item.get("cache_read_tokens", 0)
                out = item.get("output_tokens", 0)

                stats["total_input_tokens"] += inp
                stats["total_cache_tokens"] += cache
                stats["total_output_tokens"] += out

                stats["last_step"] = {
                    "step_index": item.get("step_index"),
                    "model": model,
                    "input_tokens": inp,
                    "cache_read_tokens": cache,
                    "output_tokens": out,
                    "context_size": inp + cache
                }

                for tc in item.get("tool_calls", []):
                    tname = tc.get("name", "outra")
                    stats["tool_calls"][tname] = stats["tool_calls"].get(tname, 0) + 1

            elif source == "MODEL" and stype == "GENERIC":
                stats["tool_steps"] += 1

    return stats

def display_stats(stats):
    print(f"\n{BOLD}{CYAN}========================================================================={RESET}")
    print(f"{BOLD}{CYAN}          GURI - MONITOR DE TELEMETRIA DE TOKENS E CONTEXTO              {RESET}")
    print(f"{BOLD}{CYAN}========================================================================={RESET}")

    cid = stats["conversation_id"]
    print(f"{BOLD}Sessão ID:{RESET} {cid}")
    if stats["first_timestamp"] and stats["last_timestamp"]:
        print(f"{BOLD}Início:{RESET}    {stats['first_timestamp']} | {BOLD}Última Atividade:{RESET} {stats['last_timestamp']}")

    primary_model = max(stats["models"].items(), key=lambda x: x[1])[0] if stats["models"] else "desconhecido"
    capacity = MODEL_CAPACITIES.get(primary_model, DEFAULT_CAPACITY)

    # 1. ESTADO DA JANELA DE CONTEXTO ATUAL
    print(f"\n{BOLD}📊 1. JANELA DE CONTEXTO ATUAL (ÚLTIMO TURNO):{RESET}")
    if stats["last_step"]:
        ls = stats["last_step"]
        ctx_tokens = ls["context_size"]
        pct = (ctx_tokens / capacity) * 100
        bar = render_bar(pct, width=28)

        if pct < 15.0:
            status_text = f"{GREEN}🟢 ÓTIMO (Janela leve, inferência rápida){RESET}"
        elif pct < 50.0:
            status_text = f"{YELLOW}🟡 MODERADO (Uso equilibrado){RESET}"
        else:
            status_text = f"{RED}🔴 PESADO (Considere rodar /compact){RESET}"

        print(f"  Modelo:           {BOLD}{ls['model']}{RESET}")
        print(f"  Contexto Ativo:   {BOLD}{ctx_tokens:,}{RESET} / {capacity:,} tokens ({pct:.2f}%)")
        print(f"  Indicador:        [{bar}] {status_text}")
        print(f"  Distribuição:     {ls['input_tokens']:,} novos inputs + {ls['cache_read_tokens']:,} lidos do cache")
    else:
        print(f"  {DIM}Nenhum passo de inferência registrado ainda.{RESET}")

    # 2. CONSUMO ACUMULADO DA SESSÃO
    total_in = stats["total_input_tokens"]
    total_cache = stats["total_cache_tokens"]
    total_out = stats["total_output_tokens"]
    total_all = total_in + total_cache + total_out

    cache_efficiency = 0.0
    if (total_in + total_cache) > 0:
        cache_efficiency = (total_cache / (total_in + total_cache)) * 100.0

    print(f"\n{BOLD}📈 2. CONSUMO ACUMULADO NA SESSÃO:{RESET}")
    print(f"  * Tokens de Entrada Novos (Input):   {BOLD}{total_in:>12,}{RESET}")
    print(f"  * Tokens Lidos de Cache (Prompt):    {GREEN}{total_cache:>12,}{RESET}  ({cache_efficiency:.1f}% do input total)")
    print(f"  * Tokens Gerados de Saída (Output):  {BOLD}{total_out:>12,}{RESET}")
    print(f"  {DIM}{'-'*52}{RESET}")
    print(f"  * {BOLD}Total de Tokens Processados:{RESET}         {CYAN}{BOLD}{total_all:>12,}{RESET}")

    print(f"\n  {BOLD}Economia por Caching:{RESET} {GREEN}{cache_efficiency:.1f}%{RESET}")
    print(f"  {DIM}Graças ao Prompt Caching, {total_cache:,} tokens foram lidos diretamente da memória{RESET}")
    print(f"  {DIM}sem custo de inferência completa ou latência de pré-computação.{RESET}")

    # 3. INTERAÇÕES E FERRAMENTAS
    print(f"\n{BOLD}🛠️  3. ESTATÍSTICAS DE INTERAÇÃO E FERRAMENTAS:{RESET}")
    print(f"  * Mensagens do Usuário:      {stats['user_messages']}")
    print(f"  * Turnos de Resposta do IA:  {stats['model_turns']}")
    print(f"  * Passos Totais Gravados:    {stats['total_steps']}")
    if stats['errors'] > 0:
        print(f"  * Alertas / Erros de Passo:  {YELLOW}{stats['errors']}{RESET}")

    if stats["tool_calls"]:
        print(f"\n  {BOLD}Top Ferramentas Mais Utilizadas:{RESET}")
        sorted_tools = sorted(stats["tool_calls"].items(), key=lambda x: x[1], reverse=True)
        for tname, count in sorted_tools[:8]:
            print(f"    - {tname:<25}: {BOLD}{count:>3}{RESET} chamada(s)")

    # 4. RECOMENDAÇÃO OPERACIONAL
    print(f"\n{BOLD}💡 4. DIRETRIZ OPERACIONAL:{RESET}")
    if stats["last_step"] and stats["last_step"]["context_size"] > 150_000:
        print(f"  {YELLOW}Atenção:{RESET} A janela de contexto está acima de 150k tokens.")
        print(f"  Recomenda-se digitar {BOLD}/compact{RESET} no chat para resumir a sessão e otimizar tokens.")
    else:
        print(f"  {GREEN}Janela de contexto saudável.{RESET} Sessão pronta para novas tarefas de engenharia.")
    print(f"{BOLD}{CYAN}========================================================================={RESET}\n")

def main():
    parser = argparse.ArgumentParser(description="Guri - Telemetria de Tokens e Contexto")
    parser.add_argument("--id", help="ID da conversa específica (padrão: sessão mais recente)")
    parser.add_argument("--path", help="Caminho direto para o arquivo transcript.jsonl")
    args = parser.parse_args()

    tpath = find_active_transcript(explicit_id=args.id, explicit_path=args.path)
    if not tpath:
        print(f"{RED}Erro: Nenhum arquivo transcript.jsonl encontrado em ~/.gemini/antigravity-cli/brain/{RESET}")
        sys.exit(1)

    stats = analyze_transcript(tpath)
    display_stats(stats)

if __name__ == "__main__":
    main()
