import os
import sys
import subprocess

def run_git(cmd):
    return subprocess.check_output(['git'] + cmd, stderr=subprocess.STDOUT).decode('utf-8').strip()

def list_worktrees():
    try:
        out = run_git(['worktree', 'list'])
        print("=== [git-worktree-helper] Worktrees Ativas ===")
        print(out)
    except Exception as e:
        print(f"Erro ao listar worktrees: {e}")

def create_worktree(name):
    clean_name = name.replace(' ', '-').lower()
    branch_name = f"spike/{clean_name}"
    target_path = os.path.abspath(os.path.join('..', f"worktree-{clean_name}"))
    
    print(f"[git-worktree-helper] Criando worktree em: {target_path} na branch {branch_name}...")
    try:
        run_git(['worktree', 'add', target_path, '-b', branch_name])
        print(f"[git-worktree-helper] Worktree criada com sucesso!")
        print(f"Para acessar o diretorio de teste: cd {target_path}")
    except Exception as e:
        print(f"Erro ao criar worktree: {e}")

def remove_worktree(name):
    clean_name = name.replace(' ', '-').lower()
    target_path = os.path.abspath(os.path.join('..', f"worktree-{clean_name}"))
    
    print(f"[git-worktree-helper] Removendo worktree em: {target_path}...")
    try:
        run_git(['worktree', 'remove', target_path, '--force'])
        print(f"[git-worktree-helper] Worktree removida com sucesso.")
    except Exception as e:
        print(f"Erro ao remover worktree: {e}")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        action = sys.argv[1]
        if action == '--list':
            list_worktrees()
        elif action == '--create' and len(sys.argv) > 2:
            create_worktree(sys.argv[2])
        elif action == '--remove' and len(sys.argv) > 2:
            remove_worktree(sys.argv[2])
        else:
            print("Uso: python worktree_helper.py [--list | --create <nome> | --remove <nome>]")
    else:
        list_worktrees()
