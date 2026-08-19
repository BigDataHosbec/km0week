#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Parche Km0 Week — tercera tanda, 18/08/2026
===========================================

 1. El campo de correo del boletín estaba pensado solo para el pie oscuro:
    fondo translúcido, borde tenue y texto blanco. En la sección clara de
    Noticias resultaba invisible y lo que escribías no se leía. Ahora el
    estilo por defecto es para fondo claro y la versión oscura se limita
    al pie y a las secciones azules.
 2. Asuntos de correo con prefijo, para poder filtrarlos de un vistazo:
      [Km0 Week] Alojamiento · nueva solicitud
      [Km0 Week] Boletín · nueva alta

Se ejecuta desde la raíz del proyecto:   python3 _build/parche-3.py
Después hay que recompilar:              python3 _build/build.py

Idempotente: volver a ejecutarlo no cambia nada.
"""

import os, sys, io

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
fallos, hechos = [], 0


def ed(rel, pares, obligatorio=True):
    global hechos
    ruta = os.path.join(RAIZ, rel)
    if not os.path.exists(ruta):
        if obligatorio:
            fallos.append("NO EXISTE: " + rel)
        return
    txt = original = io.open(ruta, encoding="utf-8").read()
    for par in pares:
        viejo, nuevo = par[0], par[1]
        marca = par[2] if len(par) > 2 else nuevo
        if marca in txt:
            continue
        if viejo not in txt:
            if obligatorio:
                fallos.append("%s → no encuentro: %.70s" % (rel, viejo.replace("\n", "\\n")))
            continue
        txt = txt.replace(viejo, nuevo)
        hechos += 1
    if txt != original:
        io.open(ruta, "w", encoding="utf-8").write(txt)


# ===========================================================================
# 1 · El campo del boletín, legible en cualquier fondo
# ===========================================================================
ed("assets/css/km0.css", [
    ('''.subscribe { display: flex; gap: 8px; }
.subscribe input {
  flex: 1; min-width: 0; background: rgba(255,255,255,.09); border: 1.5px solid rgba(234,246,249,.24);
  border-radius: var(--r-s); padding: 11px 15px; color: #fff; font-size: .9rem;
}
.subscribe input::placeholder { color: rgba(234,246,249,.45); }''',
     '''/* El boletín aparece en dos sitios con fondos opuestos: el pie (azul tinta)
   y la sección clara de Noticias. El estilo base es para fondo claro y la
   variante oscura se aplica solo donde toca. */
.subscribe { display: flex; gap: 8px; }
.subscribe input {
  flex: 1; min-width: 0; background: #fff; border: 1.5px solid var(--linea);
  border-radius: var(--r-s); padding: 11px 15px; color: var(--tinta); font-size: .9rem;
}
.subscribe input::placeholder { color: var(--suave); }
.subscribe input:focus-visible { border-color: var(--mar); outline: none; box-shadow: 0 0 0 3px var(--mar-p); }

.foot .subscribe input, .bg-mar .subscribe input {
  background: rgba(255,255,255,.09); border-color: rgba(234,246,249,.24); color: #fff;
}
.foot .subscribe input::placeholder, .bg-mar .subscribe input::placeholder { color: rgba(234,246,249,.45); }
.foot .subscribe input:focus-visible, .bg-mar .subscribe input:focus-visible {
  border-color: var(--arena); box-shadow: 0 0 0 3px rgba(238,216,174,.22);
}'''),
])


# ===========================================================================
# 2 · Asuntos con prefijo, para que se filtren solos en la bandeja
# ===========================================================================
ed("_build/paginas/suma.html", [
    ('<input type="hidden" name="_subject" value="Km0 Week · nueva solicitud de alojamiento">',
     '<input type="hidden" name="_subject" value="[Km0 Week] Alojamiento · nueva solicitud">'),
])

ed("assets/js/home.js", [
    ('            _subject: "Km0 Week · alta en el boletín",',
     '            _subject: "[Km0 Week] Boletín · nueva alta",'),
    ('          "?subject=" + encodeURIComponent("Km0 Week · alta en el boletín") +',
     '          "?subject=" + encodeURIComponent("[Km0 Week] Boletín · nueva alta") +'),
])


# ===========================================================================
print("cambios aplicados:", hechos)
if fallos:
    print("\n⚠  revisar (%d):" % len(fallos))
    for f in fallos:
        print("   ·", f)
    sys.exit(1)
print("todo correcto. Ahora:  python3 _build/build.py")
