# HOSBEC Km0 Week

Web de la **Km0 Week**: tres fines de semana para que quienes viven en la Comunitat
Valenciana redescubran los alojamientos de su propio territorio. Del **13 al 29 de
noviembre de 2026**.

> ## ¿Vas a cambiar contenido?
> **No toques este repositorio: usa el panel.**
> ### https://bigdatahosbec.github.io/km0week/admin/
>
> Alojamientos, agenda, noticias, textos, imágenes, fechas y contacto se cambian
> ahí, y la web se republica sola en minuto y medio. El
> `MANUAL-DE-ACTUALIZACION.md` explica qué se hace dónde.

Sitio estático: HTML, CSS y JavaScript, sin dependencias externas ni peticiones a
terceros (tipografías, scripts e imágenes están autoalojados).

**Lo que hay aquí son las fuentes.** Las 18 páginas, `sitemap.xml`, `robots.txt`,
`assets/js/data-alojamientos.js` y los 14 archivos de `descargas/` no están en el
repositorio: los genera la publicación automática en cada cambio. Para verlos en
local, `python3 _build/build.py`.

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

© HOSBEC · Asociación Empresarial Hotelera y Turística de la Comunidad Valenciana
