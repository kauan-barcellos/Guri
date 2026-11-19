import os
import sys
import subprocess
from datetime import datetime

def get_git_info():
    info = {'branch': 'N/A', 'commit': 'N/A', 'modified': []}
    try:
        branch = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], stderr=subprocess.DEVNULL).decode('utf-8').strip()
        info['branch'] = branch
    except Exception:
        pass
    try:
        commit = subprocess.check_output(['git', 'log', '-1', '--oneline'], stderr=subprocess.DEVNULL).decode('utf-8').strip()
        info['commit'] = commit
    except Exception:
        pass
    try:
        status = subprocess.check_output(['git', 'status', '--short'], stderr=subprocess.DEVNULL).decode('utf-8').strip()
        if status:
            info['modified'] = [line.strip() for line in status.splitlines()]
    except Exception:
        pass
    return info

def generate_handoff(target_dir='.'):
    context_dir = os.path.join(target_dir, '.context')
    os.makedirs(context_dir, exist_ok=True)
    handoff_path = os.path.join(context_dir, 'handoff.md')
    git_info = get_git_info()
    now_str = datetime.now().strftime('%Y-%m-%d %H:%M')
    
    modified_text = '\n'.join(['* `' + m + '`' for m in git_info['modified']]) if git_info['modified'] else '* Nenhum arquivo pendente de commit'
    
    content = f'''# Session Handoff

## 1. Metadados da Sessao
* Data/Hora: {now_str}
* Branch Git: {git_info['branch']}
* Ultimo Commit: {git_info['commit']}

## 2. O que foi Concluido
* [ ] Preencher com as tarefas fechadas nesta sessao

## 3. Estado Atual e Variaveis Criticas
* Arquivos em alteracao:
{modified_text}
* Parametros de hardware ou firmware:

## 4. Bloqueios e Questoes Pendentes
* Nao ha bloqueios criticos no momento

## 5. Proximo Passo Imediato
* [ ] Primeira acao concreta para retomar o fluxo
'''
    with open(handoff_path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')
    print(f'[session-handoff] Handoff criado/atualizado em: {handoff_path}')

def read_handoff(target_dir='.'):
    handoff_path = os.path.join(target_dir, '.context', 'handoff.md')
    if not os.path.exists(handoff_path):
        print('[session-handoff] Nenhum handoff encontrado em .context/handoff.md')
        return
    with open(handoff_path, 'r', encoding='utf-8') as f:
        print(f.read())

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--read':
        read_handoff()
    else:
        generate_handoff()
