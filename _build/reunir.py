#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Km0 Week — reunir lo que se publica
===================================

Copia a `_sitio/` solo lo que tiene que ver la gente. Lo demás —las fuentes de
contenido, los scripts que compilan, las herramientas— se queda fuera: está en
GitHub, pero no en la web.

    python3 _build/reunir.py

Lo usa la publicación automática. A mano sirve para ver exactamente qué se
sube antes de subirlo.
"""

import os
import shutil
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITIO = os.path.join(RAIZ, "_sitio")

# Lo que NO se publica
FUERA_CARPETAS = {
    ".git", ".github", "_build", "_sitio", "contenido", "node_modules",
    "__pycache__", "REGISTROS",
}
FUERA_ARCHIVOS = {
    "package.json", "package-lock.json", ".gitignore",
}
FUERA_EXTENSIONES = {".md", ".py", ".pyc"}


def se_publica(rel):
    partes = rel.split(os.sep)
    if any(p in FUERA_CARPETAS for p in partes):
        return False
    nombre = partes[-1]
    if nombre in FUERA_ARCHIVOS:
        return False
    if os.path.splitext(nombre)[1].lower() in FUERA_EXTENSIONES:
        return False
    return True


def main():
    if os.path.isdir(SITIO):
        shutil.rmtree(SITIO)
    os.makedirs(SITIO)

    copiados = 0
    peso = 0
    for base, dirs, archivos in os.walk(RAIZ):
        rel_base = os.path.relpath(base, RAIZ)
        if rel_base == ".":
            rel_base = ""
        dirs[:] = [d for d in dirs if d not in FUERA_CARPETAS]
        for a in archivos:
            rel = os.path.join(rel_base, a) if rel_base else a
            if not se_publica(rel):
                continue
            destino = os.path.join(SITIO, rel)
            os.makedirs(os.path.dirname(destino), exist_ok=True)
            shutil.copy2(os.path.join(base, a), destino)
            copiados += 1
            peso += os.path.getsize(destino)

    # GitHub Pages no debe procesar el sitio con Jekyll: si lo hiciera, se
    # dejaría de servir cualquier carpeta que empiece por guion bajo.
    open(os.path.join(SITIO, ".nojekyll"), "w").close()

    paginas = len([f for f in os.listdir(SITIO) if f.endswith(".html")])
    print("Se publican %d archivos (%.1f MB), %d páginas."
          % (copiados, peso / 1048576.0, paginas))

    faltan = [f for f in ("index.html", "sitemap.xml", "robots.txt")
              if not os.path.isfile(os.path.join(SITIO, f))]
    if faltan:
        print("FALTA: " + ", ".join(faltan))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
