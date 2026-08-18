#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Parche Km0 Week — segunda tanda, 18/08/2026
===========================================

 1. Denominación correcta: «Asociación Empresarial Hotelera y Turística de la
    Comunidad Valenciana», en el pie y en el aviso legal.
 2. Agenda: «Quiero ir» deja de abrir un correo a HOSBEC y lleva a la web de
    quien organiza la actividad (campo `enlace` nuevo en cada acto).
 3. Fuera todo lo que delataba que la web era una maqueta: avisos de «texto de
    ejemplo», instrucciones dirigidas a HOSBEC, la tabla de medios inventados y
    los datos legales sin rellenar.
 4. De paso: el boletín de la página de Noticias seguía siendo falso (se
    limitaba a vaciar el campo). Ahora envía igual que el del pie.

Se ejecuta desde la raíz del proyecto:   python3 _build/parche-2.py
Después hay que recompilar:              python3 _build/build.py

Idempotente: volver a ejecutarlo no cambia nada.
"""

import os, re, sys, io

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
fallos, hechos = [], 0


def ed(rel, pares, obligatorio=True):
    """Aplica una lista de (viejo, nuevo[, marca_de_ya_aplicado]) sobre un archivo."""
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


def borrar(rel, textos):
    """Quita trozos de texto. Es idempotente sin más: si ya no están, no hace nada."""
    global hechos
    ruta = os.path.join(RAIZ, rel)
    if not os.path.exists(ruta):
        fallos.append("NO EXISTE: " + rel); return
    txt = original = io.open(ruta, encoding="utf-8").read()
    for t in textos:
        if t in txt:
            txt = txt.replace(t, "")
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


def ed_re(rel, patron, reemplazo, marca):
    """Igual, pero con expresión regular. `marca` evita repetir la sustitución."""
    global hechos
    ruta = os.path.join(RAIZ, rel)
    if not os.path.exists(ruta):
        fallos.append("NO EXISTE: " + rel); return
    txt = io.open(ruta, encoding="utf-8").read()
    if marca in txt:
        return
    nuevo, n = re.subn(patron, reemplazo, txt)
    if not n:
        fallos.append("%s → la expresión no casa: %.50s" % (rel, patron)); return
    io.open(ruta, "w", encoding="utf-8").write(nuevo)
    hechos += n


# ===========================================================================
# 1 · Denominación oficial de HOSBEC
#     Tomada del aviso legal de hosbec.com: CIF G03270014, Paseo Els Tolls 2
#     (Edificio INVATTUR, 3ª planta), 03502 Benidorm.
# ===========================================================================
NOMBRE_ES = "Asociación Empresarial Hotelera y Turística de la Comunidad Valenciana"
NOMBRE_VA = "Associació Empresarial Hotelera i Turística de la Comunitat Valenciana"

ed("_build/build.py", [
    ('<span>© <span data-year>2026</span> HOSBEC · Asociación Empresarial Hostelera de Benidorm, Costa Blanca y Comunidad Valenciana</span>',
     # solo se traduce el nombre: el <span data-year> tiene que quedar fuera,
     # porque el conmutador de idioma reescribe textContent y se lo llevaría por delante
     '<span>© <span data-year>2026</span> HOSBEC · <span data-va="%s">%s</span></span>'
     % (NOMBRE_VA, NOMBRE_ES)),
])

ed("README.md", [
    ("© HOSBEC · Asociación Empresarial Hostelera de Benidorm, Costa Blanca y Comunitat Valenciana",
     "© HOSBEC · " + NOMBRE_ES),
], obligatorio=False)

ed("_build/paginas/aviso-legal.html", [
    ('<li data-va="Denominació: HOSBEC · Associació Empresarial Hostelera de Benidorm, Costa Blanca i Comunitat Valenciana.">Denominación: HOSBEC · Asociación Empresarial Hostelera de Benidorm, Costa Blanca y Comunidad Valenciana.</li>',
     '<li data-va="Denominació: HOSBEC · %s.">Denominación: HOSBEC · %s.</li>' % (NOMBRE_VA, NOMBRE_ES)),
])


# ===========================================================================
# 2 · Agenda: «Quiero ir» lleva a quien organiza, no a nuestro correo
# ===========================================================================

# 2.1 · campo `enlace` en cada actividad
ed_re("assets/js/data-alojamientos.js",
      r'(\{ dia: \d+, hora: "[^"]+", lugar: "[^"]+"), titulo:',
      r'\1, enlace: "https://hosbec.com", titulo:',
      'enlace: "https://hosbec.com", titulo:')

ed("assets/js/data-alojamientos.js", [
    ('   dia: 1..17 (día 1 = 13 de noviembre; día 17 = 29 de noviembre)',
     '   dia: 1..17 (día 1 = 13 de noviembre; día 17 = 29 de noviembre)\n'
     '   enlace: adónde va el botón «Quiero ir» → la web de quien organiza la\n'
     '           actividad (el hotel, el ayuntamiento, la empresa). Si se deja\n'
     '           vacío, se usa la web del alojamiento adherido de ese mismo\n'
     '           destino y, en último caso, hosbec.com.'),
])

# 2.2 · el botón deja de ser un mailto
ed("assets/js/home.js", [
    ('        <a class="btn btn-mar btn-sm" href="mailto:${CFG.emailContacto}?subject=${encodeURIComponent(L(a.titulo))}" data-va="Vull anar-hi">Quiero ir</a>',
     '        <a class="btn btn-mar btn-sm" href="${enlaceActo(a)}" target="_blank" rel="noopener" data-va="Vull anar-hi">Quiero ir</a>'),

    ('  function esGratis(a) {',
     '  // Adónde lleva «Quiero ir»: primero el enlace propio de la actividad;\n'
     '  // si no lo tiene, la web del alojamiento adherido de ese destino; y si\n'
     '  // tampoco, la de HOSBEC. Nunca queda un botón muerto.\n'
     '  function enlaceActo(a) {\n'
     '    if (a.enlace) return a.enlace;\n'
     '    const casa = D.find(x => x.destino === a.lugar && x.web);\n'
     '    return (casa && casa.web) || CFG.webHosbec || "https://hosbec.com";\n'
     '  }\n'
     '\n'
     '  function esGratis(a) {'),
])


# ===========================================================================
# 3 · El boletín de la página de Noticias también envía de verdad
# ===========================================================================
ed("_build/paginas/noticias.html", [
    ('''    <form class="subscribe mt-2" style="justify-content:center;max-width:440px;margin-inline:auto" onsubmit="event.preventDefault();this.reset();window.Km0.toast(window.Km0.lang==='va'?'Gràcies! T\\'avisarem.':'¡Gracias! Te avisaremos.');">
      <input type="email" required placeholder="tu@correo.com" aria-label="Correo">
      <button class="btn btn-terra btn-sm" type="submit" data-va="Avisa'm">Avísame</button>
    </form>''',
     '''    <form class="subscribe mt-2" style="justify-content:center;max-width:440px;margin-inline:auto">
      <input type="email" name="email" required placeholder="tu@correo.com" aria-label="Correo">
      <button class="btn btn-terra btn-sm" type="submit" data-va="Avisa'm">Avísame</button>
    </form>'''),
])

# montarBoletin pasa de un único formulario a todos los .subscribe de la página
ed("assets/js/home.js", [
    ('''  function montarBoletin() {
    const f = $("#form-boletin"); if (!f || f.dataset.listo) return;
    f.dataset.listo = "1";
    f.addEventListener("submit", async e => {''',
     '''  function montarBoletin() {
    // hay uno en el pie de todas las páginas y otro en Noticias
    $$("form.subscribe").forEach(montarUnBoletin);
  }

  function montarUnBoletin(f) {
    if (!f || f.dataset.listo) return;
    f.dataset.listo = "1";
    f.addEventListener("submit", async e => {'''),
])


# ===========================================================================
# 4 · Fuera los avisos de maqueta y las instrucciones para HOSBEC
# ===========================================================================

# 4.1 · Noticias
# (el atributo data-va varía, así que se localiza por expresión regular)
quitar_re("_build/paginas/noticias.html",
          r'\n *<p class="body-sm centrar mt-2"[^>]*>Los textos de estas entradas son de ejemplo\.[^<]*</p>')

# 4.2 · Descargas
ed("_build/paginas/descargas.html", [
    ('''      <h3 data-va="Els arxius encara no estan penjats">Los archivos todavía no están subidos</h3>
      <p class="body-sm" style="max-width:62ch;margin-inline:auto" data-va="Aquesta pàgina està muntada i llesta. Quan tingueu els PDF definitius, deixeu-los en una carpeta del servidor —per exemple /descargas/— i canvieu cada targeta perquè apunte al seu arxiu.">Esta página está montada y lista. Cuando tengáis los PDF definitivos, dejadlos en una carpeta del servidor —por ejemplo /descargas/— y cambiad cada tarjeta para que apunte a su archivo.</p>
      <div class="mt-1"><a class="btn btn-mar" href="mailto:km0week@hosbec.com" data-va="Demanar material">Pedir material</a></div>''',
     '''      <h3 data-va="Necessites alguna cosa que no està ací?">¿Necesitas algo que no está aquí?</h3>
      <p class="body-sm" style="max-width:62ch;margin-inline:auto" data-va="Anem publicant els materials a mesura que es tanquen. Si ets allotjament adherit, ajuntament o mitjà i necessites alguna cosa concreta abans, escriu-nos i te l'enviem.">Vamos publicando los materiales a medida que se cierran. Si eres alojamiento adherido, ayuntamiento o medio y necesitas algo concreto antes, escríbenos y te lo enviamos.</p>
      <div class="mt-1"><a class="btn btn-mar" href="mailto:km0week@hosbec.com" data-va="Demanar material">Pedir material</a></div>'''),
])

# 4.3 · Prensa
ed("_build/paginas/prensa.html", [
    ('''
    <p class="body-sm mt-2" style="color:var(--suave)" data-va="Els arxius encara no estan penjats. Quan els tingueu, deixeu-los en una carpeta del servidor i enllaceu-los des d'ací.">Los archivos todavía no están subidos. Cuando los tengáis, dejadlos en una carpeta del servidor y enlazadlos desde aquí.</p>''',
     '''
    <p class="body-sm mt-2" style="color:var(--suave)" data-va="Vas publicant-se a mesura que es tanquen. Si necessites algun material abans que estiga ací, escriu-nos a km0week@hosbec.com i te l'enviem.">Se van publicando a medida que se cierran. Si necesitas algún material antes de que esté aquí, escríbenos a km0week@hosbec.com y te lo enviamos.</p>''',
     'Se van publicando a medida que se cierran'),

    ('<p class="lede" data-va="Ací anirem recollint el que es publique sobre la Km0 Week. De moment, exemples per a veure com queda.">Aquí iremos recogiendo lo que se publique sobre la Km0 Week. De momento, ejemplos para ver cómo queda.</p>',
     '<p class="lede" data-va="Ací recollim el que es publica sobre la Km0 Week.">Aquí recogemos lo que se publica sobre la Km0 Week.</p>'),

    ('''          <tr><td>—</td><td data-va="Mitjà d'exemple">Medio de ejemplo</td><td data-va="Titular d'exemple sobre la primera edició de la Km0 Week">Titular de ejemplo sobre la primera edición de la Km0 Week</td></tr>
          <tr><td>—</td><td data-va="Mitjà d'exemple">Medio de ejemplo</td><td data-va="Els hotels valencians obrin les portes als seus veïns">Los hoteles valencianos abren las puertas a sus vecinos</td></tr>
          <tr><td>—</td><td data-va="Mitjà d'exemple">Medio de ejemplo</td><td data-va="Turisme de proximitat en temporada baixa: el cas de la Comunitat">Turismo de proximidad en temporada baja: el caso de la Comunitat</td></tr>''',
     '''          <tr><td colspan="3" style="color:var(--suave)" data-va="La primera edició encara no s'ha presentat en roda de premsa. En quant hi haja publicacions, apareixeran ací.">La primera edición todavía no se ha presentado en rueda de prensa. En cuanto haya publicaciones, aparecerán aquí.</td></tr>'''),
])

# 4.4 · «Pendiente de publicar» suena a nota interna; «Próximamente» es
#       lenguaje de cara al público y dice exactamente lo mismo.
for pag in ("_build/paginas/descargas.html", "_build/paginas/prensa.html"):
    ed_re(pag,
          r'<span class="peso" data-va="Pendent de publicar">Pendiente de publicar</span>',
          '<span class="peso" data-va="Pròximament">Próximamente</span>',
          'data-va="Pròximament">Próximamente<')

# 4.5 · Aviso legal: fuera la nota de plantilla y dentro los datos reales
borrar("_build/paginas/aviso-legal.html", ['''      <p class="lede" data-va="Aquest text és una plantilla de treball. Abans de publicar, feu-lo revisar pels serveis jurídics d'HOSBEC i completeu les dades marcades.">Este texto es una plantilla de trabajo. Antes de publicar, hacedlo revisar por los servicios jurídicos de HOSBEC y completad los datos marcados.</p>

'''])

ed("_build/paginas/aviso-legal.html", [
        ('<li>CIF: <em data-va="pendent">pendiente</em></li>',
     '<li>CIF: G03270014</li>'),
    ('<li data-va="Domicili: pendent">Domicilio: <em>pendiente</em></li>',
     '<li data-va="Domicili: Passeig Els Tolls, 2 (Edifici INVATTUR, 3a planta), 03502 Benidorm (Alacant).">Domicilio: Paseo Els Tolls, 2 (Edificio INVATTUR, 3.ª planta), 03502 Benidorm (Alicante).</li>'),
    ('<li data-va="Inscripció registral: pendent">Inscripción registral: <em>pendiente</em></li>',
     '<li data-va="Inscripció: Depòsit d\'Estatuts d\'Organitzacions Sindicals i Empresarials, núm. 80000007, de 6 de juny de 2011.">Inscripción: Depósito de Estatutos de Organizaciones Sindicales y Empresariales, n.º 80000007, de 6 de junio de 2011.</li>'),
])

# 4.6 · Privacidad: fuera la nota de plantilla y, ya que los formularios envían
#       de verdad, se declara FormSubmit como encargado del tratamiento.
borrar("_build/paginas/privacidad.html", ['''      <p class="lede" data-va="Aquest text és una plantilla de treball. Abans de publicar, feu-lo revisar pel responsable de protecció de dades d'HOSBEC.">Este texto es una plantilla de trabajo. Antes de publicar, hacedlo revisar por el responsable de protección de datos de HOSBEC.</p>

'''])

ed("_build/paginas/privacidad.html", [
        ('<p>HOSBEC · km0week@hosbec.com · 965 85 55 16</p>',
     '<p data-va="HOSBEC · %s. CIF G03270014. Passeig Els Tolls, 2 (Edifici INVATTUR, 3a planta), 03502 Benidorm (Alacant). km0week@hosbec.com · 965 85 55 16">HOSBEC · %s. CIF G03270014. Paseo Els Tolls, 2 (Edificio INVATTUR, 3.ª planta), 03502 Benidorm (Alicante). km0week@hosbec.com · 965 85 55 16</p>'
     % (NOMBRE_VA, NOMBRE_ES)),

    ('''      <h2 data-va="Serveis de tercers">Servicios de terceros</h2>
      <p data-va="Aquesta web no carrega recursos externs: les tipografies, els scripts i les imatges s'allotgen al mateix servidor. Això vol dir que navegar-hi no envia cap petició a Google ni a cap altra empresa.">Esta web no carga recursos externos: las tipografías, los scripts y las imágenes se alojan en el mismo servidor. Eso quiere decir que navegar por ella no envía ninguna petición a Google ni a ninguna otra empresa.</p>''',
     '''      <h2 data-va="Serveis de tercers">Servicios de terceros</h2>
      <p data-va="Navegar per aquesta web no envia cap petició a tercers: les tipografies, els scripts i les imatges s'allotgen en el mateix servidor. Ni Google, ni xarxes socials, ni cap píxel de seguiment.">Navegar por esta web no envía ninguna petición a terceros: las tipografías, los scripts y las imágenes se alojan en el mismo servidor. Ni Google, ni redes sociales, ni ningún píxel de seguimiento.</p>
      <p data-va="L'única excepció són els dos formularis. Quan n'envies un, el contingut passa per FormSubmit (formsubmit.co), un servei que es limita a reenviar-nos-ho per correu a km0week@hosbec.com i que actua com a encarregat del tractament. Si prefereixes no fer-lo servir, escriu-nos directament a aqueixa adreça.">La única excepción son los dos formularios. Cuando envías uno, su contenido pasa por FormSubmit (formsubmit.co), un servicio que se limita a reenviárnoslo por correo a km0week@hosbec.com y que actúa como encargado del tratamiento. Si prefieres no usarlo, escríbenos directamente a esa dirección.</p>'''),
])

# 4.7 · Cookies: el apartado hablaba a HOSBEC, no al visitante
ed("_build/paginas/cookies.html", [
    ('<li data-va="No comparteix res amb tercers.">No comparte nada con terceros.</li>',
     '<li data-va="No comparteix la teua navegació amb ningú.">No comparte tu navegación con nadie.</li>'),
    ('''      <h2 data-va="Si afegiu analítica més endavant">Si añadís analítica más adelante</h2>
      <p data-va="Si en algun moment s'incorpora una eina de mesura, caldrà afegir ací la seua galeta i mostrar un banner de consentiment abans de carregar-la. Aquesta pàgina està preparada per a créixer amb aqueixa taula.">Si en algún momento se incorpora una herramienta de medición, habrá que añadir aquí su cookie y mostrar un banner de consentimiento antes de cargarla. Esta página está preparada para crecer con esa tabla.</p>''',
     '''      <h2 data-va="Analítica">Analítica</h2>
      <p data-va="Ara mateix no hi ha cap eina de mesurament. Si algun dia se n'incorpora una, aquesta pàgina ho recollirà i se't demanarà consentiment abans de carregar-la.">Ahora mismo no hay ninguna herramienta de medición. Si algún día se incorpora una, esta página lo recogerá y se te pedirá consentimiento antes de cargarla.</p>'''),
])


# ===========================================================================
print("cambios aplicados:", hechos)
if fallos:
    print("\n⚠  revisar (%d):" % len(fallos))
    for f in fallos:
        print("   ·", f)
    sys.exit(1)
print("todo correcto. Ahora:  python3 _build/build.py")
