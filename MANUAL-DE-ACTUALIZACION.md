# Km0 Week — Manual de actualización

Cómo cambiar cualquier cosa de la web. Reescrito el 21/08/2026, cuando el
panel pasó a cubrirla entera.

**La regla es una: el contenido se cambia en el panel.**

## → https://bigdatahosbec.github.io/km0week/admin/

Entras con tu nombre y la clave, cambias lo que sea, pulsas **Guardar y
publicar**, y minuto y medio después está en la web. No hay que compilar nada,
ni instalar nada, ni subir archivos a ningún sitio.

---

## Lo que se hace en el panel

| Quieres cambiar | Pestaña |
|---|---|
| Alojamientos: alta, baja, precios, cupo, fotos, filtros | **Alojamientos** |
| Actividades de la agenda, su día, su hora, su enlace | **Agenda** |
| Publicar, editar o retirar una noticia | **Noticias** |
| Textos de las páginas y preguntas frecuentes | **Textos y FAQ** |
| Cabeceras, provincias, experiencias, «la iniciativa» | **Imágenes** |
| Fechas de la edición, teléfono, correo, redes, menú, pie | **Edición** |
| Repasar el valenciano que se ha traducido solo | **Traducciones** |
| Qué filtros se ven en el listado y en la portada | **Filtros** |
| Ver quién cambió qué, y deshacerlo | **Historial** |
| Comprobar si queda algo mal o a medias | **Revisión** |

Para el día a día, la guía de uso está en el proyecto de Cowork:
**`claude/km0week-guia-panel.md`**. Es la que hay que pasarle a quien vaya a
usarlo.

---

## Lo que ya no hay que hacer

Esto valía hasta agosto de 2026 y **ya no**:

| Ya no se hace | Por qué |
|---|---|
| Editar `assets/js/data-alojamientos.js` | Es un archivo generado. Se reescribe solo en cada publicación y perderías el cambio |
| Ejecutar `python3 _build/build.py` | Lo hace GitHub en cada cambio |
| Pedir «regenera los descargables» | Se rehacen solos |
| Cambiar las fechas en dos sitios | Ahora solo en el panel, pestaña Edición |
| Escribir el valenciano de cada frase | Se traduce solo. Escribe en castellano |
| Convertir la foto a webp y renombrarla | La recorta y la nombra el panel |
| Subir la carpeta entera a GitHub | El panel guarda solo el archivo que toca |
| No editar los HTML de la raíz | Ya no están en el repositorio: se generan al publicar |

---

## Lo único que sigue pasando por Cowork

Cuatro cosas, y ninguna es de contenido:

1. **Colores, tipografías, espaciados y maquetación** (`assets/css/km0.css`).
2. **Comportamiento**: filtros, mapa, contadores, envíos (`assets/js/*.js`).
3. **Páginas nuevas** o secciones nuevas dentro de una página.
4. **Textos con enlaces o negritas por dentro**: el editor de Textos los deja
   fuera a propósito, porque cambiarlos por ahí podría romper la maquetación.

Para cualquiera de esas: abre una sesión de Cowork y dilo con tus palabras.

---

## Cómo funciona por dentro (para quien mantenga esto)

### El contenido

```
contenido/alojamientos.json    los alojamientos
contenido/agenda.json          las actividades
contenido/noticias.json        las noticias, con su cuerpo
contenido/configuracion.json   fechas, contacto, dominio, formularios
contenido/navegacion.json      menú, pie, enlaces legales, redes
contenido/filtros.json         qué filtros se muestran
_build/paginas/*.html          el contenido de cada página
assets/img/foto/               las 54 imágenes
```

Eso es **todo lo que hay que respaldar**. El resto se genera.

### Lo que se genera y por qué no está en GitHub

Las 18 páginas de la raíz, `sitemap.xml`, `robots.txt`,
`assets/js/data-alojamientos.js`, `assets/traducciones.json` y los 14 archivos
de `descargas/` **no están en el repositorio a propósito**: los rehace la
publicación automática en cada cambio. Tenerlos ahí invitaba a editarlos por
error y engordaba el repositorio unos 9 MB por cada regeneración.

Para verlos en tu ordenador: `python3 _build/build.py`.

### La publicación automática

`.github/workflows/publicar.yml`, en cada cambio de `main`:

1. `_build/verificar.py` — revisa el contenido. Si algo rompería la web, **no
   publica**.
2. `_build/build.py` — traduce lo que falte, genera las 18 páginas y los datos.
3. `_build/descargables.py` — los 14 PDF, XLSX, DOCX y ZIP.
4. `_build/reunir.py` — junta lo que se sirve en `_sitio/` y lo publica.

Entre uno y cuatro minutos. Si falla, **la web publicada no se toca**: se queda
la última versión buena y GitHub avisa por correo.

El origen de GitHub Pages está en **«GitHub Actions»**, no en una rama. Si
alguien lo cambia a «Deploy from a branch», la web deja de actualizarse.

### La traducción al valencià

`_build/traducir.py`, con **Apertium** (libre y de reglas: la misma frase da
siempre la misma traducción). Solo rellena lo que esté vacío; lo escrito a mano
manda siempre.

Acierta unas dos de cada tres frases palabra por palabra. Lo demás son variantes
razonables y algún error de bulto —«Un cupo publicado» → «Va cabre publicat»—,
así que **hay que repasarlo** en la pestaña Traducciones.

Para añadir un idioma: una línea en `MOTORES` de `_build/traducir.py`. Aviso:
Apertium va muy bien entre castellano y catalán/valenciano y **mal al inglés**;
para eso haría falta un traductor neuronal con clave en los secretos de GitHub.

### El panel

`admin/index.html`, un solo archivo sin dependencias. Habla con la API de
GitHub desde el navegador y escribe directamente en `contenido/`,
`_build/paginas/` y `assets/img/foto/`.

- La clave es un *fine-grained token* limitado a este repositorio, con
  **Contents** en escritura y **Actions** en lectura. Se guarda en el navegador
  de cada persona.
- Si dos personas guardan a la vez, la segunda recibe un aviso y **no pisa** a
  la primera.
- Está fuera de los buscadores por `robots.txt`.
- Los detalles de las claves: `claude/km0week-claves.md` en el proyecto.

### El cuerpo de las noticias

Texto plano con seis marcas: `## subtítulo`, `> cita`, `- viñeta`,
`1. numerada`, `[texto](enlace)` y tablas con `|`. Lo convierte `prosa()` en
`_build/build.py`, y el panel tiene el mismo convertidor para la vista previa
(están comprobados uno contra otro).

No es un editor enriquecido a propósito: el cuerpo tiene que poder traducirse
bloque a bloque y salir con las clases exactas del sitio.

### Los formularios

Google Sheets + Apps Script. La dirección y la contraseña anti-spam se cambian
en la pestaña **Edición** del panel. Los textos del aviso y del acuse están en
el propio Apps Script (`REGISTROS/Code.gs` es la copia).

**La trampa de Apps Script:** al editarlo hay que ir a *Implementar → Gestionar
implementaciones → lápiz → Versión: **Nueva versión***. Si solo guardas, sigue
corriendo la versión antigua.

El detalle completo está en `claude/km0week-registros-formularios.md`.

---

## Si algo va mal

**La web no se actualiza.** Mira el semáforo del panel, arriba a la derecha.
Si está en rojo, púlsalo: se abre el detalle en GitHub y dice qué paso falló.
Casi siempre será el paso 1, «Comprobar el contenido», y el mensaje dirá
exactamente qué está mal y dónde.

**He guardado algo que no quería.** Pestaña **Historial** → **Deshacer**.

**El panel dice que la clave no vale.** Ha caducado o alguien la ha cambiado.
Pulsa **Salir** y entra con la nueva.

**Se ha roto algo y no sé qué.** Abre una sesión de Cowork y dilo. Nada de esto
es irreversible: todo cambio queda en el historial de GitHub con su hora y su
autor.

---

## Lo que sigue pendiente de contenido real

- Los **20 alojamientos** son ficticios, y sus `web` apuntan a hosbec.com.
- Los **14 enlaces de la agenda** apuntan a hosbec.com. El panel los marca en
  rojo.
- Las **4 noticias** son de ejemplo.
- Las **54 imágenes** son ilustraciones generadas por ordenador, **no
  fotografía**. Mientras sea así no se pueden mandar a un medio como fotos de
  los alojamientos.
- Las **bases del sorteo** están sin validar por el jurídico.
- No hay **logotipo oficial en vectorial**: el lockup se compone con las dos
  tipografías.
