#!/usr/bin/env python3
"""Validador das regras anti-IA da skill seu-tom-de-voz.

Uso:
  python3 validar_texto.py <arquivo> [novo|revisao|critica] [--canal CANAL]
                           [--original ARQ] [--permite travessao,hashtag,emoji] [--json]

Modos:
  novo     texto criado pelo Claude: o que acusar é do Claude.
  revisao  texto que partiu de rascunho de quem assina. Com --original, cada ocorrência
           sai como PRESERVADO (estava no rascunho dele, fica) ou como adição do Claude.
           Sem --original, os grupos de autoria viram VERIFICAR AUTORIA.
  critica  avaliação pedida: tudo vira DIAGNÓSTICO e nada bloqueia.

Canais: linkedin (padrão), artigo, email, interno, imprensa, bio, palestra, roteiro, instagram.
--permite libera o que o perfil de voz de quem assina liberar explicitamente.

Saída: 0 sem bloqueio, 1 com bloqueio, 2 entrada inválida. Resultado limpo não certifica
voz nem fato: o script procura padrões; a construção do argumento só se confere lendo.
Usa apenas a biblioteca padrão do Python 3.
"""
from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

CANAIS = ("linkedin", "artigo", "email", "interno", "imprensa", "bio", "palestra", "roteiro", "instagram")
MODOS = ("novo", "revisao", "critica")
LIBERAVEIS = ("travessao", "hashtag", "emoji")
EMOJI = "[\U0001F300-\U0001FAFF\u2600-\u27BF]"


@dataclass(frozen=True)
class Regra:
    codigo: str
    nome: str
    padrao: str
    nivel: str          # bloqueio | autoria | aviso
    canais: tuple = ()  # vazio = todos
    exceto: tuple = ()
    liberavel: str = ""  # nome usado em --permite
    flags: int = re.I | re.M


REGRAS = [
    # Bloqueia em qualquer modo (salvo liberação do perfil)
    Regra("travessao", "Travessão (regra 1): trocar por vírgula, ponto, dois-pontos ou parênteses", "\u2014|\u2013", "bloqueio", liberavel="travessao", flags=re.M),
    # Bloqueia em modo novo; em revisão depende de quem escreveu
    Regra("oposicao_correlativa", 'Oposição correlativa "não é X, é Y" (regra 2): afirmar só a metade que importa',
          r"não é (?:sobre )?[^.;!?\n]{1,60}?[,.] (?:é|e sim|mas)(?: |$)|não se trata de|não [^.;!?,\n]{1,40}?, (?:mas sim|e sim)(?: |$)", "autoria"),
    Regra("nao_so_mas_tambem", 'Molde "não só X, mas também Y" (regra 2)', r"não (?:só|apenas|somente) [^.;!?\n]{3,60}?(?:mas|como) também", "autoria"),
    Regra("cliches", "Clichê corporativo (regra 8)",
          r"game.?changer|divisor de águas|revolucionári|disruptiv|virada de chave|\brobust|alavanc|potencializ|sinergia|mudança de paradigma|no mundo (?:de hoje|atual)|no cenário atual|vale (?:ressaltar|destacar)|fazer a diferença|zona de conforto|\bjornada\b", "autoria"),
    Regra("abertura_cerimonial", 'Abertura cerimonial (regra 9): o fato entra na primeira linha',
          r"é com (?:grande |imensa |muita )?(?:satisfação|alegria|orgulho|prazer)|tenho o (?:prazer|orgulho) de|(?:estou|fico) honrad[oa]|hoje (?:eu )?quero (?:falar|compartilhar)", "autoria"),
    Regra("tropo_autoridade", 'Tropo de autoridade (regra 12): "a verdade é que", "no fim do dia", "o que realmente importa"',
          r"a verdade é que|no fim do dia|no final do dia|o que realmente importa|a questão de fundo|em essência|o cerne da questão|o ponto central é", "autoria"),
    # Avisos (revisar à mão)
    Regra("hashtag", "Hashtag fora do Instagram: nenhuma ou até três, específicas, no fim", r"(?:^|(?<=\s))#\w", "aviso", exceto=("instagram",), liberavel="hashtag"),
    Regra("emoji", "Emoji: zero em texto de opinião ou posicionamento (Instagram aceita até três, com função)", EMOJI, "aviso", exceto=("instagram",), liberavel="emoji", flags=re.M),
    Regra("frase_cortina", "Frase-cortina antes do dado (regra 10): abrir pela fonte",
          r"os números não mentem|os dados (?:comprovam|não mentem|mostram claramente)|o mercado já (?:percebeu|entendeu|acordou)", "aviso"),
    Regra("suspense", 'Suspense de dois-pontos (regra 11): nomear direto',
          r"quase ninguém (?:vê|enxerga|percebe|sabe|fala)|o que poucos sabem|pouca gente sabe|o detalhe que (?:ninguém|muda)", "aviso"),
    Regra("inflacao", "Inflação de importância (regra 13)",
          r"marca um momento|consolida (?:sua|nossa|a) posiç|se consolida como|reflete uma tendência|abre caminho para|pavimenta o caminho|cenário em transformação|reafirma (?:seu|nosso|o) compromisso|reafirmando (?:seu|nosso|o) compromisso|deixa uma marca", "aviso"),
    Regra("perifrase", 'Perífrase do verbo ser (regra 14): trocar por é, tem, faz',
          r"se (?:configura|apresenta|posiciona|caracteriza|constitui) como|figura como|constitui-se|\bconta com\b|dispõe de", "aviso"),
    Regra("muleta", "Muleta de preenchimento (regra 15)",
          r"com o objetivo de|devido ao fato de|é importante (?:notar|ressaltar|dizer|destacar)|no sentido de|de modo a\b|tem a capacidade de|neste momento", "aviso"),
    Regra("cauda_gerundio", "Cauda de gerúndio (regra 7): vira frase própria com sujeito ou sai",
          r",\s+(?:destacando|ressaltando|evidenciando|garantindo|refletindo|contribuindo|consolidando|reforçando|demonstrando|permitindo|possibilitando|promovendo|fomentando|impulsionando|ampliando|fortalecendo|simbolizando|marcando|pavimentando|reafirmando|sinalizando|potencializando|otimizando|assegurando)\b", "aviso"),
    Regra("passiva", "Passiva escondendo o dono (regra 17): nomear quem fez",
          r"\b(?:foi|foram) (?:implementad|conduzid|realizad|desenvolvid|criad|estabelecid|utilizad|adotad|tomad|construíd)|\b(?:é|são) (?:preservad|realizad|considerad|mantid|gerenciad)|não é necessário", "aviso", exceto=("imprensa",)),
    Regra("placa_contraste", 'Parágrafo aberto com "Só que" / "Acontece que" / "O problema é que" (regra 18)', r"^(?:Só que|Acontece que|O problema é que)", "aviso", flags=re.M),
    Regra("negativa_cauda", 'Negativa de cauda (regra 19): ", sem enrolação", ", sem achismo"',
          r",\s*sem (?:achismo|mágica|magia|enrolação|drama|frescura|rodeios)[.!?]?\s*$", "aviso"),
    Regra("observacao_generica", 'Observação genérica de consultor (regra 21): trocar por cena real ou fenômeno nomeado',
          r"percebo que|percebi que|tenho notado|venho notando|venho percebendo|converso com muitos", "aviso"),
    Regra("triade", "Possível tríade (regra 3): conferir se a enumeração existia no original", r"\b\w{4,}, \w{4,} e \w{4,}\b", "aviso"),
    Regra("formatacao", "Negrito ou título de markdown: não renderiza ou não combina com o canal", r"\*\*|^#{1,3} ", "aviso", canais=("linkedin", "email", "instagram", "interno")),
    Regra("bullet", 'Bullet "•": usar lista numerada, e só para conteúdo de fato enumerável', r"^\s*•", "aviso"),
    Regra("voces", '"vocês" em post: o padrão é falar com uma pessoa ("você"), salvo plateia ou time', r"\bvocês\b", "aviso", canais=("linkedin", "instagram")),
    Regra("isca_comentario", '"Comente X" ou "comente aqui" para alcance: no LinkedIn, trocar por pergunta genuína',
          r"\bcoment[ea]m?\s+(?:aqui|abaixo|[\"“']?[A-ZÀ-Ý]{3,})", "aviso", canais=("linkedin",), flags=re.M),
    Regra("link_instagram", "Link no corpo do Instagram: não vira clique; destino na bio ou por mensagem direta", r"https?://\S+|\bwww\.\S+", "aviso", canais=("instagram",)),
]


@dataclass
class Achado:
    codigo: str
    nivel: str   # bloqueio | aviso | diagnostico | preservado | verificar_autoria
    mensagem: str
    linhas: list = field(default_factory=list)


def _linha(texto: str, inicio: int) -> tuple[int, str]:
    n = texto.count("\n", 0, inicio) + 1
    a = texto.rfind("\n", 0, inicio) + 1
    b = texto.find("\n", inicio)
    return n, texto[a:(b if b >= 0 else len(texto))].strip()[:200]


def _blocos(original: str, texto: str):
    sm = difflib.SequenceMatcher(None, original, texto, autojunk=False)
    return [(m.b, m.b + m.size) for m in sm.get_matching_blocks() if m.size >= 15]


def validar(texto: str, modo: str = "novo", canal: str = "linkedin", original: str | None = None, permite: set | None = None) -> list[Achado]:
    permite = permite or set()
    blocos = _blocos(original, texto) if original is not None else None
    pres = lambda i, f: blocos is not None and any(a <= i and f <= b for a, b in blocos)
    achados: list[Achado] = []

    for r in REGRAS:
        if (r.canais and canal not in r.canais) or canal in r.exceto or (r.liberavel and r.liberavel in permite):
            continue
        occ = [(m.start(), m.end()) for m in re.finditer(r.padrao, texto, r.flags)]
        if not occ:
            continue
        lin = lambda oc: [_linha(texto, i) for i, _ in oc]
        if modo == "critica":
            achados.append(Achado(r.codigo, "diagnostico", r.nome, lin(occ)))
        elif r.nivel == "bloqueio" or (modo == "novo" and r.nivel == "autoria"):
            achados.append(Achado(r.codigo, "bloqueio", r.nome, lin(occ)))
        elif r.nivel == "aviso":
            achados.append(Achado(r.codigo, "aviso", r.nome, lin(occ)))
        elif blocos is None:
            achados.append(Achado(r.codigo, "verificar_autoria", r.nome, lin(occ)))
        else:
            p = [o for o in occ if pres(*o)]
            a = [o for o in occ if not pres(*o)]
            if p:
                achados.append(Achado(r.codigo, "preservado", r.nome, lin(p)))
            if a:
                achados.append(Achado(r.codigo, "bloqueio", r.nome, lin(a)))

    def contagem(codigo, padrao, limite, msg):
        occ = [m.start() for m in re.finditer(padrao, texto, re.I)]
        if len(occ) > limite:
            achados.append(Achado(codigo, "diagnostico" if modo == "critica" else "aviso", msg.format(n=len(occ)), [_linha(texto, i) for i in occ[:6]]))

    contagem("adverbios", r"\b(?:justamente|exatamente|realmente|extremamente|fundamental|essencial)\b", 1,
             "Advérbios e adjetivos de ênfase aparecem {n} vezes (regra 20: no máximo um por texto)")
    contagem("exclamacao", r"!", 3, "Exclamação aparece {n} vezes: conferir com o perfil de voz")

    if modo in ("revisao", "critica"):
        contraste = "|".join(r.padrao for r in REGRAS if r.codigo in ("oposicao_correlativa", "nao_so_mas_tambem"))
        occ = [m.start() for m in re.finditer(contraste, texto, re.I | re.M)]
        if len(occ) > 1:
            achados.append(Achado("contraste_repetido", "diagnostico" if modo == "critica" else "aviso",
                                  f'Contraste "não é X, é Y" aparece {len(occ)} vezes: mesmo no texto de quem assina, repetido vira vício; propor manter um',
                                  [_linha(texto, i) for i in occ[:6]]))

    sinonimos = [t for t in (r"organizaç", r"\bcompanhia\b", r"\bcorporaç", r"\bfirma\b", r"\binstituiç") if re.search(t, texto, re.I)]
    if re.search(r"\bempresa", texto, re.I) and len(sinonimos) >= 2:
        achados.append(Achado("ciclagem", "diagnostico" if modo == "critica" else "aviso",
                              f'Ciclagem de sinônimos de empresa ({len(sinonimos)} variantes): fixar uma palavra (regra 16)', []))
    return achados


ROTULO = {"bloqueio": "FALHOU", "aviso": "AVISO", "diagnostico": "DIAGNÓSTICO", "preservado": "PRESERVADO", "verificar_autoria": "VERIFICAR AUTORIA"}


def relatorio(achados, arquivo, modo, canal) -> str:
    out = [f"=== {arquivo} (modo: {modo}, canal: {canal}) ===", ""]
    ordem = ("bloqueio", "verificar_autoria", "aviso", "preservado", "diagnostico")
    for nivel in ordem:
        for a in [x for x in achados if x.nivel == nivel]:
            out.append(f"[{ROTULO[a.nivel]}] {a.mensagem}")
            if a.nivel == "verificar_autoria":
                out.append("    Se veio do rascunho de quem assina, fica. Se foi o Claude, corrigir. Use --original para decidir por diff.")
            vistos = []
            for n, t in a.linhas:
                if (n, t) not in vistos:
                    vistos.append((n, t))
            for n, t in vistos[:8]:
                out.append(f"    linha {n}: {t}")
            out.append("")
    b = sum(a.nivel == "bloqueio" for a in achados)
    if modo == "critica":
        out.append("RESULTADO: diagnóstico. Em modo crítica nada bloqueia; apontar, não reescrever.")
    elif b:
        out.append(f"RESULTADO: {b} bloqueio(s). Corrigir o que o Claude escreveu e rodar de novo.")
    elif achados:
        out.append("RESULTADO: sem bloqueios. Revisar os avisos à mão e seguir o checklist do SKILL.md.")
    else:
        out.append("RESULTADO: nenhum padrão encontrado. Seguir o checklist do SKILL.md.")
    return "\n".join(out)


def main() -> int:
    p = argparse.ArgumentParser(description="Validador anti-IA da skill seu-tom-de-voz")
    p.add_argument("arquivo", type=Path)
    p.add_argument("modo", nargs="?", default="novo", choices=MODOS)
    p.add_argument("--canal", default="linkedin", choices=CANAIS)
    p.add_argument("--original", type=Path)
    p.add_argument("--permite", default="", help="lista separada por vírgula: travessao, hashtag, emoji")
    p.add_argument("--json", action="store_true")
    a = p.parse_args()
    permite = {x.strip() for x in a.permite.split(",") if x.strip()}
    if permite - set(LIBERAVEIS):
        print(f"--permite aceita apenas: {', '.join(LIBERAVEIS)}", file=sys.stderr)
        return 2
    if a.original and a.modo != "revisao":
        print("--original só faz sentido em modo revisao.", file=sys.stderr)
        return 2
    try:
        texto = a.arquivo.read_text(encoding="utf-8-sig")
        original = a.original.read_text(encoding="utf-8-sig") if a.original else None
    except (OSError, UnicodeError) as e:
        print(f"Erro ao ler: {e}", file=sys.stderr)
        return 2
    achados = validar(texto, a.modo, a.canal, original, permite)
    if a.json:
        print(json.dumps([{"codigo": x.codigo, "nivel": x.nivel, "mensagem": x.mensagem,
                           "linhas": [{"linha": n, "trecho": t} for n, t in x.linhas]} for x in achados], ensure_ascii=False, indent=2))
    else:
        try:
            print(relatorio(achados, str(a.arquivo), a.modo, a.canal))
        except BrokenPipeError:
            pass
    return 1 if any(x.nivel == "bloqueio" for x in achados) else 0


if __name__ == "__main__":
    sys.exit(main())
