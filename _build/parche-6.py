#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Parche Km0 Week — sexta tanda, 18/08/2026
=========================================

 1. El botón se quedaba hasta 30 segundos en «Enviando…». El registro llegaba
    a la hoja al instante; lo que tardaba era la RESPUESTA, porque el Apps
    Script manda los dos correos antes de contestar, y encima la primera
    llamada del día arranca en frío. Por eso el tercer envío iba en 3 s.

    Solución: el navegador deja de esperar la respuesta indefinidamente. Espera
    un máximo (`ESPERA_MAX`) y, si no ha llegado, da el envío por bueno y libera
    el botón. Es seguro porque el script escribe la fila ANTES de enviar los
    correos: cuando se agota esa espera, el dato ya está guardado. La petición
    sigue viva en segundo plano, y si acaba fallando de verdad se avisa.

 2. Formato esperado bajo los campos de correo y web de «Suma tu alojamiento».

Se ejecuta desde la raíz del proyecto:   python3 _build/parche-6.py
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
# 1 · El navegador deja de esperar a que Google termine de mandar los correos
# ===========================================================================
ed("assets/js/home.js", [
    ('''  async function enviarRegistro(datos) {
    const url = CFG.endpointFormularios;
    if (!url) return "correo";

    const cuerpo = JSON.stringify(Object.assign(datosComunes(), datos));

    try {
      const r = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "text/plain;charset=utf-8" },
        body: cuerpo,
        redirect: "follow"
      });
      const j = await r.json();
      return j && j.ok ? "ok" : "error";
    } catch (_) { /* seguimos con el plan B */ }

    try {
      await fetch(url, { method: "POST", mode: "no-cors", body: cuerpo });
      return "ok";                      // no podemos leer la respuesta, pero sale
    } catch (_) { /* plan C */ }

    return "correo";
  }''',
     '''  // Cuánto espera el navegador la respuesta de Google antes de dar el envío
  // por bueno y devolverle el control al visitante. El Apps Script escribe la
  // fila ANTES de mandar los correos, así que pasado este tiempo el registro
  // ya está guardado: lo que queda pendiente son los correos, que no tiene
  // sentido hacer esperar a nadie (y en la primera llamada del día el script
  // arranca en frío y puede tardar medio minuto).
  const ESPERA_MAX = 3500;

  function conTope(promesa, ms) {
    return Promise.race([
      promesa,
      new Promise(r => setTimeout(() => r("tarda"), ms))
    ]);
  }

  async function enviarRegistro(datos) {
    const url = CFG.endpointFormularios;
    if (!url) return "correo";

    const cuerpo = JSON.stringify(Object.assign(datosComunes(), datos));

    const intento = (async () => {
      try {
        const r = await fetch(url, {
          method: "POST",
          headers: { "Content-Type": "text/plain;charset=utf-8" },
          body: cuerpo,
          redirect: "follow"
        });
        const j = await r.json();
        return j && j.ok ? "ok" : "error";
      } catch (_) { /* seguimos con el plan B */ }

      try {
        await fetch(url, { method: "POST", mode: "no-cors", body: cuerpo });
        return "ok";                    // no podemos leer la respuesta, pero sale
      } catch (_) { /* plan C */ }

      return "correo";
    })();

    // Si tarda más de la cuenta, soltamos al visitante pero no abandonamos la
    // petición: si acaba mal de verdad, se le avisa entonces.
    const r = await conTope(intento, ESPERA_MAX);
    if (r !== "tarda") return r;

    intento.then(final => {
      if (final !== "ok") toast(t("falloEnvio"));
    });
    return "ok";
  }''')
])


# ===========================================================================
# 2 · Formato esperado bajo correo y web
# ===========================================================================
ed("_build/paginas/suma.html", [
    ('''        <span data-va="Correu *">Correo *</span>
        <input type="email" name="email" required autocomplete="email">''',
     '''        <span data-va="Correu *">Correo *</span>
        <input type="email" name="email" required autocomplete="email">
        <span class="ayuda" data-va="Format: correu@exemple.com">Formato: correo@ejemplo.com</span>'''),

    ('''        <span data-va="Web o motor de reserves">Web o motor de reservas</span>
        <input type="url" name="web" placeholder="https://">''',
     '''        <span data-va="Web o motor de reserves">Web o motor de reservas</span>
        <input type="url" name="web" placeholder="https://">
        <span class="ayuda" data-va="Ha de començar per https:// — per exemple https://web.com">Debe empezar por https:// — por ejemplo https://web.com</span>'''),
])


# ===========================================================================
print("cambios aplicados:", hechos)
if fallos:
    print("\n⚠  revisar (%d):" % len(fallos))
    for f in fallos:
        print("   ·", f)
    sys.exit(1)
print("todo correcto. Ahora:  python3 _build/build.py")
