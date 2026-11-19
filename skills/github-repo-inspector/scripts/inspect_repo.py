import os
import sys
import shutil
import tempfile
import subprocess

def inspect_repository(repo_url, target_dirs=None, output_file='repo_summary.md'):
    temp_dir = tempfile.mkdtemp(prefix='guri_repo_')
    print(f"[repo-inspector] Clonando superficialmente {repo_url}...")
    try:
        subprocess.check_call(['git', 'clone', '--depth', '1', repo_url, temp_dir], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        print(f"[repo-inspector] Erro ao clonar repositorio: {e}")
        shutil.rmtree(temp_dir, ignore_errors=True)
        return

    summary_lines = [f"# Resumo de Inspecao de Repositorio", f"URL: {repo_url}\n"]
    summary_lines.append("## Estrutura de Arquivos Principais\n")
    
    file_list = []
    for root, dirs, files in os.walk(temp_dir):
        if '.git' in dirs:
            dirs.remove('.git')
        for f in files:
            rel = os.path.relpath(os.path.join(root, f), temp_dir)
            if any(rel.endswith(ext) for ext in ['.h', '.hpp', '.c', '.cpp', '.py', '.md', '.ini', '.json']):
                file_list.append(rel)
                
    for f in sorted(file_list)[:40]:
        summary_lines.append(f"* `{f}`")
    if len(file_list) > 40:
        summary_lines.append(f"* ... e mais {len(file_list) - 40} arquivos.")

    summary_lines.append("\n## Trechos e Exemplos Extraidos\n")
    
    targets = [t.strip() for t in target_dirs.split(',')] if target_dirs else ['examples', 'src']
    extracted_count = 0
    for root, dirs, files in os.walk(temp_dir):
        if '.git' in dirs:
            dirs.remove('.git')
        for f in sorted(files):
            rel = os.path.relpath(os.path.join(root, f), temp_dir)
            if any(rel.lower().startswith(t.lower()) for t in targets) and any(f.endswith(ext) for ext in ['.ino', '.cpp', '.c', '.h', '.py']):
                full_f = os.path.join(root, f)
                try:
                    with open(full_f, 'r', encoding='utf-8', errors='ignore') as code_f:
                        lines = code_f.readlines()
                    header_content = ''.join(lines[:60])
                    summary_lines.append(f"### Arquivo: `{rel}`\n```cpp\n{header_content}\n```\n")
                    extracted_count += 1
                    if extracted_count >= 5:
                        break
                except Exception:
                    pass
        if extracted_count >= 5:
            break

    shutil.rmtree(temp_dir, ignore_errors=True)
    print(f"[repo-inspector] Repositorio temporario descartado com seguranca.")

    os.makedirs(os.path.dirname(os.path.abspath(output_file)), exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as out:
        out.write('\n'.join(summary_lines) + '\n')
    print(f"[repo-inspector] Relatorio salvo em: {output_file}")

if __name__ == '__main__':
    if len(sys.argv) >= 3 and sys.argv[1] == '--url':
        url = sys.argv[2]
        extract_param = sys.argv[4] if len(sys.argv) >= 5 and sys.argv[3] == '--extract' else None
        out_param = sys.argv[6] if len(sys.argv) >= 7 and sys.argv[5] == '--output' else 'repo_summary.md'
        inspect_repository(url, extract_param, out_param)
    else:
        print("Uso: python inspect_repo.py --url <github_url> [--extract 'examples,src'] [--output <arquivo.md>]")
