# Km0 Week — web completa (v5)

Abre `index.html` en el navegador: funciona tal cual, sin servidor.
Misma piel que aprobaste en la v4, ahora con **18 páginas**, fotos en todos los
huecos y contenido de ejemplo en todas partes.

> **¿Vas a cambiar algo?** Lee antes `MANUAL-DE-ACTUALIZACION.md`: está
> todo por recetas (añadir un hotel, cambiar una foto, publicar una noticia,
> regenerar los PDF) y avisa de las trampas.


---

## 1 · Qué hay

| Página | Archivo | Qué contiene |
|---|---|---|
| Portada | `index.html` | Hero con el mapa, la idea, cómo funciona, cifras, seis planes, experiencias, territorio, pasaporte |
| La iniciativa | `iniciativa.html` | Qué es, por qué se hace, los cinco compromisos, quién hay detrás, cómo funciona |
| Alojamientos | `alojamientos.html` | **Listado completo con filtros** por provincia, tipo y experiencia, y cinco criterios de orden |
| Mapa | `mapa.html` | El mapa grande con los tres círculos y la lista de todos los alojamientos ordenada por distancia |
| Agenda | `agenda.html` | Programa día a día del 13 al 29, con filtro por día, por fin de semana y por «solo gratuitas» |
| Suma tu alojamiento | `suma.html` | Qué pone cada parte, requisitos, calendario y formulario de solicitud |
| Preguntas | `faq.html` | Doce preguntas en tres bloques, en acordeón |
| Noticias | `noticias.html` + `noticia-1..4.html` | Listado y cuatro entradas escritas enteras |
| Sala de prensa | `prensa.html` | Cifras verificables, material para medios, contacto y tabla de repercusión |
| Descargas | `descargas.html` | Nueve piezas descargables: pasaporte, programa, bases, cartelería, kit de redes, textos, manual, sello y guía de recepción |
| Legales | `aviso-legal.html` · `privacidad.html` · `cookies.html` | Con los datos reales de HOSBEC. Pendientes de revisión jurídica |
| Error | `404.html` | Con accesos a las secciones principales |

Además: `sitemap.xml` y `robots.txt`, generados solos.

---

## 2 · Lo que tienes que tocar tú

**Para añadir alojamientos:** `assets/js/data-alojamientos.js`, exactamente igual
que antes. Un alojamiento nuevo aparece solo en la portada, en el listado con
filtros, en el mapa, en los contadores de cifras, en las marquesinas de destinos
y en el bloque de provincias. No hay que tocar ninguna página.

**Para cambiar textos de una página:** `_build/paginas/<pagina>.html`. Solo lleva
el contenido; la cabecera, el menú y el pie se añaden al compilar.

**Para cambiar el menú, el pie o los metadatos:** `_build/build.py`, arriba del
todo. Ahí también está `DOMINIO`, que hay que cambiar por el definitivo antes de
publicar (afecta a `sitemap.xml`, `robots.txt` y a las etiquetas de compartir).

Después de tocar cualquiera de los dos últimos:

```
python3 _build/build.py
```

y se reescriben los 18 HTML. Si solo tocas `data-alojamientos.js`, **no hace
falta compilar nada**.

---

## 3 · Las fotos

Ahora mismo cada hueco de foto lleva una **ilustración generada por código** con
la paleta de la marca: cabeceras de página, fichas de alojamiento, noticias,
provincias y bloques de apoyo. Están en `assets/img/foto/` y las produce
`_build/arte.py`.

Son un **relleno con la medida y el encuadre correctos**: cuando tengáis la foto
real, sustituirla es cambiar una ruta.

- **Ficha de alojamiento:** el campo `imagen` de `data-alojamientos.js`.
  Ahora apunta a `assets/img/foto/alo-<id>.webp`; cámbialo por tu foto.
- **Cabecera de página, noticias, bloques:** el `src` del `<img>` en el archivo
  correspondiente de `_build/paginas/`.

Medidas recomendadas: **2000 × 900 px** para las cabeceras y **1200 × 800 px**
(3:2) para fichas, noticias y bloques. En `.webp` o `.jpg`.

---

## 4 · Qué funciona ya

- **Filtros** de provincia, tipo y experiencia, combinables, con contador y
  aviso de «ningún resultado». Aceptan parámetros en la dirección:
  `alojamientos.html?provincia=Alicante`, `?tipo=camping`, `?experiencia=gastronomia`.
- **Mapa** con selector de municipio y geolocalización, los tres círculos y la
  lista ordenada por distancia real. Todo se calcula en el navegador: no sale nada.
- **Agenda** con los siete días calculados desde `fechaInicio`, filtro por día y
  por gratuitas.
- **Castellano y valenciano** en las 18 páginas, con la preferencia guardada.
- **Cuenta atrás** en la cinta superior, en los dos idiomas.
- **Acordeón** de preguntas, **formulario** de alta con validación.

## 5 · Qué falta antes de publicar

- [ ] Sustituir los 20 alojamientos de ejemplo por los reales
- [ ] Fotografía real (ver el punto 3)
- [ ] Cambiar `DOMINIO` en `_build/build.py` y recompilar
- [ ] **Conectar el formulario de `suma.html`** al correo o al CRM: hoy solo muestra un aviso
- [ ] Conectar el boletín («Te avisamos») a la herramienta de email de HOSBEC
- [ ] Subir los PDF de `descargas.html` y `prensa.html` y enlazarlos
- [ ] Revisar los tres textos legales con vuestro jurídico
- [ ] Logotipo oficial en vectorial (ahora el lockup se compone con las tipografías)
- [ ] Sustituir las cuatro noticias de ejemplo

---

## 6 · Notas técnicas

Sin dependencias externas ni peticiones a terceros: tipografías, scripts e
imágenes están autoalojados, así que la web no envía nada a Google ni a nadie.

Nada de módulos ES: el motor de animación va en un script clásico
(`assets/vendor/anime.global.js`) para que la web funcione también abriendo el
archivo desde el disco. Si detecta `file://`, carga las tipografías embebidas de
`assets/css/fuentes-local.css`; en un servidor real ese archivo ni se descarga.

Verificado con Chromium: las 18 páginas cargan sin errores de consola, sin
enlaces rotos y sin desbordes horizontales de 360 px a 2560 px; filtros, agenda,
mapa, idioma, acordeón y formulario responden; con «reducir movimiento» activado
no se oculta ningún contenido.

```
index.html … 404.html            Las 18 páginas (generadas)
sitemap.xml · robots.txt         Generados
_build/build.py                  Menú, pie, metadatos y compilación
_build/paginas/*.html            El contenido de cada página
_build/arte.py                   Generador de las imágenes de relleno
assets/css/km0.css               Sistema de diseño (paleta en las primeras líneas)
assets/css/fuentes-local.css     Tipografías embebidas (solo para file://)
assets/js/data-alojamientos.js   LOS DATOS: alojamientos, agenda, fechas y cupos
assets/js/isocrona.js            El mapa
assets/js/home.js                Todo lo que se pinta desde los datos
assets/js/motion.js              El movimiento (anime.js v4)
assets/img/foto/                 Las 54 imágenes de relleno
assets/fonts/                    Montserrat · Lora · Caveat Brush (SIL OFL)
```
