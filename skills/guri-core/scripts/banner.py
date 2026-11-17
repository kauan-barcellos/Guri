# -*- coding: utf-8 -*-
"""
Banner de Inicialização do Guri
"""
import sys
import random
import datetime

# Cores ANSI
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
MAGENTA = "\033[95m"
WHITE = "\033[97m"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"

FRASES = [
    "Vem devagarinho. Qual a boa de hoje?",
    "Fala comigo! Em que posso ajudar hoje?",
    "Bora resolver uns problemas?",
    "Tudo em ordem por aqui. Qual é a missão de hoje?",
    "Engenharia, código ou burocracia? Pode mandar qualquer um!"
]

def gerar_banner():
    data_hoje = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    frase_sorteada = random.choice(FRASES)
    
    art = f"""
{CYAN}{BOLD}   ______  __  ______  ____
  / ____/ / / / / __ \\/  _/   {YELLOW}{BOLD}>> GURI • A mente que pensa{RESET}
{CYAN}{BOLD} / / __  / / / / /_/ // /     {WHITE}{BOLD}>> "{frase_sorteada}"{RESET}
{CYAN}{BOLD}/ /_/ / / /_/ / _, _// /      {DIM}-------------------------------------------------{RESET}
{CYAN}{BOLD}\\____/  \\____/_/ |_/___/      {GREEN}[+] Cérebro: {BOLD}Sincronizado via GitHub (Guri){RESET}
                              {GREEN}[+] Status:  {BOLD}É só querer!{RESET}
                              {DIM}[+] Data:    {data_hoje}{RESET}
{DIM}════════════════════════════════════════════════════════════════════════════════════{RESET}
"""
    return art

def print_banner():
    print(gerar_banner())

if __name__ == "__main__":
    print_banner()
