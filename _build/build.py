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

import os, re, datetime

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGS = os.path.join(RAIZ, "_build", "paginas")

# ---------------------------------------------------------------------------
# DOMINIO: la dirección donde se publica la web. Se usa en sitemap.xml,
# robots.txt, las etiquetas canonical y las imágenes de compartir en redes.
# SIN barra final.
#   GitHub Pages de proyecto : https://USUARIO.github.io/km0week
#   GitHub Pages de usuario  : https://USUARIO.github.io
#   Dominio propio           : https://km0week.hosbec.com
# Cámbialo y vuelve a ejecutar:  python3 _build/build.py
# ---------------------------------------------------------------------------
DOMINIO = "https://km0week.hosbec.com"
FECHAS_ES = "13 – 19 de noviembre de 2026"
FECHAS_VA = "13 – 19 de novembre de 2026"

# ---------------------------------------------------------------- navegación --
MENU = [
    ("iniciativa.html",   "La iniciativa",  "La iniciativa"),
    ("alojamientos.html", "Alojamientos",   "Allotjaments"),
    ("mapa.html",         "Mapa",           "Mapa"),
    ("agenda.html",       "Agenda",         "Agenda"),
    ("noticias.html",     "Noticias",       "Notícies"),
    ("faq.html",          "Preguntas",      "Preguntes"),
]

PIE_COLS = [
    ("La semana", "La setmana", [
        ("iniciativa.html", "La iniciativa", "La iniciativa"),
        ("alojamientos.html", "Alojamientos", "Allotjaments"),
        ("mapa.html", "Mapa y cercanía", "Mapa i proximitat"),
        ("agenda.html", "Agenda", "Agenda"),
        ("noticias.html", "Noticias", "Notícies"),
    ]),
    ("Alojamientos", "Allotjaments", [
        ("suma.html", "Suma tu alojamiento", "Suma el teu allotjament"),
        ("suma.html#requisitos", "Requisitos", "Requisits"),
        ("descargas.html", "Materiales y kit", "Materials i kit"),
        ("prensa.html", "Sala de prensa", "Sala de premsa"),
        ("https://hosbec.com", "hosbec.com", "hosbec.com"),
    ]),
]

PIE_LEGAL = [
    ("aviso-legal.html", "Aviso legal", "Avís legal"),
    ("privacidad.html", "Privacidad", "Privacitat"),
    ("cookies.html", "Cookies", "Galetes"),
    ("faq.html", "Preguntas frecuentes", "Preguntes freqüents"),
]


# ------------------------------------------------------------------- plantilla --
def cabeza(p):
    css_extra = "".join('\n<link rel="stylesheet" href="%s">' % c for c in p.get("css", []))
    canon = DOMINIO + "/" + p["archivo"]
    noindex = '\n<meta name="robots" content="noindex">' if p.get("noindex") else ""
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{p['titulo']}</title>
<meta name="description" content="{p['desc']}">{noindex}
<link rel="canonical" href="{canon}">
<meta name="theme-color" content="#1EA4C6">
<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
<meta property="og:site_name" content="HOSBEC Km0 Week">
<meta property="og:title" content="{p['titulo']}">
<meta property="og:description" content="{p['desc']}">
<meta property="og:type" content="website">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{DOMINIO}/{p.get('og', 'assets/img/foto/cab-iniciativa.webp')}">
<meta name="twitter:card" content="summary_large_image">
<link rel="stylesheet" href="assets/css/km0.css">{css_extra}
<!-- En un servidor normal precargamos las dos tipografías principales.
     Si la web se abre directamente desde el disco (file://) el navegador
     bloquea los .woff2 sueltos por CORS: en ese caso, y solo en ese caso,
     cargamos las mismas tipografías embebidas en base64. -->
<script>
  document.write(location.protocol === "file:"
    ? '<link rel="stylesheet" href="assets/css/fuentes-local.css">'
    : '<link rel="preload" href="assets/fonts/montserrat-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>'
    + '<link rel="preload" href="assets/fonts/lora-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>');
</script>
</head>
<body>
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
      <img class="emblema" src="assets/img/emblema.svg" alt="" width="38" height="38">
      <span class="brand-txt">
        <span><span class="k">KM0</span><span class="w">week</span></span>
        <small>Hosbec · Comunitat Valenciana</small>
      </span>
    </a>

    <nav class="nav-links" aria-label="Principal">{enlaces}
      <span class="nav-cta-mobile"><a href="suma.html" data-va="Sóc allotjament">Soy alojamiento</a></span>
    </nav>

    <div class="nav-right">
      <div class="lang" role="group" aria-label="Idioma">
        <button type="button" data-lang="es" aria-pressed="true">ES</button>
        <button type="button" data-lang="va" aria-pressed="false">VA</button>
      </div>
      <a class="btn btn-terra btn-sm" href="suma.html" data-va="Sóc allotjament">Soy alojamiento</a>
      <button class="burger" aria-label="Menú" aria-expanded="false"><i></i><i></i></button>
    </div>
  </div>
</header>
"""


def pie():
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
          <img src="assets/img/emblema.svg" alt="" width="38" height="38">
          <span><span class="k">KM0</span><span class="w">week</span></span>
        </div>
        <p class="body-sm foot-lema" data-va="Descobreix el que és a prop, viu el que és nostre.">Descubre lo cerca, vive lo nuestro.</p>
        <p class="body-sm foot-lema" data-fechas>{FECHAS_ES}</p>
      </div>{cols}
      <div>
        <h5 data-va="T'avisem">Te avisamos</h5>
        <p class="body-sm foot-lema" data-va="Deixa el teu correu i t'escrivim quan s'òbriguen les reserves.">Deja tu correo y te escribimos cuando se abran las reservas.</p>
        <form class="subscribe" onsubmit="event.preventDefault();this.reset();window.Km0.toast(window.Km0.lang==='va'?'Gràcies! T\\'avisarem.':'¡Gracias! Te avisaremos.');">
          <input type="email" required placeholder="tu@correo.com" aria-label="Correo">
          <button class="btn btn-terra btn-sm" type="submit" data-va="Avisa'm">Avísame</button>
        </form>
      </div>
    </div>
    <div class="foot-bot">
      <span>© <span data-year>2026</span> HOSBEC · Asociación Empresarial Hostelera de Benidorm, Costa Blanca y Comunidad Valenciana</span>
      <span class="foot-legal">{legal}</span>
      <span>km0week@hosbec.com · 965 85 51 12</span>
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
    cuerpo = open(os.path.join(PAGS, p["cuerpo"]), encoding="utf-8").read()
    html = (cabeza(p) + cinta() + nav(p["archivo"]) +
            '\n<main id="main">\n' + cabecera(p) + cuerpo + "\n</main>\n" +
            pie() + scripts(p))
    destino = os.path.join(RAIZ, p["archivo"])
    open(destino, "w", encoding="utf-8").write(html)
    return destino


# ------------------------------------------------------------------- páginas --
def C(foto, ante, titulo, lede=None):
    return {"foto": foto, "ante": ante, "titulo": titulo, "lede": lede}


PAGINAS = [
    dict(archivo="index.html", cuerpo="portada.html",
         titulo="HOSBEC Km0 Week · Descubre lo cerca, vive lo nuestro",
         desc="Del 13 al 19 de noviembre de 2026. Una semana para que quienes vivimos en la Comunitat Valenciana redescubramos nuestros alojamientos. Ofertas para residentes y reserva directa.",
         og="assets/img/foto/cab-iniciativa.webp"),

    dict(archivo="iniciativa.html", cuerpo="iniciativa.html",
         titulo="La iniciativa · HOSBEC Km0 Week",
         desc="Qué es la Km0 Week, por qué la hacemos, quién está detrás y qué compromisos asume cada alojamiento adherido.",
         og="assets/img/foto/cab-iniciativa.webp",
         cab=C("cab-iniciativa", ("La iniciativa", "La iniciativa"),
               ("Una semana para mirar de otra forma lo que tenemos al lado",
                "Una setmana per a mirar d'una altra manera el que tenim al costat"),
               ("Km0 Week nace de una idea simple: quien vive en un destino turístico casi nunca lo disfruta como tal. Del 13 al 19 de noviembre le damos la vuelta.",
                "Km0 Week naix d'una idea simple: qui viu en un destí turístic quasi mai el gaudeix com a tal. Del 13 al 19 de novembre li donem la volta."))),

    dict(archivo="alojamientos.html", cuerpo="alojamientos.html",
         titulo="Alojamientos y ofertas · HOSBEC Km0 Week",
         desc="Todos los alojamientos adheridos a la Km0 Week con su oferta para residentes. Filtra por provincia, tipo, experiencia y precio.",
         og="assets/img/foto/cab-alojamientos.webp",
         cab=C("cab-alojamientos", ("Dónde dormir", "On dormir"),
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
         titulo="Agenda de la semana · HOSBEC Km0 Week",
         desc="Programa día a día de la Km0 Week: visitas, talleres, rutas y actividades abiertas a todo el mundo, del 13 al 19 de noviembre de 2026.",
         og="assets/img/foto/cab-agenda.webp",
         cab=C("cab-agenda", ("Programa", "Programa"),
               ("Siete días, algo que hacer cada día", "Set dies, alguna cosa a fer cada dia"),
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
         desc="Dudas resueltas sobre la Km0 Week: quién puede reservar, cómo funcionan los descuentos, el pasaporte, el sorteo y las condiciones.",
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
         desc="Cartelería, kit de redes sociales, pasaporte imprimible, manual de marca y plantillas para los alojamientos adheridos.",
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

# ------------------------------------------------------------------ noticias --
NOTICIAS = [
    ("noticia-1", "not-1", ("Noticias", "Notícies"),
     ("20 alojamientos ya se han sumado a la primera Km0 Week",
      "20 allotjaments ja s'han sumat a la primera Km0 Week"),
     "Cerramos la primera tanda de adhesiones con presencia en las tres provincias y 504 plazas reservadas para residentes."),
    ("noticia-2", "not-2", ("Noticias", "Notícies"),
     ("Cómo se calcula el descuento de residente (y por qué es real)",
      "Com es calcula el descompte de resident (i per què és real)"),
     "El compromiso de la Km0 Week es que el precio de la semana sea el más bajo del trimestre. Explicamos cómo se comprueba."),
    ("noticia-3", "not-3", ("Noticias", "Notícies"),
     ("Doce ayuntamientos se suman con actividades abiertas",
      "Dotze ajuntaments se sumen amb activitats obertes"),
     "Visitas a espacios normalmente cerrados, rutas guiadas y talleres que se abren solo durante la semana."),
    ("noticia-4", "not-4", ("Noticias", "Notícies"),
     ("El pasaporte Km0: cómo funciona el sorteo de diez estancias",
      "El passaport Km0: com funciona el sorteig de deu estades"),
     "Tres sellos para entrar en el sorteo, cinco para la cena de clausura. Bases y calendario."),
]


def paginas_noticia():
    return [dict(archivo=slug + ".html", cuerpo=slug + ".html",
                 titulo=tit[0] + " · HOSBEC Km0 Week", desc=sub,
                 og="assets/img/foto/%s.webp" % foto,
                 cab=C(foto, ante, tit))
            for slug, foto, ante, tit, sub in NOTICIAS]


# ------------------------------------------------------------------ auxiliares --
def sitemap(paginas):
    hoy = "2026-08-17"
    urls = "".join(
        "\n  <url><loc>%s/%s</loc><lastmod>%s</lastmod><changefreq>weekly</changefreq><priority>%s</priority></url>"
        % (DOMINIO, p["archivo"], hoy, "1.0" if p["archivo"] == "index.html" else "0.7")
        for p in paginas if not p.get("noindex"))
    open(os.path.join(RAIZ, "sitemap.xml"), "w", encoding="utf-8").write(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">%s\n</urlset>\n' % urls)
    open(os.path.join(RAIZ, "robots.txt"), "w", encoding="utf-8").write(
        "User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n" % DOMINIO)


def main():
    todas = PAGINAS + paginas_noticia()
    for p in todas:
        construir(p)
    sitemap(todas)
    print("páginas generadas:", len(todas), "+ sitemap.xml + robots.txt")


if __name__ == "__main__":
    main()
