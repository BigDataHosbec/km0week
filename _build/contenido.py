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
FILTROS = _leer("filtros")

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
        "\nconst FILTROS = %s;\n" % _js(FILTROS),
        "\n/* Exponer para los módulos de la web */\n",
        "window.KM0 = { ALOJAMIENTOS, AGENDA, CONFIG, FILTROS };\n",
    ]
    ruta = os.path.join(RAIZ, "assets", "js", "data-alojamientos.js")
    with io.open(ruta, "w", encoding="utf-8") as f:
        f.write("".join(partes))
    return ruta


# ---------------------------------------------------------------------------
# Traducción automática de lo que no se ha escrito a mano
# ---------------------------------------------------------------------------
def _bilingues(obj, salida=None):
    """Recorre los datos y va soltando cada pareja {es, va} que encuentra."""
    salida = [] if salida is None else salida
    if isinstance(obj, dict):
        if "es" in obj and "va" in obj:
            salida.append(obj)
        for v in obj.values():
            _bilingues(v, salida)
    elif isinstance(obj, list):
        for v in obj:
            _bilingues(v, salida)
    return salida


def completar_traducciones(idioma="va"):
    """
    Rellena el valenciano que falte a partir del castellano.

    Lo escrito a mano manda siempre: solo se toca lo que está vacío. Devuelve
    el diccionario {castellano: traducción} de lo que se ha traducido a
    máquina, que es lo que el panel enseña marcado como «sin revisar».
    """
    import traducir

    pendientes = []          # (nodo, clave_o_indice)
    textos = []
    for nodo in _bilingues([ALOJAMIENTOS, AGENDA, NOTICIAS, CONFIG]):
        es, va = nodo.get("es"), nodo.get("va")
        if isinstance(es, list):
            destino = va if isinstance(va, list) else []
            nodo[idioma] = destino
            for i, t in enumerate(es):
                if i >= len(destino):
                    destino.append("")
                if t and t.strip() and not (destino[i] or "").strip():
                    pendientes.append((destino, i))
                    textos.append(t)
        elif isinstance(es, str) and es.strip() and not (va or "").strip():
            pendientes.append((nodo, idioma))
            textos.append(es)

    if not textos:
        return {}

    hechas = traducir.traducir(textos, idioma)
    memoria = {}
    for (nodo, clave), es, va in zip(pendientes, textos, hechas):
        if va:
            nodo[clave] = va
            memoria[es] = va
    return memoria
