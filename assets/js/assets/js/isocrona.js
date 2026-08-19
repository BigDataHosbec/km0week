/* ===========================================================================
   EL MAPA DE CASA — lienzo del hero
   Dibuja la Comunitat Valenciana, coloca tu Km 0 y extiende los círculos de
   media hora, una hora y dos horas. Los alojamientos se colorean por franja,
   con la paleta del manual de marca.
   Sin librerías. Determinista. Respeta prefers-reduced-motion.
   =========================================================================== */
window.Isocrona = (function () {
  "use strict";

  /* Contorno simplificado de la Comunitat Valenciana [lat, lng] ------------ */
  const CONTORNO = [
    [40.72, 0.52], [40.63, 0.31], [40.74, -0.16], [40.46, -0.36], [40.31, -0.71],
    [40.10, -0.76], [39.92, -0.91], [39.88, -1.22], [39.66, -1.26], [39.51, -1.46],
    [39.26, -1.36], [39.06, -1.21], [38.86, -1.21], [38.76, -1.06], [38.56, -0.96],
    [38.46, -1.06], [38.31, -1.11], [38.16, -1.06], [37.99, -0.86], [37.86, -0.76],
    [37.98, -0.68], [38.09, -0.65], [38.19, -0.56], [38.35, -0.48], [38.51, -0.23],
    [38.53, -0.13], [38.60, -0.05], [38.64, 0.07], [38.73, 0.23], [38.84, 0.11],
    [38.92, -0.12], [39.00, -0.16], [39.17, -0.25], [39.33, -0.31], [39.47, -0.33],
    [39.64, -0.26], [39.87, -0.10], [40.05, 0.07], [40.24, 0.27], [40.36, 0.40],
    [40.47, 0.48]
  ];

  /* Paleta del manual de marca */
  const C = {
    mar: "#1EA4C6", marD: "#14647D", marP: "#E2F3F8",
    verde: "#8CB26F", verdeD: "#6E9553",
    arena: "#EED8AE", terra: "#D9794D",
    tinta: "#123C4C", suave: "#7D8F98", blanco: "#FFFFFF",
    tierra: "rgba(140,178,111,.10)"   // relleno del territorio, integrado con el fondo
  };

  const ANILLOS = [30, 60, 120];                       // km
  const BANDA = [C.verde, C.terra, C.mar];             // color por franja
  let ETIQ = ["media hora", "1 hora", "2 horas"];
  let ETIQ_CASA = "tu casa";

  let cv, ctx, W = 0, H = 0, DPR = 1;
  let box = { x: 0, y: 0, w: 0, h: 0 };
  let puntos = [], trama = [];
  let origen = null;
  let barrido = 0, objetivo = 0, pulso = 0;
  let hover = null, onChange = null, reduced = false;
  let datos = [];

  /* --------------------------- proyección -------------------------------- */
  let proj = null;
  function calcProj() {
    const lats = CONTORNO.map(p => p[0]), lngs = CONTORNO.map(p => p[1]);
    const latMin = Math.min(...lats), latMax = Math.max(...lats);
    const lngMin = Math.min(...lngs), lngMax = Math.max(...lngs);
    const kx = Math.cos(((latMin + latMax) / 2) * Math.PI / 180);
    const gw = (lngMax - lngMin) * kx, gh = latMax - latMin;
    // 0.78 deja aire alrededor para que los círculos quepan dentro del lienzo
    const s = Math.min(box.w / gw, box.h / gh) * 0.86;
    const ox = box.x + (box.w - gw * s) / 2;
    const oy = box.y + (box.h - gh * s) / 2;
    proj = {
      s, kx, latMax, lngMin, ox, oy,
      to: (lat, lng) => [ox + (lng - lngMin) * kx * s, oy + (latMax - lat) * s],
      from: (px, py) => [latMax - (py - oy) / s, lngMin + (px - ox) / (kx * s)],
      kmPx: s / 111.32
    };
  }

  function haversine(a, b) {
    const R = 6371, r = x => x * Math.PI / 180;
    const dLat = r(b[0] - a[0]), dLon = r(b[1] - a[1]);
    const h = Math.sin(dLat / 2) ** 2 + Math.cos(r(a[0])) * Math.cos(r(b[0])) * Math.sin(dLon / 2) ** 2;
    return 2 * R * Math.asin(Math.sqrt(h));
  }

  function dentro(lat, lng) {
    let inside = false;
    for (let i = 0, j = CONTORNO.length - 1; i < CONTORNO.length; j = i++) {
      const yi = CONTORNO[i][0], xi = CONTORNO[i][1];
      const yj = CONTORNO[j][0], xj = CONTORNO[j][1];
      if ((yi > lat) !== (yj > lat) && lng < ((xj - xi) * (lat - yi)) / (yj - yi) + xi) inside = !inside;
    }
    return inside;
  }

  function franja(d) {
    for (let i = 0; i < ANILLOS.length; i++) if (d <= ANILLOS[i]) return i;
    return -1;
  }

  /* ------------------------------ medidas -------------------------------- */
  function medir() {
    const r = cv.getBoundingClientRect();
    DPR = Math.min(window.devicePixelRatio || 1, 2);
    W = Math.max(280, r.width); H = Math.max(240, r.height);
    cv.width = W * DPR; cv.height = H * DPR;
    ctx.setTransform(DPR, 0, 0, DPR, 0, 0);
    box = { x: 0, y: 0, w: W, h: H };
    calcProj();
    puntos = datos.map(a => {
      const [px, py] = proj.to(a.coords[0], a.coords[1]);
      return { a, px, py };
    });
    construirTrama();
  }

  function construirTrama() {
    trama = [];
    const paso = W >= 620 ? 12 : 14;
    for (let y = 0; y < H; y += paso) {
      for (let x = 0; x < W; x += paso) {
        const [lat, lng] = proj.from(x, y);
        if (dentro(lat, lng)) trama.push([x, y]);
      }
    }
  }

  function rutaTerritorio() {
    ctx.beginPath();
    CONTORNO.forEach((p, i) => {
      const [x, y] = proj.to(p[0], p[1]);
      i ? ctx.lineTo(x, y) : ctx.moveTo(x, y);
    });
    ctx.closePath();
  }

  /* Chincheta de casa, en azul Mediterráneo */
  function casita(x, y, escala) {
    const s = escala || 1;
    ctx.save();
    ctx.translate(x, y); ctx.scale(s, s);
    ctx.beginPath(); ctx.ellipse(0, 17, 13, 4, 0, 0, Math.PI * 2);
    ctx.fillStyle = "rgba(18,60,76,.16)"; ctx.fill();
    ctx.beginPath(); ctx.arc(0, 0, 16, 0, Math.PI * 2);
    ctx.fillStyle = C.mar; ctx.fill();
    ctx.lineWidth = 3; ctx.strokeStyle = "#fff"; ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(-7, 1); ctx.lineTo(0, -6.5); ctx.lineTo(7, 1);
    ctx.moveTo(-5, -0.6); ctx.lineTo(-5, 7); ctx.lineTo(5, 7); ctx.lineTo(5, -0.6);
    ctx.strokeStyle = "#fff"; ctx.lineWidth = 2.2; ctx.lineJoin = "round"; ctx.lineCap = "round";
    ctx.stroke();
    ctx.restore();
  }

  /* ------------------------------- dibujo -------------------------------- */
  function pintar() {
    ctx.clearRect(0, 0, W, H);

    // 1 · territorio: tinte cálido muy leve, integrado con el fondo de la página
    rutaTerritorio();
    ctx.fillStyle = C.tierra;
    ctx.fill();

    // 2 · trama interior
    ctx.beginPath();
    for (let i = 0; i < trama.length; i++) {
      ctx.moveTo(trama[i][0] + 1, trama[i][1]);
      ctx.arc(trama[i][0], trama[i][1], 1, 0, Math.PI * 2);
    }
    ctx.fillStyle = "rgba(140,178,111,.4)";
    ctx.fill();

    rutaTerritorio();
    ctx.strokeStyle = C.verde; ctx.lineWidth = 2; ctx.lineJoin = "round";
    ctx.stroke();

    if (origen) {
      const ox = origen.px, oy = origen.py;

      // 3 · zona alcanzada, en azul muy suave
      const rb = Math.max(1, barrido * proj.kmPx);
      const g = ctx.createRadialGradient(ox, oy, 0, ox, oy, rb);
      g.addColorStop(0, "rgba(30,164,198,.20)");
      g.addColorStop(0.6, "rgba(30,164,198,.10)");
      g.addColorStop(1, "rgba(140,178,111,.04)");
      ctx.beginPath(); ctx.arc(ox, oy, rb, 0, Math.PI * 2);
      ctx.fillStyle = g; ctx.fill();

      // 4 · círculos de tiempo punteados, uno por franja
      ANILLOS.forEach((km, i) => {
        const r = km * proj.kmPx;
        const activo = barrido >= km - 2;
        ctx.beginPath(); ctx.arc(ox, oy, r, 0, Math.PI * 2);
        ctx.setLineDash([2, 6]);
        ctx.lineCap = "round";
        ctx.strokeStyle = activo ? BANDA[i] : "rgba(125,143,152,.28)";
        ctx.lineWidth = 2;
        ctx.stroke();
        ctx.setLineDash([]);
        if (activo) {
          ctx.font = '400 17px "Caveat Brush", cursive';
          ctx.fillStyle = BANDA[i];
          ctx.textAlign = "center";
          ctx.fillText(ETIQ[i], ox, oy - r - 8);
        }
      });

      // 5 · latido
      if (!reduced) {
        const rp = (pulso % 1) * (ANILLOS[2] * proj.kmPx);
        ctx.beginPath(); ctx.arc(ox, oy, rp, 0, Math.PI * 2);
        ctx.strokeStyle = `rgba(30,164,198,${(1 - (pulso % 1)) * 0.32})`;
        ctx.lineWidth = 2; ctx.stroke();
      }
    }

    // 6 · alojamientos, coloreados por franja
    puntos.forEach(p => {
      const d = origen ? haversine([origen.lat, origen.lng], p.a.coords) : Infinity;
      const f = origen && d <= barrido ? franja(d) : -1;
      const hi = hover && hover.a.id === p.a.id;
      const col = f >= 0 ? BANDA[f] : "#fff";
      const r = hi ? 8.5 : (f >= 0 ? 6.5 : 5);
      if (hi) {
        ctx.beginPath(); ctx.arc(p.px, p.py, r + 6, 0, Math.PI * 2);
        ctx.fillStyle = "rgba(30,164,198,.22)"; ctx.fill();
      }
      ctx.beginPath(); ctx.arc(p.px, p.py, r, 0, Math.PI * 2);
      ctx.fillStyle = col; ctx.fill();
      ctx.lineWidth = 1.8;
      ctx.strokeStyle = f >= 0 ? "#fff" : "rgba(125,143,152,.75)";
      ctx.stroke();
    });

    // 7 · tu casa
    if (origen) {
      casita(origen.px, origen.py, W >= 620 ? 1 : .8);
      ctx.font = '400 20px "Caveat Brush", cursive';
      ctx.fillStyle = C.tinta;
      ctx.textAlign = "left";
      ctx.fillText(origen.label, origen.px + 22, origen.py + 1);
      ctx.font = '400 15px "Caveat Brush", cursive';
      ctx.fillStyle = C.suave;
      ctx.fillText(ETIQ_CASA, origen.px + 22, origen.py + 17);
    }
  }

  /* ------------------------------ animación ------------------------------ */
  function bucle() {
    const dif = objetivo - barrido;
    barrido += dif * (reduced ? 1 : 0.075);
    if (Math.abs(dif) < 0.4) barrido = objetivo;
    if (!reduced) pulso += 0.0032;
    pintar();
    requestAnimationFrame(bucle);
  }

  function cuentas() {
    if (!origen) return { total: datos.length, r: ANILLOS.map(() => 0), cerca: null };
    const ds = datos.map(a => ({ a, d: haversine([origen.lat, origen.lng], a.coords) }))
      .sort((x, y) => x.d - y.d);
    return { total: datos.length, r: ANILLOS.map(km => ds.filter(o => o.d <= km).length), cerca: ds[0] };
  }

  function setOrigen(lat, lng, label) {
    const [px, py] = proj.to(lat, lng);
    origen = { lat, lng, label: label || "aquí", px, py };
    objetivo = 0; barrido = 0;
    setTimeout(() => { objetivo = ANILLOS[2]; }, 90);
    if (onChange) onChange(cuentas(), origen);
  }

  function setEtiquetas(anillos, casa) {
    if (anillos) ETIQ = anillos;
    if (casa) ETIQ_CASA = casa;
  }

  function init(opts) {
    cv = document.getElementById(opts.canvas);
    if (!cv) return null;
    ctx = cv.getContext("2d");
    datos = opts.datos;
    onChange = opts.onChange;
    reduced = matchMedia("(prefers-reduced-motion: reduce)").matches;

    medir();

    const tip = document.getElementById(opts.tip);
    cv.addEventListener("pointermove", e => {
      const r = cv.getBoundingClientRect();
      const mx = e.clientX - r.left, my = e.clientY - r.top;
      let best = null, bd = 17;
      puntos.forEach(p => {
        const d = Math.hypot(p.px - mx, p.py - my);
        if (d < bd) { bd = d; best = p; }
      });
      hover = best;
      cv.style.cursor = best ? "pointer" : "crosshair";
      if (tip) {
        if (best) {
          const d = origen ? haversine([origen.lat, origen.lng], best.a.coords) : null;
          tip.innerHTML = best.a.nombre + (d !== null ? ` · <b>${d.toFixed(d < 10 ? 1 : 0)} km</b>` : "");
          tip.style.left = best.px + "px";
          tip.style.top = best.py + "px";
          tip.style.opacity = "1";
        } else tip.style.opacity = "0";
      }
    });
    cv.addEventListener("pointerleave", () => { hover = null; if (tip) tip.style.opacity = "0"; });

    cv.addEventListener("click", e => {
      const r = cv.getBoundingClientRect();
      const mx = e.clientX - r.left, my = e.clientY - r.top;
      if (hover) { window.open(hover.a.web, "_blank", "noopener"); return; }
      const [lat, lng] = proj.from(mx, my);
      if (lat < 36.5 || lat > 41.5 || lng < -2.2 || lng > 1.4) return;
      setOrigen(lat, lng, opts.etiquetaAqui ? opts.etiquetaAqui() : "aquí");
    });

    let t;
    const remedir = () => {
      medir();
      if (origen) { const [px, py] = proj.to(origen.lat, origen.lng); origen.px = px; origen.py = py; }
    };
    window.addEventListener("resize", () => { clearTimeout(t); t = setTimeout(remedir, 140); });
    if (window.ResizeObserver) new ResizeObserver(() => { clearTimeout(t); t = setTimeout(remedir, 120); }).observe(cv.parentElement || cv);
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(remedir);
    window.addEventListener("load", () => setTimeout(remedir, 60));

    bucle();
    return { setOrigen, setEtiquetas, cuentas, get origen() { return origen; }, haversine };
  }

  return { init, ANILLOS };
})();
