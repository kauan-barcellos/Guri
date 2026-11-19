import os
import sys
import re
import json
import argparse
import urllib.request
import urllib.parse
import http.cookiejar
from datetime import datetime, date, timedelta

# Cores ANSI para saida limpa no terminal
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"

STANDARD_DAILY_HOURS = 8.5

def load_env(env_path=None):
    candidates = []
    if env_path:
        candidates.append(env_path)
    else:
        candidates.extend([
            os.path.join(os.getcwd(), ".env"),
            os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"),
            os.path.expanduser("~/.gemini/.osis_env")
        ])
    env = {}
    for p in candidates:
        if os.path.exists(p):
            with open(p, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        env[k.strip()] = v.strip().strip('"').strip("'")
            break
    # Variaveis de ambiente tem precedencia
    for k in ("OSIS_URL", "OSIS_USER", "OSIS_PASS"):
        if k in os.environ:
            env[k] = os.environ[k]
    return env

class OsisClient:
    def __init__(self, base_url, user, password):
        self.base_url = base_url.rstrip("/")
        self.user = user
        self.password = password
        self.cookie_jar = http.cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cookie_jar))
        self.authenticated = False

    def login(self):
        login_url = f"{self.base_url}/login"
        payload = {"user": self.user, "password": self.password}
        data = urllib.parse.urlencode(payload).encode("utf-8")
        req = urllib.request.Request(login_url, data=data, method="POST")
        req.add_header("Content-Type", "application/x-www-form-urlencoded")
        try:
            with self.opener.open(req, timeout=8) as resp:
                html = resp.read().decode("utf-8", errors="ignore")
                if "Usuário ou senha incorretos" in html:
                    raise Exception("Credenciais rejeitadas pelo servidor.")
                self.authenticated = True
                return True
        except Exception as e:
            raise Exception(f"Falha de conexao com {login_url}: {e}")

    def get_all_user_activities(self):
        """Retorna todas as atividades do usuario, inclusive as que tem registros em aberto ou recentes."""
        if not self.authenticated:
            self.login()
        url = f"{self.base_url}/get-partial-report-page"
        req = urllib.request.Request(url)
        with self.opener.open(req, timeout=10) as resp:
            html = resp.read().decode("utf-8", errors="ignore")

        osi_blocks = re.split(r'<h3[^>]*>', html)
        activities = []
        for block in osi_blocks[1:]:
            header_part = block.split("</h3>")[0]
            osi_title = re.sub(r'<[^>]+>', '', header_part).strip()
            act_links = re.findall(r'/get-this-osi-activities/(\d+)', block)
            for aid in act_links:
                act_data = self.get_activity_details(aid, osi_title)
                if act_data:
                    activities.append(act_data)
        return activities

    def get_activity_details(self, act_id, osi_title=""):
        url = f"{self.base_url}/get-this-osi-activities/{act_id}"
        with self.opener.open(url, timeout=10) as resp:
            html = resp.read().decode("utf-8", errors="ignore")

        act_info_m = re.search(r'activityInfo\s*=\s*JSON\.parse\(\'(.*?)\'\)', html)
        act_name = "N/A"
        designated = 0.0
        spent = 0.0
        desc = ""
        osi_id = ""
        if act_info_m:
            try:
                aj = json.loads(act_info_m.group(1))
                act_name = aj.get("name", "N/A")
                designated = float(aj.get("designated_hours") or 0.0)
                spent = float(aj.get("spent_hours") or 0.0)
                desc = aj.get("description", "")
                osi_id = str(aj.get("id_osi") or aj.get("id_osis") or "")
            except Exception:
                pass

        daily_logs = []
        tables = re.findall(r'<table[^>]*>(.*?)</table>', html, re.DOTALL | re.IGNORECASE)
        if len(tables) >= 2:
            t1_rows = re.findall(r'<tr[^>]*>(.*?)</tr>', tables[1], re.DOTALL | re.IGNORECASE)
            for r in t1_rows[1:]:
                cells = [re.sub(r'<[^>]+>', '', c).strip() for c in re.findall(r'<t[dh][^>]*>(.*?)</t[dh]>', r, re.DOTALL | re.IGNORECASE)]
                if len(cells) >= 2 and cells[0] and cells[1]:
                    try:
                        h = float(cells[1].replace(",", "."))
                        daily_logs.append({"data": cells[0], "horas": h})
                    except ValueError:
                        pass

        saldo = max(0.0, designated - spent) if designated > 0 else 0.0
        return {
            "id": act_id,
            "osi_id": osi_id,
            "osi_title": osi_title,
            "name": act_name,
            "description": desc,
            "designated": designated,
            "spent": spent,
            "balance": saldo,
            "daily_logs": daily_logs
        }

    def get_weekly_summary(self):
        if not self.authenticated:
            self.login()
        url = f"{self.base_url}/dashboard-executor"
        with self.opener.open(url, timeout=10) as resp:
            html = resp.read().decode("utf-8", errors="ignore")

        m = re.search(r'const\s+activitiesInfo\s*=\s*JSON\.parse\(\'(.*?)\'\)', html)
        if m:
            try:
                return json.loads(m.group(1))
            except Exception:
                pass
        return []

    def report_hours(self, act_id, hours, date_str=None):
        if not self.authenticated:
            self.login()
        if not date_str:
            date_str = date.today().strftime("%Y-%m-%d")
        
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        dt_utc = datetime(dt.year, dt.month, dt.day, 6, 0, 0)
        ts_ms = int(dt_utc.timestamp() * 1000)

        url = f"{self.base_url}/add-report/{act_id}"
        boundary = "----GuriFormBoundary7MA4YWxkTrZu0gW"
        
        body_parts = [
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="reported_date"\r\n\r\n'
            f"{ts_ms}\r\n",
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="total_hours"\r\n\r\n'
            f"{hours}\r\n",
            f"--{boundary}--\r\n"
        ]
        body = "".join(body_parts).encode("utf-8")

        req = urllib.request.Request(url, data=body, method="POST")
        req.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")

        try:
            with self.opener.open(req, timeout=10) as resp:
                res_data = resp.read().decode("utf-8", errors="ignore")
                try:
                    res_json = json.loads(res_data)
                    if res_json.get("error") == 1:
                        raise Exception("Servidor retornou erro ao adicionar registro.")
                except Exception:
                    pass
            return True, f"Sucesso: {hours} horas reportadas em {date_str} na atividade {act_id}."
        except Exception as e:
            return False, f"Falha ao reportar: {e}"

def display_status(client):
    today = date.today()
    print(f"\n{BOLD}{CYAN}========================================================================={RESET}")
    print(f"{BOLD}{CYAN}          GURI - PAINEL DE GESTAO DE HORAS E APONTAMENTOS (OSIs)         {RESET}")
    print(f"{BOLD}{CYAN}========================================================================={RESET}")
    print(f"{BOLD}Data de Hoje:{RESET} {today.strftime('%d/%m/%Y (%A)')} | {BOLD}Usuario:{RESET} {client.user}\n")

    print(f"{YELLOW}[1/2] Sincronizando dados com o servidor...{RESET}")
    activities = client.get_all_user_activities()
    weekly = client.get_weekly_summary()

    # Consolidar todos os registros do mes corrente
    current_month_prefix = today.strftime("%Y-%m")
    all_month_logs = []
    for act in activities:
        for log in act["daily_logs"]:
            if log["data"].startswith(current_month_prefix):
                all_month_logs.append({
                    "data": log["data"],
                    "horas": log["horas"],
                    "act_id": act["id"],
                    "act_name": act["name"],
                    "osi_title": act["osi_title"],
                    "osi_id": act["osi_id"]
                })

    # Mapa de horas por dia no mes
    daily_totals_month = {}
    for l in all_month_logs:
        d = l["data"]
        daily_totals_month[d] = daily_totals_month.get(d, 0.0) + l["horas"]

    # -------------------------------------------------------------------------
    # 1. DISCRIMINACAO DA SEMANA VIGENTE (Segunda a Sexta)
    # -------------------------------------------------------------------------
    start_of_week = today - timedelta(days=today.weekday())  # Segunda-feira
    print(f"\n{BOLD}{GREEN}📍 DISCRIMINACAO DETALHADA DA SEMANA VIGENTE ({start_of_week.strftime('%d/%m')} a {(start_of_week + timedelta(days=4)).strftime('%d/%m')}):{RESET}")
    print(f"{'Dia':<12} | {'Horas':<7} | {'Atividade / OSI':<50}")
    print("-" * 75)

    week_total = 0.0
    for offset in range(5):  # Seg a Sex
        cur_day = start_of_week + timedelta(days=offset)
        cur_day_str = cur_day.strftime("%Y-%m-%d")
        day_label = cur_day.strftime("%d/%m (%a)")

        # Itens lançados neste dia
        day_items = [l for l in all_month_logs if l["data"] == cur_day_str]
        day_total = sum(item["horas"] for item in day_items)
        week_total += day_total

        if not day_items:
            if cur_day == today:
                status_text = f"{YELLOW}⏳  0.0h (Pendente para o fim do dia){RESET}"
            elif cur_day > today:
                status_text = f"{DIM}⏳  0.0h (Dia futuro){RESET}"
            else:
                status_text = f"{RED}❌  0.0h (NENHUM REGISTRO LANÇADO){RESET}"
            print(f"{BOLD}{day_label:<12}{RESET} | {status_text}")
        else:
            for idx, item in enumerate(day_items):
                osi_clean = item["osi_title"].split(" - ")[0] if " - " in item["osi_title"] else item["osi_title"]
                detail_str = f"{item['act_name']} ({osi_clean})"
                if idx == 0:
                    status_icon = "✅" if day_total >= STANDARD_DAILY_HOURS else "⚠️ "
                    print(f"{BOLD}{day_label:<12}{RESET} | {GREEN}{item['horas']:4.1f}h{RESET}   | {detail_str}")
                else:
                    print(f"{'':<12} | {GREEN}{item['horas']:4.1f}h{RESET}   | {detail_str}")
            if len(day_items) > 1 or day_total != STANDARD_DAILY_HOURS:
                comp_color = GREEN if day_total >= STANDARD_DAILY_HOURS else YELLOW
                print(f"{DIM}{'':<12} └─ Total do dia: {comp_color}{day_total:.1f}h / {STANDARD_DAILY_HOURS}h{RESET}")
        print(f"{DIM}{'-' * 75}{RESET}")

    print(f"{BOLD}Total apontado na semana vigente:{RESET} {BOLD}{GREEN}{week_total:.1f} horas{RESET} (Meta semanal: 42.5h)\n")

    # -------------------------------------------------------------------------
    # 2. AUDITORIA DE DIAS COM HORAS PENDENTES OU INCOMPLETAS NO MES
    # -------------------------------------------------------------------------
    print(f"{BOLD}{YELLOW}⚠️  DIAS COM HORAS PENDENTES OU INCOMPLETAS NO MES ({today.strftime('%B/%Y').upper()}):{RESET}")
    print(f"{'Data':<12} | {'Apontado':<9} | {'Faltam':<8} | {'Situacao'}")
    print("-" * 65)

    first_day_of_month = date(today.year, today.month, 1)
    missing_days_count = 0
    total_missing_hours = 0.0

    day_cursor = first_day_of_month
    while day_cursor <= today:
        # Pular finais de semana
        if day_cursor.weekday() < 5:
            d_str = day_cursor.strftime("%Y-%m-%d")
            h_logged = daily_totals_month.get(d_str, 0.0)
            day_fmt = day_cursor.strftime("%d/%m (%a)")

            if h_logged < STANDARD_DAILY_HOURS:
                diff = STANDARD_DAILY_HOURS - h_logged
                total_missing_hours += diff
                missing_days_count += 1

                if day_cursor == today:
                    sit = f"{YELLOW}Hoje - Reportar ao fim do dia{RESET}"
                elif h_logged == 0.0:
                    sit = f"{RED}{BOLD}Dia util zerado (Sem lancamento){RESET}"
                else:
                    sit = f"{YELLOW}Lancamento parcial (Incompleto){RESET}"

                print(f"{day_fmt:<12} | {h_logged:4.1f}h     | {RED}-{diff:3.1f}h{RESET}   | {sit}")
        day_cursor += timedelta(days=1)

    if missing_days_count == 0:
        print(f"{GREEN}Parabéns! Todos os dias úteis do mês até agora estão com a meta diária de {STANDARD_DAILY_HOURS}h 100% cumprida.{RESET}")
    else:
        print("-" * 65)
        print(f"{BOLD}Total de dias com pendencias:{RESET} {missing_days_count} dia(s) | {BOLD}Deficit total acumulado:{RESET} {RED}-{total_missing_hours:.1f}h{RESET}")

    # -------------------------------------------------------------------------
    # 3. ATIVIDADES DISPONIVEIS PARA APONTAMENTO IMEDIATO
    # -------------------------------------------------------------------------
    print(f"\n{BOLD}🎯 ONDE APONTAR AS HORAS FALTANTES (ATIVIDADES COM SALDO):{RESET}")
    for act in activities:
        if act["balance"] > 0:
            osi_clean = act["osi_title"].split(" - ")[0] if " - " in act["osi_title"] else act["osi_title"]
            print(f"  * {BOLD}ID {act['id']}{RESET}: {act['name']} [{osi_clean}] - Saldo restante: {GREEN}{act['balance']:.1f}h{RESET}")

    print(f"\n{DIM}Para lancar horas faltantes, use:{RESET}")
    print(f"  {CYAN}guri-horas --report --act <ID> --hours <H> [--date YYYY-MM-DD]{RESET}\n")

def main():
    parser = argparse.ArgumentParser(description="Guri - Gestao e Acompanhamento de Horas (OSIs)")
    parser.add_argument("--status", action="store_true", help="Exibe o painel de status completo")
    parser.add_argument("--weekly", action="store_true", help="Exibe o historico semanal do dashboard")
    parser.add_argument("--report", action="store_true", help="Reporta horas em uma atividade")
    parser.add_argument("--act", help="ID da atividade (ex: 93310)")
    parser.add_argument("--hours", type=float, help="Quantidade de horas trabalhadas (ex: 8.5)")
    parser.add_argument("--date", help="Data do apontamento no formato YYYY-MM-DD (padrao: hoje)")
    args = parser.parse_args()

    env = load_env()
    base_url = env.get("OSIS_URL", "http://10.1.1.82:1005")
    user = env.get("OSIS_USER")
    pwd = env.get("OSIS_PASS")

    if not user or not pwd:
        print(f"{RED}Erro: Credenciais OSIS_USER e OSIS_PASS nao configuradas no .env ou ambiente.{RESET}")
        sys.exit(1)

    client = OsisClient(base_url, user, pwd)

    if args.report:
        if not args.act or not args.hours:
            print(f"{RED}Erro: Para reportar e necessario informar --act <ID> e --hours <NUMERO>{RESET}")
            sys.exit(1)
        ok, msg = client.report_hours(args.act, args.hours, args.date)
        if ok:
            print(f"{GREEN}{BOLD}{msg}{RESET}")
        else:
            print(f"{RED}{BOLD}{msg}{RESET}")
    elif args.weekly:
        w_list = client.get_weekly_summary()
        print(f"\n{BOLD}=== HISTORICO SEMANAL DE HORAS (DASHBOARD) ==={RESET}")
        for w in w_list[:8]:
            print(f"  {w.get('startDate', 'Semana')}: {w.get('totalHours', 0):4.1f}h (Inicio: {w.get('start')})")
    else:
        display_status(client)

if __name__ == "__main__":
    main()
