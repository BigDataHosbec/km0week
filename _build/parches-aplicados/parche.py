#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Parche Km0 Week — 18/08/2026
============================
Aplica de una vez los cambios pedidos por Jorge sobre HOSBEC-Km0-Week-MASTER:

 1. Cifras de portada: quita la colisión de la clase `.nota` (la burbuja recortada)
 2. Fechas: del 13 al 29 de noviembre de 2026 (tres fines de semana) en todas partes
 3. «La iniciativa» → ritmo vertical en los bloques `.parte`
 4. Alojamientos → filtros reorganizados por grupos y diferenciados por color
 5. Noticias → imágenes con proporción correcta (height:auto)
 6. Formulario → envío real por correo a km0week@hosbec.com (FormSubmit)
 7. Teléfono 965 85 55 16 y redes @hosbeconline en el pie

Se ejecuta desde la raíz del proyecto:   python3 _build/parche.py
Después hay que recompilar:              python3 _build/build.py

Es idempotente: si un texto ya está cambiado, lo salta y avisa.
"""

import os, sys, io

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
fallos, hechos = [], 0


def ed(rel, pares, obligatorio=True):
    """Aplica una lista de (viejo, nuevo) sobre un archivo."""
    global hechos
    ruta = os.path.join(RAIZ, rel)
    if not os.path.exists(ruta):
        fallos.append("NO EXISTE: " + rel); return
    txt = original = io.open(ruta, encoding="utf-8").read()
    for par in pares:
        # Un par puede llevar un tercer elemento: un trozo de texto que sirve de
        # marca de «esto ya está aplicado». Hace falta cuando un cambio posterior
        # retoca lo que este mismo parche había insertado.
        viejo, nuevo = par[0], par[1]
        marca = par[2] if len(par) > 2 else nuevo
        # Primero lo primero: si la marca ya está, este cambio está hecho.
        # (Muchos «nuevo» contienen al «viejo» dentro, así que comprobar el viejo
        #  antes haría que el parche se aplicara otra vez encima de sí mismo.)
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
# 1 · build.py — fechas, pie, teléfono, redes, metadatos
# ===========================================================================
ed("_build/build.py", [
    # -- fechas -------------------------------------------------------------
    ('FECHAS_ES = "13 – 19 de noviembre de 2026"',
     'FECHAS_ES = "13 – 29 de noviembre de 2026"'),
    ('FECHAS_VA = "13 – 19 de novembre de 2026"',
     'FECHAS_VA = "13 – 29 de novembre de 2026"'),

    # -- token @@DOMINIO@@ utilizable dentro de _build/paginas/*.html --------
    ('    cuerpo = open(os.path.join(PAGS, p["cuerpo"]), encoding="utf-8").read()',
     '    cuerpo = open(os.path.join(PAGS, p["cuerpo"]), encoding="utf-8").read()\n'
     '    # las páginas pueden escribir @@DOMINIO@@ y aquí se sustituye\n'
     '    cuerpo = cuerpo.replace("@@DOMINIO@@", DOMINIO)'),

    # -- columna del pie ----------------------------------------------------
    ('    ("La semana", "La setmana", [', '    ("La edición", "L\'edició", ['),

    # -- metadatos ----------------------------------------------------------
    ('desc="Del 13 al 19 de noviembre de 2026. Una semana para que quienes vivimos en la Comunitat Valenciana redescubramos nuestros alojamientos. Ofertas para residentes y reserva directa.",',
     'desc="Del 13 al 29 de noviembre de 2026. Tres fines de semana para que quienes vivimos en la Comunitat Valenciana redescubramos nuestros alojamientos. Ofertas para residentes y reserva directa.",'),
    ('("Una semana para mirar de otra forma lo que tenemos al lado",\n                "Una setmana per a mirar d\'una altra manera el que tenim al costat"),',
     '("Tres fines de semana para mirar de otra forma lo que tenemos al lado",\n                "Tres caps de setmana per a mirar d\'una altra manera el que tenim al costat"),'),
    ('("Km0 Week nace de una idea simple: quien vive en un destino turístico casi nunca lo disfruta como tal. Del 13 al 19 de noviembre le damos la vuelta.",\n                "Km0 Week naix d\'una idea simple: qui viu en un destí turístic quasi mai el gaudeix com a tal. Del 13 al 19 de novembre li donem la volta."))),',
     '("Km0 Week nace de una idea simple: quien vive en un destino turístico casi nunca lo disfruta como tal. Del 13 al 29 de noviembre le damos la vuelta.",\n                "Km0 Week naix d\'una idea simple: qui viu en un destí turístic quasi mai el gaudeix com a tal. Del 13 al 29 de novembre li donem la volta."))),'),
    ('titulo="Agenda de la semana · HOSBEC Km0 Week",',
     'titulo="Agenda de la edición · HOSBEC Km0 Week",'),
    ('desc="Programa día a día de la Km0 Week: visitas, talleres, rutas y actividades abiertas a todo el mundo, del 13 al 19 de noviembre de 2026.",',
     'desc="Programa día a día de la Km0 Week: visitas, talleres, rutas y actividades abiertas a todo el mundo, del 13 al 29 de noviembre de 2026.",'),
    ('("Siete días, algo que hacer cada día", "Set dies, alguna cosa a fer cada dia"),',
     '("Diecisiete días, algo que hacer cada fin de semana", "Dèsset dies, alguna cosa a fer cada cap de setmana"),'),
    ('"El compromiso de la Km0 Week es que el precio de la semana sea el más bajo del trimestre. Explicamos cómo se comprueba."',
     '"El compromiso de la Km0 Week es que el precio de esos días sea el más bajo del trimestre. Explicamos cómo se comprueba."'),
    ('"Visitas a espacios normalmente cerrados, rutas guiadas y talleres que se abren solo durante la semana."',
     '"Visitas a espacios normalmente cerrados, rutas guiadas y talleres que se abren solo durante la Km0 Week."'),

    # -- boletín del pie: envío real por AJAX -------------------------------
    ('''        <form class="subscribe" onsubmit="event.preventDefault();this.reset();window.Km0.toast(window.Km0.lang==='va'?'Gràcies! T\\\\'avisarem.':'¡Gracias! Te avisaremos.');">
          <input type="email" required placeholder="tu@correo.com" aria-label="Correo">
          <button class="btn btn-terra btn-sm" type="submit" data-va="Avisa'm">Avísame</button>
        </form>''',
     '''        <form class="subscribe" id="form-boletin">
          <input type="email" name="email" required placeholder="tu@correo.com" aria-label="Correo">
          <button class="btn btn-terra btn-sm" type="submit" data-va="Avisa'm">Avísame</button>
        </form>'''),

    # -- pie: teléfono correcto + redes sociales ----------------------------
    ('''      <span>km0week@hosbec.com · 965 85 51 12</span>
    </div>''',
     '''      <span class="foot-contacto">
        <a href="mailto:km0week@hosbec.com">km0week@hosbec.com</a>
        <a href="tel:+34965855516">965 85 55 16</a>
      </span>
    </div>
    <div class="foot-redes">
      <span class="body-sm" data-va="Segueix HOSBEC">Sigue a HOSBEC</span>
      <a href="https://www.instagram.com/hosbeconline/" target="_blank" rel="noopener" aria-label="Instagram de HOSBEC" title="Instagram">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.4" cy="6.6" r="1.1" fill="currentColor" stroke="none"/></svg>
      </a>
      <a href="https://www.linkedin.com/company/hosbeconline/" target="_blank" rel="noopener" aria-label="LinkedIn de HOSBEC" title="LinkedIn">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="3"/><path d="M7.5 10.5v6M7.5 7.6v.1M11.5 16.5v-6M11.5 13.2c0-1.5.9-2.4 2.2-2.4s2.3.9 2.3 2.6v3.1"/></svg>
      </a>
      <a href="https://www.facebook.com/Hosbeconline/" target="_blank" rel="noopener" aria-label="Facebook de HOSBEC" title="Facebook">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="4"/><path d="M15.2 8.2h-1.3c-.9 0-1.5.6-1.5 1.5v1.6h2.6l-.4 2.6h-2.2v5"/><path d="M10.3 11.3h2.1"/></svg>
      </a>
      <a href="https://x.com/hosbeconline" target="_blank" rel="noopener" aria-label="X de HOSBEC" title="X">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 4l16 16M20 4L4 20"/></svg>
      </a>
      <a href="https://www.youtube.com/@hosbeconline" target="_blank" rel="noopener" aria-label="YouTube de HOSBEC" title="YouTube">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2.6" y="5.6" width="18.8" height="12.8" rx="4"/><path d="M10.4 9.6l4.4 2.4-4.4 2.4z"/></svg>
      </a>
    </div>''', 'foot-redes'),
])


# ===========================================================================
# 2 · data-alojamientos.js — fechas, teléfono y reparto de la agenda
# ===========================================================================
ed("assets/js/data-alojamientos.js", [
    ('fechaFin:    "2026-11-19T23:59:59+01:00",', 'fechaFin:    "2026-11-29T23:59:59+01:00",'),
    ('fechasTexto: { es: "13 – 19 de noviembre de 2026", va: "13 – 19 de novembre de 2026" },',
     'fechasTexto: { es: "13 – 29 de noviembre de 2026", va: "13 – 29 de novembre de 2026" },'),
    ('telefonoContacto: "965 85 51 12",', 'telefonoContacto: "965 85 55 16",'),
    ('condiciones: { es: "Válido del 13 al 19 de noviembre. Plazas limitadas. Acreditar residencia en la Comunitat Valenciana.", va: "Vàlid del 13 al 19 de novembre. Places limitades. Acreditar residència a la Comunitat Valenciana." }',
     'condiciones: { es: "Válido del 13 al 29 de noviembre. Plazas limitadas. Acreditar residencia en la Comunitat Valenciana.", va: "Vàlid del 13 al 29 de novembre. Places limitades. Acreditar residència a la Comunitat Valenciana." }'),
    ('   dia: 1..7 (día 1 = primer día de la semana Km0)',
     '   dia: 1..17 (día 1 = 13 de noviembre; día 17 = 29 de noviembre)\n'
     '   Los fines de semana son los días 1-3, 8-10 y 15-17.',
     'dia: 1..17'),

    # -- reparto: la mayoría de actividades caen en los tres fines de semana --
    ('{ dia: 4, hora: "09:30", lugar: "Oliva"',      '{ dia: 9, hora: "09:30", lugar: "Oliva"'),
    ('{ dia: 4, hora: "17:00", lugar: "Benidorm"',   '{ dia: 6, hora: "17:00", lugar: "Benidorm"'),
    ('{ dia: 5, hora: "10:30", lugar: "Elche"',      '{ dia: 10, hora: "10:30", lugar: "Elche"'),
    ('{ dia: 5, hora: "19:00", lugar: "Castelló de la Plana"', '{ dia: 8, hora: "19:00", lugar: "Castelló de la Plana"'),
    ('{ dia: 6, hora: "11:00", lugar: "Altea"',      '{ dia: 16, hora: "11:00", lugar: "Altea"'),
    ('{ dia: 6, hora: "21:00", lugar: "Torrevieja"', '{ dia: 9, hora: "21:00", lugar: "Torrevieja"'),
    ('{ dia: 7, hora: "12:00", lugar: "Gandia"',     '{ dia: 17, hora: "12:00", lugar: "Gandia"'),
    ('{ dia: 7, hora: "18:00", lugar: "Toda la Comunitat"', '{ dia: 17, hora: "18:00", lugar: "Toda la Comunitat"'),
])


# ===========================================================================
# 3 · home.js — agenda de 17 días, filtro de fines de semana y formularios
# ===========================================================================
ed("assets/js/home.js", [
    # -- textos -------------------------------------------------------------
    ('semana: "Toda la semana", gratis: "Gratis", verTodo: "Ver la semana entera",',
     'semana: "Todos los días", gratis: "Gratis", verTodo: "Ver los 17 días",\n'
     '      soloFinde: "Solo fines de semana", enviando: "Enviando…", sinActos: "sin actividades",'),
    ('semana: "Tota la setmana", gratis: "Gratis", verTodo: "Veure la setmana sencera",',
     'semana: "Tots els dies", gratis: "Gratis", verTodo: "Veure els 17 dies",\n'
     '      soloFinde: "Només caps de setmana", enviando: "Enviant…", sinActos: "sense activitats",'),

    # -- estado -------------------------------------------------------------
    ('  const AG = { dia: 0, gratis: false };     // dia 0 = toda la semana',
     '  const AG = { dia: 0, gratis: false, finde: false };   // dia 0 = todos los días'),

    ('  function fechaDia(n) {                     // n = 1..7 → Date local, sin líos de UTC\n'
     '    const [Y, M, DD] = CFG.fechaInicio.slice(0, 10).split("-").map(Number);\n'
     '    return new Date(Y, M - 1, DD + n - 1);\n'
     '  }',
     '  function fechaDia(n) {                     // n = 1..N → Date local, sin líos de UTC\n'
     '    const [Y, M, DD] = CFG.fechaInicio.slice(0, 10).split("-").map(Number);\n'
     '    return new Date(Y, M - 1, DD + n - 1);\n'
     '  }\n'
     '\n'
     '  // Cuántos días dura la edición: se deduce de fechaInicio y fechaFin.\n'
     '  function totalDias() {\n'
     '    const a = new Date(CFG.fechaInicio.slice(0, 10) + "T00:00:00");\n'
     '    const b = new Date((CFG.fechaFin || CFG.fechaInicio).slice(0, 10) + "T00:00:00");\n'
     '    return Math.max(1, Math.round((b - a) / 864e5) + 1);\n'
     '  }\n'
     '\n'
     '  const esFinde = n => [0, 6].includes(fechaDia(n).getDay());   // sábado o domingo',
     'function totalDias()'),

    # -- pintado de los días ------------------------------------------------
    ('''    cd.innerHTML = [0, 1, 2, 3, 4, 5, 6, 7].map(n => {
      if (!n) return "";
      const f = fechaDia(n);
      return `<button class="dia" type="button" data-d="${n}" aria-pressed="${AG.dia === n}">
        <span class="s">${t("dias")[(f.getDay() + 6) % 7]}</span>
        <span class="n">${f.getDate()}</span>
        <span class="s">${t("meses")[f.getMonth()].slice(0, 3)}</span>
      </button>`;
    }).join("");''',
     '''    const N = totalDias();
    const conActos = n => AGENDA.some(a => a.dia === n && (!AG.gratis || esGratis(a)));
    const dias = [];
    for (let n = 1; n <= N; n++) if (!AG.finde || esFinde(n)) dias.push(n);

    cd.innerHTML = dias.map(n => {
      const f = fechaDia(n), hay = conActos(n);
      const cls = ["dia", esFinde(n) ? "fds" : "", hay ? "" : "sin"].filter(Boolean).join(" ");
      return `<button class="${cls}" type="button" data-d="${n}" aria-pressed="${AG.dia === n}"${hay ? "" : ' disabled aria-disabled="true" title="' + t("sinActos") + '"'}>
        <span class="s">${t("dias")[(f.getDay() + 6) % 7]}</span>
        <span class="n">${f.getDate()}</span>
        <span class="s">${t("meses")[f.getMonth()].slice(0, 3)}</span>
      </button>`;
    }).join("");'''),

    ('      .filter(a => (!AG.dia || a.dia === AG.dia) && (!AG.gratis || esGratis(a)))',
     '      .filter(a => (!AG.dia || a.dia === AG.dia) && (!AG.gratis || esGratis(a)) && (!AG.finde || esFinde(a.dia)))'),

    ('''    const bg = $("#ag-gratis");
    if (bg) bg.setAttribute("aria-pressed", String(AG.gratis));''',
     '''    const bg = $("#ag-gratis");
    if (bg) bg.setAttribute("aria-pressed", String(AG.gratis));
    const bf = $("#ag-finde");
    if (bf) bf.setAttribute("aria-pressed", String(AG.finde));'''),

    ('''    const bg = $("#ag-gratis"); if (bg) bg.addEventListener("click", () => { AG.gratis = !AG.gratis; pintarAgenda(); });
    pintarAgenda();''',
     '''    const bg = $("#ag-gratis"); if (bg) bg.addEventListener("click", () => { AG.gratis = !AG.gratis; pintarAgenda(); });
    const bf = $("#ag-finde"); if (bf) bf.addEventListener("click", () => {
      AG.finde = !AG.finde;
      if (AG.finde && AG.dia && !esFinde(AG.dia)) AG.dia = 0;
      pintarAgenda();
    });
    pintarAgenda();'''),

    # -- formulario de alta: deja que el navegador envíe a FormSubmit --------
    ('''  function montarFormulario() {
    const f = $("#form-suma"); if (!f) return;
    f.addEventListener("submit", e => {
      e.preventDefault();
      if (!f.checkValidity()) { toast(t("faltan")); f.reportValidity(); return; }
      toast(t("enviado"));
      f.reset();
    });''',
     '''  function montarFormulario() {
    montarBoletin();
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
    });'''),
])

# El boletín del pie se envía por AJAX para no sacar al visitante de la página.
ed("assets/js/home.js", [
    ('  /* --------------------------- formulario de alta ------------------------ */',
     '''  /* ------------------------- boletín «Te avisamos» ------------------------
     Va por AJAX contra FormSubmit para no sacar al visitante de la página.
     Si algo falla, se abre el correo del visitante como plan B. */
  function montarBoletin() {
    const f = $("#form-boletin"); if (!f || f.dataset.listo) return;
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
            _subject: "Km0 Week · alta en el boletín",
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
          "?subject=" + encodeURIComponent("Km0 Week · alta en el boletín") +
          "&body=" + encodeURIComponent((campo ? campo.value : "") + "\\n\\nQuiero que me aviséis cuando se abran las reservas.");
      } finally {
        if (btn) { btn.disabled = false; btn.textContent = texto; }
      }
    });
  }

  /* --------------------------- formulario de alta ------------------------ */''',
     'function montarBoletin()'),
])


# ===========================================================================
# 4 · km0.css — los cinco arreglos de diseño
# ===========================================================================
ed("assets/css/km0.css", [
    # -- 4.1 imágenes: sin esto el atributo height="800" gana a aspect-ratio --
    ('img, svg, canvas { display: block; max-width: 100%; }',
     '/* height:auto es imprescindible: sin él, el atributo height="800" del HTML\n'
     '   se impone sobre aspect-ratio y las fotos salen gigantes. */\n'
     'img, svg, canvas { display: block; max-width: 100%; }\n'
     'img { height: auto; }'),

    # -- 4.2 cifras de portada: clase propia, ya no colisiona con .nota ------
    ('.fig .nota { font-size: .74rem; color: var(--suave); }',
     '.fig .fig-nota { font-size: .76rem; line-height: 1.5; color: var(--suave); max-width: 26ch; }'),
    ('.fig .u { font-size: .88rem; color: var(--texto); max-width: 20ch; font-weight: 600; line-height: 1.45; }',
     '.fig .u { font-size: .9rem; color: var(--tinta); max-width: 22ch; font-weight: 700; line-height: 1.4; }'),
    ('  display: flex; flex-direction: column; gap: 9px; align-items: flex-start;\n}',
     '  display: flex; flex-direction: column; gap: 7px; align-items: flex-start;\n}\n'
     '.fig b + .u { margin-top: 2px; }'),

    # -- 4.3 tarjetas de noticia: la grande deja de estirarse ---------------
    ('@media (min-width: 760px) { .nota.grande { flex-direction: row; } .nota.grande img { width: 46%; aspect-ratio: auto; } .nota.grande .bd { align-content: center; } }',
     '@media (min-width: 760px) {\n'
     '  .nota.grande { flex-direction: row; min-height: 300px; }\n'
     '  .nota.grande img { width: 46%; height: auto; align-self: stretch; aspect-ratio: auto; object-fit: cover; }\n'
     '  .nota.grande .bd { align-content: center; padding: clamp(1.4rem, 3vw, 2.4rem); }\n'
     '  .nota.grande h3 { font-size: clamp(1.3rem, 2.2vw, 1.7rem); }\n'
     '}'),

    # -- 4.4 ritmo vertical en los bloques de texto de dos columnas ---------
    ('.parte-foto { border-radius: var(--r-l); overflow: hidden; box-shadow: var(--sh-m); }',
     '/* Ritmo vertical de la columna de texto. Va dentro de :where() para que no\n'
     '   pese en la especificidad y las utilidades .mt-1 / .mt-2 sigan mandando. */\n'
     ':where(.parte > div:not(.parte-foto)) > * + * { margin-top: 1.1rem; }\n'
     ':where(.parte > div:not(.parte-foto)) > .label + * { margin-top: .55rem; }\n'
     ':where(.parte > div:not(.parte-foto)) > h2 + * { margin-top: .9rem; }\n'
     ':where(.parte > div:not(.parte-foto)) > .lede + p { margin-top: 1.25rem; }\n'
     ':where(.parte > div:not(.parte-foto)) > .lede { color: var(--tinta); }\n'
     '.parte-foto { border-radius: var(--r-l); overflow: hidden; box-shadow: var(--sh-m); }',
     ':where(.parte > div:not(.parte-foto))'),

    # -- 4.5 filtros: grupos separados, etiqueta con peso y color por familia -
    ('''.filtros-fila { display: flex; flex-wrap: wrap; gap: .5rem .55rem; align-items: center; }
.filtros-fila + .filtros-fila { margin-top: .55rem; }
.filtros .grp { display: flex; flex-wrap: wrap; gap: .4rem; align-items: center; }
.filtros .grp > .label { margin-right: .2rem; color: var(--suave); }''',
     '''.filtros-top {
  display: flex; flex-wrap: wrap; align-items: center; gap: .5rem .9rem;
  padding-bottom: .6rem; border-bottom: 1px solid var(--linea-2);
}
.filtros-top .res { font-size: .95rem; color: var(--suave); }
.filtros-top .res b { font-family: var(--f-disp); font-size: 1.35rem; color: var(--tinta); margin-right: .15rem; }
.f-orden { display: flex; align-items: center; gap: .4rem; margin-left: auto; font-size: .8rem;
  font-weight: 700; letter-spacing: .08em; text-transform: uppercase; color: var(--suave); }

.f-row { display: grid; gap: .4rem; padding-block: .55rem; }
.f-row + .f-row { border-top: 1px dashed var(--linea-2); }
@media (min-width: 780px) {
  .f-row { grid-template-columns: 132px minmax(0,1fr); gap: .6rem 1rem; align-items: start; }
}
.f-tit {
  display: flex; align-items: center; gap: .45rem; padding-top: .3rem;
  font-size: .72rem; font-weight: 800; letter-spacing: .12em;
  text-transform: uppercase; color: var(--tinta);
}
.f-tit::before { content: ""; width: 9px; height: 9px; border-radius: 50%; background: var(--mar); flex: none; }
.f-row[data-c="tipo"] .f-tit::before { background: var(--terra); }
.f-row[data-c="experiencia"] .f-tit::before { background: var(--verde-d); }
.filtros .grp { display: flex; flex-wrap: wrap; gap: .4rem; align-items: center; }
/* En móvil cada familia se desliza en su propia fila en vez de apilarse */
@media (max-width: 779px) {
  .filtros .grp { flex-wrap: nowrap; overflow-x: auto; scrollbar-width: none; padding-bottom: 2px; }
  .filtros .grp::-webkit-scrollbar { display: none; }
  .filtros .grp > .chip { flex: none; }
}''', '.f-tit {'),

    ('''.chip:hover { border-color: var(--mar); color: var(--mar-d); }''',
     '''.chip:hover { border-color: var(--mar); color: var(--mar-d); }
/* Cada familia de filtros lleva su tinte también apagada, para no confundirlas */
.f-row[data-c="provincia"] .chip { border-color: #CDE6F0; background: #FAFDFE; }
.chip.terra { border-color: #F1D7C8; background: #FFFBF9; }
.chip.terra:hover { border-color: var(--terra); color: var(--terra-h); }
.chip.verde { border-color: #DCE8CF; background: #FBFDF8; }
.chip.verde:hover { border-color: var(--verde-d); color: var(--verde-d); }''', '.chip.terra:hover'),

    ('.filtros .res { margin-left: auto; font-size: .85rem; color: var(--suave); }\n.filtros .res b { color: var(--tinta); }',
     '.btn-limpiar { margin-left: .2rem; }'),

    # -- 4.6 días de la agenda: fines de semana marcados, vacíos apagados ----
    ('.dia:hover { border-color: var(--mar); }',
     '''.dia:hover:not(:disabled) { border-color: var(--mar); }
.dia.fds { background: var(--arena-p); border-color: #E7D6B4; }
.dia.fds .s { color: #9A7B3F; opacity: 1; }
.dia.sin { opacity: .38; cursor: default; }
.dia.sin:hover { border-color: var(--linea); }'''),

    # -- 4.7 pie: contacto y redes ------------------------------------------
    ('.mt-2 { margin-top: clamp(1.4rem, 3vw, 2.2rem); }',
     '''.foot-contacto { display: flex; gap: .2rem 1rem; flex-wrap: wrap; }
.foot-contacto a { border-bottom: 1px solid rgba(240,250,252,.3); }
.foot-contacto a:hover { border-color: currentColor; }
.foot-redes {
  display: flex; align-items: center; gap: .55rem; flex-wrap: wrap;
  margin-top: 1rem; padding-top: 1rem; border-top: 1px solid rgba(240,250,252,.14);
}
.foot-redes > span { margin-right: .3rem; opacity: .72; }
.foot-redes a {
  display: grid; place-items: center; width: 36px; height: 36px; border-radius: 50%;
  border: 1px solid rgba(240,250,252,.24); color: inherit;
  transition: background .18s var(--e-out), border-color .18s var(--e-out), transform .18s var(--e-out);
}
.foot-redes a svg { width: 19px; height: 19px; }
.foot-redes a:hover { background: rgba(240,250,252,.12); border-color: rgba(240,250,252,.55); transform: translateY(-2px); }

.mt-2 { margin-top: clamp(1.4rem, 3vw, 2.2rem); }'''),
])


# ===========================================================================
# 5 · Portada
# ===========================================================================
ed("_build/paginas/portada.html", [
    ('<span class="pill pill-terra" data-va="Primera edició · 13–19 de novembre de 2026">Primera edición · 13–19 de noviembre de 2026</span>',
     '<span class="pill pill-terra" data-va="Primera edició · 13–29 de novembre de 2026">Primera edición · 13–29 de noviembre de 2026</span>'),
    ('<p class="lede" data-va="Set dies perquè els qui vivim ací tornem a dormir als nostres hotels, a menjar als seus restaurants i a mirar el nostre destí amb ulls de qui arriba per primera vegada.">Siete días para que quienes vivimos aquí volvamos a dormir en nuestros hoteles, a comer en sus restaurantes y a mirar nuestro destino con ojos de quien llega por primera vez.</p>',
     '<p class="lede" data-va="Tres caps de setmana perquè els qui vivim ací tornem a dormir als nostres hotels, a menjar als seus restaurants i a mirar el nostre destí amb ulls de qui arriba per primera vegada.">Tres fines de semana para que quienes vivimos aquí volvamos a dormir en nuestros hoteles, a comer en sus restaurantes y a mirar nuestro destino con ojos de quien llega por primera vez.</p>'),
    ('<span class="label label-verde" data-va="La setmana en xifres">La semana en cifras</span>',
     '<span class="label label-verde" data-va="L\'edició en xifres">La edición en cifras</span>'),
    ('<span class="nota" data-va="hotels, apartaments, càmpings i cases rurals">hoteles, apartamentos, campings y casas rurales</span>',
     '<span class="fig-nota" data-va="hotels, apartaments, càmpings i cases rurals">hoteles, apartamentos, campings y casas rurales</span>'),
    ('<span class="nota" data-va="a les tres províncies, costa i interior">en las tres provincias, costa e interior</span>',
     '<span class="fig-nota" data-va="a les tres províncies, costa i interior">en las tres provincias, costa e interior</span>'),
    ('<span class="nota" data-va="cupó compromés per cada allotjament">cupo comprometido por cada alojamiento</span>',
     '<span class="fig-nota" data-va="cupó compromés per cada allotjament">cupo comprometido por cada alojamiento</span>'),
    ('<span class="nota" data-va="sense necessitat d\'allotjar-se">sin necesidad de alojarse</span>',
     '<span class="fig-nota" data-va="sense necessitat d\'allotjar-se">sin necesidad de alojarse</span>'),
])


# ===========================================================================
# 6 · La iniciativa
# ===========================================================================
ed("_build/paginas/iniciativa.html", [
    ('<h2 class="d2" data-va="Set dies perquè els de casa tornen a ser hostes">Siete días para que los de casa vuelvan a ser huéspedes</h2>',
     '<h2 class="d2" data-va="Tres caps de setmana perquè els de casa tornen a ser hostes">Tres fines de semana para que los de casa vuelvan a ser huéspedes</h2>'),
    ('<p data-va="La Km0 Week és una setmana de novembre —del 13 al 19 de 2026— en què els allotjaments adherits obrin les portes als seus veïns amb una oferta pensada per a ells. Ni temporada alta, ni cues, ni avió. Dormir a vint minuts de casa i tornar l\'endemà.">La Km0 Week es una semana de noviembre —del 13 al 19 de 2026— en la que los alojamientos adheridos abren las puertas a sus vecinos con una oferta pensada para ellos. Ni temporada alta, ni colas, ni avión. Dormir a veinte minutos de casa y volver al día siguiente.</p>',
     '<p data-va="La Km0 Week ocupa dèsset dies de novembre —del 13 al 29 de 2026, tres caps de setmana sencers— en què els allotjaments adherits obrin les portes als seus veïns amb una oferta pensada per a ells. Ni temporada alta, ni cues, ni avió. Dormir a vint minuts de casa i tornar l\'endemà.">La Km0 Week ocupa diecisiete días de noviembre —del 13 al 29 de 2026, tres fines de semana enteros— en los que los alojamientos adheridos abren las puertas a sus vecinos con una oferta pensada para ellos. Ni temporada alta, ni colas, ni avión. Dormir a veinte minutos de casa y volver al día siguiente.</p>'),
])


# ===========================================================================
# 7 · Alojamientos — nuevo bloque de filtros
# ===========================================================================
ed("_build/paginas/alojamientos.html", [
    ('''    <div class="filtros-fila">
      <div class="grp" id="f-provincia" data-grupo="provincia">
        <span class="label" data-va="Província">Provincia</span>
      </div>
      <label class="grp" style="gap:.4rem">
        <span class="label" data-va="Ordenar">Ordenar</span>
        <select id="f-orden" aria-label="Ordenar los resultados"></select>
      </label>
      <span class="res"><b id="f-total">0</b> <span id="f-total-txt" data-va="allotjaments">alojamientos</span></span>
    </div>
    <div class="filtros-fila">
      <div class="grp" id="f-tipo" data-grupo="tipo">
        <span class="label" data-va="Tipus">Tipo</span>
      </div>
    </div>
    <div class="filtros-fila">
      <div class="grp" id="f-exp" data-grupo="experiencia">
        <span class="label" data-va="Experiència">Experiencia</span>
      </div>
      <button class="btn-limpiar" type="button" id="f-limpiar" data-va="Netejar filtres">Limpiar filtros</button>
    </div>''',
     '''    <div class="filtros-top">
      <span class="res"><b id="f-total">0</b> <span id="f-total-txt" data-va="allotjaments">alojamientos</span></span>
      <button class="btn-limpiar" type="button" id="f-limpiar" data-va="Netejar filtres">Limpiar filtros</button>
      <label class="f-orden">
        <span data-va="Ordenar">Ordenar</span>
        <select id="f-orden" aria-label="Ordenar los resultados"></select>
      </label>
    </div>

    <div class="f-row" data-c="provincia">
      <span class="f-tit" data-va="Província">Provincia</span>
      <div class="grp" id="f-provincia" data-grupo="provincia" role="group" aria-label="Filtrar por provincia"></div>
    </div>
    <div class="f-row" data-c="tipo">
      <span class="f-tit" data-va="Tipus d\'allotjament">Tipo de alojamiento</span>
      <div class="grp" id="f-tipo" data-grupo="tipo" role="group" aria-label="Filtrar por tipo"></div>
    </div>
    <div class="f-row" data-c="experiencia">
      <span class="f-tit" data-va="Experiència">Experiencia</span>
      <div class="grp" id="f-exp" data-grupo="experiencia" role="group" aria-label="Filtrar por experiencia"></div>
    </div>''', 'data-c="provincia"'),
    ('<p data-va="Prova a llevar-ne algun: encara estem sumant cases i cada setmana n\'entren de noves.">Prueba a quitar alguno: seguimos sumando casas y cada semana entran nuevas.</p>',
     '<p data-va="Prova a llevar-ne algun: encara estem sumant cases i cada setmana n\'entren de noves.">Prueba a quitar alguno: seguimos sumando casas y entran nuevas cada semana.</p>'),
])


# ===========================================================================
# 8 · Agenda
# ===========================================================================
ed("_build/paginas/agenda.html", [
    ('<h2 class="d2" data-va="Tria un dia">Elige un día</h2>',
     '<h2 class="d2" data-va="Tria un dia">Elige un día</h2>\n'
     '        <p class="body-sm" style="color:var(--suave);margin-top:.4rem" data-va="Del 13 al 29 de novembre. Els dies destacats en color són caps de setmana.">Del 13 al 29 de noviembre. Los días destacados en color son fines de semana.</p>'),
    ('<button class="chip" type="button" id="ag-todo" aria-pressed="true" data-va="Veure la setmana sencera">Ver la semana entera</button>',
     '<button class="chip" type="button" id="ag-todo" aria-pressed="true" data-va="Veure els 17 dies">Ver los 17 días</button>\n'
     '        <button class="chip terra" type="button" id="ag-finde" aria-pressed="false" data-va="Només caps de setmana">Solo fines de semana</button>'),
    ('<div class="dias" id="ag-dias" role="group" aria-label="Días de la semana"></div>',
     '<div class="dias" id="ag-dias" role="group" aria-label="Días de la edición"></div>'),
    ('<p data-va="Prova amb un altre dia o mira la setmana sencera.">Prueba con otro día o mira la semana entera.</p>',
     '<p data-va="Prova amb un altre dia o mira els 17 dies.">Prueba con otro día o mira los 17 días.</p>'),
])


# ===========================================================================
# 9 · Suma tu alojamiento — formulario con envío real
# ===========================================================================
ed("_build/paginas/suma.html", [
    ('<h3 class="mt-1" data-va="La setmana">La semana</h3>',
     '<h3 class="mt-1" data-va="Els tres caps de setmana">Los tres fines de semana</h3>'),
    ('<p class="body-sm" data-va="Set dies. Després t\'enviem l\'informe amb els números de la teua fitxa.">Siete días. Después te enviamos el informe con los números de tu ficha.</p>',
     '<p class="body-sm" data-va="Dèsset dies i tres caps de setmana. Després t\'enviem l\'informe amb els números de la teua fitxa.">Diecisiete días y tres fines de semana. Después te enviamos el informe con los números de tu ficha.</p>'),
    ('<td data-va="Un mínim de 5 places o habitacions per a residents durant la setmana. El nombre es publica a la fitxa.">Un mínimo de 5 plazas o habitaciones para residentes durante la semana. El número se publica en la ficha.</td>',
     '<td data-va="Un mínim de 5 places o habitacions per a residents durant els dèsset dies. El nombre es publica a la fitxa.">Un mínimo de 5 plazas o habitaciones para residentes durante los diecisiete días. El número se publica en la ficha.</td>'),
    ('<p class="body-sm mt-2" style="color:var(--suave)" data-va="HOSBEC comprova els preus amb una mostra aleatòria durant la setmana. Qui no complisca queda fora de l\'edició següent.">HOSBEC comprueba los precios con una muestra aleatoria durante la semana. Quien no cumpla queda fuera de la siguiente edición.</p>',
     '<p class="body-sm mt-2" style="color:var(--suave)" data-va="HOSBEC comprova els preus amb una mostra aleatòria durant l\'edició. Qui no complisca queda fora de l\'edició següent.">HOSBEC comprueba los precios con una muestra aleatoria durante la edición. Quien no cumpla queda fuera de la siguiente edición.</p>'),

    # -- el formulario pasa a enviar de verdad ------------------------------
    ('    <form class="form-grid" id="form-suma" novalidate>',
     '''    <div class="aviso-ok" id="form-ok" hidden>
      <b data-va="Sol·licitud rebuda">Solicitud recibida</b>
      <p data-va="Ja ens ha arribat el correu. Et responem en 48 hores laborables amb el pas següent.">Ya nos ha llegado el correo. Te respondemos en 48 horas laborables con el siguiente paso.</p>
    </div>

    <!-- El envío lo hace FormSubmit: reenvía el contenido por correo a
         km0week@hosbec.com. No guarda nada ni requiere servidor propio. -->
    <form class="form-grid" id="form-suma" novalidate
          action="https://formsubmit.co/km0week@hosbec.com" method="POST">
      <input type="hidden" name="_subject" value="Km0 Week · nueva solicitud de alojamiento">
      <input type="hidden" name="_template" value="table">
      <input type="hidden" name="_captcha" value="false">
      <input type="hidden" name="_next" value="@@DOMINIO@@/suma.html?enviado=1#formulario">
      <input type="text" name="_honey" style="display:none" tabindex="-1" autocomplete="off" aria-hidden="true">'''),
    ('<p class="ayuda mt-1" data-va="Aquest formulari és una demostració: encara no envia res. Connecta\'l al correu o al CRM d\'HOSBEC abans de publicar.">Este formulario es una demostración: todavía no envía nada. Conéctalo al correo o al CRM de HOSBEC antes de publicar.</p>',
     '<p class="ayuda mt-1" data-va="En enviar-lo ens arriba un correu a km0week@hosbec.com amb aquestes dades. No es guarden en cap altre lloc.">Al enviarlo nos llega un correo a km0week@hosbec.com con estos datos. No se guardan en ningún otro sitio.</p>'),
])


# ===========================================================================
# 10 · Resto de páginas — fechas y referencias a «la semana»
# ===========================================================================
ed("_build/paginas/faq.html", [
    ('HOSBEC lo comprueba con una muestra aleatoria durante la semana.',
     'HOSBEC lo comprueba con una muestra aleatoria durante la edición.'),
    ('El sorteo se celebra el domingo 19 de noviembre a las 18:00 ante notario.',
     'El sorteo se celebra el domingo 29 de noviembre a las 18:00 ante notario.'),
    ('El sorteig es fa el diumenge 19 de novembre a les 18:00 davant de notari.',
     'El sorteig es fa el diumenge 29 de novembre a les 18:00 davant de notari.'),
    ('El cupo mínimo son 5 plazas durante la semana.',
     'El cupo mínimo son 5 plazas durante los diecisiete días.'),
])

ed("_build/paginas/noticias.html", [
    ('El compromiso de la Km0 Week es que el precio de la semana sea el más bajo del trimestre.',
     'El compromiso de la Km0 Week es que el precio de esos días sea el más bajo del trimestre.'),
    ('talleres que se abren solo durante la semana.', 'talleres que se abren solo durante la Km0 Week.'),
])

ed("_build/paginas/noticia-1.html", [
    ('504 plazas comprometidas para residentes durante la semana del 13 al 19 de noviembre.',
     '504 plazas comprometidas para residentes del 13 al 29 de noviembre.'),
    ('504 places compromeses per a residents durant la setmana del 13 al 19 de novembre.',
     '504 places compromeses per a residents del 13 al 29 de novembre.'),
    ('el número de habitaciones o plazas que reserva para residentes durante los siete días.',
     'el número de habitaciones o plazas que reserva para residentes durante los diecisiete días.'),
    ('el nombre d\'habitacions o places que reserva per a residents durant els set dies.',
     'el nombre d\'habitacions o places que reserva per a residents durant els dèsset dies.'),
])

ed("_build/paginas/noticia-2.html", [
    ('para la misma noche de la semana y el mismo tipo de habitación.',
     'para el mismo día de la semana y el mismo tipo de habitación.'),
    ('Durante la semana, HOSBEC consulta una muestra aleatoria de fichas',
     'Durante la edición, HOSBEC consulta una muestra aleatoria de fichas'),
])

ed("_build/paginas/noticia-3.html", [
    ('El enlace de inscripción se abre quince días antes de la semana.',
     'El enlace de inscripción se abre quince días antes del arranque.'),
])

ed("_build/paginas/noticia-4.html", [
    ('Se cierra el domingo 19 de noviembre a las 14:00.', 'Se cierra el domingo 29 de noviembre a las 14:00.'),
    ('Es tanca el diumenge 19 de novembre a les 14:00.', 'Es tanca el diumenge 29 de novembre a les 14:00.'),
])

ed("_build/paginas/prensa.html", [
    ('acompañamiento durante la semana, escríbenos o llámanos.',
     'acompañamiento durante la edición, escríbenos o llámanos.'),
    ("acompanyament durant la setmana, escriu-nos o telefona'ns.",
     "acompanyament durant l'edició, escriu-nos o telefona'ns."),
    ('<li>965 85 51 12</li>', '<li><a href="tel:+34965855516">965 85 55 16</a></li>'),
])

ed("_build/paginas/descargas.html", [
    ('Las catorce actividades abiertas de la semana, día a día, con hora y lugar.',
     'Las catorce actividades abiertas de la edición, día a día, con hora y lugar.'),
    ("Les catorze activitats obertes de la setmana, dia a dia, amb hora i lloc.",
     "Les catorze activitats obertes de l'edició, dia a dia, amb hora i lloc."),
])


# ===========================================================================
# 11 · Aviso de recibido del formulario (estilo)
# ===========================================================================
ed("assets/css/km0.css", [
    ('.campo .ayuda { font-size: .78rem; color: var(--suave); }',
     '''.aviso-ok {
  display: grid; gap: .3rem; margin-bottom: clamp(1.2rem, 2.6vw, 1.8rem);
  padding: clamp(1rem, 2.4vw, 1.4rem) clamp(1.1rem, 2.6vw, 1.6rem);
  background: var(--verde-p); border: 1.5px solid #C4D8AC;
  border-left: 5px solid var(--verde-d); border-radius: var(--r-m);
}
.aviso-ok b { font-family: var(--f-disp); font-size: 1.2rem; color: var(--tinta); }
.aviso-ok p { font-size: .9rem; color: var(--texto); }
.campo .ayuda { font-size: .78rem; color: var(--suave); }'''),
])


# ===========================================================================
# 13 · Retoques finos después de revisar las capturas
# ===========================================================================
ed("_build/paginas/noticias.html", [
    ('Publicaremos la agenda cerrada de las siete jornadas cuando se confirmen las últimas actividades.',
     'Publicaremos la agenda cerrada de los diecisiete días cuando se confirmen las últimas actividades.'),
    ("Publicarem l'agenda tancada de les set jornades quan es confirmen les últimes activitats.",
     "Publicarem l'agenda tancada dels dèsset dies quan es confirmen les últimes activitats."),
])

ed("assets/css/km0.css", [
    # el tinte de provincia no debe ganarle al estado «pulsado» (texto blanco)
    ('.f-row[data-c="provincia"] .chip { border-color: #CDE6F0; background: #FAFDFE; }',
     ':where(.f-row[data-c="provincia"]) .chip { border-color: #CDE6F0; background: #FAFDFE; }'),

    # el punto de color se alinea con la primera línea del rótulo
    ('''.f-tit {
  display: flex; align-items: center; gap: .45rem; padding-top: .3rem;''',
     '''.f-tit {
  display: flex; align-items: flex-start; gap: .45rem; padding-top: .3rem; line-height: 1.35;'''),
    ('.f-tit::before { content: ""; width: 9px; height: 9px; border-radius: 50%; background: var(--mar); flex: none; }',
     '.f-tit::before { content: ""; width: 9px; height: 9px; margin-top: .32em; border-radius: 50%; background: var(--mar); flex: none; }'),
    ('  .f-row { grid-template-columns: 132px minmax(0,1fr); gap: .6rem 1rem; align-items: start; }',
     '  .f-row { grid-template-columns: 152px minmax(0,1fr); gap: .6rem 1rem; align-items: start; }'),

    # un poco más de aire entre antetítulo, titular y entradilla
    (':where(.parte > div:not(.parte-foto)) > .label + * { margin-top: .55rem; }',
     ':where(.parte > div:not(.parte-foto)) > .label + * { margin-top: .7rem; }'),
    (':where(.parte > div:not(.parte-foto)) > h2 + * { margin-top: .9rem; }',
     ':where(.parte > div:not(.parte-foto)) > h2 + * { margin-top: 1rem; }'),

    # pista de que la tira de días se desliza
    ('.dias { display: flex; gap: .5rem; overflow-x: auto; padding-bottom: .4rem; scrollbar-width: thin; }',
     '.dias {\n'
     '  display: flex; gap: .5rem; overflow-x: auto; padding-bottom: .4rem; scrollbar-width: thin;\n'
     '  /* difuminado en el borde derecho: avisa de que hay más días */\n'
     '  -webkit-mask-image: linear-gradient(90deg, #000 calc(100% - 46px), transparent);\n'
     '          mask-image: linear-gradient(90deg, #000 calc(100% - 46px), transparent);\n'
     '}\n'
     '.dias:not(:hover) { scrollbar-color: var(--linea) transparent; }'),
])

# icono de Facebook con la «f» de verdad
ed("_build/build.py", [
    ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="4"/><path d="M15.2 8.2h-1.3c-.9 0-1.5.6-1.5 1.5v1.6h2.6l-.4 2.6h-2.2v5"/><path d="M10.3 11.3h2.1"/></svg>',
     '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M13.4 20.5v-6.9h2.3l.35-2.7h-2.65V9.2c0-.78.22-1.31 1.34-1.31h1.43V5.47c-.25-.03-1.1-.11-2.09-.11-2.07 0-3.48 1.26-3.48 3.58v2h-2.34v2.7h2.34v6.86z"/></svg>'),
])


# ===========================================================================
# 14 · En móvil los filtros se pliegan: si no, la barra pegajosa se come
#      media pantalla del teléfono.
# ===========================================================================
ed("_build/paginas/alojamientos.html", [
    ('''      <label class="f-orden">
        <span data-va="Ordenar">Ordenar</span>
        <select id="f-orden" aria-label="Ordenar los resultados"></select>
      </label>
    </div>

    <div class="f-row" data-c="provincia">''',
     '''      <label class="f-orden">
        <span data-va="Ordenar">Ordenar</span>
        <select id="f-orden" aria-label="Ordenar los resultados"></select>
      </label>
      <button class="f-toggle" type="button" id="f-toggle" aria-expanded="false" aria-controls="f-grupos">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M7 12h10M10 17h4"/></svg>
        <span data-va="Filtres">Filtros</span>
        <b id="f-activos" hidden>0</b>
      </button>
    </div>

    <div class="filtros-grupos" id="f-grupos">
    <div class="f-row" data-c="provincia">'''),
    ('''      <div class="grp" id="f-exp" data-grupo="experiencia" role="group" aria-label="Filtrar por experiencia"></div>
    </div>''',
     '''      <div class="grp" id="f-exp" data-grupo="experiencia" role="group" aria-label="Filtrar por experiencia"></div>
    </div>
    </div>'''),
])

ed("assets/css/km0.css", [
    ('.btn-limpiar { margin-left: .2rem; }',
     '''.btn-limpiar { margin-left: .2rem; }
.f-toggle {
  display: none; align-items: center; gap: .45rem; font: inherit; cursor: pointer;
  font-size: .84rem; font-weight: 700; color: var(--tinta);
  background: #fff; border: 1.5px solid var(--linea); border-radius: var(--r-full);
  padding: .4rem .85rem;
}
.f-toggle svg { width: 17px; height: 17px; }
.f-toggle b {
  display: grid; place-items: center; min-width: 20px; height: 20px; padding: 0 5px;
  border-radius: var(--r-full); background: var(--mar); color: #fff; font-size: .72rem;
}
.f-toggle[aria-expanded="true"] { border-color: var(--mar); color: var(--mar-d); }
@media (max-width: 779px) {
  .f-toggle { display: inline-flex; }
  .f-orden { margin-left: 0; font-size: .74rem; }
  .filtros-top { gap: .45rem .7rem; }
  .filtros-grupos { display: none; }
  .filtros-grupos.abierto { display: block; }
  .f-row { padding-block: .45rem; }
}'''),
])

ed("assets/js/home.js", [
    ('''    const limpiar = () => {
      FILTRO.provincia = ""; FILTRO.tipo = []; FILTRO.experiencia = [];''',
     '''    // En móvil los tres grupos se pliegan tras un botón «Filtros».
    // (montarFiltros() se llama más de una vez, de ahí el pestillo dataset.listo:
    //  sin él el listener se registraría dos veces y el toggle se anularía solo)
    const tg = $("#f-toggle"), grupos = $("#f-grupos");
    if (tg && grupos && !tg.dataset.listo) {
      tg.dataset.listo = "1";
      tg.addEventListener("click", () => {
        const abierto = grupos.classList.toggle("abierto");
        tg.setAttribute("aria-expanded", String(abierto));
      });
    }

    const limpiar = () => {
      FILTRO.provincia = ""; FILTRO.tipo = []; FILTRO.experiencia = [];'''),
    ('''    document.dispatchEvent(new CustomEvent("km0:fichas"));
    document.dispatchEvent(new CustomEvent("km0:render"));
  }''',
     '''    // contador del botón «Filtros» de móvil
    const act = (FILTRO.provincia ? 1 : 0) + FILTRO.tipo.length + FILTRO.experiencia.length;
    const ba = $("#f-activos");
    if (ba) { ba.textContent = act; ba.hidden = !act; }

    document.dispatchEvent(new CustomEvent("km0:fichas"));
    document.dispatchEvent(new CustomEvent("km0:render"));
  }'''),
])


# ===========================================================================
# 16 · Los tres fines de semana son de viernes a domingo (13-15, 20-22, 27-29),
#      así que el viernes cuenta como fin de semana.
# ===========================================================================
ed("assets/js/home.js", [
    ('  const esFinde = n => [0, 6].includes(fechaDia(n).getDay());   // sábado o domingo',
     '  // viernes, sábado y domingo: los tres findes de la edición son 13-15, 20-22 y 27-29\n'
     '  const esFinde = n => [5, 6, 0].includes(fechaDia(n).getDay());'),
])


# ===========================================================================
# 15 · De paso: el marcador del textarea estaba escrito solo en valencià y no
#      existía manera de traducir marcadores. Se añade el atributo data-va-ph.
# ===========================================================================
ed("assets/js/home.js", [
    ('    $$("[data-va-html]").forEach(el => {',
     '    // marcadores de campo bilingües:  <input data-va-ph="…" placeholder="…">\n'
     '    $$("[data-va-ph]").forEach(el => {\n'
     '      if (!el.hasAttribute("data-es-ph")) el.setAttribute("data-es-ph", el.getAttribute("placeholder") || "");\n'
     '      el.setAttribute("placeholder", LANG === "va" ? el.getAttribute("data-va-ph") : el.getAttribute("data-es-ph"));\n'
     '    });\n'
     '    $$("[data-va-html]").forEach(el => {'),
])

ed("_build/paginas/suma.html", [
    ('<textarea name="oferta" placeholder="Nit + sopar per a dos, circuit termal, check-out tardà..."></textarea>',
     '<textarea name="oferta" placeholder="Noche + cena para dos, circuito termal, salida tardía..." data-va-ph="Nit + sopar per a dos, circuit termal, check-out tardà..."></textarea>'),
])


# ===========================================================================
# 12 · Barrido final sobre todas las páginas
#      (teléfono viejo, fechas de respaldo y valencià que quedaba suelto)
# ===========================================================================
import glob

BARRIDO = [
    # teléfono correcto en todas partes, incluidos los data-va
    ("965 85 51 12", "965 85 55 16"),
    # texto de respaldo de los [data-fechas] (el JS lo reescribe, pero debe
    # ser correcto si el visitante llega con JavaScript desactivado)
    ("13 – 19 de noviembre de 2026", "13 – 29 de noviembre de 2026"),
    ("13 – 19 de novembre de 2026", "13 – 29 de novembre de 2026"),
    # valencià que quedaba con la redacción antigua
    ("El cupo mínim són 5 places durant la setmana.",
     "El cupo mínim són 5 places durant els dèsset dies."),
    ("HOSBEC ho comprova amb una mostra aleatòria durant la setmana.",
     "HOSBEC ho comprova amb una mostra aleatòria durant l'edició."),
    ("El compromís de la Km0 Week és que el preu de la setmana siga el més baix del trimestre.",
     "El compromís de la Km0 Week és que el preu d'aqueixos dies siga el més baix del trimestre."),
    ("tallers que s'obrin només durant la setmana.",
     "tallers que s'obrin només durant la Km0 Week."),
    ("Durant la setmana, HOSBEC consulta una mostra aleatòria de fitxes",
     "Durant l'edició, HOSBEC consulta una mostra aleatòria de fitxes"),
    ("L'enllaç d'inscripció s'obri quinze dies abans de la setmana.",
     "L'enllaç d'inscripció s'obri quinze dies abans de l'arrancada."),
    ("per a la mateixa nit de la setmana i el mateix tipus d'habitació.",
     "per al mateix dia de la setmana i el mateix tipus d'habitació."),
]

for ruta in sorted(glob.glob(os.path.join(RAIZ, "_build", "paginas", "*.html"))) + \
            [os.path.join(RAIZ, "_build", "build.py")]:
    txt = original = io.open(ruta, encoding="utf-8").read()
    for viejo, nuevo in BARRIDO:
        if viejo in txt:
            txt = txt.replace(viejo, nuevo)
            hechos += 1
    if txt != original:
        io.open(ruta, "w", encoding="utf-8").write(txt)


# ===========================================================================
print("cambios aplicados:", hechos)
if fallos:
    print("\n⚠  revisar (%d):" % len(fallos))
    for f in fallos:
        print("   ·", f)
    sys.exit(1)
print("todo correcto. Ahora:  python3 _build/build.py")
