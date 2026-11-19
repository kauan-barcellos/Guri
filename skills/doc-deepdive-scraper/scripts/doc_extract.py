import os
import sys
import re

def clean_html_to_markdown(raw_text):
    text = re.sub(r'<(script|style|nav|footer|header)[^>]*>.*?</\1>', '', raw_text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'&#?[a-zA-Z0-9]+;', ' ', text)
    lines = [line.strip() for line in text.splitlines()]
    clean_lines = [l for l in lines if l and len(l) > 3]
    return '\n'.join(clean_lines)

def extract_technical_sections(text):
    patterns = [
        r'(?i)(pin\s*configuration|pinout|pin\s*description|pin\s*assignment)',
        r'(?i)(registers|register\s*map|memory\s*map)',
        r'(?i)(quickstart|example|sample\s*code|getting\s*started)',
        r'(?i)(specifications|absolute\s*maximum\s*ratings|electrical\s*characteristics)',
        r'(?i)(api\s*reference|methods|functions)'
    ]
    
    sections = []
    lines = text.splitlines()
    capturing = False
    current_block = []
    current_title = "Secao Tecnica"
    
    for line in lines:
        matched = False
        for p in patterns:
            if re.search(p, line):
                if current_block:
                    sections.append((current_title, '\n'.join(current_block[:50])))
                    current_block = []
                current_title = line[:60]
                capturing = True
                matched = True
                break
        if capturing:
            current_block.append(line)
            if len(current_block) > 100:
                capturing = False
                sections.append((current_title, '\n'.join(current_block)))
                current_block = []
                
    if current_block:
        sections.append((current_title, '\n'.join(current_block[:50])))
        
    return sections

def process_document(input_path, output_path):
    if not os.path.exists(input_path):
        print(f"[doc-extract] Arquivo nao encontrado: {input_path}")
        return
    with open(input_path, 'r', encoding='utf-8', errors='ignore') as f:
        raw = f.read()
    
    cleaned = clean_html_to_markdown(raw)
    sections = extract_technical_sections(cleaned)
    
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f"# Resumo Tecnico Destilado\nFonte: {os.path.basename(input_path)}\n\n")
        if sections:
            for title, content in sections:
                f.write(f"## {title}\n\n```text\n{content}\n```\n\n")
        else:
            f.write("## Conteudo Filtrado\n\n```text\n" + cleaned[:3000] + "\n```\n")
            
    print(f"[doc-extract] Documentacao condensada salva em: {output_path}")

if __name__ == '__main__':
    if len(sys.argv) >= 3 and sys.argv[1] == '--input':
        inp = sys.argv[2]
        out = sys.argv[4] if len(sys.argv) >= 5 and sys.argv[3] == '--output' else 'extracted_doc.md'
        process_document(inp, out)
    else:
        print("Uso: python doc_extract.py --input <arquivo> --output <destino.md>")
