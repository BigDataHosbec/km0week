#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Parche Km0 Week — séptima tanda, 19/08/2026
===========================================

Enlaza las quince tarjetas de descarga con los archivos reales.

Hasta ahora todas las tarjetas de «Materiales y kit» (descargas.html) y de
«Sala de prensa» (prensa.html) llevaban la etiqueta «Próximamente». Los
archivos ya existen en descargas/, así que aquí:

  1. Se añade el CSS del botón de descarga y se alinean las tarjetas para que
     el botón quede a la misma altura en toda la fila, sin importar cuánto
     ocupe la descripción.
  2. Se sustituye cada «Próximamente» por un botón real con el enlace, el peso
     del archivo y un icono. El peso se lee del archivo de verdad si está en
     descargas/; si no, se usa el valor de referencia de esta tabla.
  3. Se corrigen dos etiquetas de formato que ya no eran ciertas: el pasaporte
     se imprime en A4 apaisado (no en A5) y la cartelería está maquetada
     entera en A4 (no en A3).

Cada tarjeta se identifica por su <h3>, no por su posición, así que si se
reordenan las tarjetas el parche sigue acertando.

Se ejecuta desde la raíz del proyecto:   python3 _build/parche-7.py
Después hay que recompilar:              python3 _build/build.py

Idempotente: volver a ejecutarlo no cambia nada.
"""

import os, sys, io, re

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SALIDA = os.path.join(RAIZ, "descargas")
fallos, hechos = [], 0


# ---------------------------------------------------------------------------
# Qué archivo va en cada tarjeta. La clave es un trozo del <h3> en castellano,
# suficiente para distinguirla. El tercer valor es el peso de referencia, que
# solo se usa si el archivo todavía no está en descargas/.
# ---------------------------------------------------------------------------
TARJETAS = [
    ("Pasaporte Km0 imprimible",        "pasaporte-km0.pdf",           "270 KB"),
    ("Programa de actividades",         "programa-actividades.pdf",    "314 KB"),
    ("Bases del sorteo",                "bases-sorteo.pdf",            "261 KB"),
    ("Cartelería para recepción",       "carteleria.pdf",              "191 KB"),
    ("Kit de redes sociales",           "kit-redes-sociales.zip",      "303 KB"),
    ("Textos para tu web y tu correo",  "textos-para-tu-web.docx",     "10 KB"),
    ("Manual de marca",                 "manual-de-marca.pdf",         "482 KB"),
    ("Sello para el pasaporte",         "sello-pasaporte.pdf",         "263 KB"),
    ("Guía rápida para recepción",      "guia-recepcion.pdf",          "292 KB"),
    ("Dossier de prensa 2026",          "dossier-prensa.pdf",          "539 KB"),
    ("Nota de prensa",                  "nota-prensa-presentacion.pdf", "245 KB"),
    ("Logotipos y marca",               "logotipos-y-marca.zip",       "740 KB"),
    ("Banco de imágenes",               "banco-imagenes.zip",          "5.6 MB"),
    ("Listado de alojamientos",         "alojamientos-adheridos.xlsx", "9 KB"),
]

ICONO = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" '
         'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
         '<path d="M12 3v12"></path><path d="m7 11 5 5 5-5"></path>'
         '<path d="M4 20h16"></path></svg>')


def peso(archivo, respaldo):
    ruta = os.path.join(SALIDA, archivo)
    if not os.path.exists(ruta):
        return respaldo
    n = os.path.getsize(ruta)
    return "%.1f MB" % (n / 1048576.0) if n >= 1048576 else "%d KB" % max(1, round(n / 1024.0))


def bloque(archivo, texto):
    return ('<div class="desc-bajar">\n'
            '          <a class="bajar" href="descargas/%s" download>%s<span '
            'data-va="Descarregar">Descargar</span></a>\n'
            '          <span class="peso">%s</span>\n'
            '        </div>' % (archivo, ICONO, texto))


PROXIMAMENTE = '<span class="peso" data-va="Pròximament">Próximamente</span>'


def enlazar(rel):
    """Recorre las tarjetas del archivo y cambia «Próximamente» por el botón."""
    global hechos
    ruta = os.path.join(RAIZ, rel)
    if not os.path.exists(ruta):
        fallos.append("NO EXISTE: " + rel)
        return
    txt = original = io.open(ruta, encoding="utf-8").read()

    def cambiar(m):
        global hechos
        tarjeta = m.group(0)
        if PROXIMAMENTE not in tarjeta:
            return tarjeta                      # ya enlazada, o no lleva etiqueta
        for clave, archivo, respaldo in TARJETAS:
            if clave in tarjeta:
                hechos += 1
                return tarjeta.replace(PROXIMAMENTE,
                                       bloque(archivo, peso(archivo, respaldo)))
        fallos.append("%s → tarjeta sin archivo asignado: %.60s"
                      % (rel, re.sub(r"\s+", " ", tarjeta)))
        return tarjeta

    # Las tarjetas no llevan divs anidados, así que el cierre no goloso basta.
    txt = re.sub(r'<div class="desc">.*?</div>', cambiar, txt, flags=re.S)
    if txt != original:
        io.open(ruta, "w", encoding="utf-8").write(txt)


def ed(rel, pares):
    global hechos
    ruta = os.path.join(RAIZ, rel)
    if not os.path.exists(ruta):
        fallos.append("NO EXISTE: " + rel)
        return
    txt = original = io.open(ruta, encoding="utf-8").read()
    for par in pares:
        viejo, nuevo = par[0], par[1]
        marca = par[2] if len(par) > 2 else nuevo
        if marca in txt:
            continue
        if viejo not in txt:
            fallos.append("%s → no encuentro: %.70s" % (rel, viejo.replace("\n", "\\n")))
            continue
        txt = txt.replace(viejo, nuevo)
        hechos += 1
    if txt != original:
        io.open(ruta, "w", encoding="utf-8").write(txt)


# ===========================================================================
# 1 · CSS del botón de descarga
# ===========================================================================
ed("assets/css/km0.css", [
    ('''.desc .peso { font-size: .78rem; color: var(--suave); }
.desc h3 { font-size: 1.06rem; }''',
     '''.desc .peso { font-size: .78rem; color: var(--suave); }
.desc h3 { font-size: 1.06rem; }
/* La descripción ocupa el hueco sobrante para que el botón de descarga quede
   a la misma altura en todas las tarjetas de una fila. */
.desc { grid-template-rows: auto auto 1fr auto; align-content: stretch; }
.desc-bajar { display: flex; flex-wrap: wrap; align-items: center; gap: .55rem .8rem; margin-top: .2rem; }
.bajar {
  display: inline-flex; align-items: center; gap: .45rem; text-decoration: none;
  font-weight: 700; font-size: .9rem; line-height: 1; color: #fff;
  background: var(--mar); border-radius: var(--r-s); padding: .62rem .95rem;
  transition: background .16s ease, transform .16s ease;
}
.bajar:hover, .bajar:focus-visible { background: var(--tinta); color: #fff; transform: translateY(-1px); }
.bajar svg { width: 1.05rem; height: 1.05rem; flex: 0 0 auto; }
@media (prefers-reduced-motion: reduce) { .bajar { transition: none; } .bajar:hover { transform: none; } }''',
     '.desc-bajar {'),
])


# ===========================================================================
# 2 · Etiquetas de formato que ya no eran ciertas
# ===========================================================================
# Las dos etiquetas viejas comparten el mismo destino, así que no sirve la
# comprobación por marca de `ed()`: basta con que las cadenas viejas dejen de
# aparecer, y eso ya lo hace `str.replace` sin repetir nada.
_ruta = os.path.join(RAIZ, "_build/paginas/descargas.html")
if os.path.exists(_ruta):
    _t = _orig = io.open(_ruta, encoding="utf-8").read()
    for _viejo in ("PDF · A5", "PDF · A3 / A4"):
        if '<span class="tipo">%s</span>' % _viejo in _t:
            _t = _t.replace('<span class="tipo">%s</span>' % _viejo,
                            '<span class="tipo">PDF · A4</span>')
            hechos += 1
    if _t != _orig:
        io.open(_ruta, "w", encoding="utf-8").write(_t)
else:
    fallos.append("NO EXISTE: _build/paginas/descargas.html")


# ===========================================================================
# 3 · Enlazar las quince tarjetas
# ===========================================================================
enlazar("_build/paginas/descargas.html")
enlazar("_build/paginas/prensa.html")


# ===========================================================================
# 4 · El banco de imágenes no son fotografías reales
# ===========================================================================
# El ZIP lleva las ilustraciones provisionales de la web, no reportaje de los
# establecimientos. Prometerle a un medio «fotografías de los alojamientos
# adheridos» y darle otra cosa es el tipo de detalle que se paga caro, así que
# la tarjeta dice lo que hay (el LEEME del ZIP lo repite por dentro).
ed("_build/paginas/prensa.html", [
    ('''<p class="body-sm" data-va="Fotografies dels destins i dels allotjaments adherits, lliures per a ús editorial amb crèdit.">Fotografías de los destinos y de los alojamientos adheridos, libres para uso editorial con crédito.</p>''',
     '''<p class="body-sm" data-va="Les imatges de la web, ordenades per destí, allotjament i experiència. Ús editorial citant HOSBEC · Km0 Week.">Las imágenes de la web, ordenadas por destino, alojamiento y experiencia. Uso editorial citando HOSBEC · Km0 Week.</p>'''),
])


# ===========================================================================
# 5 · Ya no hay nada «pendiente de publicar»
# ===========================================================================
# Los dos avisos daban por hecho que el material iba saliendo poco a poco. Ya
# está todo colgado, así que ahora lo que tienen que decir es a quién escribir
# si hace falta algo distinto (una medida rara, un formato editable, una foto
# concreta de una casa).
ed("_build/paginas/descargas.html", [
    ('''data-va="Anem publicant els materials a mesura que es tanquen. Si ets allotjament adherit, ajuntament o mitjà i necessites alguna cosa concreta abans, escriu-nos i te l'enviem.">Vamos publicando los materiales a medida que se cierran. Si eres alojamiento adherido, ayuntamiento o medio y necesitas algo concreto antes, escríbenos y te lo enviamos.''',
     '''data-va="Tot el material de l'edició està ací. Si ets allotjament adherit, ajuntament o mitjà i necessites una altra mida, un format editable o una peça a mida, escriu-nos i te la preparem.">Todo el material de la edición está aquí. Si eres alojamiento adherido, ayuntamiento o medio y necesitas otra medida, un formato editable o una pieza a medida, escríbenos y te la preparamos.'''),
])

ed("_build/paginas/prensa.html", [
    ('''data-va="Vas publicant-se a mesura que es tanquen. Si necessites algun material abans que estiga ací, escriu-nos a km0week@hosbec.com i te l'enviem.">Se van publicando a medida que se cierran. Si necesitas algún material antes de que esté aquí, escríbenos a km0week@hosbec.com y te lo enviamos.''',
     '''data-va="Descàrrega lliure per a ús editorial. Si necessites una xifra concreta, una declaració atribuïble o material que no estiga ací, escriu-nos a km0week@hosbec.com.">Descarga libre para uso editorial. Si necesitas una cifra concreta, una declaración atribuible o material que no esté aquí, escríbenos a km0week@hosbec.com.'''),
])


# ===========================================================================
print("cambios aplicados:", hechos)
if fallos:
    print("\n⚠  revisar (%d):" % len(fallos))
    for f in fallos:
        print("   ·", f)
    sys.exit(1)
print("todo correcto. Ahora:  python3 _build/build.py")
