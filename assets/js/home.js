/* ===========================================================================
   Portada — de los datos al DOM
   Fichas, ilustraciones, experiencias, destinos, cifras y marquesinas.
   =========================================================================== */
window.Km0 = (function () {
  "use strict";
  const $ = (s, c) => (c || document).querySelector(s);
  const $$ = (s, c) => Array.from((c || document).querySelectorAll(s));
  const D = window.KM0.ALOJAMIENTOS;
  const CFG = window.KM0.CONFIG;

  /* ------------------------------- idioma -------------------------------- */
  let LANG = (() => { try { return localStorage.getItem("km0v4-lang") || "es"; } catch (e) { return "es"; } })();
  const T = {
    es: {
      tipos: { hotel: "Hotel", apartamentos: "Apartamentos", camping: "Camping", rural: "Casa rural", hostal: "Hostal", balneario: "Balneario" },
      exp: {
        gastronomia: "Gastronomía", bienestar: "Bienestar", familia: "En familia",
        cultura: "Cultura y pueblos", mar: "Junto al mar", deporte: "Naturaleza y deporte",
        romantico: "En pareja", mascotas: "Con mascota", accesible: "Accesible",
        sostenible: "Sostenible", noche: "De noche"
      },
      desde: "desde", ver: "Ver oferta", aTi: "a {d} km de casa", nuevo: "Nuevo",
      alojamientos: "alojamientos", alojamiento: "alojamiento", destinos: "destinos", destino: "destino",
      elige: "— elige tu municipio —", ubic: "No hemos podido ubicarte", loc: "Buscándote…",
      seis: "Seis planes para empezar", seisCerca: "Los seis que tienes más cerca",
      nota: "cambia si nos dices dónde vives", notaOk: "ordenados desde tu casa",
      anillos: ["media hora", "1 hora", "2 horas"], casa: "tu casa", aqui: "aquí",
      lema: ["Descubre lo cerca, vive lo nuestro", "Km 0", "Sé turista donde vives", "Km 0"],
      todo: "Todos", ordenar: {
        destacados: "Destacados primero", precio: "Precio más bajo",
        dto: "Mayor descuento", nombre: "Nombre (A-Z)", destino: "Destino (A-Z)"
      },
      dias: ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"],
      meses: ["enero","febrero","marzo","abril","mayo","junio","julio","agosto","septiembre","octubre","noviembre","diciembre"],
      semana: "Todos los días", gratis: "Gratis", verTodo: "Ver los 17 días",
      soloFinde: "Solo fines de semana", enviando: "Enviando…", sinActos: "sin actividades",
      boletinOk: "¡Listo! Te avisaremos por correo.",
      falloEnvio: "No hemos podido enviarlo. Escríbenos a km0week@hosbec.com.",
      actos: "actividades", acto: "actividad",
      ordenados: "Ordenados desde {m}", sinOrigen: "Todos los alojamientos, del más cerca al más lejos",
      enviado: "¡Recibido! Te escribimos en 48 h.", faltan: "Revisa los campos obligatorios."
    },
    va: {
      tipos: { hotel: "Hotel", apartamentos: "Apartaments", camping: "Càmping", rural: "Casa rural", hostal: "Hostal", balneario: "Balneari" },
      exp: {
        gastronomia: "Gastronomia", bienestar: "Benestar", familia: "En família",
        cultura: "Cultura i pobles", mar: "Vora la mar", deporte: "Natura i esport",
        romantico: "En parella", mascotas: "Amb mascota", accesible: "Accessible",
        sostenible: "Sostenible", noche: "De nit"
      },
      desde: "des de", ver: "Veure oferta", aTi: "a {d} km de casa", nuevo: "Nou",
      alojamientos: "allotjaments", alojamiento: "allotjament", destinos: "destins", destino: "destí",
      elige: "— tria el teu municipi —", ubic: "No hem pogut ubicar-te", loc: "Buscant-te…",
      seis: "Sis plans per a començar", seisCerca: "Els sis que tens més a prop",
      nota: "canvia si ens dius on vius", notaOk: "ordenats des de ta casa",
      anillos: ["mitja hora", "1 hora", "2 hores"], casa: "ta casa", aqui: "ací",
      lema: ["Descobreix el que és a prop, viu el que és nostre", "Km 0", "Sigues turista on vius", "Km 0"],
      todo: "Tots", ordenar: {
        destacados: "Destacats primer", precio: "Preu més baix",
        dto: "Major descompte", nombre: "Nom (A-Z)", destino: "Destí (A-Z)"
      },
      dias: ["Dl", "Dt", "Dc", "Dj", "Dv", "Ds", "Dg"],
      meses: ["gener","febrer","març","abril","maig","juny","juliol","agost","setembre","octubre","novembre","desembre"],
      semana: "Tots els dies", gratis: "Gratis", verTodo: "Veure els 17 dies",
      soloFinde: "Només caps de setmana", enviando: "Enviant…", sinActos: "sense activitats",
      boletinOk: "Fet! T'avisarem per correu.",
      falloEnvio: "No hem pogut enviar-ho. Escriu-nos a km0week@hosbec.com.",
      actos: "activitats", acto: "activitat",
      ordenados: "Ordenats des de {m}", sinOrigen: "Tots els allotjaments, del més a prop al més lluny",
      enviado: "Rebut! T'escrivim en 48 h.", faltan: "Revisa els camps obligatoris."
    }
  };
  const t = k => k.split(".").reduce((o, p) => o && o[p], T[LANG]) ?? k;
  const L = o => (!o ? "" : typeof o === "string" ? o : (o[LANG] ?? o.es));
  // "1 alojamiento" / "3 alojamientos"
  const pl = (n, clave) => n + " " + t(n === 1 ? clave : clave + "s");

  /* ------------------------- iconografía del manual ---------------------- */
  const IC = {
    cercania: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="2.6"/></svg>',
    costa: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M2.5 9c1.6-2.4 3.2-2.4 4.8 0s3.2 2.4 4.7 0 3.2-2.4 4.8 0 3.2 2.4 4.7 0"/><path d="M2.5 14c1.6-2.4 3.2-2.4 4.8 0s3.2 2.4 4.7 0 3.2-2.4 4.8 0 3.2 2.4 4.7 0"/><path d="M2.5 19c1.6-2.4 3.2-2.4 4.8 0s3.2 2.4 4.7 0 3.2-2.4 4.8 0 3.2 2.4 4.7 0"/></svg>',
    montana: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M2.5 18l5.5-8 3.4 4.6"/><path d="M9.4 18l4.8-7.5L21.5 18z"/></svg>',
    pueblos: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 20.5h18"/><path d="M5 20.5v-8l4-3 4 3v8"/><path d="M13 20.5v-6l3-2.2 3 2.2v6"/><path d="M9 5.5v2M8 6.5h2"/></svg>',
    naturaleza: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M11 20c-4.7 0-7.6-3.3-7.6-7.6 0-4.7 3.8-8 9.4-8 2.8 0 5.6.9 7.6 2.4-1 8.4-5.2 13.2-9.4 13.2z"/><path d="M4.4 20.4c2.8-5.6 6.6-8.4 11.2-10.3"/></svg>',
    sol: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4.2"/><path d="M12 3v2.2M12 18.8V21M3 12h2.2M18.8 12H21M5.6 5.6l1.6 1.6M16.8 16.8l1.6 1.6M18.4 5.6l-1.6 1.6M7.2 16.8l-1.6 1.6"/></svg>',
    escapadas: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M4 8h16v12H4z"/><path d="M9 8V5.5A1.5 1.5 0 0 1 10.5 4h3A1.5 1.5 0 0 1 15 5.5V8"/><path d="M4 13h16"/></svg>',
    bienestar: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20.5c-3.6-2-5.6-4.6-5.6-7.2 0-2 1.4-3.4 2.9-3.4 1.2 0 2.1.7 2.7 1.8.6-1.1 1.5-1.8 2.7-1.8 1.5 0 2.9 1.4 2.9 3.4 0 2.6-2 5.2-5.6 7.2z"/><path d="M12 9.5c0-2.6 1.4-4.6 3.4-5.5-.4 2.3-1.5 4-3.4 5.5zM12 9.5C12 6.9 10.6 4.9 8.6 4c.4 2.3 1.5 4 3.4 5.5z"/></svg>',
    gastronomia: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M6.5 3v7.4a2.6 2.6 0 0 0 5.2 0V3M9.1 13v8M17.5 3c-1.4 1.4-2.1 3.2-2.1 5.4s.7 2.7 2.1 2.7V21"/></svg>',
    familia: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="8.4" cy="7.4" r="2.9"/><circle cx="17" cy="8.6" r="2.2"/><path d="M3 20.5c0-3.2 2.4-5.5 5.4-5.5s5.4 2.3 5.4 5.5M15.4 20.5c0-2.3.8-4 2.3-4.8"/></svg>',
    romantico: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20.4 5.6a4.6 4.6 0 0 0-6.8.3L12 7.4l-1.6-1.5a4.6 4.6 0 1 0-6.6 6.4L12 20.8l8.2-8.5a4.6 4.6 0 0 0 .2-6.7z"/></svg>',
    mascotas: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><ellipse cx="6" cy="9.4" rx="1.9" ry="2.3"/><ellipse cx="10.6" cy="6.2" rx="1.9" ry="2.3"/><ellipse cx="15.4" cy="6.2" rx="1.9" ry="2.3"/><ellipse cx="19" cy="9.8" rx="1.9" ry="2.3"/><path d="M12.5 11.4c2.4 0 4.3 1.9 4.8 4.2.4 1.9-.9 3.4-2.8 3.4-1 0-1.5-.5-2.4-.5s-1.4.5-2.4.5c-1.9 0-3.2-1.5-2.8-3.4.5-2.3 2.4-4.2 4.8-4.2z"/></svg>',
    accesible: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="4.4" r="1.9"/><path d="M9 9.4h6M12 8.4v6h4l2 6M12 14.4a4.4 4.4 0 1 0 3 7.6"/></svg>',
    noche: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20 14.4A8.4 8.4 0 0 1 9.6 4 8.4 8.4 0 1 0 20 14.4z"/></svg>'
  };
  // Cada experiencia toma su icono y su color del manual
  const EXP_ICO = {
    gastronomia: ["gastronomia", "t-terra"], bienestar: ["bienestar", "t-verde"],
    familia: ["familia", ""], cultura: ["pueblos", "t-terra"], mar: ["costa", ""],
    deporte: ["montana", "t-verde"], romantico: ["romantico", "t-terra"],
    mascotas: ["mascotas", "t-arena"], accesible: ["accesible", ""],
    sostenible: ["naturaleza", "t-verde"], noche: ["noche", "t-arena"]
  };

  /* --------------------- ilustración de cada alojamiento -----------------
     Curvas suaves generadas desde el id: siempre iguales para el mismo
     alojamiento. Si algún día hay foto real, la foto manda. */
  function rng(seed) {
    let s = seed >>> 0 || 1;
    return () => { s ^= s << 13; s ^= s >>> 17; s ^= s << 5; s >>>= 0; return s / 4294967296; };
  }
  function hash(str) {
    let h = 2166136261;
    for (let i = 0; i < str.length; i++) { h ^= str.charCodeAt(i); h = Math.imul(h, 16777619); }
    return h >>> 0;
  }
  const PALS = [
    { cielo: "#E2F3F8", agua: "#1EA4C6", tierra: "#8CB26F", sol: "#EED8AE" },
    { cielo: "#FBF2DE", agua: "#7BC0D4", tierra: "#6E9553", sol: "#D9794D" },
    { cielo: "#EDF3E4", agua: "#1EA4C6", tierra: "#D9794D", sol: "#EED8AE" },
    { cielo: "#FBE7DB", agua: "#4FB2CE", tierra: "#8CB26F", sol: "#EED8AE" }
  ];

  function ilustracion(item, w, h) {
    w = w || 560; h = h || 350;
    const r = rng(hash(item.id));
    const p = PALS[Math.floor(r() * PALS.length)];
    const horizonte = h * (0.6 + r() * 0.08);
    const solX = w * (0.16 + r() * 0.68), solY = horizonte - h * (0.2 + r() * 0.14);
    const solR = Math.min(w, h) * (0.075 + r() * 0.03);

    // colinas: dos capas de curvas suaves
    const colina = (base, amp, color, op) => {
      const pts = 5;
      let d = `M0 ${h} L0 ${base}`;
      for (let i = 1; i <= pts; i++) {
        const x = (w / pts) * i;
        const y = base - amp * (0.35 + r() * 0.65);
        d += ` Q ${(x - w / pts / 2).toFixed(1)} ${y.toFixed(1)} ${x.toFixed(1)} ${(base - amp * 0.2 * r()).toFixed(1)}`;
      }
      return `<path d="${d} L${w} ${h} Z" fill="${color}" opacity="${op}"/>`;
    };

    // olas del manual sobre el agua
    let olas = "";
    for (let i = 0; i < 4; i++) {
      const y = horizonte + (h - horizonte) * (0.22 + i * 0.2);
      const off = (r() - 0.5) * w * 0.3;
      olas += `<path d="M${(w * 0.1 + off).toFixed(0)} ${y.toFixed(0)}c${(w * 0.07).toFixed(0)}-9 ${(w * 0.14).toFixed(0)}-9 ${(w * 0.21).toFixed(0)} 0s${(w * 0.14).toFixed(0)} 9 ${(w * 0.21).toFixed(0)} 0"
        fill="none" stroke="#FFFFFF" stroke-opacity=".55" stroke-width="2.4" stroke-linecap="round"/>`;
    }

    return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${w} ${h}" preserveAspectRatio="xMidYMid slice" role="img" aria-label="Ilustración de ${item.destino}">
      <rect width="${w}" height="${h}" fill="${p.cielo}"/>
      <circle cx="${solX.toFixed(0)}" cy="${solY.toFixed(0)}" r="${solR.toFixed(0)}" fill="${p.sol}"/>
      ${colina(horizonte + 6, h * 0.3, p.tierra, .28)}
      ${colina(horizonte + 4, h * 0.22, p.tierra, .45)}
      ${colina(horizonte + 2, h * 0.13, p.tierra, .72)}
      <rect x="0" y="${horizonte.toFixed(0)}" width="${w}" height="${(h - horizonte).toFixed(0)}" fill="${p.agua}"/>
      ${olas}
    </svg>`;
  }

  /* -------------------------------- fichas ------------------------------- */
  function ficha(a, dist) {
    const inc = (L(a.oferta.incluye) || []).slice(0, 3);
    const estrellas = a.categoria ? " · " + "★".repeat(a.categoria) : "";
    const tema = a.experiencias[0];
    return `<article class="ficha" data-id="${a.id}">
      <div class="ficha-art">
        ${a.imagen ? `<img src="${a.imagen}" alt="${a.nombre}" loading="lazy">` : ilustracion(a, 560, 350)}
        <div class="ficha-tags">
          ${tema ? `<span class="pill pill-verde">${t("exp." + tema)}</span>` : ""}
          ${a.oferta.dto ? `<span class="pill pill-solida">−${a.oferta.dto}%</span>` : ""}
          ${a.nuevo ? `<span class="pill pill-arena">${t("nuevo")}</span>` : ""}
        </div>
        ${dist != null ? `<span class="ficha-dist">${IC.cercania} ${t("aTi").replace("{d}", dist.toFixed(dist < 10 ? 1 : 0))}</span>` : ""}
      </div>
      <div class="ficha-bd">
        <span class="label">${t("tipos." + a.tipo)}${estrellas} · ${a.destino}</span>
        <h3>${a.nombre}</h3>
        <p class="ficha-claim">${L(a.claim)}</p>
        <div class="ficha-oferta">
          <div class="ttl">${L(a.oferta.titulo)}</div>
          <ul>${inc.map(i => `<li>${i}</li>`).join("")}</ul>
        </div>
      </div>
      <div class="ficha-ft">
        <div class="ficha-price">
          <span class="label" style="display:block;margin-bottom:3px;color:var(--suave)">${t("desde")}</span>
          <b>${a.oferta.precioDesde} €</b>${a.oferta.precioOriginal ? `<s>${a.oferta.precioOriginal} €</s>` : ""}
          <span class="u">${L(a.oferta.unidad)}</span>
        </div>
        <a class="btn btn-mar btn-sm" href="${a.web}" target="_blank" rel="noopener">${t("ver")}</a>
      </div>
    </article>`;
  }

  /* -------------------------------- pintar ------------------------------- */
  let ORIGEN = null;
  const hav = (a, b) => {
    const R = 6371, r = x => x * Math.PI / 180;
    const dLat = r(b[0] - a[0]), dLon = r(b[1] - a[1]);
    const h = Math.sin(dLat / 2) ** 2 + Math.cos(r(a[0])) * Math.cos(r(b[0])) * Math.sin(dLon / 2) ** 2;
    return 2 * R * Math.asin(Math.sqrt(h));
  };

  function pintarFichas() {
    const box = $("#fichas"); if (!box) return;
    const lista = D.slice();
    if (ORIGEN) lista.sort((x, y) => hav(ORIGEN, x.coords) - hav(ORIGEN, y.coords));
    else lista.sort((x, y) => (y.destacado - x.destacado) || (y.oferta.dto - x.oferta.dto));
    box.innerHTML = lista.slice(0, 6).map(a => ficha(a, ORIGEN ? hav(ORIGEN, a.coords) : null)).join("");
    const tit = $("#fichas-titulo"); if (tit) tit.textContent = ORIGEN ? t("seisCerca") : t("seis");
    const nota = $("#fichas-nota"); if (nota) nota.textContent = ORIGEN ? t("notaOk") : t("nota");
  }

  function pintarTemas() {
    const box = $("#temas"); if (!box) return;
    const c = {};
    D.forEach(a => a.experiencias.forEach(e => c[e] = (c[e] || 0) + 1));
    box.innerHTML = Object.keys(c).sort((a, b) => c[b] - c[a]).map(k => {
      const [ico, tono] = EXP_ICO[k] || ["costa", ""];
      const destino = $("#lista-alojamientos") ? "#filtros" : "alojamientos.html?experiencia=" + k;
      return `<a class="tema" href="${destino}" data-exp="${k}">
        <span class="ico ico-sm ${tono}">${IC[ico]}</span>
        <span><span class="t">${t("exp." + k)}</span><span class="c">${pl(c[k], "alojamiento")}</span></span>
      </a>`;
    }).join("");
  }

  function pintarProvincias() {
    const box = $("#provincias"); if (!box) return;
    const p = {};
    D.forEach(a => { (p[a.provincia] = p[a.provincia] || new Set()).add(a.destino); });
    const orden = ["Castelló", "València", "Alicante"];
    const tonos = ["", "t-verde", "t-terra"];
    box.innerHTML = orden.filter(k => p[k]).map((k, i) => `
      <div class="prov">
        <div class="prov-hd">
          <span class="ico ico-sm ${tonos[i]}">${IC.pueblos}</span>
          <div>
            <h4>${k}</h4>
            <span class="n">${pl(p[k].size, "destino")} · ${pl(D.filter(a => a.provincia === k).length, "alojamiento")}</span>
          </div>
        </div>
        <ul>${[...p[k]].sort((a, b) => a.localeCompare(b, "es")).map(d => `<li><a href="alojamientos.html?provincia=${encodeURIComponent(k)}" data-destino="${d}">${d}</a></li>`).join("")}</ul>
      </div>`).join("");
  }

  /* ----------------------------- marquesinas -----------------------------
     Rellenamos el carril con copias hasta cubrir el doble del ancho visible.
     Así el bucle nunca deja hueco, sea cual sea la pantalla. */
  function unidadDestinos() {
    return [...new Set(D.map(a => a.destino))].map(d => `<span>${d}</span>`).join("");
  }
  function unidadLema() {
    return t("lema").map((x, i) => `<span class="${i % 2 ? "" : "lema"}">${x}</span>`).join("");
  }

  function rellenar(track, unidadHTML) {
    if (!track) return;
    const cont = track.parentElement;
    track.innerHTML = unidadHTML;
    const anchoUnidad = track.scrollWidth || 1;
    const anchoCont = cont.clientWidth || window.innerWidth;
    // copias necesarias para tapar la pantalla, y luego el doble para el bucle
    const n = Math.max(1, Math.ceil((anchoCont * 1.2) / anchoUnidad));
    track.innerHTML = unidadHTML.repeat(n * 2);
    track.dataset.mitad = String(track.scrollWidth / 2);
  }

  function montarMarquesinas() {
    rellenar($("#strip-destinos"), unidadDestinos());
    rellenar($("#strip-lema"), unidadLema());
    document.dispatchEvent(new CustomEvent("km0:marquee"));
  }

  /* -------------------- cifras calculadas desde los datos ---------------- */
  function cifrasAutomaticas() {
    const v = {
      alojamientos: D.length,
      destinos: new Set(D.map(a => a.destino)).size,
      cupo: D.reduce((a, b) => a + (b.cupo || 0), 0),
      actividades: (window.KM0.AGENDA || []).length
    };
    $$("[data-auto]").forEach(el => {
      const n = v[el.dataset.auto];
      if (n === undefined) return;
      el.dataset.count = n;
      el.textContent = n.toLocaleString("es-ES") + (el.dataset.suffix || "");
    });
  }

  /* ------------------------------- municipios ---------------------------- */
  const MUNIS = [
    ["Alacant / Alicante", 38.3452, -0.4810], ["Alcoi / Alcoy", 38.6989, -0.4739],
    ["Alzira", 39.1509, -0.4363], ["Altea", 38.5990, -0.0518],
    ["Benicarló", 40.4163, 0.4270], ["Benicàssim", 40.0546, 0.0653],
    ["Benidorm", 38.5342, -0.1314], ["Borriana / Burriana", 39.8892, -0.0855],
    ["Calp / Calpe", 38.6446, 0.0447], ["Castelló de la Plana", 39.9864, -0.0513],
    ["Cullera", 39.1646, -0.2519], ["Dénia", 38.8408, 0.1057],
    ["Elda", 38.4779, -0.7947], ["Elx / Elche", 38.2669, -0.6983],
    ["Gandia", 38.9676, -0.1810], ["Guardamar del Segura", 38.0894, -0.6537],
    ["Morella", 40.6193, -0.1013], ["Oliva", 38.9187, -0.1188],
    ["Ontinyent", 38.8214, -0.6069], ["Orihuela", 38.0847, -0.9447],
    ["Paterna", 39.5028, -0.4407], ["Peníscola / Peñíscola", 40.3585, 0.4028],
    ["Requena", 39.4885, -1.1000], ["Sagunt / Sagunto", 39.6795, -0.2760],
    ["Santa Pola", 38.1913, -0.5605], ["Segorbe", 39.8500, -0.4833],
    ["Torrent", 39.4370, -0.4653], ["Torrevieja", 37.9787, -0.6822],
    ["València", 39.4699, -0.3763], ["Vila-real", 39.9377, -0.1013],
    ["La Vila Joiosa", 38.5069, -0.2331], ["Vinaròs", 40.4700, 0.4750],
    ["Xàbia / Jávea", 38.7891, 0.1663], ["Xàtiva", 38.9871, -0.5188]
  ];


  /* =========================================================================
     PÁGINAS INTERIORES
     Cada bloque se activa solo si encuentra su marcado, así el mismo archivo
     vale para toda la web.
     ========================================================================= */

  /* ------------------------ listado con filtros -------------------------- */
  const FILTRO = { provincia: "", tipo: [], experiencia: [], orden: "destacados" };

  function chipsDe(cont, valores, etiqueta, multiple) {
    const grupo = cont.dataset.grupo;
    const previos = $$("button", cont); previos.forEach(b => b.remove());
    const marca = v => multiple ? FILTRO[grupo].includes(v) : FILTRO[grupo] === v;
    const html = [];
    if (!multiple) html.push(`<button class="chip" type="button" data-v="" aria-pressed="${FILTRO[grupo] === ""}">${t("todo")}</button>`);
    valores.forEach(v => {
      html.push(`<button class="chip${grupo === "experiencia" ? " verde" : grupo === "tipo" ? " terra" : ""}" type="button" data-v="${v}" aria-pressed="${marca(v)}">${etiqueta(v)}</button>`);
    });
    cont.insertAdjacentHTML("beforeend", html.join(""));
    $$("button", cont).forEach(b => b.addEventListener("click", () => {
      const v = b.dataset.v;
      if (multiple) {
        const i = FILTRO[grupo].indexOf(v);
        if (i < 0) FILTRO[grupo].push(v); else FILTRO[grupo].splice(i, 1);
      } else {
        FILTRO[grupo] = FILTRO[grupo] === v ? "" : v;
      }
      pintarListado();
    }));
  }

  function filtrados() {
    return D.filter(a =>
      (!FILTRO.provincia || a.provincia === FILTRO.provincia) &&
      (!FILTRO.tipo.length || FILTRO.tipo.includes(a.tipo)) &&
      (!FILTRO.experiencia.length || FILTRO.experiencia.some(e => a.experiencias.includes(e)))
    );
  }

  const ORDEN = {
    destacados: (x, y) => (y.destacado - x.destacado) || (y.oferta.dto - x.oferta.dto),
    precio: (x, y) => (x.oferta.precioDesde || 1e9) - (y.oferta.precioDesde || 1e9),
    dto: (x, y) => (y.oferta.dto || 0) - (x.oferta.dto || 0),
    nombre: (x, y) => x.nombre.localeCompare(y.nombre, "es"),
    destino: (x, y) => x.destino.localeCompare(y.destino, "es") || x.nombre.localeCompare(y.nombre, "es")
  };

  function pintarListado() {
    const box = $("#lista-alojamientos"); if (!box) return;
    const lista = filtrados().sort(ORDEN[FILTRO.orden] || ORDEN.destacados);
    box.innerHTML = lista.map(a => ficha(a, null)).join("");
    box.hidden = !lista.length;
    const vacio = $("#lista-vacia"); if (vacio) vacio.hidden = !!lista.length;
    const tot = $("#f-total"); if (tot) tot.textContent = lista.length;
    const tt = $("#f-total-txt"); if (tt) tt.textContent = t(lista.length === 1 ? "alojamiento" : "alojamientos");
    $$("[data-grupo]").forEach(g => {
      const grupo = g.dataset.grupo;
      $$("button", g).forEach(b => {
        const v = b.dataset.v;
        b.setAttribute("aria-pressed", String(Array.isArray(FILTRO[grupo]) ? FILTRO[grupo].includes(v) : FILTRO[grupo] === v));
      });
    });
    // contador del botón «Filtros» de móvil
    const act = (FILTRO.provincia ? 1 : 0) + FILTRO.tipo.length + FILTRO.experiencia.length;
    const ba = $("#f-activos");
    if (ba) { ba.textContent = act; ba.hidden = !act; }

    document.dispatchEvent(new CustomEvent("km0:fichas"));
    document.dispatchEvent(new CustomEvent("km0:render"));
  }

  function montarFiltros() {
    const zona = $("#filtros"); if (!zona) return;
    const provs = ["Castelló", "València", "Alicante"].filter(p => D.some(a => a.provincia === p));
    const tipos = [...new Set(D.map(a => a.tipo))];
    const exps = [...new Set(D.flatMap(a => a.experiencias))]
      .sort((a, b) => t("exp." + a).localeCompare(t("exp." + b), "es"));
    chipsDe($("#f-provincia"), provs, v => v, false);
    chipsDe($("#f-tipo"), tipos, v => t("tipos." + v), true);
    chipsDe($("#f-exp"), exps, v => t("exp." + v), true);

    const sel = $("#f-orden");
    if (sel) {
      sel.innerHTML = Object.keys(ORDEN).map(k =>
        `<option value="${k}"${k === FILTRO.orden ? " selected" : ""}>${t("ordenar." + k)}</option>`).join("");
      sel.onchange = () => { FILTRO.orden = sel.value; pintarListado(); };
    }
    // En móvil los tres grupos se pliegan tras un botón «Filtros».
    // (montarFiltros() se llama más de una vez, de ahí el pestillo dataset.listo:
    //  sin él el listener se registraría dos veces y el toggle se anularía solo)
    const tg = $("#f-toggle"), grupos = $("#f-grupos");
    if (tg && grupos && !tg.dataset.listo) {
      tg.dataset.listo = "1";
      tg.addEventListener("click", () => {
        const abierto = grupos.classList.toggle("abierto");
        tg.setAttribute("aria-expanded", String(abierto));
      });
    }

    const limpiar = () => {
      FILTRO.provincia = ""; FILTRO.tipo = []; FILTRO.experiencia = [];
      FILTRO.orden = "destacados";
      if (sel) sel.value = "destacados";
      pintarListado();
    };
    const bl = $("#f-limpiar"); if (bl) bl.addEventListener("click", limpiar);
    $$("[data-limpiar]").forEach(b => b.addEventListener("click", limpiar));

    // ?provincia=Alicante  ·  ?experiencia=gastronomia  ·  ?tipo=camping
    const q = new URLSearchParams(location.search);
    if (q.get("provincia")) FILTRO.provincia = q.get("provincia");
    if (q.get("tipo")) FILTRO.tipo = [q.get("tipo")];
    if (q.get("experiencia")) FILTRO.experiencia = [q.get("experiencia")];
    pintarListado();
  }

  /* ---------------------------- página del mapa -------------------------- */
  function pintarCercanos() {
    const box = $("#cercanos"); if (!box) return;
    const col = ["#8CB26F", "#D9794D", "#1EA4C6"];
    const lista = D.slice();
    if (ORIGEN) lista.sort((x, y) => hav(ORIGEN, x.coords) - hav(ORIGEN, y.coords));
    else lista.sort((x, y) => x.destino.localeCompare(y.destino, "es"));
    box.innerHTML = lista.map(a => {
      const d = ORIGEN ? hav(ORIGEN, a.coords) : null;
      const banda = d == null ? 2 : d <= 30 ? 0 : d <= 60 ? 1 : 2;
      return `<a class="cercano" href="${a.web}" target="_blank" rel="noopener">
        <span class="bolita" style="background:${d == null ? "#C9D6DB" : col[banda]}"></span>
        <span><span class="n">${a.nombre}</span><br><span class="d">${t("tipos." + a.tipo)} · ${a.destino}</span></span>
        <span class="km">${d == null ? "—" : d.toFixed(d < 10 ? 1 : 0) + " km"}</span>
      </a>`;
    }).join("");
  }

  /* ------------------------------- agenda -------------------------------- */
  const AG = { dia: 0, gratis: false, finde: false };   // dia 0 = todos los días

  function fechaDia(n) {                     // n = 1..N → Date local, sin líos de UTC
    const [Y, M, DD] = CFG.fechaInicio.slice(0, 10).split("-").map(Number);
    return new Date(Y, M - 1, DD + n - 1);
  }

  // Cuántos días dura la edición: se deduce de fechaInicio y fechaFin.
  function totalDias() {
    const a = new Date(CFG.fechaInicio.slice(0, 10) + "T00:00:00");
    const b = new Date((CFG.fechaFin || CFG.fechaInicio).slice(0, 10) + "T00:00:00");
    return Math.max(1, Math.round((b - a) / 864e5) + 1);
  }

  // viernes, sábado y domingo: los tres findes de la edición son 13-15, 20-22 y 27-29
  const esFinde = n => [5, 6, 0].includes(fechaDia(n).getDay());

  // Adónde lleva «Quiero ir»: primero el enlace propio de la actividad;
  // si no lo tiene, la web del alojamiento adherido de ese destino; y si
  // tampoco, la de HOSBEC. Nunca queda un botón muerto.
  function enlaceActo(a) {
    if (a.enlace) return a.enlace;
    const casa = D.find(x => x.destino === a.lugar && x.web);
    return (casa && casa.web) || CFG.webHosbec || "https://hosbec.com";
  }

  function esGratis(a) {
    const p = (L(a.precio) || "").toLowerCase();
    return !p || p.includes("gratis") || p.includes("0 €");
  }

  function pintarAgenda() {
    const cd = $("#ag-dias"), ca = $("#ag-actos"); if (!cd || !ca) return;
    const AGENDA = window.KM0.AGENDA || [];

    const N = totalDias();
    const conActos = n => AGENDA.some(a => a.dia === n && (!AG.gratis || esGratis(a)));
    const dias = [];
    for (let n = 1; n <= N; n++) if (!AG.finde || esFinde(n)) dias.push(n);

    cd.innerHTML = dias.map(n => {
      const f = fechaDia(n), hay = conActos(n);
      const cls = ["dia", esFinde(n) ? "fds" : "", hay ? "" : "sin"].filter(Boolean).join(" ");
      return `<button class="${cls}" type="button" data-d="${n}" aria-pressed="${AG.dia === n}"${hay ? "" : ' disabled aria-disabled="true" title="' + t("sinActos") + '"'}>
        <span class="s">${t("dias")[(f.getDay() + 6) % 7]}</span>
        <span class="n">${f.getDate()}</span>
        <span class="s">${t("meses")[f.getMonth()].slice(0, 3)}</span>
      </button>`;
    }).join("");
    $$("button", cd).forEach(b => b.addEventListener("click", () => {
      AG.dia = AG.dia === +b.dataset.d ? 0 : +b.dataset.d;
      pintarAgenda();
    }));

    const lista = AGENDA
      .filter(a => (!AG.dia || a.dia === AG.dia) && (!AG.gratis || esGratis(a)) && (!AG.finde || esFinde(a.dia)))
      .sort((x, y) => x.dia - y.dia || x.hora.localeCompare(y.hora));

    ca.innerHTML = lista.map(a => {
      const f = fechaDia(a.dia);
      return `<article class="acto ${a.tipo}">
        <div>
          <div class="h">${a.hora}</div>
          <div class="body-sm" style="color:var(--suave)">${t("dias")[(f.getDay() + 6) % 7]} ${f.getDate()}</div>
        </div>
        <div>
          <h3>${L(a.titulo)}</h3>
          <p class="body-sm">${L(a.desc)}</p>
          <div class="meta">
            <span class="pill pill-verde">${a.lugar}</span>
            <span class="pill ${esGratis(a) ? "pill-arena" : "pill-terra"}">${esGratis(a) ? t("gratis") : L(a.precio)}</span>
          </div>
        </div>
        <a class="btn btn-mar btn-sm" href="${enlaceActo(a)}" target="_blank" rel="noopener" data-va="Vull anar-hi">Quiero ir</a>
      </article>`;
    }).join("");

    const v = $("#ag-vacio"); if (v) v.hidden = !!lista.length;
    const bt = $("#ag-todo");
    if (bt) bt.setAttribute("aria-pressed", String(!AG.dia));
    const bg = $("#ag-gratis");
    if (bg) bg.setAttribute("aria-pressed", String(AG.gratis));
    const bf = $("#ag-finde");
    if (bf) bf.setAttribute("aria-pressed", String(AG.finde));
    document.dispatchEvent(new CustomEvent("km0:render"));
  }

  function montarAgenda() {
    if (!$("#ag-dias")) return;
    const bt = $("#ag-todo"); if (bt) bt.addEventListener("click", () => { AG.dia = 0; pintarAgenda(); });
    const bg = $("#ag-gratis"); if (bg) bg.addEventListener("click", () => { AG.gratis = !AG.gratis; pintarAgenda(); });
    const bf = $("#ag-finde"); if (bf) bf.addEventListener("click", () => {
      AG.finde = !AG.finde;
      if (AG.finde && AG.dia && !esFinde(AG.dia)) AG.dia = 0;
      pintarAgenda();
    });
    pintarAgenda();
  }

  /* ------------------------- envío de formularios -------------------------
     Todo va al Apps Script de la hoja de registros. Tres intentos en cascada,
     para que un registro no se pierda nunca:

       1. fetch normal leyendo la respuesta (así sabemos de verdad si ha ido
          bien). Se manda como text/plain a propósito: es una «petición
          simple» y evita el preflight, que Apps Script no sabe contestar.
       2. si eso falla por CORS o por red, se reintenta en modo no-cors: llega
          igual, aunque no podamos leer la contestación.
       3. si tampoco, se abre el correo del visitante con los datos escritos.

     Mientras CFG.endpointFormularios esté vacío se va directo al paso 3. */

  function datosComunes() {
    return {
      _token: CFG.tokenFormularios || "",
      idioma: LANG,
      origen: location.href
    };
  }

  async function enviarRegistro(datos) {
    const url = CFG.endpointFormularios;
    if (!url) return "correo";

    const cuerpo = JSON.stringify(Object.assign(datosComunes(), datos));

    try {
      const r = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "text/plain;charset=utf-8" },
        body: cuerpo,
        redirect: "follow"
      });
      const j = await r.json();
      return j && j.ok ? "ok" : "error";
    } catch (_) { /* seguimos con el plan B */ }

    try {
      await fetch(url, { method: "POST", mode: "no-cors", body: cuerpo });
      return "ok";                      // no podemos leer la respuesta, pero sale
    } catch (_) { /* plan C */ }

    return "correo";
  }

  // Plan C: abrir el gestor de correo con todo escrito
  function porCorreo(asunto, lineas) {
    location.href = "mailto:" + (CFG.emailContacto || "km0week@hosbec.com") +
      "?subject=" + encodeURIComponent(asunto) +
      "&body=" + encodeURIComponent(lineas.filter(Boolean).join("\n"));
  }

  /* ------------------------- boletín «Te avisamos» ------------------------
     Va por AJAX contra FormSubmit para no sacar al visitante de la página.
     Si algo falla, se abre el correo del visitante como plan B. */
  function montarBoletin() {
    // hay uno en el pie de todas las páginas y otro en Noticias
    $$("form.subscribe").forEach(montarUnBoletin);
  }

  function montarUnBoletin(f) {
    if (!f || f.dataset.listo) return;
    f.dataset.listo = "1";
    f.addEventListener("submit", async e => {
      e.preventDefault();
      if (!f.checkValidity()) { f.reportValidity(); return; }

      const btn = f.querySelector("button");
      const texto = btn ? btn.textContent : "";
      if (btn) { btn.disabled = true; btn.textContent = t("enviando"); }

      const email = (f.querySelector("input[type=email]") || {}).value || "";
      const r = await enviarRegistro({
        formulario: "boletin",
        email: email,
        _honey: (f.querySelector("[name=_honey]") || {}).value || ""
      });

      if (btn) { btn.disabled = false; btn.textContent = texto; }

      if (r === "ok") { f.reset(); toast(t("boletinOk")); }
      else if (r === "correo") {
        porCorreo("[Km0 Week] Alta en el boletín", [
          email,
          LANG === "va" ? "Vull que m'aviseu quan s'òbriguen les reserves."
                        : "Quiero que me aviséis cuando se abran las reservas."
        ]);
      } else toast(t("falloEnvio"));
    });
  }

  /* --------------------------- formulario de alta ------------------------ */
  function montarFormulario() {
    montarBoletin();

    const f = $("#form-suma"); if (!f) return;

    f.addEventListener("submit", async e => {
      e.preventDefault();
      if (!f.checkValidity()) { toast(t("faltan")); f.reportValidity(); return; }

      const b = f.querySelector('button[type="submit"]');
      const texto = b ? b.textContent : "";
      if (b) { b.disabled = true; b.textContent = t("enviando"); }

      const v = n => { const el = f.querySelector("[name=" + n + "]"); return el ? el.value.trim() : ""; };
      const datos = {
        formulario: "alojamiento",
        nombre: v("nombre"), municipio: v("municipio"), tipo: v("tipo"),
        cupo: v("cupo"), contacto: v("contacto"), email: v("email"),
        telefono: v("telefono"), web: v("web"), oferta: v("oferta"),
        acepto: !!f.querySelector("[name=acepto]:checked"),
        _honey: v("_honey")
      };

      const r = await enviarRegistro(datos);
      if (b) { b.disabled = false; b.textContent = texto; }

      if (r === "ok") {
        const ok = $("#form-ok");
        if (ok) { ok.hidden = false; ok.scrollIntoView({ behavior: "smooth", block: "center" }); }
        toast(t("enviado"));
        f.reset();
      } else if (r === "correo") {
        porCorreo("[Km0 Week] Solicitud de alojamiento: " + (datos.nombre || datos.email), [
          "Alojamiento: " + datos.nombre,
          "Municipio: " + datos.municipio,
          "Tipo: " + datos.tipo,
          "Plazas comprometidas: " + datos.cupo,
          "Persona de contacto: " + datos.contacto,
          "Correo: " + datos.email,
          "Teléfono: " + datos.telefono,
          "Web: " + datos.web,
          "",
          "Oferta propuesta:",
          datos.oferta
        ]);
      } else toast(t("falloEnvio"));
    });
  }

  /* --------------------------------- aviso ------------------------------- */
  let tt;
  function toast(msg) {
    let el = $(".toast");
    if (!el) { el = document.createElement("div"); el.className = "toast"; document.body.appendChild(el); }
    el.textContent = msg;
    requestAnimationFrame(() => el.classList.add("on"));
    clearTimeout(tt); tt = setTimeout(() => el.classList.remove("on"), 2600);
  }

  /* -------------------------------- idioma ------------------------------- */
  let radar = null;
  let refrescarCuenta = null;   // la cuenta atrás también cambia de idioma
  function aplicarIdioma() {
    document.documentElement.lang = LANG === "va" ? "ca-ES-valencia" : "es";
    $$("[data-va]").forEach(el => {
      if (!el.hasAttribute("data-es")) el.setAttribute("data-es", el.textContent.trim());
      el.textContent = LANG === "va" ? el.getAttribute("data-va") : el.getAttribute("data-es");
    });
    // marcadores de campo bilingües:  <input data-va-ph="…" placeholder="…">
    $$("[data-va-ph]").forEach(el => {
      if (!el.hasAttribute("data-es-ph")) el.setAttribute("data-es-ph", el.getAttribute("placeholder") || "");
      el.setAttribute("placeholder", LANG === "va" ? el.getAttribute("data-va-ph") : el.getAttribute("data-es-ph"));
    });
    $$("[data-va-html]").forEach(el => {
      if (!el.hasAttribute("data-es-html")) el.setAttribute("data-es-html", el.innerHTML.trim());
      el.innerHTML = LANG === "va" ? el.getAttribute("data-va-html") : el.getAttribute("data-es-html");
    });
    $$(".lang button").forEach(b => b.setAttribute("aria-pressed", String(b.dataset.lang === LANG)));
    const sel = $("#origen-select");
    if (sel && sel.options.length) sel.options[0].text = t("elige");
    if (radar) radar.setEtiquetas(t("anillos"), t("casa"));
    $$("[data-fechas]").forEach(e => e.textContent = L(CFG.fechasTexto));
    if (refrescarCuenta) refrescarCuenta();
    pintarFichas(); pintarTemas(); pintarProvincias(); montarMarquesinas();
    if ($("#filtros")) montarFiltros();
    pintarCercanos();
    if ($("#ag-dias")) pintarAgenda();
    document.dispatchEvent(new CustomEvent("km0:lang", { detail: { lang: LANG } }));
    document.dispatchEvent(new CustomEvent("km0:render"));
  }

  /* -------------------------------- arranque ----------------------------- */
  function init() {
    const sel = $("#origen-select");
    if (sel) {
      sel.innerHTML = `<option value="">${t("elige")}</option>` +
        MUNIS.map(m => `<option value="${m[1]},${m[2]}">${m[0]}</option>`).join("");
    }

    cifrasAutomaticas();
    pintarFichas(); pintarTemas(); pintarProvincias();
    montarFiltros(); montarAgenda(); montarFormulario();
    $$("[data-fechas]").forEach(e => e.textContent = L(CFG.fechasTexto));

    radar = window.Isocrona.init({
      canvas: "isocrona", tip: "radar-tip", datos: D,
      etiquetaAqui: () => t("aqui"),
      onChange: (c, o) => {
        ORIGEN = [o.lat, o.lng];
        $$("[data-ring]").forEach((el, i) => { el.textContent = c.r[i]; });
        const cerca = $("#cerca-nombre");
        if (cerca && c.cerca) cerca.textContent = c.cerca.a.nombre + " · " + c.cerca.d.toFixed(c.cerca.d < 10 ? 1 : 0) + " km";
        pintarFichas();
        pintarCercanos();
        const ct = $("#cercanos-titulo");
        if (ct) ct.textContent = t("ordenados").replace("{m}", o.label || t("casa"));
        document.dispatchEvent(new CustomEvent("km0:fichas"));
      }
    });
    if (radar) radar.setEtiquetas(t("anillos"), t("casa"));

    if (sel) sel.addEventListener("change", () => {
      if (!sel.value) return;
      const [la, lo] = sel.value.split(",").map(Number);
      radar.setOrigen(la, lo, sel.options[sel.selectedIndex].text.split(" / ")[0]);
    });

    const geo = $("#origen-geo");
    if (geo) geo.addEventListener("click", () => {
      if (!navigator.geolocation) { toast(t("ubic")); return; }
      toast(t("loc"));
      navigator.geolocation.getCurrentPosition(
        p => radar.setOrigen(p.coords.latitude, p.coords.longitude, t("aqui")),
        () => toast(t("ubic")), { timeout: 8000 }
      );
    });

    $$(".lang button").forEach(b => b.addEventListener("click", () => {
      LANG = b.dataset.lang;
      try { localStorage.setItem("km0v4-lang", LANG); } catch (e) {}
      aplicarIdioma();
      document.dispatchEvent(new CustomEvent("km0:fichas"));
    }));

    const bur = $(".burger"), links = $(".nav-links");
    if (bur && links) {
      bur.addEventListener("click", () => {
        const o = links.classList.toggle("open");
        bur.setAttribute("aria-expanded", String(o));
      });
      links.addEventListener("click", e => {
        if (e.target.tagName === "A") { links.classList.remove("open"); bur.setAttribute("aria-expanded", "false"); }
      });
    }

    const nav = $(".nav");
    if (nav) {
      const onScroll = () => nav.classList.toggle("stuck", window.scrollY > 10);
      window.addEventListener("scroll", onScroll, { passive: true }); onScroll();
    }

    const cd = $("#cuenta");
    if (cd) {
      const fin = new Date(CFG.fechaInicio).getTime();
      const tick = () => {
        const d = Math.max(0, fin - Date.now());
        const dd = Math.floor(d / 864e5), hh = Math.floor(d % 864e5 / 36e5);
        cd.textContent = LANG === "va" ? `${dd} dies i ${hh} h` : `${dd} días y ${hh} h`;
      };
      refrescarCuenta = tick;
      tick(); setInterval(tick, 30000);
    }

    pintarCercanos();

    montarMarquesinas();
    let mt;
    window.addEventListener("resize", () => { clearTimeout(mt); mt = setTimeout(montarMarquesinas, 200); });

    aplicarIdioma();
    $$("[data-year]").forEach(e => e.textContent = new Date().getFullYear());
  }

  // Va al final del <body>: el marcado ya existe. Arrancamos antes que
  // motion.js (módulo), que necesita las cifras ya calculadas.
  init();

  return { toast, get lang() { return LANG; } };
})();
