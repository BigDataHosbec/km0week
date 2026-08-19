#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Km0 Week — generador de imágenes de relleno.

Produce las fotos de marcador de posición de toda la web: cabeceras de página,
fichas de alojamiento, noticias, provincias y experiencias. Son ilustraciones
planas hechas con la paleta del manual de marca; ocupan exactamente el mismo
hueco que ocuparán las fotos reales, así que sustituir una es cambiar la ruta.

  python3 _build/arte.py            → regenera todo en assets/img/foto/

Cada imagen se genera a partir de una semilla de texto: la misma semilla da
siempre la misma imagen, así que el sitio no "baila" entre compilaciones.
"""

import os, math, hashlib
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SALIDA = os.path.join(RAIZ, "assets", "img", "foto")

# ---------------------------------------------------------------- paleta ----
MAR      = (30, 164, 198)
MAR_D    = (20, 100, 125)
VERDE    = (140, 178, 111)
VERDE_D  = (110, 149, 83)
ARENA    = (238, 216, 174)
TERRA    = (217, 121, 77)
TINTA    = (18, 60, 76)
ROTO     = (250, 245, 236)

# Cada ambiente define cielo (arriba/abajo), sol, capas de terreno y agua.
AMBIENTES = {
    "amanecer":  dict(cielo=((252, 228, 196), (247, 199, 173)), sol=(255, 236, 205), agua=(94, 165, 190)),
    "mediodia":  dict(cielo=((214, 238, 246), (240, 246, 240)), sol=(255, 249, 226), agua=MAR),
    "tarde":     dict(cielo=((250, 233, 205), (245, 205, 176)), sol=(255, 226, 174), agua=(60, 143, 172)),
    "atardecer": dict(cielo=((246, 205, 178), (233, 160, 137)), sol=(255, 214, 160), agua=(46, 110, 138)),
    "bruma":     dict(cielo=((232, 240, 240), (245, 240, 228)), sol=(255, 250, 235), agua=(120, 175, 194)),
    "noche":     dict(cielo=((40, 78, 100), (86, 124, 142)),    sol=(232, 240, 246), agua=(22, 60, 82)),
}


# ------------------------------------------------------------- utilidades ---
def semilla(txt):
    return int(hashlib.sha1(txt.encode("utf-8")).hexdigest()[:8], 16)


def mezcla(c1, c2, k):
    return tuple(int(round(a + (b - a) * k)) for a, b in zip(c1, c2))


def aclarar(c, k):
    return mezcla(c, (255, 255, 255), k)


def oscurecer(c, k):
    return mezcla(c, TINTA, k)


def degradado(w, h, arriba, abajo, curva=1.0):
    """Franja vertical de arriba a abajo, con posibilidad de curvar el reparto."""
    t = (np.linspace(0, 1, h) ** curva)[:, None]
    top = np.array(arriba, float)[None, :]
    bot = np.array(abajo, float)[None, :]
    col = top + (bot - top) * t                       # h x 3
    return np.repeat(col[:, None, :], w, axis=1)


def perfil(rnd, w, base, amplitud, rugosidad=3):
    """Silueta suave: suma de senos con fases al azar. Devuelve un array de alturas."""
    x = np.linspace(0, 1, w)
    y = np.zeros(w)
    peso = 0.0
    for i in range(rugosidad):
        f = 1.0 + i * 1.7 + rnd.random() * 1.3
        a = 1.0 / (i + 1.35)
        y += a * np.sin(2 * math.pi * f * x + rnd.random() * 6.28)
        peso += a
    y /= peso
    return base - amplitud * (0.45 + 0.55 * (y * 0.5 + 0.5))


def pintar_perfil(cap, alturas, color, w, h):
    """Rellena por debajo de una silueta sobre un lienzo RGBA."""
    d = ImageDraw.Draw(cap)
    pts = [(int(i), int(alturas[i])) for i in range(w)]
    d.polygon(pts + [(w, h), (0, h)], fill=color + (255,))


def grano(arr, rnd, fuerza=6.0):
    ruido = rnd.normal(0, fuerza, arr.shape[:2])[:, :, None]
    return np.clip(arr + ruido, 0, 255)


def vinyeta(arr, fuerza=0.16):
    h, w = arr.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w]
    dx = (xx - w / 2) / (w / 2)
    dy = (yy - h / 2) / (h / 2)
    r = np.sqrt(dx * dx + dy * dy) / 1.414
    k = 1 - fuerza * (r ** 2.2)
    return np.clip(arr * k[:, :, None], 0, 255)


def sol(img, cx, cy, radio, color, halo=3.2):
    """Disco con resplandor, dibujado en una capa aparte y fundido con pantalla."""
    w, h = img.size
    capa = Image.new("RGB", (w, h), (0, 0, 0))
    d = ImageDraw.Draw(capa)
    d.ellipse([cx - radio * halo, cy - radio * halo, cx + radio * halo, cy + radio * halo],
              fill=tuple(int(c * 0.30) for c in color))
    capa = capa.filter(ImageFilter.GaussianBlur(radio * 0.9))
    d = ImageDraw.Draw(capa)
    d.ellipse([cx - radio, cy - radio, cx + radio, cy + radio], fill=color)
    capa = capa.filter(ImageFilter.GaussianBlur(radio * 0.10))
    a = np.asarray(img, float)
    b = np.asarray(capa, float)
    return Image.fromarray(np.clip(255 - (255 - a) * (255 - b) / 255, 0, 255).astype("uint8"))


def brillos_agua(cap, rnd, w, horizonte, h, color):
    d = ImageDraw.Draw(cap)
    n = int(18 + rnd.random() * 14)
    for _ in range(n):
        y = horizonte + (h - horizonte) * (rnd.random() ** 1.5)
        largo = w * (0.04 + rnd.random() * 0.16)
        x = rnd.random() * (w - largo)
        grosor = max(1, int((y - horizonte) / (h - horizonte) * 5) + 1)
        op = int(90 + rnd.random() * 90)
        d.rounded_rectangle([x, y, x + largo, y + grosor], radius=grosor / 2, fill=color + (op,))


# ----------------------------------------------------------------- escenas --
def escena_costa(img, rnd, w, h, amb, ancho_playa=True):
    horizonte = h * (0.52 + rnd.random() * 0.10)
    img = sol(img, w * (0.14 + rnd.random() * 0.7), horizonte - h * (0.18 + rnd.random() * 0.16),
              min(w, h) * (0.055 + rnd.random() * 0.03), amb["sol"])
    cap = Image.new("RGBA", (w, h), (0, 0, 0, 0))

    # cabos lejanos, cada vez más nítidos
    for i, k in enumerate((0.62, 0.42, 0.24)):
        alt = perfil(rnd, w, horizonte + 2, h * (0.22 - i * 0.05), 2 + i)
        pintar_perfil(cap, alt, aclarar(oscurecer(VERDE_D, 0.25), k), w, h)

    d = ImageDraw.Draw(cap)
    d.rectangle([0, horizonte, w, h], fill=amb["agua"] + (255,))
    d.rectangle([0, horizonte, w, horizonte + h * 0.05],
                fill=aclarar(amb["agua"], 0.22) + (255,))
    brillos_agua(cap, rnd, w, horizonte, h, (255, 255, 255))

    escena_costa.orilla = None
    if ancho_playa:
        orilla = perfil(rnd, w, h * 0.92, h * 0.15, 2)
        pintar_perfil(cap, orilla, aclarar(ARENA, 0.18), w, h)
        esp = orilla - h * 0.012
        d.line([(i, esp[i]) for i in range(0, w, 3)], fill=(255, 255, 255, 190), width=max(2, h // 220))
        escena_costa.orilla = orilla
    img.paste(Image.alpha_composite(img.convert("RGBA"), cap).convert("RGB"), (0, 0))
    return img


def escena_pueblo(img, rnd, w, h, amb):
    base = h * (0.70 + rnd.random() * 0.06)
    img = sol(img, w * (0.1 + rnd.random() * 0.8), h * (0.16 + rnd.random() * 0.12),
              min(w, h) * 0.055, amb["sol"])
    cap = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    for i, k in enumerate((0.6, 0.35)):
        alt = perfil(rnd, w, base + h * 0.06, h * (0.26 - i * 0.07), 2 + i)
        pintar_perfil(cap, alt, aclarar(VERDE_D, k), w, h)

    d = ImageDraw.Draw(cap)
    # caserío: bloques encalados con ventanas
    x = -w * 0.05
    tonos = [aclarar(ROTO, 0.0), aclarar(ARENA, 0.45), aclarar(MAR, 0.78), aclarar(TERRA, 0.72)]
    while x < w * 1.05:
        an = w * (0.05 + rnd.random() * 0.075)
        al = h * (0.10 + rnd.random() * 0.16)
        y0 = base - al
        col = tonos[int(rnd.random() * len(tonos))]
        d.rectangle([x, y0, x + an, base + h * 0.05], fill=col + (255,))
        d.rectangle([x, y0, x + an, y0 + h * 0.022], fill=TERRA + (255,))     # teja
        filas = max(1, int(al / (h * 0.055)))
        cols = max(1, int(an / (w * 0.022)))
        for fy in range(filas):
            for fx in range(cols):
                vx = x + an * (fx + 0.5) / cols - w * 0.006
                vy = y0 + h * 0.045 + fy * h * 0.05
                if vy + h * 0.026 < base and rnd.random() > 0.22:
                    d.rectangle([vx, vy, vx + w * 0.012, vy + h * 0.026],
                                fill=oscurecer(col, 0.55) + (235,))
        x += an * (0.98 + rnd.random() * 0.12)

    # campanario
    tx = w * (0.2 + rnd.random() * 0.6)
    ta = h * (0.30 + rnd.random() * 0.1)
    d.rectangle([tx, base - ta, tx + w * 0.045, base], fill=aclarar(ARENA, 0.55) + (255,))
    d.polygon([(tx - w * 0.012, base - ta), (tx + w * 0.057, base - ta),
               (tx + w * 0.0225, base - ta - h * 0.07)], fill=MAR_D + (255,))
    d.rectangle([tx + w * 0.013, base - ta * 0.82, tx + w * 0.032, base - ta * 0.58],
                fill=oscurecer(ARENA, 0.6) + (255,))
    img.paste(Image.alpha_composite(img.convert("RGBA"), cap).convert("RGB"), (0, 0))
    return img


def escena_montana(img, rnd, w, h, amb):
    img = sol(img, w * (0.12 + rnd.random() * 0.76), h * (0.15 + rnd.random() * 0.08),
              min(w, h) * 0.055, amb["sol"])
    cap = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    capas = 5
    for i in range(capas):
        base = h * (0.66 + i * 0.095)
        alt = perfil(rnd, w, base, h * (0.22 - i * 0.03), 2 + i)
        col = mezcla(aclarar(MAR, 0.80), oscurecer(VERDE_D, 0.42), (i / (capas - 1)) ** 0.75)
        pintar_perfil(cap, alt, col, w, h)
        if i:  # una sola banda de bruma al pie de cada cresta
            d = ImageDraw.Draw(cap)
            d.line([(x, alt[x] + h * 0.014) for x in range(0, w, 2)],
                   fill=(255, 255, 255, 40), width=max(2, h // 150))
    # pinos sueltos en la ladera de delante
    d = ImageDraw.Draw(cap)
    ult = perfil(rnd, w, h * (0.66 + (capas - 1) * 0.095), h * (0.22 - (capas - 1) * 0.03), 2 + capas - 1)
    for _ in range(int(6 + rnd.random() * 7)):
        cx = int(rnd.random() * (w - 4))
        hh = h * (0.035 + rnd.random() * 0.05)
        cy = ult[cx] + h * 0.02 + rnd.random() * h * 0.14
        d.polygon([(cx, cy - hh), (cx - hh * 0.34, cy), (cx + hh * 0.34, cy)],
                  fill=oscurecer(VERDE_D, 0.52) + (255,))
    img.paste(Image.alpha_composite(img.convert("RGBA"), cap).convert("RGB"), (0, 0))
    return img


def escena_campo(img, rnd, w, h, amb):
    horizonte = h * (0.42 + rnd.random() * 0.08)
    img = sol(img, w * (0.1 + rnd.random() * 0.8), horizonte - h * 0.2,
              min(w, h) * 0.055, amb["sol"])
    cap = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(cap)
    alt = perfil(rnd, w, horizonte + h * 0.02, h * 0.06, 2)
    pintar_perfil(cap, alt, aclarar(VERDE_D, 0.55), w, h)

    # bancales en franjas que se ensanchan hacia abajo
    y = horizonte + h * 0.04
    i = 0
    while y < h:
        alto = h * (0.035 + 0.02 * i)
        col = [aclarar(VERDE, 0.30), VERDE, aclarar(ARENA, 0.30), aclarar(VERDE_D, 0.12)][i % 4]
        d.polygon([(0, y), (w, y - h * 0.01), (w, y + alto - h * 0.01), (0, y + alto)],
                  fill=col + (255,))
        y += alto
        i += 1

    # cipreses y algarrobos
    for _ in range(int(5 + rnd.random() * 6)):
        cx = rnd.random() * w
        cy = horizonte + h * (0.10 + rnd.random() * 0.7)
        esc = (cy - horizonte) / h
        if rnd.random() < 0.45:
            hh = h * (0.06 + esc * 0.18)
            d.polygon([(cx, cy - hh), (cx - hh * 0.16, cy), (cx + hh * 0.16, cy)],
                      fill=oscurecer(VERDE_D, 0.30) + (255,))
        else:
            rr = h * (0.025 + esc * 0.06)
            d.line([cx, cy, cx, cy - rr * 0.9], fill=oscurecer(TERRA, 0.45) + (255,), width=max(2, int(rr * 0.22)))
            d.ellipse([cx - rr, cy - rr * 2.1, cx + rr, cy - rr * 0.3],
                      fill=oscurecer(VERDE, 0.22) + (255,))
    img.paste(Image.alpha_composite(img.convert("RGBA"), cap).convert("RGB"), (0, 0))
    return img


def palmera(d, cx, base, altura, w, grosor=None, color=None):
    color = color or oscurecer(VERDE_D, 0.34)
    tronco = oscurecer(TERRA, 0.5)
    g = grosor or max(3, int(w * 0.006))
    inc = altura * 0.09
    d.line([cx, base, cx + inc, base - altura], fill=tronco + (255,), width=g)
    cima = (cx + inc, base - altura)
    for k in range(9):
        a = -math.pi + k * (math.pi / 8)
        d.line([cima[0], cima[1],
                cima[0] + math.cos(a) * altura * 0.40,
                cima[1] + abs(math.sin(a)) * altura * 0.06 - math.sin(a) * altura * 0.20],
               fill=color + (255,), width=max(2, int(g * 0.75)))


def escena_hotel(img, rnd, w, h, amb):
    horizonte = h * (0.56 + rnd.random() * 0.05)
    img = sol(img, w * (0.62 + rnd.random() * 0.3), h * (0.16 + rnd.random() * 0.08),
              min(w, h) * 0.05, amb["sol"])
    cap = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(cap)

    # mar al fondo, terraza delante
    d.rectangle([0, horizonte - h * 0.06, w, horizonte], fill=aclarar(amb["agua"], 0.35) + (255,))
    d.rectangle([0, horizonte, w, h], fill=aclarar(ARENA, 0.58) + (255,))

    # bloque principal, apoyado en el suelo y con retícula de balcones
    bx = w * (0.05 + rnd.random() * 0.08)
    ba = w * (0.40 + rnd.random() * 0.16)
    bal = h * (0.46 + rnd.random() * 0.12)
    d.rectangle([bx, horizonte - bal, bx + ba, horizonte + h * 0.03], fill=aclarar(ROTO, 0.0) + (255,))
    d.rectangle([bx, horizonte - bal, bx + ba, horizonte - bal + h * 0.018], fill=MAR_D + (255,))
    plantas = max(4, int(bal / (h * 0.07)))
    paso = (bal - h * 0.055) / plantas
    for p in range(plantas):
        y = horizonte - bal + h * 0.042 + p * paso
        d.rectangle([bx + w * 0.014, y, bx + ba - w * 0.014, y + paso * 0.46],
                    fill=aclarar(MAR, 0.52) + (255,))
        d.rectangle([bx + w * 0.014, y + paso * 0.46, bx + ba - w * 0.014, y + paso * 0.60],
                    fill=aclarar(TINTA, 0.72) + (255,))
    # torre secundaria, más baja y en arena
    tx = bx + ba + w * 0.015
    tal = bal * (0.52 + rnd.random() * 0.22)
    d.rectangle([tx, horizonte - tal, tx + w * 0.17, horizonte + h * 0.03],
                fill=aclarar(ARENA, 0.42) + (255,))
    for p in range(max(3, int(tal / (h * 0.09)))):
        y = horizonte - tal + h * 0.04 + p * h * 0.085
        if y + h * 0.04 < horizonte:
            d.rectangle([tx + w * 0.02, y, tx + w * 0.15, y + h * 0.04],
                        fill=aclarar(TINTA, 0.72) + (255,))

    # piscina en la terraza, en perspectiva
    py0, py1 = horizonte + h * 0.14, h * 0.90
    d.polygon([(w * 0.16, py0), (w * 0.80, py0), (w * 0.90, py1), (w * 0.06, py1)],
              fill=amb["agua"] + (255,))
    d.polygon([(w * 0.17, py0 + h * 0.012), (w * 0.79, py0 + h * 0.012),
               (w * 0.80, py0 + h * 0.05), (w * 0.16, py0 + h * 0.05)],
              fill=aclarar(amb["agua"], 0.28) + (255,))
    brillos_agua(cap, rnd, w, int(py0), int(py1), (255, 255, 255))

    # hamacas al borde
    for k in range(3):
        hx = w * (0.06 + k * 0.055)
        d.polygon([(hx, horizonte + h * 0.10), (hx + w * 0.035, horizonte + h * 0.10),
                   (hx + w * 0.032, horizonte + h * 0.055), (hx + w * 0.012, horizonte + h * 0.055)],
                  fill=aclarar(TERRA, 0.35) + (255,))

    # palmeras en primer plano, cortadas por el borde
    palmera(d, w * 0.90, h * 1.02, h * (0.62 + rnd.random() * 0.14), w, int(w * 0.011))
    palmera(d, w * 0.78, h * 0.98, h * (0.40 + rnd.random() * 0.10), w, int(w * 0.008))
    img.paste(Image.alpha_composite(img.convert("RGBA"), cap).convert("RGB"), (0, 0))
    return img


def escena_playa(img, rnd, w, h, amb):
    img = escena_costa(img, rnd, w, h, amb, ancho_playa=True)
    cap = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(cap)
    orilla = escena_costa.orilla                     # la sombrilla va SIEMPRE sobre arena
    for _ in range(int(3 + rnd.random() * 4)):
        cx = int(w * (0.05 + rnd.random() * 0.9))
        suelo = float(orilla[min(cx, w - 1)]) if orilla is not None else h * 0.9
        banda = max(h * 0.02, h * 0.99 - suelo)
        rr = min(h * (0.04 + rnd.random() * 0.04), banda / 2.6)
        cy = suelo + 2.2 * rr + (banda - 2.2 * rr) * rnd.random()
        col = [TERRA, MAR, VERDE_D, MAR_D][int(rnd.random() * 4)]
        d.line([cx, cy, cx, cy - rr * 1.6], fill=oscurecer(ARENA, 0.5) + (255,), width=max(2, int(w * 0.004)))
        d.pieslice([cx - rr, cy - rr * 2.2, cx + rr, cy - rr * 1.0], 180, 360, fill=col + (255,))
    img.paste(Image.alpha_composite(img.convert("RGBA"), cap).convert("RGB"), (0, 0))
    return img


def escena_ciudad(img, rnd, w, h, amb):
    base = h * (0.78 + rnd.random() * 0.05)
    img = sol(img, w * (0.1 + rnd.random() * 0.8), h * 0.18, min(w, h) * 0.05, amb["sol"])
    cap = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(cap)
    noct = amb["cielo"][0][0] < 120                     # ambiente "noche"
    fondo = [aclarar(MAR, 0.74), aclarar(ARENA, 0.30), aclarar(ROTO, 0.0)]
    if noct:
        fondo = [aclarar(MAR_D, 0.42), aclarar(MAR_D, 0.20), aclarar(TINTA, 0.10)]
    for capa in range(3):
        x = -w * 0.05
        yb = base - h * 0.085 * (2 - capa)
        while x < w * 1.05:
            an = w * (0.045 + rnd.random() * 0.075)
            al = h * (0.13 + rnd.random() * (0.30 - capa * 0.06))
            col = fondo[capa]
            d.rectangle([x, yb - al, x + an, base + h * 0.1], fill=col + (255,))
            if capa == 2:                                # cornisa de teja
                d.rectangle([x, yb - al, x + an, yb - al + h * 0.016],
                            fill=(TERRA if not noct else oscurecer(TERRA, 0.4)) + (255,))
            if capa >= 1:
                cols = max(1, int(an / (w * 0.024)))
                for fy in range(int(al / (h * 0.058))):
                    for fx in range(cols):
                        if rnd.random() > (0.34 if noct else 0.28):
                            vx = x + an * (fx + 0.5) / cols - w * 0.006
                            vy = yb - al + h * 0.036 + fy * h * 0.058
                            luz = aclarar(ARENA, 0.10) if noct else oscurecer(col, 0.5)
                            d.rectangle([vx, vy, vx + w * 0.012, vy + h * 0.026], fill=luz + (235,))
            x += an * 1.04
    # una cúpula y un campanario para que se reconozca la ciudad
    cx = w * (0.28 + rnd.random() * 0.44)
    cal = h * (0.30 + rnd.random() * 0.1)
    d.rectangle([cx, base - cal, cx + w * 0.05, base], fill=aclarar(ARENA, 0.34) + (255,))
    d.polygon([(cx - w * 0.012, base - cal), (cx + w * 0.062, base - cal),
               (cx + w * 0.025, base - cal - h * 0.075)], fill=MAR_D + (255,))
    dx = cx - w * (0.10 + rnd.random() * 0.1)
    d.pieslice([dx, base - h * 0.30, dx + w * 0.13, base - h * 0.08], 180, 360,
               fill=(MAR_D if noct else MAR) + (255,))
    d.rectangle([dx, base - h * 0.19, dx + w * 0.13, base], fill=aclarar(ARENA, 0.34) + (255,))
    img.paste(Image.alpha_composite(img.convert("RGBA"), cap).convert("RGB"), (0, 0))
    return img


ESCENAS = {
    "costa": escena_costa, "pueblo": escena_pueblo, "montana": escena_montana,
    "campo": escena_campo, "hotel": escena_hotel, "playa": escena_playa,
    "ciudad": escena_ciudad,
}


# ------------------------------------------------------------------ render --
def crear(nombre, escena, w, h, ambiente=None, sem=None):
    rnd = np.random.RandomState(semilla(sem or nombre))
    amb = AMBIENTES[ambiente or list(AMBIENTES)[int(rnd.random() * len(AMBIENTES))]]
    arr = degradado(w, h, amb["cielo"][0], amb["cielo"][1], curva=0.85)
    img = Image.fromarray(arr.astype("uint8"), "RGB")
    img = ESCENAS[escena](img, rnd, w, h, amb)
    arr = np.asarray(img, float)
    arr = vinyeta(arr, 0.14)
    arr = grano(arr, rnd, 5.0)
    img = Image.fromarray(arr.astype("uint8"), "RGB")
    ruta = os.path.join(SALIDA, nombre + ".webp")
    img.save(ruta, "WEBP", quality=80, method=5)
    return ruta


# ------------------------------------------------------------------ listas --
CABECERAS = [  # (archivo, escena, ambiente)
    ("cab-iniciativa", "pueblo", "tarde"),
    ("cab-alojamientos", "hotel", "mediodia"),
    ("cab-mapa", "montana", "bruma"),
    ("cab-agenda", "ciudad", "atardecer"),
    ("cab-suma", "costa", "amanecer"),
    ("cab-faq", "campo", "mediodia"),
    ("cab-prensa", "ciudad", "mediodia"),
    ("cab-noticias", "pueblo", "amanecer"),
    ("cab-descargas", "playa", "tarde"),
    ("cab-legal", "montana", "mediodia"),
    ("cab-404", "costa", "atardecer"),
]

PROVINCIAS = [("prov-castello", "pueblo", "amanecer"),
              ("prov-valencia", "ciudad", "tarde"),
              ("prov-alicante", "playa", "mediodia")]

NOTICIAS = [("not-1", "pueblo", "tarde"), ("not-2", "hotel", "mediodia"),
            ("not-3", "campo", "amanecer"), ("not-4", "costa", "atardecer"),
            ("not-5", "montana", "bruma")]

TEMAS = [("tema-gastronomia", "pueblo", "tarde"), ("tema-bienestar", "hotel", "bruma"),
         ("tema-familia", "playa", "mediodia"), ("tema-cultura", "ciudad", "amanecer"),
         ("tema-mar", "costa", "mediodia"), ("tema-deporte", "montana", "amanecer"),
         ("tema-romantico", "costa", "atardecer"), ("tema-mascotas", "campo", "tarde"),
         ("tema-accesible", "playa", "tarde"), ("tema-sostenible", "campo", "mediodia"),
         ("tema-noche", "ciudad", "noche")]

IDEA = [("idea-1", "pueblo", "mediodia"), ("idea-2", "hotel", "tarde"), ("idea-3", "campo", "amanecer")]


def escena_para(alo):
    """Elige el ambiente de la ficha según el tipo y las etiquetas."""
    exp = alo.get("experiencias", [])
    if alo.get("tipo") in ("hotel", "apartamentos", "balneario", "hostal"):
        return "hotel" if "mar" not in exp else "playa"
    if alo.get("tipo") == "camping":
        return "campo"
    if "deporte" in exp or "sostenible" in exp:
        return "montana"
    return "pueblo"


def main():
    os.makedirs(SALIDA, exist_ok=True)
    n = 0
    for nom, esc, amb in CABECERAS:
        crear(nom, esc, 2000, 900, amb); n += 1
    for grupo in (PROVINCIAS, NOTICIAS, TEMAS, IDEA):
        for nom, esc, amb in grupo:
            crear(nom, esc, 1200, 800, amb); n += 1

    # fichas de alojamiento: se leen del archivo de datos
    import re, json
    datos = open(os.path.join(RAIZ, "assets", "js", "data-alojamientos.js"), encoding="utf-8").read()
    ids = re.findall(r'\n    id:\s*"([^"]+)"', datos)
    tipos = re.findall(r'\n    tipo:\s*"([^"]+)"', datos)
    exps = re.findall(r'\n    experiencias:\s*\[([^\]]*)\]', datos)
    ambientes = list(AMBIENTES)
    for i, ident in enumerate(ids):
        alo = {"tipo": tipos[i] if i < len(tipos) else "hotel",
               "experiencias": re.findall(r'"([^"]+)"', exps[i]) if i < len(exps) else []}
        amb = ambientes[semilla(ident) % len(ambientes)]
        if amb == "noche":
            amb = "tarde"
        crear("alo-" + ident, escena_para(alo), 1200, 800, amb); n += 1
    print("imágenes generadas:", n, "→", SALIDA)


if __name__ == "__main__":
    main()
