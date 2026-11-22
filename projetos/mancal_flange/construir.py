# -*- coding: utf-8 -*-
"""
Projeto: Mancal Flangeado com Eixo e Tampa
Descricao: Modelagem de conjunto mecanico multi-pecas passo a passo com nomes curtos em pt-BR.
"""

import os
import sys

# Garante acesso ao cliente guri_cad
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "tools")))
from guri_cad import GuriCadClient

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")

STEPS = [
    {
        "name": "novo_documento",
        "desc": "Criando o espaco de trabalho do mancal no FreeCAD",
        "delay": 1.2,
        "code": """
import FreeCAD, Part

doc_name = "mancal_flange"
try:
    FreeCAD.closeDocument(doc_name)
except Exception:
    pass
doc = FreeCAD.newDocument(doc_name)
doc.Label = "mancal_flange"
""",
    },
    {
        "name": "base",
        "desc": "Criando a base retangular (60x40x6mm) com 4 furos M3 nos cantos",
        "delay": 2.0,
        "code": """
doc = FreeCAD.getDocument("mancal_flange")

# Placa base retangular centralizada
placa = Part.makeBox(60, 40, 6, FreeCAD.Vector(-30, -20, 0))

# 4 furos de fixacao M3 (D=3.4mm)
furos = []
for x in [-22.0, 22.0]:
    for y in [-13.0, 13.0]:
        f = Part.makeCylinder(1.7, 10, FreeCAD.Vector(x, y, -2))
        furos.append(f)

for f in furos:
    placa = placa.cut(f)

base_obj = doc.addObject("Part::Feature", "base")
base_obj.Shape = placa
if getattr(base_obj, "ViewObject", None):
    base_obj.ViewObject.ShapeColor = (0.75, 0.77, 0.80)

doc.recompute()
""",
    },
    {
        "name": "colar",
        "desc": "Adicionando o colar central do mancal com alojamento interno D=12mm",
        "delay": 2.0,
        "code": """
doc = FreeCAD.getDocument("mancal_flange")
base_obj = doc.getObject("base")

# Colar cilindrico externo (D=26mm, H=18mm)
cilindro_ext = Part.makeCylinder(13.0, 18.0, FreeCAD.Vector(0, 0, 6))

# Uniao do colar com a base
corpo = base_obj.Shape.fuse(cilindro_ext)

# Furo passante usinado para o eixo (D=12mm)
furo_eixo = Part.makeCylinder(6.0, 30.0, FreeCAD.Vector(0, 0, -2))
corpo = corpo.cut(furo_eixo)

base_obj.Shape = corpo
doc.recompute()
""",
    },
    {
        "name": "eixo",
        "desc": "Modelando o eixo usinado (D=12mm, L=45mm) com flange de topo",
        "delay": 2.0,
        "code": """
doc = FreeCAD.getDocument("mancal_flange")

# Corpo do eixo com folga de deslizamento (D=11.8mm, L=38mm)
haste_eixo = Part.makeCylinder(5.9, 38.0, FreeCAD.Vector(0, 0, 3))

# Flange/cabeca de encosto no topo do eixo (D=18mm, H=4mm)
cabeca_eixo = Part.makeCylinder(9.0, 4.0, FreeCAD.Vector(0, 0, 41))

eixo_solido = haste_eixo.fuse(cabeca_eixo)

eixo_obj = doc.addObject("Part::Feature", "eixo")
eixo_obj.Shape = eixo_solido
if getattr(eixo_obj, "ViewObject", None):
    eixo_obj.ViewObject.ShapeColor = (0.25, 0.55, 0.90) # Aco azulado

doc.recompute()
""",
    },
    {
        "name": "tampa",
        "desc": "Criando a tampa superior de retencao em latao dourado",
        "delay": 2.0,
        "code": """
doc = FreeCAD.getDocument("mancal_flange")

# Anel externo da tampa (D=26mm, H=4mm)
anel_ext = Part.makeCylinder(13.0, 4.0, FreeCAD.Vector(0, 0, 24))

# Furo central livre para passagem do eixo (D=12.4mm)
furo_centro = Part.makeCylinder(6.2, 8.0, FreeCAD.Vector(0, 0, 22))
tampa_solido = anel_ext.cut(furo_centro)

# 2 furos de travamento M2.5
furo_t1 = Part.makeCylinder(1.25, 8.0, FreeCAD.Vector(9.5, 0, 22))
furo_t2 = Part.makeCylinder(1.25, 8.0, FreeCAD.Vector(-9.5, 0, 22))
tampa_solido = tampa_solido.cut(furo_t1).cut(furo_t2)

tampa_obj = doc.addObject("Part::Feature", "tampa")
tampa_obj.Shape = tampa_solido
if getattr(tampa_obj, "ViewObject", None):
    tampa_obj.ViewObject.ShapeColor = (0.85, 0.70, 0.25) # Latao

doc.recompute()
""",
    },
    {
        "name": "salvar",
        "desc": "Salvando o arquivo nativo e exportando arquivos STEP individuais e montados",
        "delay": 0.5,
        "code": f"""
doc = FreeCAD.getDocument("mancal_flange")
save_path = "{PROJECT_DIR}/mancal_flange.FCStd"
doc.saveAs(save_path)

base_obj = doc.getObject("base")
eixo_obj = doc.getObject("eixo")
tampa_obj = doc.getObject("tampa")

import Import
Import.export([base_obj], "{PROJECT_DIR}/base.step")
Import.export([eixo_obj], "{PROJECT_DIR}/eixo.step")
Import.export([tampa_obj], "{PROJECT_DIR}/tampa.step")
Import.export([base_obj, eixo_obj, tampa_obj], "{PROJECT_DIR}/conjunto.step")

print(f"[OK] Projeto salvo com sucesso em: {PROJECT_DIR}")
""",
    },
]


def main():
    client = GuriCadClient()
    print("==================================================")
    print("   Guri CAD - Modelagem Parametrica Passo a Passo")
    print("==================================================")
    client.run_steps(STEPS, default_delay=1.8, doc_name="mancal_flange")


if __name__ == "__main__":
    main()
