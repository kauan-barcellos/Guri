import os
import sys
import shutil

TRASH_EXTENSIONS = [
    '.pyc', '.pyo', '.tmp', '.log', '.dmp', '.bak',
    '.kicad_pcb-bak', '.kicad_sch-bak', '.autosave'
]

TRASH_DIRS = [
    '__pycache__', '.pytest_cache'
]

TRASH_EXACT_FILES = [
    'Thumbs.db', '.DS_Store', 'desktop.ini'
]

def scan_workspace(root_dir='.'):
    found_files = []
    found_dirs = []
    total_bytes = 0

    for current_root, dirs, files in os.walk(root_dir):
        if '.git' in dirs:
            dirs.remove('.git')
        
        for d in list(dirs):
            if d in TRASH_DIRS:
                d_path = os.path.join(current_root, d)
                found_dirs.append(d_path)
                dirs.remove(d)

        for f in files:
            is_trash = False
            if f in TRASH_EXACT_FILES:
                is_trash = True
            elif any(f.endswith(ext) for ext in TRASH_EXTENSIONS):
                is_trash = True

            if is_trash:
                f_path = os.path.join(current_root, f)
                try:
                    size = os.path.getsize(f_path)
                    total_bytes += size
                except Exception:
                    size = 0
                found_files.append((f_path, size))

    return found_files, found_dirs, total_bytes

def report_scan(found_files, found_dirs, total_bytes):
    print("=== [workspace-janitor] Relatorio de Varredura ===")
    print(f"Diretorios de cache encontrados: {len(found_dirs)}")
    for d in found_dirs:
        print(f"  [DIR]  {d}")
    print(f"Arquivos temporarios/backup encontrados: {len(found_files)}")
    for f, sz in found_files[:30]:
        print(f"  [FILE] {f} ({sz} bytes)")
    if len(found_files) > 30:
        print(f"  ... e mais {len(found_files) - 30} arquivos.")
    print(f"Espaco total passivel de limpeza: {total_bytes / 1024:.2f} KB")

def clean_workspace(root_dir='.'):
    found_files, found_dirs, total_bytes = scan_workspace(root_dir)
    report_scan(found_files, found_dirs, total_bytes)
    
    if not found_files and not found_dirs:
        print("[workspace-janitor] Workspace ja esta completamente limpo.")
        return

    print("\nRemovendo arquivos...")
    for f, _ in found_files:
        try:
            os.remove(f)
        except Exception as e:
            print(f"Erro ao remover {f}: {e}")

    for d in found_dirs:
        try:
            shutil.rmtree(d, ignore_errors=True)
        except Exception as e:
            print(f"Erro ao remover diretorio {d}: {e}")

    print("[workspace-janitor] Limpeza concluida com sucesso.")

if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else '--scan'
    if mode == '--clean':
        clean_workspace()
    else:
        files, dirs, b = scan_workspace()
        report_scan(files, dirs, b)
        print("\nPara executar a remocao, utilize: python janitor.py --clean")
