#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Km0 Week — comprobación del contenido
=====================================

Revisa `contenido/*.json` antes de publicar y avisa de los fallos que hoy son
silenciosos: un `tipo` mal escrito que deja un hotel fuera de los filtros, unas
coordenadas del revés que lo mandan a Argelia, una frase sin valenciano, una
foto que no existe.

    python3 _build/verificar.py

Distingue dos cosas:

  ERROR   rompe algo que se ve. Detiene la publicación.
  AVISO   conviene arreglarlo, pero la web funciona. No detiene nada.

Las mismas reglas las usa el panel de administración para validar antes de
guardar, así que lo normal es que aquí no salte nunca nada.
"""

import datetime
import os
import re
import sys
import unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import contenido  # noqa: E402

RAIZ = contenido.RAIZ

TIPOS = {"hotel", "apartamentos", "camping", "rural", "hostal", "balneario"}
PROVINCIAS = {"Alicante", "València", "Castelló"}
EXPERIENCIAS = {"gastronomia", "bienestar", "familia", "cultura", "mar",
                "deporte", "romantico", "mascotas", "accesible", "sostenible",
                "noche"}
SERVICIOS = {"piscina", "spa", "parking", "wifi", "restaurante", "gimnasio",
             "playa", "mascotas", "accesible", "familiar", "vistas", "terraza"}

# Recuadro generoso alrededor de la Comunitat Valenciana. Sirve para cazar el
# error clásico de pegar las coordenadas en el orden contrario.
LAT = (37.7, 40.9)
LNG = (-1.7, 0.9)

errores = []
avisos = []


def error(donde, msg):
    errores.append("%s · %s" % (donde, msg))


def aviso(donde, msg):
    avisos.append("%s · %s" % (donde, msg))


sin_revisar = [0]


def bilingue(donde, campo, valor, obligatorio_va=False):
    """
    Comprueba un {es, va}.

    El valenciano vacío ya no es un problema: lo rellena Apertium al publicar.
    Lo que sí se cuenta es cuántos textos van a salir traducidos a máquina sin
    que nadie los haya mirado, que es lo que el panel deja revisar.
    """
    if not isinstance(valor, dict):
        error(donde, "«%s» debería tener texto en castellano y en valenciano" % campo)
        return
    if not (valor.get("es") or "").strip():
        error(donde, "«%s» está vacío en castellano" % campo)
        return
    if not (valor.get("va") or "").strip():
        if obligatorio_va:
            error(donde, "«%s» necesita el valenciano escrito a mano" % campo)
        else:
            sin_revisar[0] += 1


def existe_imagen(ruta):
    return os.path.isfile(os.path.join(RAIZ, ruta.replace("/", os.sep)))


# ---------------------------------------------------------------------------
# Alojamientos
# ---------------------------------------------------------------------------
def revisar_alojamientos():
    vistos = {}
    for i, a in enumerate(contenido.ALOJAMIENTOS):
        donde = "Alojamiento «%s»" % (a.get("nombre") or a.get("id") or "sin nombre nº %d" % (i + 1))

        ident = a.get("id") or ""
        if not ident:
            error(donde, "no tiene identificador")
        else:
            if ident in vistos:
                error(donde, "repite el identificador «%s», que ya usa «%s»" % (ident, vistos[ident]))
            vistos[ident] = a.get("nombre", ident)
            if not re.fullmatch(r"[a-z0-9-]+", ident):
                error(donde, "el identificador «%s» debe ser minúsculas, números y guiones, "
                             "sin espacios ni acentos" % ident)

        if a.get("tipo") not in TIPOS:
            error(donde, "tipo «%s» no válido. Solo: %s"
                  % (a.get("tipo"), ", ".join(sorted(TIPOS))))
        if a.get("provincia") not in PROVINCIAS:
            error(donde, "provincia «%s» no válida. Solo: Alicante, València, Castelló"
                  % a.get("provincia"))
        if not (a.get("destino") or "").strip():
            error(donde, "no tiene municipio")

        coords = a.get("coords")
        if not (isinstance(coords, list) and len(coords) == 2
                and all(isinstance(c, (int, float)) for c in coords)):
            error(donde, "las coordenadas deben ser dos números: [latitud, longitud]")
        else:
            lat, lng = coords
            if not (LAT[0] <= lat <= LAT[1] and LNG[0] <= lng <= LNG[1]):
                if LAT[0] <= lng <= LAT[1] and LNG[0] <= lat <= LNG[1]:
                    error(donde, "las coordenadas están del revés: pon [%s, %s]" % (lng, lat))
                else:
                    error(donde, "las coordenadas [%s, %s] caen fuera de la Comunitat Valenciana"
                          % (lat, lng))

        web = a.get("web") or ""
        if not web.startswith("https://"):
            error(donde, "la web debe empezar por https:// (ahora: «%s»)" % web)

        cupo = a.get("cupo")
        if not isinstance(cupo, int) or isinstance(cupo, bool) or cupo < 0:
            error(donde, "el cupo debe ser un número entero (ahora: %r)" % (cupo,))

        for exp in a.get("experiencias") or []:
            if exp not in EXPERIENCIAS:
                aviso(donde, "la experiencia «%s» no existe: no saldrá en ese filtro" % exp)
        for srv in a.get("servicios") or []:
            if srv not in SERVICIOS:
                aviso(donde, "el servicio «%s» no existe: no se verá su icono" % srv)

        img = a.get("imagen") or ""
        if img and not img.startswith("http") and not existe_imagen(img):
            error(donde, "la foto «%s» no está en el proyecto" % img)

        bilingue(donde, "claim", a.get("claim"))
        bilingue(donde, "descripcion", a.get("descripcion"))
        oferta = a.get("oferta") or {}
        if oferta:
            bilingue(donde, "oferta → titulo", oferta.get("titulo"))


# ---------------------------------------------------------------------------
# Agenda
# ---------------------------------------------------------------------------
def total_dias():
    ini = datetime.datetime.fromisoformat(contenido.CONFIG["fechaInicio"])
    fin = datetime.datetime.fromisoformat(contenido.CONFIG["fechaFin"])
    return (fin.date() - ini.date()).days + 1


def revisar_agenda():
    try:
        dias = total_dias()
    except Exception as e:
        error("Configuración", "las fechas de la edición no se entienden (%s)" % e)
        return

    for i, act in enumerate(contenido.AGENDA):
        titulo = ((act.get("titulo") or {}).get("es")) or "actividad nº %d" % (i + 1)
        donde = "Agenda · «%s»" % titulo

        dia = act.get("dia")
        if not isinstance(dia, int) or isinstance(dia, bool) or not (1 <= dia <= dias):
            error(donde, "el día %r está fuera de la edición, que tiene %d días: "
                         "esta actividad no aparecerá" % (dia, dias))

        if not re.fullmatch(r"([01]\d|2[0-3]):[0-5]\d", act.get("hora") or ""):
            error(donde, "la hora «%s» debe ir como HH:MM" % act.get("hora"))

        if not (act.get("lugar") or "").strip():
            error(donde, "no tiene lugar")

        enlace = act.get("enlace") or ""
        if enlace and not enlace.startswith("https://"):
            error(donde, "el enlace debe empezar por https:// (ahora: «%s»)" % enlace)
        if enlace.rstrip("/") in ("https://hosbec.com", "https://www.hosbec.com"):
            aviso(donde, "el botón «Quiero ir» sigue apuntando a hosbec.com, "
                         "no a la actividad")

        bilingue(donde, "titulo", act.get("titulo"))
        bilingue(donde, "desc", act.get("desc"))
        bilingue(donde, "precio", act.get("precio"))


# ---------------------------------------------------------------------------
# Configuración y noticias
# ---------------------------------------------------------------------------
def revisar_configuracion():
    c = contenido.CONFIG
    donde = "Configuración"
    try:
        ini = datetime.datetime.fromisoformat(c["fechaInicio"])
        fin = datetime.datetime.fromisoformat(c["fechaFin"])
        if fin <= ini:
            error(donde, "la fecha de fin no puede ser anterior a la de inicio")
    except Exception:
        error(donde, "fechaInicio o fechaFin no tienen el formato esperado")

    bilingue(donde, "fechasTexto", c.get("fechasTexto"), obligatorio_va=True)

    if not (c.get("dominio") or "").startswith("https://"):
        error(donde, "el dominio debe empezar por https://")
    if c.get("dominio", "").endswith("/"):
        error(donde, "el dominio no debe acabar en barra")
    if "@" not in (c.get("emailContacto") or ""):
        error(donde, "el correo de contacto no parece un correo")
    if not (c.get("endpointFormularios") or "").endswith("/exec"):
        aviso(donde, "la dirección de los formularios no acaba en /exec: "
                     "los envíos abrirán el correo del visitante en vez de guardarse")

    # Las cuatro cifras de portada (alojamientos, destinos, plazas y
    # actividades) no se configuran: se calculan solas a partir de los datos,
    # tanto en el HTML como en el navegador. No hay nada que cuadrar aquí.


def revisar_noticias():
    vistos = set()
    for n in contenido.NOTICIAS:
        slug = n.get("slug") or "?"
        donde = "Noticia «%s»" % ((n.get("titulo") or {}).get("es") or slug)
        if slug in vistos:
            error(donde, "repite el identificador «%s»" % slug)
        vistos.add(slug)
        if not os.path.isfile(os.path.join(RAIZ, "_build", "paginas", slug + ".html")):
            error(donde, "falta su página en _build/paginas/%s.html" % slug)
        img = "assets/img/foto/%s.webp" % n.get("imagen", "")
        if not existe_imagen(img):
            error(donde, "falta su imagen destacada «%s»" % img)
        bilingue(donde, "titulo", n.get("titulo"))
        if not (n.get("resumen") or "").strip():
            error(donde, "no tiene frase de resumen (sale en el listado y en Google)")


# ---------------------------------------------------------------------------
def main():
    revisar_configuracion()
    revisar_alojamientos()
    revisar_agenda()
    revisar_noticias()

    print("Km0 Week · comprobación del contenido")
    print("  %d alojamientos · %d actividades · %d noticias · %d plazas"
          % (len(contenido.ALOJAMIENTOS), len(contenido.AGENDA),
             len(contenido.NOTICIAS), contenido.CUPO_TOTAL))
    if sin_revisar[0]:
        print("  %d texto(s) saldrán traducidos al valencià a máquina, "
              "sin revisar" % sin_revisar[0])
        print("  → se repasan en el panel: /admin/ → Traducciones")
    print("")

    for a in avisos:
        print("  AVISO  " + a)
    if avisos:
        print("")
    for e in errores:
        print("  ERROR  " + e)

    if errores:
        print("\n%d error(es). No se publica hasta arreglarlos." % len(errores))
        return 1
    print("Todo correcto%s." % (" (%d aviso[s])" % len(avisos) if avisos else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
