#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Km0 Week — generador del sitio.

Junta la parte común de todas las páginas (cabecera, navegación, pie y scripts)
con el contenido de cada una, que vive suelto en _build/paginas/*.html.

  python3 _build/build.py       → escribe los .html en la raíz del proyecto

Para cambiar el menú, el pie o los metadatos: se toca AQUÍ y sale en todas.
Para cambiar el texto de una página: se toca su archivo en _build/paginas/.
"""

import os, re, datetime, sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGS = os.path.join(RAIZ, "_build", "paginas")

# ---------------------------------------------------------------------------
# TODO EL CONTENIDO VIENE DE contenido/*.json, que es lo que escribe el panel.
# Antes estaba a mano aquí abajo y en assets/js/data-alojamientos.js, con el
# resultado de que lo que se guardaba en el panel no llegaba nunca a la web.
# Desde el 14/09/2026 el orden es: el panel escribe el JSON -> build.py lo lee
# -> de ahí salen las páginas Y assets/js/data-alojamientos.js.
#
# Consecuencia: data-alojamientos.js pasa a ser un ARCHIVO GENERADO. No se
# edita a mano; lo que se escriba ahí se pierde en la siguiente compilación.
# ---------------------------------------------------------------------------
sys.path.insert(0, os.path.join(RAIZ, "_build"))
import contenido

# ---------------------------------------------------------------------------
# DOMINIO: la dirección donde se publica la web. Se usa en sitemap.xml,
# robots.txt, las etiquetas canonical y las imágenes de compartir en redes.
# SIN barra final.
#   Dominio propio           : https://km0week.com      <-- EL QUE SE USA
#   GitHub Pages de proyecto : https://USUARIO.github.io/km0week
#   GitHub Pages de usuario  : https://USUARIO.github.io
# El build escribe tambien el archivo CNAME a partir de este valor: es lo que
# le dice a GitHub Pages cual es el dominio propio. Si el CNAME desaparece del
# repositorio, GitHub deja de servir la web en km0week.com.
# Cambialo y vuelve a ejecutar:  python3 _build/build.py
# ---------------------------------------------------------------------------
DOMINIO = contenido.DOMINIO
EMAIL_KM0 = contenido.EMAIL
FECHAS_ES = contenido.FECHAS_ES
FECHAS_VA = contenido.FECHAS_VA

# ---------------------------------------------------------------- navegación --
# Sale de contenido/navegacion.json (panel -> Edición -> Menú y pie). Se pasa
# a la forma de tuplas que ya usaban nav() y pie(), para no tocarlas.
def _enlaces(lista):
    return [(e["url"], e["es"], e["va"]) for e in lista]


MENU = _enlaces(contenido.NAVEGACION["menu"])

PIE_COLS = [(c["titulo"]["es"], c["titulo"]["va"], _enlaces(c["enlaces"]))
            for c in contenido.NAVEGACION["pie"]]

PIE_LEGAL = _enlaces(contenido.NAVEGACION["legal"])


# ------------------------------------------------------------------- plantilla --
def cabeza(p):
    cuerpo_clase = ' class="home"' if p["archivo"] == "index.html" else ""
    css_extra = "".join('\n<link rel="stylesheet" href="%s">' % c for c in p.get("css", []))
    # la portada canoniza a la carpeta, no a /index.html
    canon = DOMINIO + "/" + ("" if p["archivo"] == "index.html" else p["archivo"])
    noindex = '\n<meta name="robots" content="noindex">' if p.get("noindex") else ""
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{p['titulo']}</title>
<meta name="description" content="{p['desc']}">{noindex}
<link rel="canonical" href="{canon}">
<meta name="theme-color" content="#394642">
<link rel="icon" href="assets/img/favicon-32.png" sizes="32x32" type="image/png">
<link rel="icon" href="assets/img/icono-512.png" sizes="512x512" type="image/png">
<link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png">
<meta property="og:site_name" content="HOSBEC Km0 Week">
<meta property="og:title" content="{p['titulo']}">
<meta property="og:description" content="{p['desc']}">
<meta property="og:type" content="website">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{DOMINIO}/{p.get('og', 'assets/img/foto/hero-cocktail.webp')}">
<meta name="twitter:card" content="summary_large_image">
<link rel="stylesheet" href="assets/css/km0.css">{css_extra}
<!-- En un servidor normal precargamos la tipografía de la marca.
     Si la web se abre directamente desde el disco (file://) el navegador
     bloquea los .woff2 sueltos por CORS: en ese caso, y solo en ese caso,
     cargamos la misma tipografía embebida en base64. -->
<script>
  document.write(location.protocol === "file:"
    ? '<link rel="stylesheet" href="assets/css/fuentes-local.css">'
    : '<link rel="preload" href="assets/fonts/bricolage-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>');
</script>
</head>
<body{cuerpo_clase}>
<a class="skip" href="#main" data-va="Anar al contingut">Ir al contenido</a>
"""


def cinta():
    return f"""
<!-- ============================== CINTA ================================= -->
<div class="ribbon">
  <div class="wrap">
    <span class="r-left" data-va="Una iniciativa de HOSBEC per als veïns i veïnes de la Comunitat Valenciana">Una iniciativa de HOSBEC para los vecinos y vecinas de la Comunitat Valenciana</span>
    <span class="r-right">
      <span data-fechas>{FECHAS_ES}</span>
      <span><span data-va="Queden">Quedan</span> <b id="cuenta">—</b></span>
    </span>
  </div>
</div>
"""


def nav(activo):
    enlaces = "".join(
        '\n      <a href="%s"%s data-va="%s">%s</a>' %
        (url, ' class="on" aria-current="page"' if url == activo else "", va, es)
        for url, es, va in MENU)
    return f"""
<!-- ============================ NAVEGACIÓN ============================== -->
<header class="nav">
  <div class="wrap">
    <a class="brand" href="index.html" aria-label="Km0 Week — inicio">
      <img class="logo logo-h" src="assets/img/logo-h-blanco.png" alt="Km0 Week · HOSBEC" width="900" height="379">
      <img class="logo logo-v" src="assets/img/logo-v-blanco.png" alt="" width="520" height="916" aria-hidden="true">
    </a>

    <nav class="nav-links" aria-label="Principal">{enlaces}
      <span class="nav-cta-mobile"><a href="suma.html" data-va="Sóc allotjament">Soy alojamiento</a></span>
    </nav>

    <div class="nav-right">
      <div class="lang" role="group" aria-label="Idioma">
        <button type="button" data-lang="es" aria-pressed="true">ES</button>
        <button type="button" data-lang="va" aria-pressed="false">VA</button>
      </div>
      <button class="burger" aria-label="Menú" aria-expanded="false"><i></i><i></i></button>
    </div>
  </div>
</header>
"""


def pie(p):
    cols = ""
    for es, va, enl in PIE_COLS:
        items = "".join(
            '\n          <li><a href="%s"%s data-va="%s">%s</a></li>' %
            (u, ' target="_blank" rel="noopener"' if u.startswith("http") else "", tva, tes)
            for u, tes, tva in enl)
        cols += f"""
      <div>
        <h5 data-va="{va}">{es}</h5>
        <ul>{items}
        </ul>
      </div>"""
    legal = " · ".join('<a href="%s" data-va="%s">%s</a>' % (u, va, es) for u, es, va in PIE_LEGAL)
    return f"""
<!-- =============================== PIE ================================== -->
<footer class="foot">
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <div class="foot-marca">
          <img src="assets/img/logo-v-verde.png" alt="Km0 Week · HOSBEC" width="520" height="916">
        </div>
        <p class="body-sm foot-lema" data-va="Descobreix el que és a prop, viu el que és nostre.">Descubre lo cerca, vive lo nuestro.</p>
        <p class="body-sm foot-lema" data-fechas>{FECHAS_ES}</p>
      </div>{cols}
      <div>
        <h5 data-va="T'avisem">Te avisamos</h5>
        <p class="body-sm foot-lema" data-va="Deixa el teu correu i t'escrivim quan s'òbriguen les reserves.">Deja tu correo y te escribimos cuando se abran las reservas.</p>
        <form class="subscribe" id="form-boletin" novalidate>
          <input type="text" name="_honey" style="display:none" tabindex="-1" autocomplete="off" aria-hidden="true">
          <input type="email" name="email" required placeholder="tu@correo.com" aria-label="Correo">
          <button class="btn btn-terra btn-sm" type="submit" data-va="Avisa'm">Avísame</button>
        </form>
      </div>
    </div>
    <div class="foot-bot">
      <span>© <span data-year>2026</span> HOSBEC · <span data-va="Associació Empresarial Hotelera i Turística de la Comunitat Valenciana">Asociación Empresarial Hotelera y Turística de la Comunidad Valenciana</span></span>
      <span class="foot-legal">{legal}</span>
      <span class="foot-contacto">
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
        <svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M13.4 20.5v-6.9h2.3l.35-2.7h-2.65V9.2c0-.78.22-1.31 1.34-1.31h1.43V5.47c-.25-.03-1.1-.11-2.09-.11-2.07 0-3.48 1.26-3.48 3.58v2h-2.34v2.7h2.34v6.86z"/></svg>
      </a>
      <a href="https://x.com/hosbeconline" target="_blank" rel="noopener" aria-label="X de HOSBEC" title="X">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 4l16 16M20 4L4 20"/></svg>
      </a>
      <a href="https://www.youtube.com/@hosbeconline" target="_blank" rel="noopener" aria-label="YouTube de HOSBEC" title="YouTube">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2.6" y="5.6" width="18.8" height="12.8" rx="4"/><path d="M10.4 9.6l4.4 2.4-4.4 2.4z"/></svg>
      </a>
    </div>
  </div>
</footer>
"""


def scripts(p):
    extra = "".join('\n<script src="%s"></script>' % s for s in p.get("js", []))
    return f"""
<script src="assets/js/data-alojamientos.js"></script>
<script src="assets/js/isocrona.js"></script>
<script src="assets/js/home.js"></script>{extra}
<script src="assets/vendor/anime.global.js"></script>
<script src="assets/js/motion.js"></script>
</body>
</html>
"""


def cabecera(p):
    """Cabecera ilustrada de página interior."""
    if not p.get("cab"):
        return ""
    foto = p["cab"]["foto"]
    ante_es, ante_va = p["cab"]["ante"]
    tit_es, tit_va = p["cab"]["titulo"]
    lede = p["cab"].get("lede")
    lede_html = ('\n      <p class="lede" data-va="%s">%s</p>' % (lede[1], lede[0])) if lede else ""
    migas = '<a href="index.html" data-va="Inici">Inicio</a> <i>/</i> <span data-va="%s">%s</span>' % (tit_va, tit_es)
    return f"""
<section class="cabecera">
  <img class="cabecera-foto" src="assets/img/foto/{foto}.webp" alt="" width="2000" height="900" fetchpriority="high">
  <div class="wrap cabecera-in">
    <nav class="migas" aria-label="Ruta">{migas}</nav>
    <span class="label label-arena" data-va="{ante_va}">{ante_es}</span>
    <h1 class="d1" data-va="{tit_va}">{tit_es}</h1>{lede_html}
  </div>
</section>
"""


def construir(p):
    # El cuerpo viene de un archivo de _build/paginas/ o ya renderizado desde
    # los datos (las noticias, que salen de contenido/noticias.json).
    cuerpo = p.get("html")
    if cuerpo is None:
        cuerpo = open(os.path.join(PAGS, p["cuerpo"]), encoding="utf-8").read()
    # las páginas pueden escribir @@DOMINIO@@ y aquí se sustituye
    cuerpo = cuerpo.replace("@@DOMINIO@@", DOMINIO)
    cuerpo = cuerpo.replace("@@TARJETAS_NOTICIAS@@", TARJETAS_NOTICIAS)
    html = (cabeza(p) + nav(p["archivo"]) +
            '\n<main id="main">\n' + cabecera(p) + cuerpo + "\n</main>\n" +
            pie(p) + scripts(p))
    destino = os.path.join(RAIZ, p["archivo"])
    open(destino, "w", encoding="utf-8").write(html)
    return destino


# ------------------------------------------------------------------- páginas --
def C(foto, ante, titulo, lede=None):
    return {"foto": foto, "ante": ante, "titulo": titulo, "lede": lede}


PAGINAS = [
    dict(archivo="index.html", cuerpo="portada.html",
         titulo="HOSBEC Km0 Week · Descubre lo cerca, vive lo nuestro",
         desc="Del 13 al 29 de noviembre de 2026. Tres fines de semana para que quienes vivimos en la Comunitat Valenciana redescubramos nuestros alojamientos. Ofertas para residentes y reserva directa.",
         og="assets/img/foto/cab-iniciativa.webp"),

    dict(archivo="iniciativa.html", cuerpo="iniciativa.html",
         titulo="La iniciativa · HOSBEC Km0 Week",
         desc="Qué es la Km0 Week, por qué la hacemos, quién está detrás y qué compromisos asume cada alojamiento adherido.",
         og="assets/img/foto/cab-iniciativa.webp",
         cab=C("cab-iniciativa", ("La iniciativa", "La iniciativa"),
               ("Tres fines de semana para mirar de otra forma lo que tenemos al lado",
                "Tres caps de setmana per a mirar d'una altra manera el que tenim al costat"),
               ("Km0 Week nace de una idea simple: quien vive en un destino turístico casi nunca lo disfruta como tal. Del 13 al 29 de noviembre le damos la vuelta.",
                "Km0 Week naix d'una idea simple: qui viu en un destí turístic quasi mai el gaudeix com a tal. Del 13 al 29 de novembre li donem la volta."))),

    dict(archivo="alojamientos.html", cuerpo="alojamientos.html",
         titulo="Experiencias y ofertas · HOSBEC Km0 Week",
         desc="Todas las experiencias y alojamientos adheridos a la Km0 Week con su oferta para residentes. Filtra por provincia, tipo, experiencia y precio.",
         og="assets/img/foto/cab-alojamientos.webp",
         cab=C("cab-alojamientos", ("Experiencias", "Experiències"),
               ("Todas las ofertas, en un sitio", "Totes les ofertes, en un lloc"),
               ("Cada alojamiento pone su propuesta y sus condiciones. Reservas directamente con él: aquí no hay comisiones ni intermediarios.",
                "Cada allotjament posa la seua proposta i les seues condicions. Reserves directament amb ell: ací no hi ha comissions ni intermediaris."))),

    dict(archivo="mapa.html", cuerpo="mapa.html",
         titulo="Mapa y cercanía · HOSBEC Km0 Week",
         desc="Dinos dónde vives y te decimos qué alojamientos de la Km0 Week tienes a menos de media hora, una hora y dos horas de casa.",
         og="assets/img/foto/cab-mapa.webp",
         cab=C("cab-mapa", ("Cerca de ti", "Prop de tu"),
               ("¿Cuánto es «cerca» para ti?", "Quant és «a prop» per a tu?"),
               ("Elige tu municipio y el mapa te ordena todos los alojamientos por tiempo de viaje. Sin instalar nada y sin dar tu ubicación si no quieres.",
                "Tria el teu municipi i el mapa t'ordena tots els allotjaments per temps de viatge. Sense instal·lar res i sense donar la teua ubicació si no vols."))),

    dict(archivo="agenda.html", cuerpo="agenda.html",
         titulo="Agenda de la edición · HOSBEC Km0 Week",
         desc="Programa día a día de la Km0 Week: visitas, talleres, rutas y actividades abiertas a todo el mundo, del 13 al 29 de noviembre de 2026.",
         og="assets/img/foto/cab-agenda.webp",
         cab=C("cab-agenda", ("Programa", "Programa"),
               ("Diecisiete días, algo que hacer cada fin de semana", "Dèsset dies, alguna cosa a fer cada cap de setmana"),
               ("Actividades abiertas: no hace falta alojarse para venir. Algunas son gratuitas y otras tienen una aportación simbólica.",
                "Activitats obertes: no cal allotjar-se per a vindre. Algunes són gratuïtes i altres tenen una aportació simbòlica."))),

    dict(archivo="suma.html", cuerpo="suma.html",
         titulo="Suma tu alojamiento · HOSBEC Km0 Week",
         desc="Cómo adherir tu hotel, apartamento, camping o casa rural a la Km0 Week: requisitos, plazos, qué pone HOSBEC y qué pones tú.",
         og="assets/img/foto/cab-suma.webp",
         cab=C("cab-suma", ("Para alojamientos", "Per a allotjaments"),
               ("Tu alojamiento también puede ser Km 0", "El teu allotjament també pot ser Km 0"),
               ("Sumarse es gratuito para los asociados de HOSBEC. Tú pones la oferta; nosotros ponemos la campaña, el tráfico y la comunicación.",
                "Sumar-se és gratuït per als associats d'HOSBEC. Tu poses l'oferta; nosaltres posem la campanya, el trànsit i la comunicació."))),

    dict(archivo="faq.html", cuerpo="faq.html",
         titulo="Preguntas frecuentes · HOSBEC Km0 Week",
         desc="Dudas resueltas sobre la Km0 Week: quién puede reservar, cómo funcionan los descuentos, las actividades abiertas y las condiciones.",
         og="assets/img/foto/cab-faq.webp",
         cab=C("cab-faq", ("Preguntas frecuentes", "Preguntes freqüents"),
               ("Lo que más nos preguntáis", "El que més ens pregunteu"),
               ("Si no encuentras tu respuesta, escríbenos a km0week@hosbec.com y la añadimos aquí.",
                "Si no trobes la teua resposta, escriu-nos a km0week@hosbec.com i l'afegim ací."))),

    dict(archivo="noticias.html", cuerpo="noticias.html",
         titulo="Noticias · HOSBEC Km0 Week",
         desc="Cómo avanza la Km0 Week: adhesiones, acuerdos con ayuntamientos, novedades del programa y balance de la edición.",
         og="assets/img/foto/cab-noticias.webp",
         cab=C("cab-noticias", ("Noticias", "Notícies"),
               ("Cómo va la Km0 Week", "Com va la Km0 Week"),
               ("Vamos contando aquí lo que se mueve: adhesiones, acuerdos, programa y todo lo que os pueda interesar.",
                "Anem contant ací el que es mou: adhesions, acords, programa i tot el que us puga interessar."))),

    dict(archivo="prensa.html", cuerpo="prensa.html",
         titulo="Sala de prensa · HOSBEC Km0 Week",
         desc="Material para medios: dossier, notas de prensa, cifras de la edición, logotipos y contacto de comunicación de HOSBEC.",
         og="assets/img/foto/cab-prensa.webp",
         cab=C("cab-prensa", ("Sala de prensa", "Sala de premsa"),
               ("Material para medios", "Material per a mitjans"),
               ("Dossier, notas de prensa, cifras verificables y logotipos. Si necesitas algo que no está aquí, llámanos.",
                "Dossier, notes de premsa, xifres verificables i logotips. Si necessites alguna cosa que no està ací, telefona'ns."))),

    dict(archivo="descargas.html", cuerpo="descargas.html",
         titulo="Materiales y kit gráfico · HOSBEC Km0 Week",
         desc="Cartelería, kit de redes sociales, manual de marca y textos preparados para los alojamientos adheridos.",
         og="assets/img/foto/cab-descargas.webp",
         cab=C("cab-descargas", ("Descargas", "Descàrregues"),
               ("Todo lo que necesitas para contarlo", "Tot el que necessites per a contar-ho"),
               ("Material listo para imprimir y para redes. Descarga libre para los alojamientos adheridos, ayuntamientos y medios.",
                "Material llest per a imprimir i per a xarxes. Descàrrega lliure per als allotjaments adherits, ajuntaments i mitjans."))),

    dict(archivo="aviso-legal.html", cuerpo="aviso-legal.html",
         titulo="Aviso legal · HOSBEC Km0 Week",
         desc="Aviso legal e información del titular de la web de la HOSBEC Km0 Week.",
         cab=C("cab-legal", ("Legal", "Legal"), ("Aviso legal", "Avís legal"))),

    dict(archivo="privacidad.html", cuerpo="privacidad.html",
         titulo="Política de privacidad · HOSBEC Km0 Week",
         desc="Cómo tratamos los datos personales en la web de la HOSBEC Km0 Week.",
         cab=C("cab-legal", ("Legal", "Legal"), ("Política de privacidad", "Política de privacitat"))),

    dict(archivo="cookies.html", cuerpo="cookies.html",
         titulo="Política de cookies · HOSBEC Km0 Week",
         desc="Qué se guarda en tu navegador al usar la web de la HOSBEC Km0 Week.",
         cab=C("cab-legal", ("Legal", "Legal"), ("Política de cookies", "Política de galetes"))),

    dict(archivo="404.html", cuerpo="404.html", noindex=True,
         titulo="Página no encontrada · HOSBEC Km0 Week",
         desc="La página que buscas no existe. Te dejamos los accesos a los alojamientos, el mapa, la agenda y la información de la HOSBEC Km0 Week.",
         cab=C("cab-404", ("Error 404", "Error 404"),
               ("Esta página se ha ido de escapada", "Aquesta pàgina se n'ha anat d'escapada"),
               ("No hemos encontrado lo que buscabas. Te dejamos por dónde seguir.",
                "No hem trobat el que buscaves. Et deixem per on continuar."))),
]

# ---------------------------------------------------------------- noticias --
# Las noticias salen de contenido/noticias.json, que es lo que escribe el
# panel. El cuerpo se guarda en texto plano con seis marcas y se convierte
# aquí. El panel tiene el MISMO convertidor (`cuerpoAHtml` en admin/index.html)
# para que la vista previa enseñe exactamente lo que se va a publicar: si se
# toca uno, hay que tocar el otro.
#
#   ## subtítulo        <h2>
#   > cita              <blockquote class="cita">
#   - viñeta            <ul>
#   1. numerada         <ol>
#   | a | b |           <table class="tabla"> dentro de .tabla-envolt
#   [texto](enlace)     <a href="enlace">
#
# Lo bilingüe: se renderizan el castellano y el valenciano por separado y el
# valenciano se cuelga del elemento como `data-va` (texto suelto) o
# `data-va-html` (cuando dentro hay un enlace), que es lo que sabe leer el
# selector de idioma. Si un idioma tiene más bloques que el otro —porque
# alguien ha editado solo uno— el bloque descabalado sale sin traducir en vez
# de emparejarse con el que no toca.

MESES_ES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
            "agosto", "septiembre", "octubre", "noviembre", "diciembre"]


def _esc(t):
    return (str(t).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def _con_enlaces(t):
    return re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", r'<a href="\2">\1</a>', _esc(t))


def _bloques(txt):
    return [b for b in re.split(r"\n\s*\n", (txt or "").strip()) if b.strip()]


def _atrib(va):
    """Cómo se cuelga una traducción: como texto o como HTML."""
    if not va:
        return ""
    return ' %s="%s"' % ("data-va-html" if "<" in va else "data-va", _esc(va))


def _lineas(b):
    return [l.strip() for l in b.split("\n") if l.strip()]


def _celdas(l):
    return [c.strip() for c in l.strip().strip("|").split("|")]


def _empareja(a, b):
    """Empareja dos listas; lo que no tenga pareja se queda sin traducir."""
    return [(x, b[k] if k < len(b) else "") for k, x in enumerate(a)]


def _bloque(b, v=""):
    """Un bloque de texto plano -> su HTML, ya bilingüe.

    La traducción se cuelga del elemento más pequeño posible: de cada <li> y
    no de la lista entera, y del <a> cuando el párrafo es solo un enlace. Así,
    si alguien traduce media lista, la otra media sigue funcionando.
    """
    lineas, vlineas = _lineas(b), _lineas(v)
    if b.startswith("## "):
        return "<h2%s>%s</h2>" % (_atrib(v[3:].strip() if v.startswith("## ") else ""),
                                  _esc(b[3:].strip()))
    if b.startswith("> "):
        return '<blockquote class="cita"%s>%s</blockquote>' % (
            _atrib(v[2:].strip() if v.startswith("> ") else ""), _esc(b[2:].strip()))
    if lineas[0].startswith("|"):
        quita = lambda L: [l for l in L if not re.match(r"^\|[\s\-|:]+\|$", l)]
        filas, vfilas = quita(lineas), quita(vlineas)
        h = '<div class="tabla-envolt mt-1"><table class="tabla">'
        for k, (f, vf) in enumerate(_empareja(filas, vfilas)):
            etq = "th" if k == 0 else "td"
            if k == 0:
                h += "<thead>"
            elif k == 1:
                h += "<tbody>"
            h += "<tr>%s</tr>" % "".join(
                "<%s%s>%s</%s>" % (etq, _atrib(vc), _esc(c), etq)
                for c, vc in _empareja(_celdas(f), _celdas(vf) if vf else []))
            if k == 0:
                h += "</thead>"
        return h + ("</tbody>" if len(filas) > 1 else "") + "</table></div>"
    vinetas = all(l.startswith("- ") for l in lineas)
    nums = all(re.match(r"^\d+\.\s", l) for l in lineas)
    if vinetas or nums:
        pela = lambda l: re.sub(r"^(- |\d+\.\s*)", "", l)
        return "<%s>%s</%s>" % (
            "ol" if nums else "ul",
            "".join("<li%s>%s</li>" % (_atrib(_con_enlaces(pela(vl)) if vl else ""),
                                       _con_enlaces(pela(l)))
                    for l, vl in _empareja(lineas, vlineas)),
            "ol" if nums else "ul")
    # Párrafo. Si es SOLO un enlace, la traducción va en el <a>, que es lo que
    # se traduce de verdad; si no, en el <p>.
    texto, vtexto = " ".join(lineas), " ".join(vlineas)
    solo = re.match(r"^\[([^\]]+)\]\(([^)\s]+)\)$", texto)
    vsolo = re.match(r"^\[([^\]]+)\]\(([^)\s]+)\)$", vtexto)
    if solo:
        return '<p><a href="%s"%s>%s</a></p>' % (
            solo.group(2), _atrib(vsolo.group(1) if vsolo else ""), _esc(solo.group(1)))
    return "<p%s>%s</p>" % (_atrib(_con_enlaces(vtexto) if vtexto else ""),
                            _con_enlaces(texto))


def prosa(es, va=""):
    """El cuerpo de una noticia, bilingüe."""
    return "\n      ".join(
        _bloque(b, v) for b, v in _empareja(_bloques(es), _bloques(va)))


def _fecha_larga(iso):
    if not iso:
        return ""
    a, m, d = iso.split("-")
    return "%d de %s de %s" % (int(d), MESES_ES[int(m) - 1], a)


def _bi(n, campo, idioma="es"):
    return (n.get(campo) or {}).get(idioma, "")


def tarjeta_noticia(n):
    """Una tarjeta del listado de Noticias."""
    if n.get("proxima"):
        return '''      <article class="nota" aria-label="Próxima entrada">
        <img src="assets/img/foto/%s.webp" alt="" width="1200" height="800" loading="lazy">
        <div class="bd">
          <span class="label" style="color:var(--suave)" data-va="%s">%s</span>
          <h3 data-va="%s">%s</h3>
          <p class="body-sm" data-va="%s">%s</p>
          <span class="dato-fecha" data-va="%s">%s</span>
        </div>
      </article>''' % (
            n["imagen"], _esc(_bi(n, "etiqueta", "va")), _esc(_bi(n, "etiqueta")),
            _esc(_bi(n, "titulo", "va")), _esc(_bi(n, "titulo")),
            _esc(_bi(n, "resumen", "va")), _esc(_bi(n, "resumen")),
            _esc(_bi(n, "cuando", "va")), _esc(_bi(n, "cuando")))

    color = " label-%s" % n["color"] if n.get("color") else ""
    grande = " grande" if n.get("destacada") else ""
    tit = "h3 class=\"d3\"" if n.get("destacada") else "h3"
    a, m, d = (n.get("fecha") or "--- - -").split("-")
    lectura = "%d min de lectura" % (n.get("lectura") or 0)
    return '''      <a class="nota%s" href="%s.html">
        <img src="assets/img/foto/%s.webp" alt="" width="1200" height="800" loading="lazy">
        <div class="bd">
          <span class="label%s" data-va="%s">%s</span>
          <%s data-va="%s">%s</h3>
          <p class="body-sm" data-va="%s">%s</p>
          <span class="dato-fecha">%s · %s · %s · <span data-va="%s">%s</span></span>
        </div>
      </a>''' % (
        grande, n["slug"], n["imagen"], color,
        _esc(_bi(n, "etiqueta", "va")), _esc(_bi(n, "etiqueta")),
        tit, _esc(_bi(n, "titulo", "va")), _esc(_bi(n, "titulo")),
        _esc(_bi(n, "resumen", "va")), _esc(_bi(n, "resumen")),
        d, m, a, lectura, lectura)


def cuerpo_noticia(n):
    """La página entera de una noticia."""
    b = n.get("boton") or {}
    boton = ('\n      <a class="btn btn-mar" href="%s" data-va="%s">%s</a>'
             % (b["url"], _esc(b.get("va", "")), _esc(b.get("es", "")))) if b.get("url") else ""
    return '''<section class="sec">
  <div class="wrap">
    <article class="prosa">
      <p class="dato-fecha">%s · HOSBEC</p>
      <p class="lede" data-va="%s">%s</p>

      %s
    </article>

    <div class="mt-2" style="display:flex;gap:.8rem;flex-wrap:wrap">
      <a class="btn btn-linea" href="noticias.html" data-va="← Totes les notícies">← Todas las noticias</a>%s
    </div>
  </div>
</section>
''' % (_fecha_larga(n.get("fecha")),
       _esc(_bi(n, "entradilla", "va")), _esc(_bi(n, "entradilla")),
       prosa(_bi(n, "cuerpo"), _bi(n, "cuerpo", "va")), boton)


NOTICIAS = [n for n in contenido.NOTICIAS if not n.get("proxima")]

TARJETAS_NOTICIAS = "\n\n".join(tarjeta_noticia(n) for n in contenido.NOTICIAS)


def paginas_noticia():
    return [dict(archivo=n["slug"] + ".html", html=cuerpo_noticia(n),
                 titulo=_bi(n, "titulo") + " · HOSBEC Km0 Week",
                 desc=_bi(n, "resumen"),
                 og="assets/img/foto/%s.webp" % n["imagen"],
                 cab=C(n["imagen"], (_bi(n, "seccion"), _bi(n, "seccion", "va")),
                       (_bi(n, "titulo"), _bi(n, "titulo", "va"))))
            for n in NOTICIAS]


# ------------------------------------------------------------------ auxiliares --
def sitemap(paginas):
    hoy = "2026-08-17"
    urls = "".join(
        "\n  <url><loc>%s/%s</loc><lastmod>%s</lastmod><changefreq>weekly</changefreq><priority>%s</priority></url>"
        % (DOMINIO, "" if p["archivo"] == "index.html" else p["archivo"], hoy,
           "1.0" if p["archivo"] == "index.html" else "0.7")
        for p in paginas if not p.get("noindex"))
    open(os.path.join(RAIZ, "sitemap.xml"), "w", encoding="utf-8").write(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">%s\n</urlset>\n' % urls)
    open(os.path.join(RAIZ, "robots.txt"), "w", encoding="utf-8").write(
        "User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n" % DOMINIO)


def cname():
    """Escribe el archivo CNAME que GitHub Pages necesita para servir la web en
    el dominio propio. Se saca de DOMINIO, sin protocolo ni barra final.
    Si DOMINIO apunta a github.io no se escribe nada y se borra el CNAME que
    hubiera, porque ahí el dominio propio no pinta nada."""
    ruta = os.path.join(RAIZ, "CNAME")
    host = DOMINIO.split("//", 1)[-1].split("/", 1)[0].strip()
    if host.endswith("github.io"):
        if os.path.exists(ruta):
            os.remove(ruta)
        return None
    open(ruta, "w", encoding="utf-8", newline="\n").write(host + "\n")
    return host


def main():
    # Primero los datos: assets/js/data-alojamientos.js se REESCRIBE desde
    # contenido/*.json en cada compilación. Es lo que hace que un alta hecha
    # en el panel aparezca de verdad en la web.
    contenido.escribir_js()

    todas = PAGINAS + paginas_noticia()
    for p in todas:
        construir(p)
    sitemap(todas)
    host = cname()
    print("páginas generadas:", len(todas), "+ sitemap.xml + robots.txt"
          + (" + CNAME (%s)" % host if host else "")
          + " + data-alojamientos.js")


if __name__ == "__main__":
    main()
