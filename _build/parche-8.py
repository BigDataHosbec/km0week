#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Parche Km0 Week — octava tanda, 19/08/2026
==========================================

Tres botones de la portada que no hacían lo que prometían, y un «Inicio» en el
menú.

 1. «Dossier (PDF)», en el bloque de compromisos, llevaba a `suma.html`. Ahora
    descarga el dossier de prensa.
 2. «Descargar el pasaporte», en la sección del Pasaporte Km0, llevaba a la
    página de descargas. Ahora descarga el pasaporte directamente.
 3. «Bases del sorteo», al lado del anterior, llevaba al FAQ. Ahora descarga el
    PDF de las bases.

    Los tres apuntaban a una página intermedia porque cuando se escribió la
    portada los archivos todavía no existían. Ya existen.

 4. El menú de navegación no tenía forma de volver a la portada salvo pulsando
    el logotipo, que es una convención que no todo el mundo conoce. Se añade
    «Inicio» como primer enlace. Al ir en `MENU`, sale igual en la barra de
    escritorio y en el desplegable de móvil, y se marca solo como página activa
    cuando estás en la portada.

Se ejecuta desde la raíz del proyecto:   python3 _build/parche-8.py
Después hay que recompilar:              python3 _build/build.py

Idempotente: volver a ejecutarlo no cambia nada.
"""

import os, sys, io

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
fallos, hechos = [], 0


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
# 1, 2 y 3 · Los tres botones de la portada descargan el archivo
# ===========================================================================
ed("_build/paginas/portada.html", [
    # «¿Lo quieres por escrito?» → el dossier de prensa
    ('''<a class="btn btn-arena btn-sm" href="suma.html" style="margin-top:auto;align-self:flex-start" data-va="Dossier (PDF)">Dossier (PDF)</a>''',
     '''<a class="btn btn-arena btn-sm" href="descargas/dossier-prensa.pdf" download style="margin-top:auto;align-self:flex-start" data-va="Dossier (PDF)">Dossier (PDF)</a>'''),

    # Sección Pasaporte Km0 → el pasaporte imprimible
    ('''<a class="btn btn-arena" href="descargas.html" data-va="Descarregar el passaport">Descargar el pasaporte</a>''',
     '''<a class="btn btn-arena" href="descargas/pasaporte-km0.pdf" download data-va="Descarregar el passaport">Descargar el pasaporte</a>'''),

    # Sección Pasaporte Km0 → las bases del sorteo
    ('''<a class="btn btn-linea" href="faq.html#sorteo" data-va="Bases del sorteig">Bases del sorteo</a>''',
     '''<a class="btn btn-linea" href="descargas/bases-sorteo.pdf" download data-va="Bases del sorteig">Bases del sorteo</a>'''),
])


# ===========================================================================
# 4 · «Inicio» en el menú
# ===========================================================================
# Va dentro de MENU y no suelto en la plantilla para que lo herede también el
# desplegable de móvil y para que `nav()` le ponga solo el estado de página
# activa cuando el visitante está en la portada.
ed("_build/build.py", [
    ('''MENU = [
    ("iniciativa.html",   "La iniciativa",  "La iniciativa"),''',
     '''MENU = [
    ("index.html",        "Inicio",         "Inici"),
    ("iniciativa.html",   "La iniciativa",  "La iniciativa"),'''),
])


# ===========================================================================
# 5 · Que la barra de navegación quepa en una sola fila
# ===========================================================================
# Al medirlo apareció un fallo que ya estaba antes de este parche: entre 1060 y
# 1180 px —portátiles pequeños, tablet en horizontal— la barra se partía en dos
# filas y el nombre de la asociación bajo el logotipo se apilaba en tres
# renglones. Con «Inicio» son siete enlaces y la banda rota se ensancharía, así
# que se arregla de raíz.
#
# El hamburguesa aparece a partir de 1060 px hacia abajo, así que solo hay que
# cubrir la franja de justo encima: ahí se aprieta el interlineado (menos
# relleno, tipo algo más pequeño) y se esconde el «HOSBEC · COMUNITAT
# VALENCIANA» del logotipo, que es lo que más ancho ocupa y es redundante con
# la cinta superior. Por encima de 1240 px no cambia nada.
ed("assets/css/km0.css", [
    ('''.nav-links a:hover { background: var(--mar-p); color: var(--mar-d); }''',
     '''.nav-links a:hover { background: var(--mar-p); color: var(--mar-d); }

/* Ni un enlace del menú ni el logotipo se parten por la mitad. */
.nav-links a, .nav-right .btn, .brand-txt > span { white-space: nowrap; }
.brand { flex-shrink: 0; }

/* Franja justa antes de que salga el hamburguesa (1060 px): con siete enlaces
   no cabía y la barra se iba a dos filas. */
@media (min-width: 1061px) and (max-width: 1240px) {
  .nav .wrap { gap: .55rem; }
  .brand-txt small { display: none; }
  .nav-links { gap: 0; }
  .nav-links a { font-size: .82rem; padding: 9px 8px; }
  .nav-right { gap: 7px; }
  .lang button { padding: 7px 9px; }
}''',
     '@media (min-width: 1061px) and (max-width: 1240px)'),
])


# ===========================================================================
print("cambios aplicados:", hechos)
if fallos:
    print("\n⚠  revisar (%d):" % len(fallos))
    for f in fallos:
        print("   ·", f)
    sys.exit(1)
print("todo correcto. Ahora:  python3 _build/build.py")
