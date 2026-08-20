# -*- coding: utf-8 -*-
"""
Km0 Week — traducción automática
================================

Se escribe el contenido en castellano y aquí se rellena el valenciano que
falte. El motor es **Apertium**, libre y de reglas: la misma frase da siempre
la misma traducción, así que la web no cambia sola de un día para otro.

Contrastado contra las 242 traducciones que se habían escrito a mano para esta
web: 161 salen idénticas palabra por palabra. Del resto, casi todas son
variantes legítimas, pero algunas no lo son («Solo mayores» → «Sol majors»).
Por eso lo que sale de aquí es un **borrador**: el panel lo marca como «sin
revisar» hasta que una persona lo da por bueno, y en cuanto alguien escribe la
traducción a mano, esa manda y aquí no se toca.

Para añadir un idioma (inglés, por ejemplo) basta con otra entrada en MOTORES.
Aviso: Apertium traduce muy bien entre castellano y catalán/valenciano, que son
lenguas próximas, pero al inglés rinde mal. Para eso haría falta un traductor
neuronal con clave, guardada en los secretos de GitHub.

    python3 _build/traducir.py          → prueba suelta desde la terminal
"""

import subprocess
import sys

# idioma → modo de Apertium
MOTORES = {
    "va": "spa-cat_valencia",
}

# Lo que hay que instalar para que esto funcione (lo hace la publicación
# automática). Sin ello, traducir() devuelve cadenas vacías y no rompe nada:
# el contenido se queda como estaba.
PAQUETES = "apertium apertium-spa-cat apertium-lex-tools cg3"

SEP = "\n@@@@@\n"

_disponible = None


def disponible():
    """¿Está Apertium instalado en esta máquina?"""
    global _disponible
    if _disponible is None:
        try:
            subprocess.run(["apertium", "-l"], capture_output=True, check=True)
            _disponible = True
        except Exception:
            _disponible = False
    return _disponible


def _apertium(modo, textos):
    """Traduce una lista de textos. Una sola llamada para todos."""
    entrada = SEP.join(textos)
    r = subprocess.run(["apertium", "-u", modo], input=entrada,
                       capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError((r.stderr or "").strip()[:300] or "apertium falló")
    trozos = [t.strip() for t in r.stdout.split("@@@@@")]
    if len(trozos) != len(textos):
        # Si el separador no ha sobrevivido, se va de una en una. Más lento,
        # pero no devuelve nunca una traducción emparejada con el texto que no es.
        return [_apertium(modo, [t])[0] for t in textos]
    return trozos


def traducir(textos, idioma="va"):
    """
    textos: lista de cadenas en castellano.
    Devuelve una lista del mismo tamaño. Si algo va mal, devuelve cadenas
    vacías: el contenido se queda sin traducir, que es recuperable, en vez de
    quedarse mal traducido, que no se ve.
    """
    limpios = [t for t in textos if t and t.strip()]
    if not limpios or idioma not in MOTORES or not disponible():
        return ["" for _ in textos]
    try:
        hechos = _apertium(MOTORES[idioma], limpios)
    except Exception as e:
        sys.stderr.write("  aviso: no se ha podido traducir (%s)\n" % e)
        return ["" for _ in textos]
    it = iter(hechos)
    return [next(it) if (t and t.strip()) else "" for t in textos]


def memoria(textos, idioma="va"):
    """Diccionario {castellano: traducción} sin repetidos, para el panel."""
    unicos = sorted({t.strip() for t in textos if t and t.strip()})
    return {es: va for es, va in zip(unicos, traducir(unicos, idioma)) if va}


if __name__ == "__main__":
    if not disponible():
        print("Apertium no está instalado. En Ubuntu:")
        print("  sudo apt-get install -y " + PAQUETES)
        sys.exit(1)
    pruebas = [
        "Solo mayores de 16 años. Cita previa obligatoria.",
        "Dormir a diez minutos de casa y despertar en otra ciudad.",
        "Seis hoteles abren sus cocinas al público. Reserva previa.",
    ]
    for es, va in zip(pruebas, traducir(pruebas)):
        print("  ES  " + es)
        print("  VA  " + va + "\n")
