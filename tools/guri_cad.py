#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
guri_cad.py - Cliente e orquestrador de modelagem 3D do Guri para o FreeCAD.
Suporta streaming passo a passo para visualizacao ao vivo (GUI) ou compilacao headless (FreeCADCmd).
"""

import sys
import os
import json
import time
import argparse
import subprocess
import xmlrpc.client

DEFAULT_RPC_URL = "http://127.0.0.1:9875"
FREECAD_CMD_PATH = r"C:\Program Files\FreeCAD 1.1\bin\FreeCADCmd.exe"


class GuriCadClient:
    def __init__(self, rpc_url: str = DEFAULT_RPC_URL):
        self.rpc_url = rpc_url
        self.server = xmlrpc.client.ServerProxy(self.rpc_url)

    def is_connected(self) -> bool:
        """Verifica se o servidor RPC do FreeCAD MCP esta ativo."""
        try:
            self.server.list_documents()
            return True
        except Exception:
            return False

    def send_command(self, code: str, description: str = "", fit_view: bool = True) -> dict:
        """Envia codigo Python diretamente para a thread de interface do FreeCAD."""
        full_code = code
        if fit_view:
            full_code += """
try:
    import FreeCADGui
    if FreeCADGui.activeDocument() and FreeCADGui.activeDocument().activeView():
        FreeCADGui.activeDocument().activeView().fitAll()
except Exception:
    pass
"""
        try:
            res = self.server.execute_code(full_code)
            return res
        except Exception as e:
            return {"success": False, "error": str(e)}

    def run_steps(self, steps: list, default_delay: float = 1.5, doc_name: str = "Projeto"):
        """
        Executa uma sequencia de passos no FreeCAD.
        Se a GUI estiver aberta, envia passo a passo via RPC com pausa visual.
        Se a GUI estiver fechada, executa em lote via FreeCADCmd.
        """
        connected = self.is_connected()

        if connected:
            print(f"[GuriCAD] Conectado ao FreeCAD MCP em {self.rpc_url}!")
            print(f"[GuriCAD] Iniciando construcao ao vivo de '{doc_name}' com {len(steps)} etapas...\n")

            total = len(steps)
            for idx, step in enumerate(steps, 1):
                name = step.get("name", f"etapa_{idx}")
                desc = step.get("desc", f"Construindo {name}")
                code = step.get("code", "")
                delay = step.get("delay", default_delay)

                print(f"[{idx}/{total}] -> {desc} (peca: '{name}')")
                res = self.send_command(code, description=f"[{idx}/{total}] {desc}")

                if not res.get("success", False):
                    print(f"[ERRO] Falha na etapa '{name}': {res.get('error') or res.get('message')}")
                    return False

                if idx < total and delay > 0:
                    time.sleep(delay)

            print(f"\n[GuriCAD] Construcao concluida com sucesso na tela do FreeCAD!")
            return True
        else:
            print(f"[GuriCAD] FreeCAD GUI nao detectado. Compilando em modo headless (FreeCADCmd)...")
            combined_code = "\n".join([step.get("code", "") for step in steps])
            temp_script = os.path.abspath("temp_build.py")
            with open(temp_script, "w", encoding="utf-8") as f:
                f.write(combined_code)

            try:
                proc = subprocess.run([FREECAD_CMD_PATH, temp_script], capture_output=True, text=True)
                if proc.stdout:
                    print(proc.stdout)
                if proc.stderr:
                    print(proc.stderr)
                has_error = (
                    "Traceback" in proc.stdout
                    or "Traceback" in proc.stderr
                    or "Exception while processing file" in proc.stdout
                    or "Exception while processing file" in proc.stderr
                    or proc.returncode != 0
                )
                if has_error:
                    print("[ERRO] Falha na execucao do script no FreeCADCmd.")
                    return False
                print("[GuriCAD] Modelo gerado com sucesso via FreeCADCmd!")
                return True
            finally:
                if os.path.exists(temp_script):
                    os.remove(temp_script)


def main():
    parser = argparse.ArgumentParser(description="Guri CAD CLI")
    parser.add_argument("command", choices=["status", "ping"], help="Comando a executar")
    args = parser.parse_args()

    client = GuriCadClient()
    if args.command in ["status", "ping"]:
        if client.is_connected():
            print(f"[OK] FreeCAD conectado e pronto para modelagem ao vivo em {DEFAULT_RPC_URL}.")
            sys.exit(0)
        else:
            print(f"[INFO] FreeCAD nao esta aberto ou servidor RPC nao esta respondendo em {DEFAULT_RPC_URL}.")
            sys.exit(1)


if __name__ == "__main__":
    main()
