# Km0 Week — Manual de actualización

Cómo cambiar cualquier cosa de la web sin romper nada. Cada apartado es una
receta cerrada: qué archivo tocas, qué haces después y cómo compruebas que ha
salido bien.

Actualizado el 19/08/2026.

---

## Las tres reglas

**1. Nunca edites los HTML de la raíz.**
`index.html`, `alojamientos.html`, `prensa.html`… están **generados**. Los pisa
el compilador la próxima vez que se ejecute y perderás el cambio sin avisar. El
contenido de cada página vive en `_build/paginas/`.

**2. Al subir a GitHub, sube la carpeta entera.**
Ya nos costó una tarde: se subieron las páginas pero no `assets/js/`, y la web
siguió mandando los formularios al sistema antiguo aunque el código nuevo
estuviera «hecho». Si tocas JavaScript o CSS y no lo ves en producción, abre el
archivo directamente en `bigdatahosbec.github.io` y compara.

**3. Cuando dudes de si hay que compilar, compila.**
`python3 _build/build.py` es inofensivo: reescribe las 18 páginas a partir de
las fuentes. Ejecutarlo de más no rompe nada; no ejecutarlo cuando tocaba, sí.

---

## Qué manda sobre qué

| Lo que quieres cambiar | Archivo | ¿Compilar? | ¿Regenerar descargables? |
|---|---|---|---|
| Alojamientos (añadir, editar, quitar) | `assets/js/data-alojamientos.js` | No | **Sí** |
| Actividades de la agenda | `assets/js/data-alojamientos.js` (`AGENDA`) | No | **Sí** |
| Fechas de la edición | `data-alojamientos.js` (`CONFIG`) **y** `_build/build.py` | **Sí** | **Sí** |
| Teléfono, correo, token de formularios | `data-alojamientos.js` (`CONFIG`) | No | **Sí** |
| Fotos | `assets/img/foto/` | No | **Sí** (solo el banco de imágenes) |
| Texto de una página | `_build/paginas/<pagina>.html` | **Sí** | No |
| Menú, pie, metadatos, dominio | `_build/build.py` | **Sí** | No |
| Noticias (nuevas o editadas) | `_build/build.py` + `_build/paginas/noticia-N.html` | **Sí** | No |
| Colores, tipos, espaciados | `assets/css/km0.css` | No | No |
| Comportamiento (filtros, mapa, envíos) | `assets/js/*.js` | No | No |
| Contenido de un PDF descargable | `_build/descargables.py` | No | **Sí** |
| Dónde llegan los registros | Apps Script de la hoja de Google | No | No |

«Compilar» = `python3 _build/build.py`.
«Regenerar descargables» = `python3 _build/descargables.py` (ver apartado 8;
necesita un entorno que tu Windows no tiene, se hace desde Cowork).

---

## 1 · Añadir, editar o quitar un alojamiento

**Archivo:** `assets/js/data-alojamientos.js`
**Compilar:** no hace falta.

Busca `const ALOJAMIENTOS = [`. Dentro hay un bloque `{ … },` por casa. Copia
uno entero, pégalo debajo y cambia los datos. **Ojo con las comas:** cada bloque
termina en `},` y el último de la lista puede ir sin coma.

Al principio del archivo, en el comentario grande, está la explicación de cada
campo. Los que más se equivocan:

| Campo | Cuidado con |
|---|---|
| `id` | Único, sin espacios ni acentos. Es también el nombre de su foto: `alo-<id>.webp` |
| `tipo` | Solo vale: `hotel`, `apartamentos`, `camping`, `rural`, `hostal`, `balneario`. Otra cosa y no sale en los filtros |
| `provincia` | Exactamente `Alicante`, `València` o `Castelló`. Con la tilde y la ce trencada donde toca |
| `coords` | `[latitud, longitud]`. Clic derecho en Google Maps sobre el hotel → salen los dos números → cópialos. Si te los cambias de orden, el hotel aparece en Argelia |
| `web` | URL completa **con `https://`**. Es a donde va el botón de la ficha |
| `cupo` | Número, sin comillas. Es lo que se suma para el contador de «plazas para vecinos» de la portada |
| `experiencias` | Solo los once valores de la lista del comentario. Uno mal escrito no rompe nada, simplemente ese hotel no sale en ese filtro |

**Para quitar uno:** borra su bloque entero, desde `{` hasta `},`. Comprueba que
no te dejas una coma suelta.

**Qué se actualiza solo, sin tocar nada más:** la portada, el listado con
filtros, el mapa, los cuatro contadores de cifras, las marquesinas de destinos y
el bloque de provincias.

**Después:** regenera los descargables. El listado en Excel, el dossier de
prensa, la nota de prensa y el programa llevan el número de casas y la suma de
plazas dentro.

**Cómo compruebas:** abre `alojamientos.html` en el navegador. Si la página sale
en blanco o el listado vacío, has roto la sintaxis del JavaScript: abre la
consola del navegador (F12) y mira la línea que te señala. Casi siempre es una
coma.

---

## 2 · Cambiar una foto

**Archivo:** `assets/img/foto/`
**Compilar:** no.

Las 54 imágenes de hoy son ilustraciones generadas por código, no fotografía.
Ocupan exactamente el hueco que ocupará la foto real, así que sustituir una es
**dejar un archivo con el mismo nombre encima**.

| Familia | Nombre | Medida | Qué es |
|---|---|---|---|
| Cabeceras | `cab-<pagina>.webp` | 2000 × 900 | La franja de arriba de cada página |
| Alojamientos | `alo-<id>.webp` | 1200 × 800 | La foto de cada ficha. El `<id>` es el del alojamiento |
| Noticias | `not-1..5.webp` | 1200 × 800 | La imagen de cada entrada |
| Provincias | `prov-alicante / valencia / castello.webp` | 1200 × 800 | El bloque de territorio |
| Experiencias | `tema-<experiencia>.webp` | 1200 × 800 | Las once temáticas |
| La iniciativa | `idea-1..3.webp` | 1200 × 800 | Los tres bloques de «Qué es» |

Formato **`.webp`** (o `.jpg`, ver abajo). Proporción respetada: si subes una
foto de otra proporción se recorta desde el centro y puedes perder la cabeza de
alguien.

**Si tu foto es `.jpg` y no quieres convertirla:** déjala igual en esa carpeta y
cambia la ruta a mano. Para un alojamiento, el campo `imagen` de su bloque en
`data-alojamientos.js`. Para una cabecera o una noticia, el `src` en
`_build/paginas/` y luego compilar.

**Después:** regenera los descargables para que `banco-imagenes.zip` recoja las
nuevas. **Y edita el aviso del LEEME de ese ZIP** —está en `_build/descargables.py`,
variable `LEEME_BANCO`—: hoy dice que son ilustraciones provisionales y no
fotografía de los establecimientos. Cuando ya sean fotos reales, esa advertencia
sobra y conviene sustituirla por el crédito del fotógrafo.

**Aviso serio.** Mientras sean ilustraciones, no las mandes a un medio como
«fotografías de los alojamientos adheridos». La tarjeta de la sala de prensa y
el LEEME del ZIP ya lo dicen; no lo deshagas antes de tiempo.

---

## 3 · Cambiar la agenda de actividades

**Archivo:** `assets/js/data-alojamientos.js`, lista `const AGENDA = [`
**Compilar:** no.

Cada actividad es una línea. Los campos:

```js
{ dia: 1, hora: "12:00", lugar: "Benidorm", enlace: "https://…",
  titulo: { es: "…", va: "…" },
  desc:   { es: "…", va: "…" },
  tipo: "gastronomia", precio: { es: "Gratis", va: "Gratis" } },
```

- **`dia`** es el número de día de la edición, **no la fecha**: `1` = 13 de
  noviembre, `17` = 29 de noviembre. La web calcula la fecha real desde
  `CONFIG.fechaInicio`, así que si mueves las fechas de la edición las
  actividades se mueven con ellas.
- **`enlace`** es a dónde lleva el botón «Quiero ir». Hoy las catorce apuntan a
  `hosbec.com` porque no hay web de cada actividad todavía. **Esto está en la
  lista de pendientes.** Si lo dejas vacío, la web busca el alojamiento adherido
  de ese mismo destino y lleva a su web; si tampoco lo hay, a hosbec.com. Nunca
  queda un botón muerto, pero tampoco lleva a donde debería.
- **`precio`** es texto libre. Si pones exactamente `Gratis`, la actividad entra
  en el filtro «solo gratuitas».
- Los días de fin de semana se resaltan solos. Los días sin actividades salen
  apagados y no se pueden pulsar.

**Después:** regenera los descargables. El programa de actividades en PDF sale
de aquí, día a día.

---

## 4 · Cambiar el texto de una página

**Archivo:** `_build/paginas/<pagina>.html`
**Compilar:** **sí**.

Ahí solo está el contenido: la cabecera, el menú, el pie y los scripts los pone
el compilador. Un archivo por página, con el mismo nombre que el HTML final
(`iniciativa.html`, `faq.html`, `suma.html`…). La portada es `portada.html`.

**El bilingüe.** Cada texto lleva su traducción al valenciano en un atributo del
propio elemento:

```html
<p data-va="Text en valencià">Texto en castellano</p>
```

- `data-va` para texto normal.
- `data-va-html` cuando dentro hay negritas o enlaces (se sustituye el HTML entero).
- `data-va-ph` para el texto gris de dentro de un campo de formulario.

**Si añades una frase y no le pones `data-va`, al cambiar a valencià se quedará
en castellano.** No da error, simplemente no traduce. Es el fallo más habitual.

Y al revés: **no metas etiquetas HTML dentro de un `data-va`** normal. El
selector de idioma escribe ese atributo como texto plano, así que un `<span>`
ahí dentro se vería literalmente en pantalla. Para eso está `data-va-html`.

---

## 5 · Publicar una noticia

**Archivos:** `_build/build.py` y `_build/paginas/noticia-N.html`
**Compilar:** **sí**.

Son dos pasos y medio.

**a)** Crea `_build/paginas/noticia-5.html`. Lo más rápido es copiar
`noticia-1.html` y reescribir dentro; ya trae la estructura de artículo
(`<article class="prosa">`, fecha, entradilla, subtítulos, cita).

**b)** En `_build/build.py`, busca `NOTICIAS = [` y añade una entrada:

```python
("noticia-5", "not-5", ("Noticias", "Notícies"),
 ("Titular en castellano", "Titular en valencià"),
 "Frase de resumen que sale en el listado y en Google."),
```

El segundo valor (`not-5`) es el nombre de la imagen en `assets/img/foto/`, sin
la extensión.

**c)** Añade la tarjeta al listado en `_build/paginas/noticias.html`, copiando
una de las que ya hay y cambiando enlace, imagen y textos.

Compila. La página nueva, el `sitemap.xml` y la imagen de compartir en redes
salen solos.

---

## 6 · Cambiar las fechas de la edición

**Archivos:** dos, y hay que tocar los dos.
**Compilar:** **sí**.

1. `assets/js/data-alojamientos.js` → `CONFIG`:
   `fechaInicio`, `fechaFin` y `fechasTexto` (en `es` y en `va`).
2. `_build/build.py` → `FECHAS_ES` y `FECHAS_VA`, arriba del todo.

Si cambias uno y no el otro, la web queda diciendo dos cosas distintas: el
contador y la agenda harán caso al primero, y el pie y los metadatos al segundo.

**Consecuencias que igual no esperas:**

- La agenda recalcula cuántos días tiene la edición. Si acortas, las actividades
  con `dia` mayor que el nuevo total **desaparecen** sin avisar.
- El texto «tres fines de semana» está escrito a mano en varios sitios
  (portada, iniciativa, dossier). Si el nuevo rango tiene otro número de fines
  de semana, hay que buscarlo y cambiarlo.
- Regenera los descargables: las fechas salen en los catorce.

---

## 7 · Menú, pie, teléfono, correo, redes, dominio

**Archivo:** `_build/build.py`, todo en la parte de arriba.
**Compilar:** **sí**.

| Qué | Dónde |
|---|---|
| Dirección donde se publica | `DOMINIO` (sin barra final) |
| Correo de contacto | `EMAIL_KM0` |
| Enlaces del menú | lista `MENU` |
| Columnas del pie | `PIE_COLS` |
| Redes sociales | el bloque de SVG de la función `pie()` |

El teléfono y el correo **también** están en `CONFIG` de
`data-alojamientos.js` (`telefonoContacto`, `emailContacto`), porque los usan el
JavaScript y los descargables. Si cambias uno, cambia el otro.

Sobre `DOMINIO`: hoy apunta a `https://bigdatahosbec.github.io/km0week`. Si
algún día HOSBEC concede `km0week.hosbec.com`, son tres cosas: cambiar
`DOMINIO`, compilar, y crear un archivo `CNAME` en la raíz con el dominio
dentro. No existe hoy.

---

## 8 · Regenerar los descargables

**Archivo:** `_build/descargables.py`
**Comando:** `python3 _build/descargables.py`

Un solo script genera los catorce archivos de `descargas/`. Lee los datos reales
de `data-alojamientos.js`, así que las cifras, los alojamientos, la agenda y las
fechas de los PDF salen siempre cuadrados con la web.

**No lo vas a poder ejecutar en tu Windows tal cual.** Necesita Node con
Playwright y Chromium (para imprimir los PDF), la librería `docx` y `openpyxl`.
Lo práctico: **pídemelo en una sesión de Cowork** —«regenera los descargables»—
y te dejo los archivos en `descargas/`. Tarda un par de minutos.

Si quieres montarlo en tu máquina de todas formas:

```bash
pip install openpyxl
npm install -g playwright docx
npx playwright install chromium
python3 _build/descargables.py
```

**Para cambiar el contenido de un PDF** se edita la función correspondiente
dentro de `descargables.py`: `doc_pasaporte`, `doc_programa`, `doc_bases`,
`doc_carteleria`, `doc_manual`, `doc_sello`, `doc_guia`, `doc_dossier`,
`doc_nota`. Son HTML normal con estilos en línea; lo que ves ahí es lo que se
imprime.

**Dos cosas de las que estar pendiente:**

- **Las bases del sorteo son un borrador.** El propio PDF lo advierte en el
  cuerpo y en el pie de cada página. Cuando el jurídico las valide, hay que
  quitar esas dos advertencias: están en `doc_bases()` y en el diccionario
  `PIES_REPETIDOS`, ambos en `descargables.py`.
- **El banco de imágenes se arma solo** con lo que haya en `assets/img/foto/`.
  No hay lista que mantener: cambias las fotos, lo regeneras y ya está.

**Si añades o quitas un descargable** hay que enlazarlo a mano en
`_build/paginas/descargas.html` o `prensa.html`, copiando una tarjeta existente
y cambiando el `href` y el peso. Luego compilar.

---

## 9 · Dónde llegan los registros

Los dos formularios —el boletín «Te avisamos» del pie y de Noticias, y «Suma tu
alojamiento»— escriben en una hoja de cálculo de Google, avisan a
km0week@hosbec.com y mandan acuse de recibo a quien rellenó.

- **La URL de la hoja** está en `CONFIG.endpointFormularios` de
  `data-alojamientos.js`. Si la dejas vacía, los formularios siguen funcionando
  pero abriendo el correo del visitante en vez de guardar la fila.
- **Los textos del aviso y del acuse, las columnas y la dirección de destino**
  están en el Apps Script de la propia hoja (`REGISTROS/Code.gs` es la copia).
- **La contraseña anti-spam** (`tokenFormularios`) tiene que ser la misma en los
  dos sitios: en `data-alojamientos.js` y en el `CONFIG.token` del script.

**La trampa clásica de Apps Script:** cada vez que edites el script hay que ir a
*Implementar → Gestionar implementaciones → lápiz → Versión: **Nueva versión***.
Si guardas y ya está, sigue corriendo la versión antigua y parece que tu cambio
no ha hecho nada.

El detalle completo (arquitectura, las dos pestañas, los campos, el montaje paso
a paso) está en `REGISTROS/GUIA-REGISTROS.md`.

---

## 10 · Compilar y subir

```bash
python3 _build/build.py
```

Reescribe las 18 páginas de la raíz más `sitemap.xml` y `robots.txt`. Debe
terminar diciendo `páginas generadas: 18 + sitemap.xml + robots.txt`.

En Windows, si tienes Python instalado, es `python _build\build.py`. Si no,
pídemelo en Cowork.

**Subir a GitHub:** la carpeta entera, al repo `bigdatahosbec/km0week`. Tarda
uno o dos minutos en verse publicado. Lo que **no** hace falta subir:
`_build/_desc/` (archivos temporales de los PDF) y `_build/__pycache__/`.

---

## 11 · Cómo compruebas que no has roto nada

Por orden de rapidez:

1. **Abre `index.html` con doble clic.** Funciona sin servidor. Si la portada
   carga y el contador de cifras no marca 0, el JavaScript está sano.
2. **Abre la consola del navegador (F12 → Consola).** Si hay algo en rojo, es
   tuyo y es de ahora.
3. **Cambia a valencià** con el selector. Si algo se queda en castellano, le
   falta el `data-va`.
4. **Pasa por `alojamientos.html` y prueba los filtros**, y por `agenda.html`
   para ver que salen los días que tocan.
5. **Estrecha la ventana** hasta el ancho de un móvil. Si aparece barra de
   desplazamiento horizontal, algo se sale.
6. Si tocaste descargas o prensa, **pulsa un par de botones de descarga.**

Y siempre puedes pedirme en Cowork que pase la verificación completa: 18 páginas
por 6 anchos, errores de consola, desbordes y enlaces rotos.

---

## 12 · Qué NO tocar

- **Los HTML de la raíz.** Regla 1.
- **`_build/parche-5.py`, `-6`, `-7`, `-8` y `parches-aplicados/`.** Son el registro
  histórico de los cambios ya hechos. Son inofensivos —volver a ejecutarlos no
  cambia nada— pero no aportan nada nuevo. Se pueden borrar el día que no
  interese el historial.
- **`_build/_desc/`.** Temporales de la generación de PDF. Se rehacen solos.
- **`assets/fonts/`.** Las tres tipografías de la marca, autoalojadas con
  licencia libre. Si las quitas, la web pierde la cara.
- **`.nojekyll`.** Le dice a GitHub Pages que no procese el sitio con Jekyll. Sin
  ese archivo, las carpetas que empiezan por guion bajo dejan de servirse.

---

## Chuleta

```
Añadir un hotel        →  data-alojamientos.js                  →  regenerar descargables
Cambiar una foto       →  assets/img/foto/ (mismo nombre)       →  regenerar descargables
Cambiar la agenda      →  data-alojamientos.js (AGENDA)         →  regenerar descargables
Cambiar un texto       →  _build/paginas/<pagina>.html          →  compilar
Nueva noticia          →  build.py + paginas/noticia-N.html     →  compilar
Cambiar fechas         →  data-alojamientos.js + build.py       →  compilar + regenerar
Menú, pie, dominio     →  _build/build.py                       →  compilar
Colores y estilos      →  assets/css/km0.css                    →  nada
Contenido de un PDF    →  _build/descargables.py                →  regenerar descargables

compilar               =  python3 _build/build.py
regenerar descargables =  python3 _build/descargables.py   (pídemelo en Cowork)
```

---

## Lo que sigue pendiente de contenido real

- Los **20 alojamientos** son ficticios, y sus `web` apuntan a hosbec.com.
- Los **14 `enlace` de la agenda** apuntan a hosbec.com.
- Las **4 noticias** son de ejemplo.
- Las **54 imágenes** son ilustraciones, no fotografía.
- Las **bases del sorteo** están sin validar por el jurídico.
- No hay **logotipo oficial en vectorial**: el lockup se compone con las dos
  tipografías.
