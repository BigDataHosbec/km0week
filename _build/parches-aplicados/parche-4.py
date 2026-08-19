#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Parche Km0 Week — cuarta tanda, 18/08/2026
==========================================
Acuse de recibo automático en los dos formularios.

FormSubmit solo manda el acuse (`_autoresponse`) si el formulario lleva su
reCAPTCHA y NO se envía por AJAX. Su documentación es explícita:
«autoresponse won't work with forms that are disabled reCAPTCHA and forms
that are submitting through AJAX».

Consecuencias, que conviene tener presentes:

  · Alta de alojamiento  → se quita `_captcha=false`. Al enviar aparece un
    paso de reCAPTCHA en formsubmit.co y luego vuelve a suma.html?enviado=1.
  · Boletín «Te avisamos» → deja de enviarse en segundo plano. Pasa a ser un
    envío normal con reCAPTCHA que devuelve a la MISMA página con ?boletin=1,
    donde sale el aviso de confirmación. El `_next` lo calcula build.py para
    cada página, así que nadie acaba en la portada por error.

Si algún día se prefiere volver al envío silencioso del boletín, basta con
deshacer el punto 2 de este parche y recuperar el bloque AJAX del parche 1.

Se ejecuta desde la raíz del proyecto:   python3 _build/parche-4.py
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
# 1 · Alta de alojamiento: reCAPTCHA + acuse de recibo
# ===========================================================================
ACUSE_ALTA = (
    "Hemos recibido tu solicitud para sumar tu alojamiento a la HOSBEC Km0 Week "
    "(13 - 29 de noviembre de 2026). Le echamos un vistazo y te respondemos en 48 horas "
    "laborables con el siguiente paso. Si necesitas algo antes, escribe a km0week@hosbec.com "
    "o llama al 965 85 55 16. -- Hem rebut la teua sol.licitud per a sumar el teu allotjament "
    "a la HOSBEC Km0 Week. Et responem en 48 hores laborables. "
    "-- HOSBEC, Associacio Empresarial Hotelera i Turistica de la Comunitat Valenciana."
)

ed("_build/paginas/suma.html", [
    ('      <input type="hidden" name="_captcha" value="false">\n',
     '      <input type="hidden" name="_autoresponse" value="%s">\n' % ACUSE_ALTA,
     '_autoresponse'),
])


# ===========================================================================
# 2 · Boletín: envío normal (con reCAPTCHA y acuse) en vez de AJAX
# ===========================================================================
ACUSE_BOLETIN = (
    "Gracias por apuntarte al aviso de la HOSBEC Km0 Week. Te escribiremos cuando se abran "
    "las reservas y otra vez con el programa cerrado de los tres fines de semana "
    "(13 - 29 de noviembre de 2026). Nada mas: ni promociones de terceros, ni listas compartidas. "
    "Para darte de baja, responde a este correo. "
    "-- Gracies per apuntar-te a l'avis de la HOSBEC Km0 Week. "
    "-- HOSBEC, Associacio Empresarial Hotelera i Turistica de la Comunitat Valenciana."
)

# 2.1 · el pie necesita saber en qué página está para volver a ella
ed("_build/build.py", [
    ('def pie():\n    cols = ""', 'def pie(p):\n    cols = ""', 'def pie(p):'),
    ('            pie() + scripts(p))', '            pie(p) + scripts(p))'),

    ('''        <form class="subscribe" id="form-boletin">
          <input type="email" name="email" required placeholder="tu@correo.com" aria-label="Correo">
          <button class="btn btn-terra btn-sm" type="submit" data-va="Avisa'm">Avísame</button>
        </form>''',
     '''        <form class="subscribe" id="form-boletin" action="https://formsubmit.co/{EMAIL_KM0}" method="POST">
          <input type="hidden" name="_subject" value="[Km0 Week] Boletín · nueva alta">
          <input type="hidden" name="_template" value="table">
          <input type="hidden" name="_next" value="{vuelta}">
          <input type="hidden" name="_autoresponse" value="{ACUSE_BOLETIN}">
          <input type="text" name="_honey" style="display:none" tabindex="-1" autocomplete="off" aria-hidden="true">
          <input type="email" name="email" required placeholder="tu@correo.com" aria-label="Correo">
          <button class="btn btn-terra btn-sm" type="submit" data-va="Avisa'm">Avísame</button>
        </form>'''),

    ('''def pie(p):
    cols = ""''',
     '''def pie(p):
    # a dónde vuelve el visitante después de apuntarse al boletín: a la misma
    # página en la que estaba, con ?boletin=1 para que salga la confirmación
    vuelta = DOMINIO + "/" + ("" if p["archivo"] == "index.html" else p["archivo"]) + "?boletin=1"
    cols = ""''',
     'a dónde vuelve el visitante'),
])

# 2.2 · las constantes del correo, arriba del todo junto a DOMINIO
ed("_build/build.py", [
    ('FECHAS_ES = "13 – 29 de noviembre de 2026"',
     'EMAIL_KM0 = "km0week@hosbec.com"\n'
     '\n'
     '# Texto del acuse de recibo automático que FormSubmit envía a quien se\n'
     '# apunta al boletín. Sin acentos raros ni HTML: va como texto plano.\n'
     'ACUSE_BOLETIN = (\n'
     '    "%s"\n'
     ')\n'
     '\n'
     'FECHAS_ES = "13 – 29 de noviembre de 2026"' % ACUSE_BOLETIN,
     'EMAIL_KM0 ='),
])

# 2.3 · el boletín de la página de Noticias, igual
ed("_build/paginas/noticias.html", [
    ('''    <form class="subscribe mt-2" style="justify-content:center;max-width:440px;margin-inline:auto">
      <input type="email" name="email" required placeholder="tu@correo.com" aria-label="Correo">''',
     '''    <form class="subscribe mt-2" style="justify-content:center;max-width:440px;margin-inline:auto"
          action="https://formsubmit.co/km0week@hosbec.com" method="POST">
      <input type="hidden" name="_subject" value="[Km0 Week] Boletín · nueva alta">
      <input type="hidden" name="_template" value="table">
      <input type="hidden" name="_next" value="@@DOMINIO@@/noticias.html?boletin=1">
      <input type="hidden" name="_autoresponse" value="%s">
      <input type="text" name="_honey" style="display:none" tabindex="-1" autocomplete="off" aria-hidden="true">
      <input type="email" name="email" required placeholder="tu@correo.com" aria-label="Correo">''' % ACUSE_BOLETIN),
])

# 2.4 · el JS deja de interceptar el envío y solo confirma a la vuelta
ed("assets/js/home.js", [
    ('''  function montarUnBoletin(f) {
    if (!f || f.dataset.listo) return;
    f.dataset.listo = "1";
    f.addEventListener("submit", async e => {
      e.preventDefault();
      const campo = f.querySelector("input[type=email]");
      if (!f.checkValidity()) { f.reportValidity(); return; }
      const btn = f.querySelector("button"); const texto = btn ? btn.textContent : "";
      if (btn) { btn.disabled = true; btn.textContent = t("enviando"); }
      try {
        const r = await fetch("https://formsubmit.co/ajax/" + (CFG.emailContacto || "km0week@hosbec.com"), {
          method: "POST",
          headers: { "Content-Type": "application/json", Accept: "application/json" },
          body: JSON.stringify({
            _subject: "[Km0 Week] Boletín · nueva alta",
            _captcha: "false",
            email: campo ? campo.value : "",
            origen: location.href
          })
        });
        if (!r.ok) throw new Error(r.status);
        f.reset();
        toast(LANG === "va" ? "Gràcies! T'avisarem." : "¡Gracias! Te avisaremos.");
      } catch (_) {
        location.href = "mailto:" + (CFG.emailContacto || "km0week@hosbec.com") +
          "?subject=" + encodeURIComponent("[Km0 Week] Boletín · nueva alta") +
          "&body=" + encodeURIComponent((campo ? campo.value : "") + "\\n\\nQuiero que me aviséis cuando se abran las reservas.");
      } finally {
        if (btn) { btn.disabled = false; btn.textContent = texto; }
      }
    });
  }''',
     '''  function montarUnBoletin(f) {
    if (!f || f.dataset.listo) return;
    f.dataset.listo = "1";
    f.addEventListener("submit", e => {
      if (!f.checkValidity()) { e.preventDefault(); f.reportValidity(); return; }
      const btn = f.querySelector("button");
      if (btn) { btn.disabled = true; btn.textContent = t("enviando"); }
      // sin preventDefault: lo envía el navegador a FormSubmit, que nos manda
      // el correo, envía el acuse de recibo y devuelve aquí con ?boletin=1
    });
  }'''),

    ('''  function montarFormulario() {
    montarBoletin();''',
     '''  function montarFormulario() {
    montarBoletin();

    // vuelta de FormSubmit después de apuntarse al boletín
    if (new URLSearchParams(location.search).has("boletin")) {
      toast(t("boletinOk"));
      history.replaceState(null, "", location.pathname + location.hash);
    }'''),

    ('      soloFinde: "Solo fines de semana", enviando: "Enviando…", sinActos: "sin actividades",',
     '      soloFinde: "Solo fines de semana", enviando: "Enviando…", sinActos: "sin actividades",\n'
     '      boletinOk: "¡Listo! Te avisaremos por correo.",'),
    ('      soloFinde: "Només caps de setmana", enviando: "Enviant…", sinActos: "sense activitats",',
     '      soloFinde: "Només caps de setmana", enviando: "Enviant…", sinActos: "sense activitats",\n'
     '      boletinOk: "Fet! T\'avisarem per correu.",'),
])


# ===========================================================================
# 3 · Privacidad al día: ahora aparece el reCAPTCHA de Google en el paso de envío
# ===========================================================================
ed("_build/paginas/privacidad.html", [
    ('Si prefieres no usarlo, escríbenos directamente a esa dirección.</p>',
     'Si prefieres no usarlo, escríbenos directamente a esa dirección.</p>\n'
     '      <p data-va="En enviar un formulari, FormSubmit mostra una comprovació anti-robots (reCAPTCHA de Google) en el seu propi lloc, no en aquest. Aqueixa comprovació la carrega formsubmit.co; ací no s\'executa cap script de Google. També t\'enviem un acusament de recepció automàtic a l\'adreça que ens deixes.">Al enviar un formulario, FormSubmit muestra una comprobación anti-robots (reCAPTCHA de Google) en su propio sitio, no en este. Esa comprobación la carga formsubmit.co; aquí no se ejecuta ningún script de Google. También te enviamos un acuse de recibo automático a la dirección que nos dejes.</p>'),
])


# ===========================================================================
print("cambios aplicados:", hechos)
if fallos:
    print("\n⚠  revisar (%d):" % len(fallos))
    for f in fallos:
        print("   ·", f)
    sys.exit(1)
print("todo correcto. Ahora:  python3 _build/build.py")
