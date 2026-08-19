/* ===========================================================================
   Movimiento — anime.js v4
   Entradas cortas, marquesinas infinitas y nada que estorbe la lectura.
   =========================================================================== */
/* anime.js se carga antes como script clásico (assets/vendor/anime.global.js).
   Nada de módulos ES: así la web también funciona abriendo index.html desde el
   disco, sin servidor. */
(function(){
"use strict";
const { animate, createTimeline, stagger, svg, utils, onScroll } = window.anime;

const REDUCED = matchMedia("(prefers-reduced-motion: reduce)").matches;
document.documentElement.classList.add("js-motion");

/* ------------------------------- contadores -------------------------------
   Nunca arrancan en 0: suben desde un valor cercano, así el indicador
   siempre muestra una cifra con sentido. */
function contadores() {
  utils.$("[data-count]").forEach(el => {
    const objetivo = +el.dataset.count;
    const suf = el.dataset.suffix || "";
    el.textContent = objetivo.toLocaleString("es-ES") + suf;
    if (REDUCED || !objetivo) return;
    const desde = Math.max(1, Math.round(objetivo * 0.68));
    const o = { v: desde };
    animate(o, {
      v: objetivo, duration: 1100, ease: "out(3)",
      modifier: utils.round(0),
      onUpdate: () => { el.textContent = o.v.toLocaleString("es-ES") + suf; },
      autoplay: onScroll({ target: el, enter: "bottom-=60 top", sync: "play complete" })
    });
  });
}

/* ---------------------------------- hero ---------------------------------- */
function hero() {
  const tl = createTimeline({ defaults: { duration: 700, ease: "out(3)" } });
  tl.add(".hero-copy > *", { opacity: [0, 1], y: [18, 0], delay: stagger(90) })
    .add(".hero-mapa", { opacity: [0, 1], scale: [.985, 1], duration: 900 }, "-=700");
  const p = document.querySelector(".brush svg path");
  if (p) animate(svg.createDrawable(".brush svg path"), { draw: ["0 0", "0 1"], duration: 620, ease: "out(2)", delay: 700 });
}

/* ------------------------------- revelados -------------------------------- */
const visto = new WeakSet();
function revelados() {
  utils.$("[data-reveal]").forEach(el => {
    if (visto.has(el)) return;
    visto.add(el);
    const hijos = el.hasAttribute("data-reveal-kids") ? Array.from(el.children) : el;
    utils.set(el, { opacity: 1 });
    if (hijos !== el) utils.set(hijos, { opacity: 0 });
    animate(hijos, {
      opacity: [0, 1], y: [22, 0], duration: 680, ease: "out(3)", delay: stagger(65),
      autoplay: onScroll({ target: el, enter: "bottom-=80 top", sync: "play complete" })
    });
  });
}

/* ------------------------------ marquesinas -------------------------------
   El carril lo rellena home.js con copias suficientes; aquí solo lo movemos
   media longitud, que es exactamente un ciclo. Velocidad constante en px/s,
   así el ritmo es el mismo en un portátil y en un monitor de 34". */
const enMarcha = new Map();
function cintas() {
  utils.$("[data-marquee]").forEach(cont => {
    const track = cont.querySelector(".strip-track");
    if (!track) return;
    const previa = enMarcha.get(track);
    if (previa) previa.revert();
    const mitad = parseFloat(track.dataset.mitad || "0") || track.scrollWidth / 2;
    if (!mitad) return;
    const px = parseFloat(cont.dataset.speed || "50");   // píxeles por segundo
    if (REDUCED) { utils.set(track, { x: 0 }); return; }
    // dirección: "ltr" el contenido viaja hacia la derecha, "rtl" hacia la izquierda
    const ltr = (cont.dataset.dir || "rtl") === "ltr";
    enMarcha.set(track, animate(track, {
      x: ltr ? [-mitad, 0] : [0, -mitad],
      duration: (mitad / px) * 1000,
      ease: "linear",
      loop: true
    }));
  });
}

/* ------------------------------- tarjetas --------------------------------- */
function tarjetas() {
  const pintar = () => {
    const els = utils.$(".ficha");
    if (!els.length) return;
    animate(els, { opacity: [0, 1], y: [20, 0], duration: 620, ease: "out(3)", delay: stagger(55) });
  };
  pintar();
  document.addEventListener("km0:fichas", () => setTimeout(pintar, 20));
}

function sellos() {
  if (!utils.$(".sello").length) return;
  animate(".sello", {
    opacity: [0, 1], scale: [1.3, 1],
    rotate: el => [0, parseFloat(el.dataset.rot || 0)],
    duration: 620, ease: "out(4)", delay: stagger(160),
    autoplay: onScroll({ target: ".sellos", enter: "bottom-=80 top", sync: "play complete" })
  });
}

/* --------------------------------- arranque ------------------------------- */
function init() {
  contadores();
  if (REDUCED) {
    utils.set("[data-reveal], .hero-copy > *, .hero-mapa, .ficha, .sello", { opacity: 1, y: 0, scale: 1 });
    cintas();
    return;
  }
  hero();
  document.addEventListener("km0:render", () => revelados());
  document.addEventListener("km0:marquee", () => cintas());
  revelados();
  requestAnimationFrame(() => revelados());
  setTimeout(() => revelados(), 250);
  cintas();
  sellos();
  tarjetas();
}

if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
else init();
})();
