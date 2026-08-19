#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Parche Km0 Week — quinta tanda, 18/08/2026
==========================================
Se abandona FormSubmit. Los tres formularios pasan a enviarse a un Google
Apps Script propio, que escribe cada registro en una hoja de cálculo y manda
los dos correos (aviso a HOSBEC y acuse a quien rellena).

Qué cambia para el visitante:

  · ya no hay paso de reCAPTCHA en un sitio ajeno,
  · ya no se recarga la página: el envío va en segundo plano y la
    confirmación sale ahí mismo,
  · si el envío falla, se le abre el correo con los datos ya escritos, para
    que ningún registro se pierda por un fallo de red.

Qué hace falta para que funcione:

  1. Montar la hoja y desplegar el script (guía aparte, GUIA-REGISTROS.md).
  2. Pegar la URL del despliegue en assets/js/data-alojamientos.js →
     CONFIG.endpointFormularios. Mientras esté vacía, los formularios siguen
     funcionando pero por correo, no contra la hoja.

IMPORTANTE: este parche sustituye la parte de formularios de los parches 1 a
4, así que al terminar los mueve a _build/parches-aplicados/ para que nadie
los vuelva a ejecutar por encima.

Se ejecuta desde la raíz del proyecto:   python3 _build/parche-5.py
Después hay que recompilar:              python3 _build/build.py

Idempotente: volver a ejecutarlo no cambia nada.
"""

import os, re, sys, io, shutil

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


def quitar_re(rel, patron):
    """Borra por expresión regular. Idempotente: si ya no casa, no hace nada."""
    global hechos
    ruta = os.path.join(RAIZ, rel)
    if not os.path.exists(ruta):
        fallos.append("NO EXISTE: " + rel); return
    txt = io.open(ruta, encoding="utf-8").read()
    nuevo, n = re.subn(patron, "", txt)
    if n:
        io.open(ruta, "w", encoding="utf-8").write(nuevo)
        hechos += n


# ===========================================================================
# 1 · Dónde se configura el destino de los formularios
# ===========================================================================
ed("assets/js/data-alojamientos.js", [
    ('  emailContacto: "km0week@hosbec.com",',
     '  emailContacto: "km0week@hosbec.com",\n'
     '\n'
     '  // ---------------------------------------------------------------------\n'
     '  // A dónde van los formularios (boletín y alta de alojamientos).\n'
     '  // Pega aquí la URL que da Google al desplegar el Apps Script; termina\n'
     '  // siempre en /exec. Mientras esté vacía, los formularios siguen\n'
     '  // funcionando, pero abriendo el correo del visitante en vez de\n'
     '  // escribir en la hoja.\n'
     '  //   Ejemplo: "https://script.google.com/macros/s/AKfycb.../exec"\n'
     '  // ---------------------------------------------------------------------\n'
     '  endpointFormularios: "",\n'
     '\n'
     '  // La misma contraseña que hay en el Apps Script, en CONFIG.token.\n'
     '  tokenFormularios: "km0week-2026",',
     'endpointFormularios'),
])


# ===========================================================================
# 2 · El boletín del pie vuelve a ser un formulario limpio
# ===========================================================================
ed("_build/build.py", [
    ('''        <form class="subscribe" id="form-boletin" action="https://formsubmit.co/{EMAIL_KM0}" method="POST">
          <input type="hidden" name="_subject" value="[Km0 Week] Boletín · nueva alta">
          <input type="hidden" name="_template" value="table">
          <input type="hidden" name="_next" value="{vuelta}">
          <input type="hidden" name="_autoresponse" value="{ACUSE_BOLETIN}">
          <input type="text" name="_honey" style="display:none" tabindex="-1" autocomplete="off" aria-hidden="true">
          <input type="email" name="email" required placeholder="tu@correo.com" aria-label="Correo">
          <button class="btn btn-terra btn-sm" type="submit" data-va="Avisa'm">Avísame</button>
        </form>''',
     '''        <form class="subscribe" id="form-boletin" novalidate>
          <input type="text" name="_honey" style="display:none" tabindex="-1" autocomplete="off" aria-hidden="true">
          <input type="email" name="email" required placeholder="tu@correo.com" aria-label="Correo">
          <button class="btn btn-terra btn-sm" type="submit" data-va="Avisa'm">Avísame</button>
        </form>'''),
])

# la vuelta de FormSubmit ya no hace falta
quitar_re("_build/build.py",
          r'    # a dónde vuelve el visitante después de apuntarse al boletín: a la misma\n'
          r'    # página en la que estaba, con \?boletin=1 para que salga la confirmación\n'
          r'    vuelta = DOMINIO \+ "/" \+ \("" if p\["archivo"\] == "index\.html" else p\["archivo"\]\) \+ "\?boletin=1"\n')

quitar_re("_build/build.py",
          r'\n# Texto del acuse de recibo automático que FormSubmit envía a quien se\n'
          r'# apunta al boletín\. Sin acentos raros ni HTML: va como texto plano\.\n'
          r'ACUSE_BOLETIN = \(\n    "[^"]*"\n\)\n')


# ===========================================================================
# 3 · El boletín de Noticias, igual
# ===========================================================================
quitar_re("_build/paginas/noticias.html",
          r'\n *action="https://formsubmit\.co/km0week@hosbec\.com" method="POST">'
          r'\n *<input type="hidden" name="_subject"[^>]*>'
          r'\n *<input type="hidden" name="_template"[^>]*>'
          r'\n *<input type="hidden" name="_next"[^>]*>'
          r'\n *<input type="hidden" name="_autoresponse"[^>]*>')

ed("_build/paginas/noticias.html", [
    ('<form class="subscribe mt-2" style="justify-content:center;max-width:440px;margin-inline:auto"\n'
     '      <input type="text" name="_honey"',
     '<form class="subscribe mt-2" style="justify-content:center;max-width:440px;margin-inline:auto" novalidate>\n'
     '      <input type="text" name="_honey"',
     'margin-inline:auto" novalidate>'),
])


# ===========================================================================
# 4 · El alta de alojamiento deja de ir a FormSubmit
# ===========================================================================
ed("_build/paginas/suma.html", [
    ('''    <!-- El envío lo hace FormSubmit: reenvía el contenido por correo a
         km0week@hosbec.com. No guarda nada ni requiere servidor propio. -->
    <form class="form-grid" id="form-suma" novalidate
          action="https://formsubmit.co/km0week@hosbec.com" method="POST">
      <input type="hidden" name="_subject" value="[Km0 Week] Alojamiento · nueva solicitud">
      <input type="hidden" name="_template" value="table">''',
     '''    <!-- El envío lo recoge assets/js/home.js y lo manda al Apps Script, que
         escribe la fila en la hoja de registros y manda los dos correos. -->
    <form class="form-grid" id="form-suma" novalidate>'''),
])

quitar_re("_build/paginas/suma.html",
          r'\n *<input type="hidden" name="_autoresponse" value="Hemos recibido[^"]*">'
          r'\n *<input type="hidden" name="_next" value="[^"]*">')

ed("_build/paginas/suma.html", [
    ('<p class="ayuda mt-1" data-va="En enviar-lo ens arriba un correu a km0week@hosbec.com amb aquestes dades. No es guarden en cap altre lloc.">Al enviarlo nos llega un correo a km0week@hosbec.com con estos datos. No se guardan en ningún otro sitio.</p>',
     '<p class="ayuda mt-1" data-va="En enviar-lo, les teues dades queden registrades i ens arriba un avís a km0week@hosbec.com. Tu reps a l\'instant un acusament de recepció.">Al enviarlo, tus datos quedan registrados y nos llega un aviso a km0week@hosbec.com. Tú recibes al instante un acuse de recibo.</p>'),
])


# ===========================================================================
# 5 · El JavaScript: un único envío para los tres formularios
# ===========================================================================
ENVIO = r'''  /* ------------------------- envío de formularios -------------------------
     Todo va al Apps Script de la hoja de registros. Tres intentos en cascada,
     para que un registro no se pierda nunca:

       1. fetch normal leyendo la respuesta (así sabemos de verdad si ha ido
          bien). Se manda como text/plain a propósito: es una «petición
          simple» y evita el preflight, que Apps Script no sabe contestar.
       2. si eso falla por CORS o por red, se reintenta en modo no-cors: llega
          igual, aunque no podamos leer la contestación.
       3. si tampoco, se abre el correo del visitante con los datos escritos.

     Mientras CFG.endpointFormularios esté vacío se va directo al paso 3. */

  function datosComunes() {
    return {
      _token: CFG.tokenFormularios || "",
      idioma: LANG,
      origen: location.href
    };
  }

  async function enviarRegistro(datos) {
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
  }

  // Plan C: abrir el gestor de correo con todo escrito
  function porCorreo(asunto, lineas) {
    location.href = "mailto:" + (CFG.emailContacto || "km0week@hosbec.com") +
      "?subject=" + encodeURIComponent(asunto) +
      "&body=" + encodeURIComponent(lineas.filter(Boolean).join("\n"));
  }

'''

ed("assets/js/home.js", [
    ('  /* ------------------------- boletín «Te avisamos» ------------------------', ENVIO +
     '  /* ------------------------- boletín «Te avisamos» ------------------------',
     'envío de formularios'),

    # -- el boletín ---------------------------------------------------------
    ('''  function montarUnBoletin(f) {
    if (!f || f.dataset.listo) return;
    f.dataset.listo = "1";
    f.addEventListener("submit", e => {
      if (!f.checkValidity()) { e.preventDefault(); f.reportValidity(); return; }
      const btn = f.querySelector("button");
      if (btn) { btn.disabled = true; btn.textContent = t("enviando"); }
      // sin preventDefault: lo envía el navegador a FormSubmit, que nos manda
      // el correo, envía el acuse de recibo y devuelve aquí con ?boletin=1
    });
  }''',
     '''  function montarUnBoletin(f) {
    if (!f || f.dataset.listo) return;
    f.dataset.listo = "1";
    f.addEventListener("submit", async e => {
      e.preventDefault();
      if (!f.checkValidity()) { f.reportValidity(); return; }

      const btn = f.querySelector("button");
      const texto = btn ? btn.textContent : "";
      if (btn) { btn.disabled = true; btn.textContent = t("enviando"); }

      const email = (f.querySelector("input[type=email]") || {}).value || "";
      const r = await enviarRegistro({
        formulario: "boletin",
        email: email,
        _honey: (f.querySelector("[name=_honey]") || {}).value || ""
      });

      if (btn) { btn.disabled = false; btn.textContent = texto; }

      if (r === "ok") { f.reset(); toast(t("boletinOk")); }
      else if (r === "correo") {
        porCorreo("[Km0 Week] Alta en el boletín", [
          email,
          LANG === "va" ? "Vull que m'aviseu quan s'òbriguen les reserves."
                        : "Quiero que me aviséis cuando se abran las reservas."
        ]);
      } else toast(t("falloEnvio"));
    });
  }'''),

    # -- el alta de alojamiento --------------------------------------------
    ('''    // vuelta de FormSubmit después de apuntarse al boletín
    if (new URLSearchParams(location.search).has("boletin")) {
      toast(t("boletinOk"));
      history.replaceState(null, "", location.pathname + location.hash);
    }
    const f = $("#form-suma"); if (!f) return;

    // Al volver de FormSubmit (?enviado=1) confirmamos y limpiamos la URL.
    if (new URLSearchParams(location.search).has("enviado")) {
      const ok = $("#form-ok"); if (ok) ok.hidden = false;
      toast(t("enviado"));
      history.replaceState(null, "", location.pathname + location.hash);
      if (ok) ok.scrollIntoView({ behavior: "smooth", block: "center" });
    }

    f.addEventListener("submit", e => {
      if (!f.checkValidity()) { e.preventDefault(); toast(t("faltan")); f.reportValidity(); return; }
      const b = f.querySelector('button[type="submit"]');
      if (b) { b.disabled = true; b.textContent = t("enviando"); }
      // sin preventDefault: el navegador envía el formulario a FormSubmit,
      // que reenvía el contenido por correo a km0week@hosbec.com
    });
  }''',
     '''    const f = $("#form-suma"); if (!f) return;

    f.addEventListener("submit", async e => {
      e.preventDefault();
      if (!f.checkValidity()) { toast(t("faltan")); f.reportValidity(); return; }

      const b = f.querySelector('button[type="submit"]');
      const texto = b ? b.textContent : "";
      if (b) { b.disabled = true; b.textContent = t("enviando"); }

      const v = n => { const el = f.querySelector("[name=" + n + "]"); return el ? el.value.trim() : ""; };
      const datos = {
        formulario: "alojamiento",
        nombre: v("nombre"), municipio: v("municipio"), tipo: v("tipo"),
        cupo: v("cupo"), contacto: v("contacto"), email: v("email"),
        telefono: v("telefono"), web: v("web"), oferta: v("oferta"),
        acepto: !!f.querySelector("[name=acepto]:checked"),
        _honey: v("_honey")
      };

      const r = await enviarRegistro(datos);
      if (b) { b.disabled = false; b.textContent = texto; }

      if (r === "ok") {
        const ok = $("#form-ok");
        if (ok) { ok.hidden = false; ok.scrollIntoView({ behavior: "smooth", block: "center" }); }
        toast(t("enviado"));
        f.reset();
      } else if (r === "correo") {
        porCorreo("[Km0 Week] Solicitud de alojamiento: " + (datos.nombre || datos.email), [
          "Alojamiento: " + datos.nombre,
          "Municipio: " + datos.municipio,
          "Tipo: " + datos.tipo,
          "Plazas comprometidas: " + datos.cupo,
          "Persona de contacto: " + datos.contacto,
          "Correo: " + datos.email,
          "Teléfono: " + datos.telefono,
          "Web: " + datos.web,
          "",
          "Oferta propuesta:",
          datos.oferta
        ]);
      } else toast(t("falloEnvio"));
    });
  }'''),

    # -- textos nuevos ------------------------------------------------------
    ('      boletinOk: "¡Listo! Te avisaremos por correo.",',
     '      boletinOk: "¡Listo! Te avisaremos por correo.",\n'
     '      falloEnvio: "No hemos podido enviarlo. Escríbenos a km0week@hosbec.com.",'),
    ('      boletinOk: "Fet! T\'avisarem per correu.",',
     '      boletinOk: "Fet! T\'avisarem per correu.",\n'
     '      falloEnvio: "No hem pogut enviar-ho. Escriu-nos a km0week@hosbec.com.",'),
])


# ===========================================================================
# 6 · Privacidad y cookies: el encargado ya no es FormSubmit, es Google
# ===========================================================================
ed("_build/paginas/privacidad.html", [
    ('<p data-va="L\'única excepció són els dos formularis. Quan n\'envies un, el contingut passa per FormSubmit (formsubmit.co), un servei que es limita a reenviar-nos-ho per correu a km0week@hosbec.com i que actua com a encarregat del tractament. Si prefereixes no fer-lo servir, escriu-nos directament a aqueixa adreça.">La única excepción son los dos formularios. Cuando envías uno, su contenido pasa por FormSubmit (formsubmit.co), un servicio que se limita a reenviárnoslo por correo a km0week@hosbec.com y que actúa como encargado del tratamiento. Si prefieres no usarlo, escríbenos directamente a esa dirección.</p>',
     '<p data-va="L\'única excepció són els dos formularis. En enviar-ne un, les dades viatgen a Google (Apps Script i Google Sheets), on es guarden en un full de càlcul d\'HOSBEC i des d\'on s\'envien els dos correus: l\'avís intern i el teu acusament de recepció. Google actua com a encarregat del tractament. Si prefereixes no fer-ho servir, escriu-nos directament a km0week@hosbec.com.">La única excepción son los dos formularios. Al enviar uno, los datos viajan a Google (Apps Script y Google Sheets), donde se guardan en una hoja de cálculo de HOSBEC y desde donde se envían los dos correos: el aviso interno y tu acuse de recibo. Google actúa como encargado del tratamiento. Si prefieres no usarlo, escríbenos directamente a km0week@hosbec.com.</p>'),

    ('<p data-va="En enviar un formulari, FormSubmit mostra una comprovació anti-robots (reCAPTCHA de Google) en el seu propi lloc, no en aquest. Aqueixa comprovació la carrega formsubmit.co; ací no s\'executa cap script de Google. També t\'enviem un acusament de recepció automàtic a l\'adreça que ens deixes.">Al enviar un formulario, FormSubmit muestra una comprobación anti-robots (reCAPTCHA de Google) en su propio sitio, no en este. Esa comprobación la carga formsubmit.co; aquí no se ejecuta ningún script de Google. También te enviamos un acuse de recibo automático a la dirección que nos dejes.</p>',
     '<p data-va="No hi ha cap comprovació anti-robots ni cap script de Google carregat en aquesta web: l\'enviament es fa en segon pla i la teua navegació no ix d\'ací. Els correus que et puguen arribar (l\'acusament de recepció i, si t\'apuntes al butlletí, els avisos) els envia HOSBEC.">No hay ninguna comprobación anti-robots ni ningún script de Google cargado en esta web: el envío se hace en segundo plano y tu navegación no sale de aquí. Los correos que puedas recibir (el acuse de recibo y, si te apuntas al boletín, los avisos) los envía HOSBEC.</p>'),
])

ed("_build/paginas/privacidad.html", [
    ('<strong data-va="Butlletí:">Boletín:</strong> solo la dirección de correo que escribes en el formulario «Te avisamos».',
     '<strong data-va="Butlletí:">Boletín:</strong> solo la dirección de correo que escribes en el formulario «Te avisamos», junto con la fecha y el idioma en el que navegabas.'),
], obligatorio=False)


# ===========================================================================
# 7 · Los parches 1 a 4 quedan superados: se apartan para no reejecutarlos
# ===========================================================================
destino = os.path.join(RAIZ, "_build", "parches-aplicados")
movidos = []
for n in ("parche.py", "parche-2.py", "parche-3.py", "parche-4.py"):
    origen = os.path.join(RAIZ, "_build", n)
    if os.path.exists(origen):
        if not os.path.isdir(destino):
            os.makedirs(destino)
        shutil.move(origen, os.path.join(destino, n))
        movidos.append(n)


# ===========================================================================
print("cambios aplicados:", hechos)
if movidos:
    print("apartados a _build/parches-aplicados/:", ", ".join(movidos))
if fallos:
    print("\n⚠  revisar (%d):" % len(fallos))
    for f in fallos:
        print("   ·", f)
    sys.exit(1)
print("todo correcto. Ahora:  python3 _build/build.py")
