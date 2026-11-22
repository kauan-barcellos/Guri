# -*- coding: utf-8 -*-
"""
Projeto: Parafuso Allen M6 com Porca
Descricao: Modelagem paramétrica passo a passo com nomes curtos em pt-BR.
"""

import os
import sys

# Garante acesso ao modulo guri_cad
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "tools")))
from guri_cad import GuriCadClient

# ----------------------------------------------------
# Parametros de Projeto (M6x25)
# ----------------------------------------------------
RAIO_HASTE = 3.0           # Diametro 6mm
COMP_HASTE = 25.0          # Comprimento 25mm
RAIO_CABECA = 5.0          # Diametro 10mm
ALTURA_CABECA = 6.0        # Altura 6mm
RAIO_ALLEN = 2.88          # Chave Allen 5mm (circunscrito)
PROF_ALLEN = 3.5           # Profundidade 3.5mm

# Porca M6
RAIO_PORCA = 5.77          # Sextavado 10mm entre faces
ALTURA_PORCA = 5.0         # Espessura 5mm
RAIO_FURO_PORCA = 2.5      # Furo interno para M6

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")

# ----------------------------------------------------
# Etapas de Construcao (passo a passo ao vivo)
# ----------------------------------------------------
STEPS = [
    {
        "name": "novo_documento",
        "desc": "Criando novo documento do projeto no FreeCAD",
        "delay": 1.0,
        "code": f"""
import FreeCAD, Part, math

doc_name = "parafuso_allen"
try:
    FreeCAD.closeDocument(doc_name)
except Exception:
    pass
doc = FreeCAD.newDocument(doc_name)
doc.Label = "parafuso_allen"
""",
    },
    {
        "name": "haste",
        "desc": "Criando a haste cilindrica (D=6mm, L=25mm)",
        "delay": 1.5,
        "code": f"""
doc = FreeCAD.getDocument("parafuso_allen")
haste = doc.addObject("Part::Cylinder", "haste")
haste.Radius = {RAIO_HASTE}
haste.Height = {COMP_HASTE}
haste.Placement.Base = FreeCAD.Vector(0, 0, 0)
doc.recompute()
""",
    },
    {
        "name": "cabeca",
        "desc": "Criando a cabeca cilindrica no topo da haste",
        "delay": 1.5,
        "code": f"""
doc = FreeCAD.getDocument("parafuso_allen")
cabeca = doc.addObject("Part::Cylinder", "cabeca")
cabeca.Radius = {RAIO_CABECA}
cabeca.Height = {ALTURA_CABECA}
cabeca.Placement.Base = FreeCAD.Vector(0, 0, {COMP_HASTE})
doc.recompute()
""",
    },
    {
        "name": "fenda",
        "desc": "Esculpindo o encaixe sextavado Allen 5mm na cabeca",
        "delay": 1.5,
        "code": f"""
doc = FreeCAD.getDocument("parafuso_allen")
fenda = doc.addObject("Part::Prism", "fenda")
fenda.Polygon = 6
fenda.Circumradius = {RAIO_ALLEN}
fenda.Height = {PROF_ALLEN} + 0.5
fenda.Placement.Base = FreeCAD.Vector(0, 0, {COMP_HASTE + ALTURA_CABECA - PROF_ALLEN})

# Uniao da haste com a cabeca e subtracao da fenda
haste = doc.getObject("haste")
cabeca = doc.getObject("cabeca")

corpo = doc.addObject("Part::Fuse", "corpo")
corpo.Base = haste
corpo.Tool = cabeca
doc.recompute()

parafuso = doc.addObject("Part::Cut", "parafuso")
parafuso.Base = corpo
parafuso.Tool = fenda

# Esconde os intermediarios na visualizacao
for obj in [haste, cabeca, fenda, corpo]:
    if getattr(obj, "ViewObject", None):
        obj.ViewObject.Visibility = False

if getattr(parafuso, "ViewObject", None):
    parafuso.ViewObject.ShapeColor = (0.75, 0.75, 0.78)

doc.recompute()
""",
    },
    {
        "name": "porca",
        "desc": "Criando a porca sextavada M6 ao lado do parafuso",
        "delay": 1.5,
        "code": f"""
doc = FreeCAD.getDocument("parafuso_allen")

# Prisma sextavado da porca
corpo_porca = doc.addObject("Part::Prism", "corpo_porca")
corpo_porca.Polygon = 6
corpo_porca.Circumradius = {RAIO_PORCA}
corpo_porca.Height = {ALTURA_PORCA}
corpo_porca.Placement.Base = FreeCAD.Vector(18, 0, 0)

# Furo central da porca
furo_porca = doc.addObject("Part::Cylinder", "furo_porca")
furo_porca.Radius = {RAIO_FURO_PORCA}
furo_porca.Height = {ALTURA_PORCA} + 2.0
furo_porca.Placement.Base = FreeCAD.Vector(18, 0, -1.0)
doc.recompute()

# Subtracao para gerar a porca
porca = doc.addObject("Part::Cut", "porca")
porca.Base = corpo_porca
porca.Tool = furo_porca

for obj in [corpo_porca, furo_porca]:
    if getattr(obj, "ViewObject", None):
        obj.ViewObject.Visibility = False

if getattr(porca, "ViewObject", None):
    porca.ViewObject.ShapeColor = (0.85, 0.70, 0.30)

doc.recompute()
""",
    },
    {
        "name": "salvar",
        "desc": "Salvando o modelo final e exportando STEP na pasta do projeto",
        "delay": 0.5,
        "code": f"""
doc = FreeCAD.getDocument("parafuso_allen")
save_path = "{PROJECT_DIR}/parafuso_allen.FCStd"
doc.saveAs(save_path)

# Exportacao de arquivos STEP individuais organizados
parafuso = doc.getObject("parafuso")
porca = doc.getObject("porca")

import Import
Import.export([parafuso], "{PROJECT_DIR}/parafuso.step")
Import.export([porca], "{PROJECT_DIR}/porca.step")
Import.export([parafuso, porca], "{PROJECT_DIR}/conjunto.step")

print(f"[OK] Projeto salvo com sucesso em: {PROJECT_DIR}")
""",
    },
]


def main():
    client = GuriCadClient()
    print("==================================================")
    print("   Guri CAD - Modelagem Parametrica Passo a Passo")
    print("==================================================")
    client.run_steps(STEPS, default_delay=1.5, doc_name="parafuso_allen")


if __name__ == "__main__":
    main()
