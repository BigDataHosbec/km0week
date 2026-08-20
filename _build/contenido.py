# -*- coding: utf-8 -*-
"""
HOSBEC Km0 Week — acceso al contenido
=====================================

El contenido de la web (alojamientos, agenda, noticias y la configuración de
la edición) vive en `contenido/*.json`. Este módulo es el único sitio que sabe
leerlo, y lo usan tanto `build.py` como `descargables.py`, de modo que las dos
cosas siempre cuentan lo mismo.

Nadie edita esos JSON a mano: los escribe el panel de administración
(`admin/`). Y nadie edita `assets/js/data-alojamientos.js`: lo genera
`escribir_js()` cada vez que se compila.
"""

import io
import json
import os

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR = os.path.join(RAIZ, "contenido")


def _leer(nombre):
    ruta = os.path.join(DIR, nombre + ".json")
    try:
        with io.open(ruta, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        raise SystemExit("Falta el archivo de contenido: contenido/%s.json" % nombre)
    except ValueError as e:
        raise SystemExit(
            "contenido/%s.json no se entiende: %s\n"
            "Suele ser una coma de más o de menos. Si lo has editado a mano, "
            "deshaz el cambio; si lo guardó el panel, avisa." % (nombre, e))


ALOJAMIENTOS = _leer("alojamientos")
AGENDA = _leer("agenda")
CONFIG = _leer("configuracion")
NOTICIAS = _leer("noticias")

# Atajos de lo que se usa en todas partes
DOMINIO = CONFIG["dominio"].rstrip("/")
EMAIL = CONFIG["emailContacto"]
TELEFONO = CONFIG["telefonoContacto"]
FECHAS_ES = CONFIG["fechasTexto"]["es"]
FECHAS_VA = CONFIG["fechasTexto"]["va"]


def _entero(v):
    """Tolerante a propósito: si un dato viene mal, que lo diga verificar.py
    con un mensaje entendible, no que reviente aquí con un error de Python."""
    return v if isinstance(v, int) and not isinstance(v, bool) else 0


CUPO_TOTAL = sum(_entero(a.get("cupo")) for a in ALOJAMIENTOS)
DESTINOS = sorted({a["destino"] for a in ALOJAMIENTOS
                   if isinstance(a.get("destino"), str) and a["destino"].strip()})


# ---------------------------------------------------------------------------
# Generación de assets/js/data-alojamientos.js
# ---------------------------------------------------------------------------
CABECERA_JS = """\
/* ===========================================================================
   HOSBEC Km0 Week — DATOS DE LA WEB

   ARCHIVO GENERADO. NO LO EDITES A MANO: lo reescribe `python3 _build/build.py`
   a partir de los archivos de `contenido/`, y perderías el cambio.

   Para cambiar el contenido:
     · desde el panel de administración  →  /admin/   (lo normal)
     · o editando  contenido/alojamientos.json
                   contenido/agenda.json
                   contenido/configuracion.json
   =========================================================================== */
"""


def _js(dato):
    """JSON válido también como JavaScript."""
    txt = json.dumps(dato, ensure_ascii=False, indent=2)
    # U+2028 y U+2029 son saltos de línea legales en JSON pero rompen JavaScript
    return txt.replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")


def escribir_js():
    """Reescribe assets/js/data-alojamientos.js desde contenido/*.json."""
    partes = [
        CABECERA_JS,
        "\nconst ALOJAMIENTOS = %s;\n" % _js(ALOJAMIENTOS),
        "\nconst AGENDA = %s;\n" % _js(AGENDA),
        "\nconst CONFIG = %s;\n" % _js(CONFIG),
        "\n/* Exponer para los módulos de la web */\n",
        "window.KM0 = { ALOJAMIENTOS, AGENDA, CONFIG };\n",
    ]
    ruta = os.path.join(RAIZ, "assets", "js", "data-alojamientos.js")
    with io.open(ruta, "w", encoding="utf-8") as f:
        f.write("".join(partes))
    return ruta
