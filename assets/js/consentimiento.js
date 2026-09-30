/* ===========================================================================
   HOSBEC Km0 Week — CONSENTIMIENTO DE COOKIES
   ---------------------------------------------------------------------------
   Nada de medición se carga hasta que el visitante dice que sí. No es una
   formalidad: la analítica de terceros exige consentimiento previo, y hasta
   que lo hay aquí no se pide ni un archivo a Google.

   Cómo funciona:
     1. Se declaran los valores por defecto del «consent mode» de Google, todos
        denegados. Así, si algún día se cargara una etiqueta antes de tiempo,
        ya nace sin permiso.
     2. Si no hay una decisión guardada, sale el aviso.
     3. Solo al aceptar se inyecta Google Tag Manager. Si se rechaza, no se
        carga nada y se recuerda la respuesta para no volver a preguntar.

   La decisión se guarda en el propio navegador (localStorage), nunca se envía
   a ningún sitio, y se puede cambiar desde el enlace del pie o desde la
   página de cookies.

   El identificador de GTM sale de contenido/configuracion.json. Si se deja
   vacío, este archivo no hace absolutamente nada: ni aviso, ni medición.
   =========================================================================== */
(function () {
  "use strict";

  var CFG = (window.KM0 && window.KM0.CONFIG) || {};
  var GTM = (CFG.gtm || "").trim();
  var LLAVE = "km0-consentimiento";

  // --- los textos, en los dos idiomas ------------------------------------
  var T = {
    es: {
      titulo: "Queremos medir cómo va la campaña",
      texto: "Usaríamos Google Analytics para medir las visitas a la campaña. " +
             "Son cookies de terceros: sin tu permiso no se carga ninguna.",
      mas: "Más detalle",
      si: "Aceptar",
      no: "Rechazar",
      cambiar: "Cookies"
    },
    va: {
      titulo: "Volem mesurar com va la campanya",
      texto: "Faríem servir Google Analytics per a mesurar les visites a la campanya. " +
             "Són galetes de tercers: sense el teu permís no se'n carrega cap.",
      mas: "Més detall",
      si: "Acceptar",
      no: "Rebutjar",
      cambiar: "Galetes"
    }
  };

  function idioma() {
    // El selector de idioma escribe el código en <html lang>.
    return /^ca/.test(document.documentElement.lang || "") ? "va" : "es";
  }
  function t(k) { return (T[idioma()] || T.es)[k]; }

  // --- la decisión guardada ----------------------------------------------
  function leer() {
    try { return localStorage.getItem(LLAVE); } catch (e) { return null; }
  }
  function guardar(v) {
    try { localStorage.setItem(LLAVE, v); } catch (e) { /* modo privado */ }
  }

  // --- consent mode: todo denegado de salida ------------------------------
  window.dataLayer = window.dataLayer || [];
  function gtag() { window.dataLayer.push(arguments); }
  gtag("consent", "default", {
    ad_storage: "denied",
    ad_user_data: "denied",
    ad_personalization: "denied",
    analytics_storage: "denied",
    functionality_storage: "granted",   // el idioma, que es técnico
    personalization_storage: "denied",
    security_storage: "granted",
    wait_for_update: 500
  });

  // --- cargar GTM, solo cuando toca ---------------------------------------
  var cargado = false;
  function cargarGTM() {
    if (cargado || !GTM) return;
    cargado = true;
    gtag("consent", "update", {
      ad_storage: "granted",
      ad_user_data: "granted",
      ad_personalization: "granted",
      analytics_storage: "granted",
      personalization_storage: "granted"
    });
    window.dataLayer.push({ "gtm.start": new Date().getTime(), event: "gtm.js" });
    var s = document.createElement("script");
    s.async = true;
    s.src = "https://www.googletagmanager.com/gtm.js?id=" + encodeURIComponent(GTM);
    document.head.appendChild(s);
  }

  // --- el aviso ------------------------------------------------------------
  var caja = null;

  function cerrar() {
    if (!caja) return;
    caja.remove();
    caja = null;
    document.removeEventListener("keydown", escape);
  }

  function escape(e) {
    // Esc equivale a rechazar: no decidir nunca puede significar aceptar.
    if (e.key === "Escape") responder("no");
  }

  function responder(v) {
    guardar(v);
    cerrar();
    if (v === "si") cargarGTM();
  }

  function pintar() {
    if (caja) return;
    caja = document.createElement("div");
    caja.className = "consent";
    caja.setAttribute("role", "dialog");
    caja.setAttribute("aria-modal", "false");
    caja.setAttribute("aria-labelledby", "consent-tit");
    caja.innerHTML =
      '<div class="consent-bd">' +
        '<h2 id="consent-tit">' + t("titulo") + "</h2>" +
        "<p>" + t("texto") + " " +
          '<a href="cookies.html">' + t("mas") + "</a>.</p>" +
      "</div>" +
      '<div class="consent-bt">' +
        '<button type="button" class="btn btn-linea btn-sm" data-c="no">' + t("no") + "</button>" +
        '<button type="button" class="btn btn-mar btn-sm" data-c="si">' + t("si") + "</button>" +
      "</div>";
    document.body.appendChild(caja);
    caja.querySelectorAll("[data-c]").forEach(function (b) {
      b.addEventListener("click", function () { responder(b.dataset.c); });
    });
    document.addEventListener("keydown", escape);
    // El foco va a «Rechazar»: la opción que no compromete nada.
    var no = caja.querySelector('[data-c="no"]');
    if (no) setTimeout(function () { no.focus(); }, 60);
  }

  // --- volver a preguntar, desde el pie o desde la página de cookies -------
  function montarCambiar() {
    document.querySelectorAll("[data-consent]").forEach(function (el) {
      el.addEventListener("click", function (e) {
        e.preventDefault();
        try { localStorage.removeItem(LLAVE); } catch (err) {}
        pintar();
      });
    });
  }

  function arrancar() {
    montarCambiar();
    if (!GTM) return;              // sin identificador no hay nada que pedir
    var d = leer();
    if (d === "si") cargarGTM();
    else if (d !== "no") pintar();
  }

  if (document.readyState === "loading")
    document.addEventListener("DOMContentLoaded", arrancar);
  else arrancar();

  // Si se cambia de idioma con el aviso abierto, se repinta en el nuevo.
  document.addEventListener("km0:idioma", function () {
    if (caja) { cerrar(); pintar(); }
  });
})();
