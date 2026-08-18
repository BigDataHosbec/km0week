# HOSBEC Km0 Week

Web de la **Km0 Week**: una semana para que quienes viven en la Comunitat Valenciana
redescubran los alojamientos de su propio territorio. Del **13 al 19 de noviembre de 2026**.

Sitio estático: HTML, CSS y JavaScript. Sin build obligatorio, sin dependencias externas
y sin peticiones a terceros (tipografías, scripts e imágenes están autoalojados).

## Publicado en

https://bigdatahosbec.github.io/km0week/

## Para añadir un alojamiento

Edita **`assets/js/data-alojamientos.js`** y guarda. Aparece solo en la portada, en el
listado con filtros, en el mapa, en los contadores, en las marquesinas y en el bloque de
provincias. No hay que tocar ninguna página ni compilar nada.

## Para cambiar textos, menú o pie

- Contenido de una página: `_build/paginas/<pagina>.html`
- Menú, pie, metadatos y dominio: `_build/build.py`

Después de tocar cualquiera de los dos:

```bash
python3 _build/build.py
```

y se reescriben los 18 HTML de la raíz.

## Estructura

```
index.html … 404.html            Las 18 páginas (generadas)
sitemap.xml · robots.txt         Generados
.nojekyll                        Le dice a GitHub Pages que no procese el sitio con Jekyll
_build/                          Fuentes de contenido y generadores
assets/                          CSS, JS, tipografías e imágenes
LEEME.md                         Documentación completa en castellano
```

© HOSBEC · Asociación Empresarial Hostelera de Benidorm, Costa Blanca y Comunitat Valenciana
