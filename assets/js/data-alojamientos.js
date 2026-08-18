/* ===========================================================================
   HOSBEC Km0 Week — BASE DE DATOS DE ALOJAMIENTOS
   ---------------------------------------------------------------------------
   ESTE ES EL ÚNICO ARCHIVO QUE TIENES QUE TOCAR PARA AÑADIR ALOJAMIENTOS.

   Para añadir uno nuevo: copia el bloque de ejemplo de abajo, pégalo dentro
   de la lista ALOJAMIENTOS (entre los corchetes [ ]) y cambia los datos.
   Ojo con las comas: cada bloque termina en "},".

   ---------------------------------------------------------------------------
   CAMPOS
   ---------------------------------------------------------------------------
   id            Identificador único, sin espacios ni acentos. Ej: "hotel-marena"
   nombre        Nombre comercial del alojamiento.
   tipo          Uno de: hotel | apartamentos | camping | rural | hostal | balneario
   categoria     Número de estrellas/llaves (1-5). Usa 0 si no aplica.
   destino       Municipio. Ej: "Benidorm"
   provincia     Alicante | València | Castelló
   coords        [latitud, longitud]. Se sacan de Google Maps: clic derecho
                 sobre el hotel → aparecen los dos números → cópialos aquí.
   web           URL COMPLETA a la que quieres enviar al usuario (su web,
                 su motor de reservas, una landing concreta...). Con https://
   telefono      Teléfono de contacto (opcional, deja "" si no lo quieres).
   imagen        Ruta o URL de la foto de la ficha. Ahora apunta a la
                 ilustración de relleno assets/img/foto/alo-<id>.webp; cámbiala
                 por la foto real cuando la tengas (1200x800 px, .webp o .jpg).
                 Si lo dejas en "", la web dibuja una portada ilustrada sola.
   claim         Frase corta de gancho (una línea). {es: "...", va: "..."}
   descripcion   2-3 frases. {es: "...", va: "..."}
   oferta        La propuesta Km0:
                   titulo        Nombre de la oferta. {es, va}
                   incluye       Lista de lo que entra. {es: [...], va: [...]}
                   precioDesde   Precio final en € (número). 0 = "consultar"
                   precioOriginal Precio habitual en € (número). 0 = no mostrar
                   unidad        "por noche", "por persona"... {es, va}
                   dto           % de descuento (número). 0 = no mostrar etiqueta
                   condiciones   Letra pequeña. {es, va}
   experiencias  Etiquetas temáticas. Valores admitidos:
                 gastronomia | bienestar | familia | cultura | mar | deporte
                 | romantico | mascotas | accesible | sostenible | noche
   servicios     Iconos de servicios. Valores admitidos:
                 piscina | spa | parking | wifi | restaurante | gimnasio
                 | playa | mascotas | accesible | familiar | vistas | terraza
   destacado     true / false → aparece en portada y con marco dorado
   nuevo         true / false → etiqueta "Nuevo"
   cupo          Nº de habitaciones o plazas comprometidas para residentes
                 (número). Se suma para el indicador "plazas para vecinos".
   plazas        Texto libre sobre disponibilidad (opcional). {es, va}
   =========================================================================== */

/* ---------------------------------------------------------------------------
   BLOQUE DE EJEMPLO PARA COPIAR Y PEGAR (quita las barras de comentario)
-----------------------------------------------------------------------------
  {
    id: "mi-hotel",
    nombre: "Nombre del Hotel",
    tipo: "hotel",
    categoria: 4,
    destino: "Benidorm",
    provincia: "Alicante",
    coords: [38.5342, -0.1314],
    web: "https://www.mihotel.com",
    telefono: "965 00 00 00",
    imagen: "",
    claim: { es: "Frase de gancho.", va: "Frase de ganxo." },
    descripcion: { es: "Descripción breve.", va: "Descripció breu." },
    oferta: {
      titulo: { es: "Nombre de la oferta", va: "Nom de l'oferta" },
      incluye: {
        es: ["Cosa 1", "Cosa 2", "Cosa 3"],
        va: ["Cosa 1", "Cosa 2", "Cosa 3"]
      },
      precioDesde: 89, precioOriginal: 130,
      unidad: { es: "por noche / hab. doble", va: "per nit / hab. doble" },
      dto: 30,
      condiciones: { es: "Condiciones.", va: "Condicions." }
    },
    experiencias: ["gastronomia", "bienestar"],
    servicios: ["piscina", "spa", "parking"],
    destacado: false,
    nuevo: true,
    cupo: 20,
    plazas: { es: "20 habitaciones", va: "20 habitacions" }
  },
--------------------------------------------------------------------------- */

const ALOJAMIENTOS = [

  {
    id: "gran-hotel-mirador-poniente",
    nombre: "Gran Hotel Mirador de Poniente",
    tipo: "hotel", categoria: 4,
    destino: "Benidorm", provincia: "Alicante",
    coords: [38.5342, -0.1314],
    web: "https://hosbec.com", telefono: "965 00 01 01", imagen: "assets/img/foto/alo-gran-hotel-mirador-poniente.webp",
    claim: { es: "El skyline que ves desde la autovía, ahora desde dentro.", va: "L'skyline que veus des de l'autovia, ara des de dins." },
    descripcion: {
      es: "Un clásico de Poniente reformado en 2024, con terraza panorámica sobre la bahía y una carta que reivindica el arroz de la comarca.",
      va: "Un clàssic de Ponent reformat en 2024, amb terrassa panoràmica sobre la badia i una carta que reivindica l'arròs de la comarca."
    },
    oferta: {
      titulo: { es: "Noche de vecino + cena en la terraza 20", va: "Nit de veí + sopar a la terrassa 20" },
      incluye: {
        es: ["Habitación superior con vistas al mar", "Cena degustación para dos en la planta 20", "Check-out tardío hasta las 16 h", "Acceso libre a la piscina panorámica"],
        va: ["Habitació superior amb vistes al mar", "Sopar degustació per a dos a la planta 20", "Check-out tardà fins a les 16 h", "Accés lliure a la piscina panoràmica"]
      },
      precioDesde: 96, precioOriginal: 168,
      unidad: { es: "por noche / hab. doble", va: "per nit / hab. doble" },
      dto: 43,
      condiciones: { es: "Válido del 13 al 29 de noviembre. Plazas limitadas. Acreditar residencia en la Comunitat Valenciana.", va: "Vàlid del 13 al 29 de novembre. Places limitades. Acreditar residència a la Comunitat Valenciana." }
    },
    experiencias: ["gastronomia", "mar", "romantico"],
    servicios: ["piscina", "restaurante", "parking", "vistas", "terraza", "wifi"],
    destacado: true, nuevo: false,
    cupo: 35,
    plazas: { es: "35 habitaciones en oferta", va: "35 habitacions en oferta" }
  },

  {
    id: "sercotel-almadraba-suites",
    nombre: "Almadraba Suites & Rooftop",
    tipo: "hotel", categoria: 4,
    destino: "Alicante", provincia: "Alicante",
    coords: [38.3452, -0.4810],
    web: "https://hosbec.com", telefono: "965 00 01 02", imagen: "assets/img/foto/alo-sercotel-almadraba-suites.webp",
    claim: { es: "Dormir a diez minutos de casa y despertar en otra ciudad.", va: "Dormir a deu minuts de casa i despertar en una altra ciutat." },
    descripcion: {
      es: "En pleno casco antiguo, a los pies del Benacantil. Azoteas, tapeo del barrio y una ruta guiada por el Alicante que los alicantinos ya no miran.",
      va: "En ple casc antic, als peus del Benacantil. Terrats, tapeig del barri i una ruta guiada per l'Alacant que els alacantins ja no miren."
    },
    oferta: {
      titulo: { es: "Turista en tu ciudad: 24 h de Alicante", va: "Turista a la teua ciutat: 24 h d'Alacant" },
      incluye: {
        es: ["Suite con terraza privada", "Ruta guiada Santa Bárbara al atardecer", "Vermut de bienvenida en el rooftop", "Desayuno de mercado"],
        va: ["Suite amb terrassa privada", "Ruta guiada Santa Bàrbara al capvespre", "Vermut de benvinguda al rooftop", "Esmorzar de mercat"]
      },
      precioDesde: 109, precioOriginal: 179,
      unidad: { es: "por noche / hab. doble", va: "per nit / hab. doble" },
      dto: 39,
      condiciones: { es: "Ruta sujeta a mínimo de 4 personas. Reserva directa.", va: "Ruta subjecta a mínim de 4 persones. Reserva directa." }
    },
    experiencias: ["cultura", "gastronomia", "noche"],
    servicios: ["terraza", "restaurante", "wifi", "vistas"],
    destacado: true, nuevo: false,
    cupo: 18,
    plazas: { es: "18 suites", va: "18 suites" }
  },

  {
    id: "balneario-serra-gelada",
    nombre: "Balneario Serra Gelada",
    tipo: "balneario", categoria: 5,
    destino: "Villajoyosa", provincia: "Alicante",
    coords: [38.5069, -0.2331],
    web: "https://hosbec.com", telefono: "965 00 01 03", imagen: "assets/img/foto/alo-balneario-serra-gelada.webp",
    claim: { es: "Cinco horas de silencio a veinte kilómetros de tu oficina.", va: "Cinc hores de silenci a vint quilòmetres de la teua oficina." },
    descripcion: {
      es: "Circuito termal frente al Mediterráneo, con agua de mar climatizada y un ritual de chocolate de la Vila que solo se hace en noviembre.",
      va: "Circuit termal davant del Mediterrani, amb aigua de mar climatitzada i un ritual de xocolate de la Vila que només es fa al novembre."
    },
    oferta: {
      titulo: { es: "Ritual Km0: mar, sal y chocolate", va: "Ritual Km0: mar, sal i xocolate" },
      incluye: {
        es: ["Circuito termal de 2 horas", "Masaje de 50 min con cacao de la Vila", "Almuerzo saludable", "Uso de albornoz y toalla"],
        va: ["Circuit termal de 2 hores", "Massatge de 50 min amb cacau de la Vila", "Dinar saludable", "Ús de barnús i tovallola"]
      },
      precioDesde: 65, precioOriginal: 120,
      unidad: { es: "por persona / sin alojamiento", va: "per persona / sense allotjament" },
      dto: 46,
      condiciones: { es: "Solo mayores de 16 años. Cita previa obligatoria.", va: "Només majors de 16 anys. Cita prèvia obligatòria." }
    },
    experiencias: ["bienestar", "gastronomia", "mar"],
    servicios: ["spa", "piscina", "restaurante", "parking", "accesible"],
    destacado: true, nuevo: true,
    cupo: 40,
    plazas: { es: "40 plazas por día", va: "40 places per dia" }
  },

  {
    id: "hotel-penyal-ifach",
    nombre: "Hotel Penyal d'Ifac",
    tipo: "hotel", categoria: 4,
    destino: "Calpe", provincia: "Alicante",
    coords: [38.6446, 0.0447],
    web: "https://hosbec.com", telefono: "965 00 01 04", imagen: "assets/img/foto/alo-hotel-penyal-ifach.webp",
    claim: { es: "Amanecer con el Peñón en la ventana. Sin hacer maleta.", va: "Amanéixer amb el Penyal a la finestra. Sense fer maleta." },
    descripcion: {
      es: "A pie de las salinas y del casco antiguo. Programa de observación de flamencos al amanecer con un biólogo del parque natural.",
      va: "A peu de les salines i del casc antic. Programa d'observació de flamencs a l'alba amb un biòleg del parc natural."
    },
    oferta: {
      titulo: { es: "Flamencos al amanecer", va: "Flamencs a l'alba" },
      incluye: {
        es: ["Habitación con vistas al Peñón", "Salida ornitológica guiada en las salinas", "Desayuno temprano de campo", "Préstamo de prismáticos"],
        va: ["Habitació amb vistes al Penyal", "Eixida ornitològica guiada a les salines", "Esmorzar matiner de camp", "Préstec de prismàtics"]
      },
      precioDesde: 84, precioOriginal: 139,
      unidad: { es: "por noche / hab. doble", va: "per nit / hab. doble" },
      dto: 40,
      condiciones: { es: "Salida sujeta a meteorología. Grupos de máx. 12 personas.", va: "Eixida subjecta a meteorologia. Grups de màx. 12 persones." }
    },
    experiencias: ["mar", "sostenible", "familia"],
    servicios: ["piscina", "playa", "parking", "restaurante", "vistas"],
    destacado: false, nuevo: false,
    cupo: 24,
    plazas: { es: "24 habitaciones", va: "24 habitacions" }
  },

  {
    id: "apartamentos-marina-alta",
    nombre: "Apartamentos Marina Alta",
    tipo: "apartamentos", categoria: 3,
    destino: "Dénia", provincia: "Alicante",
    coords: [38.8408, 0.1057],
    web: "https://hosbec.com", telefono: "965 00 01 05", imagen: "assets/img/foto/alo-apartamentos-marina-alta.webp",
    claim: { es: "Cocina propia y la lonja a cinco minutos.", va: "Cuina pròpia i la llotja a cinc minuts." },
    descripcion: {
      es: "Apartamentos junto al puerto en la Ciudad Creativa de la Gastronomía UNESCO. Incluye visita a la subasta de pescado y clase de arroz a banda.",
      va: "Apartaments vora el port a la Ciutat Creativa de la Gastronomia UNESCO. Inclou visita a la subhasta de peix i classe d'arròs a banda."
    },
    oferta: {
      titulo: { es: "De la lonja a tu fuego", va: "De la llotja al teu foc" },
      incluye: {
        es: ["Apartamento de 2 dormitorios", "Visita guiada a la lonja de Dénia", "Taller de arroz a banda con cocinero local", "Cesta de producto de temporada"],
        va: ["Apartament de 2 dormitoris", "Visita guiada a la llotja de Dénia", "Taller d'arròs a banda amb cuiner local", "Cistella de producte de temporada"]
      },
      precioDesde: 79, precioOriginal: 125,
      unidad: { es: "por noche / hasta 4 personas", va: "per nit / fins a 4 persones" },
      dto: 37,
      condiciones: { es: "Lonja abierta de martes a viernes. Estancia mínima 2 noches.", va: "Llotja oberta de dimarts a divendres. Estada mínima 2 nits." }
    },
    experiencias: ["gastronomia", "familia", "mar"],
    servicios: ["parking", "wifi", "playa", "terraza", "familiar"],
    destacado: false, nuevo: true,
    cupo: 12,
    plazas: { es: "12 apartamentos", va: "12 apartaments" }
  },

  {
    id: "casa-altea-la-vella",
    nombre: "Casa Altea la Vella",
    tipo: "rural", categoria: 3,
    destino: "Altea", provincia: "Alicante",
    coords: [38.5990, -0.0518],
    web: "https://hosbec.com", telefono: "965 00 01 06", imagen: "assets/img/foto/alo-casa-altea-la-vella.webp",
    claim: { es: "Una casa de pueblo con el mar al fondo y nadie alrededor.", va: "Una casa de poble amb el mar al fons i ningú al voltant." },
    descripcion: {
      es: "Seis habitaciones en una finca de bancales recuperada, con horno de leña, huerto y taller de cerámica con artesanos de Altea.",
      va: "Sis habitacions en una finca de bancals recuperada, amb forn de llenya, hort i taller de ceràmica amb artesans d'Altea."
    },
    oferta: {
      titulo: { es: "Manos en el barro", va: "Mans al fang" },
      incluye: {
        es: ["Habitación doble con desayuno de huerto", "Taller de cerámica de 3 horas", "Pieza propia cocida y enviada a casa", "Cena de horno de leña"],
        va: ["Habitació doble amb esmorzar d'hort", "Taller de ceràmica de 3 hores", "Peça pròpia cuita i enviada a casa", "Sopar de forn de llenya"]
      },
      precioDesde: 92, precioOriginal: 145,
      unidad: { es: "por noche / hab. doble", va: "per nit / hab. doble" },
      dto: 36,
      condiciones: { es: "Envío de la pieza a domicilio incluido en la Comunitat.", va: "Enviament de la peça a domicili inclòs a la Comunitat." }
    },
    experiencias: ["cultura", "sostenible", "romantico", "gastronomia"],
    servicios: ["piscina", "parking", "restaurante", "vistas", "mascotas"],
    destacado: false, nuevo: false,
    cupo: 6,
    plazas: { es: "6 habitaciones", va: "6 habitacions" }
  },

  {
    id: "hotel-palmeral-elx",
    nombre: "Hotel Palmeral d'Elx",
    tipo: "hotel", categoria: 4,
    destino: "Elche", provincia: "Alicante",
    coords: [38.2669, -0.6983],
    web: "https://hosbec.com", telefono: "965 00 01 07", imagen: "assets/img/foto/alo-hotel-palmeral-elx.webp",
    claim: { es: "Dormir dentro de un Patrimonio de la Humanidad.", va: "Dormir dins d'un Patrimoni de la Humanitat." },
    descripcion: {
      es: "Rodeado de palmeras datileras, con visita nocturna al huerto histórico y demostración de trenzado de palma blanca.",
      va: "Envoltat de palmeres datileres, amb visita nocturna a l'hort històric i demostració de trenat de palma blanca."
    },
    oferta: {
      titulo: { es: "Noche en el palmeral", va: "Nit al palmerar" },
      incluye: {
        es: ["Habitación con balcón al huerto", "Visita nocturna guiada al Palmeral", "Demostración de palma blanca", "Desayuno con dátiles de Elche"],
        va: ["Habitació amb balcó a l'hort", "Visita nocturna guiada al Palmerar", "Demostració de palma blanca", "Esmorzar amb dàtils d'Elx"]
      },
      precioDesde: 72, precioOriginal: 115,
      unidad: { es: "por noche / hab. doble", va: "per nit / hab. doble" },
      dto: 37,
      condiciones: { es: "Visita nocturna los días 14, 16 y 18 de noviembre.", va: "Visita nocturna els dies 14, 16 i 18 de novembre." }
    },
    experiencias: ["cultura", "familia", "sostenible"],
    servicios: ["piscina", "parking", "restaurante", "wifi", "accesible"],
    destacado: false, nuevo: false,
    cupo: 30,
    plazas: { es: "30 habitaciones", va: "30 habitacions" }
  },

  {
    id: "camping-dunas-guardamar",
    nombre: "Camping Dunas de Guardamar",
    tipo: "camping", categoria: 3,
    destino: "Guardamar del Segura", provincia: "Alicante",
    coords: [38.0894, -0.6537],
    web: "https://hosbec.com", telefono: "965 00 01 08", imagen: "assets/img/foto/alo-camping-dunas-guardamar.webp",
    claim: { es: "El pinar más grande de la costa, para ti solo en noviembre.", va: "La pineda més gran de la costa, per a tu a soles al novembre." },
    descripcion: {
      es: "Bungalows entre pinos plantados hace un siglo para frenar las dunas. Rutas de bici, observación de estrellas y fogata de otoño.",
      va: "Bungalows entre pins plantats fa un segle per a frenar les dunes. Rutes de bici, observació d'estreles i foguera de tardor."
    },
    oferta: {
      titulo: { es: "Bungalow bajo las estrellas", va: "Bungalow sota les estreles" },
      incluye: {
        es: ["Bungalow para 4 personas", "Alquiler de 2 bicicletas 24 h", "Sesión de astronomía guiada", "Fogata con torrà de otoño"],
        va: ["Bungalow per a 4 persones", "Lloguer de 2 bicicletes 24 h", "Sessió d'astronomia guiada", "Foguera amb torrà de tardor"]
      },
      precioDesde: 58, precioOriginal: 92,
      unidad: { es: "por noche / bungalow 4 pax", va: "per nit / bungalow 4 pax" },
      dto: 37,
      condiciones: { es: "Sesión de astronomía sujeta a cielo despejado.", va: "Sessió d'astronomia subjecta a cel clar." }
    },
    experiencias: ["familia", "deporte", "sostenible", "mascotas"],
    servicios: ["piscina", "playa", "parking", "mascotas", "familiar"],
    destacado: false, nuevo: false,
    cupo: 20,
    plazas: { es: "20 bungalows", va: "20 bungalows" }
  },

  {
    id: "hotel-cap-de-la-nau",
    nombre: "Hotel Cap de la Nau",
    tipo: "hotel", categoria: 4,
    destino: "Xàbia", provincia: "Alicante",
    coords: [38.7891, 0.1663],
    web: "https://hosbec.com", telefono: "965 00 01 09", imagen: "assets/img/foto/alo-hotel-cap-de-la-nau.webp",
    claim: { es: "Acantilados, calas vacías y una carretera que no lleva a ninguna parte.", va: "Penya-segats, cales buides i una carretera que no porta a cap lloc." },
    descripcion: {
      es: "Sobre las calas del Cap de la Nau. En noviembre el agua sigue a 20 grados y las calas están vacías: snorkel guiado incluido.",
      va: "Damunt les cales del Cap de la Nau. Al novembre l'aigua continua a 20 graus i les cales estan buides: snorkel guiat inclòs."
    },
    oferta: {
      titulo: { es: "Última calas del año", va: "Últimes cales de l'any" },
      incluye: {
        es: ["Habitación con vistas al acantilado", "Snorkel guiado en cala Ambolo", "Pícnic de mediodía con producto local", "Neopreno y material incluidos"],
        va: ["Habitació amb vistes al penya-segat", "Snorkel guiat a cala Ambolo", "Pícnic de migdia amb producte local", "Neoprè i material inclosos"]
      },
      precioDesde: 98, precioOriginal: 165,
      unidad: { es: "por noche / hab. doble", va: "per nit / hab. doble" },
      dto: 41,
      condiciones: { es: "Actividad sujeta a estado de la mar. Saber nadar.", va: "Activitat subjecta a estat de la mar. Saber nadar." }
    },
    experiencias: ["mar", "deporte", "romantico"],
    servicios: ["piscina", "vistas", "restaurante", "parking", "terraza"],
    destacado: false, nuevo: true,
    cupo: 22,
    plazas: { es: "22 habitaciones", va: "22 habitacions" }
  },

  {
    id: "hotel-salinas-torrevieja",
    nombre: "Hotel Salinas de Torrevieja",
    tipo: "hotel", categoria: 3,
    destino: "Torrevieja", provincia: "Alicante",
    coords: [37.9787, -0.6822],
    web: "https://hosbec.com", telefono: "965 00 01 10", imagen: "assets/img/foto/alo-hotel-salinas-torrevieja.webp",
    claim: { es: "La laguna rosa a diez minutos andando.", va: "La llacuna rosa a deu minuts caminant." },
    descripcion: {
      es: "Frente al parque natural de La Mata. Baños flotantes en la laguna salada, spa marino y habanera en directo el sábado.",
      va: "Davant del parc natural de La Mata. Banys flotants a la llacuna salada, spa marí i havanera en directe el dissabte."
    },
    oferta: {
      titulo: { es: "Flotar en rosa", va: "Flotar en rosa" },
      incluye: {
        es: ["Habitación doble con desayuno", "Baño guiado en la laguna rosa", "Circuito de agua salada en el spa", "Concierto de habaneras"],
        va: ["Habitació doble amb esmorzar", "Bany guiat a la llacuna rosa", "Circuit d'aigua salada a l'spa", "Concert d'havaneres"]
      },
      precioDesde: 62, precioOriginal: 99,
      unidad: { es: "por noche / hab. doble", va: "per nit / hab. doble" },
      dto: 37,
      condiciones: { es: "Baño en laguna sujeto a normativa del parque natural.", va: "Bany a la llacuna subjecte a normativa del parc natural." }
    },
    experiencias: ["bienestar", "cultura", "mar", "accesible"],
    servicios: ["spa", "piscina", "restaurante", "accesible", "parking"],
    destacado: false, nuevo: false,
    cupo: 45,
    plazas: { es: "45 habitaciones", va: "45 habitacions" }
  },

  {
    id: "hotel-platja-gandia",
    nombre: "Hotel Platja de Gandia",
    tipo: "hotel", categoria: 4,
    destino: "Gandia", provincia: "València",
    coords: [39.0033, -0.1615],
    web: "https://hosbec.com", telefono: "962 00 01 11", imagen: "assets/img/foto/alo-hotel-platja-gandia.webp",
    claim: { es: "La playa de tu infancia, sin sombrillas.", va: "La platja de la teua infància, sense para-sols." },
    descripcion: {
      es: "Primera línea en la playa nord. Noviembre es la mejor época: paseos de 3 km sin nadie y fideuà en el puerto pesquero.",
      va: "Primera línia a la platja nord. Novembre és la millor època: passejos de 3 km sense ningú i fideuà al port pesquer."
    },
    oferta: {
      titulo: { es: "Playa vacía + fideuà de puerto", va: "Platja buida + fideuà de port" },
      incluye: {
        es: ["Habitación frente al mar", "Fideuà para dos en el Grau", "Alquiler de bicicletas 24 h", "Acceso al spa del hotel"],
        va: ["Habitació davant del mar", "Fideuà per a dos al Grau", "Lloguer de bicicletes 24 h", "Accés a l'spa de l'hotel"]
      },
      precioDesde: 74, precioOriginal: 128,
      unidad: { es: "por noche / hab. doble", va: "per nit / hab. doble" },
      dto: 42,
      condiciones: { es: "Spa cerrado los lunes por mantenimiento.", va: "Spa tancat els dilluns per manteniment." }
    },
    experiencias: ["mar", "gastronomia", "familia", "bienestar"],
    servicios: ["spa", "piscina", "playa", "restaurante", "parking", "vistas"],
    destacado: true, nuevo: false,
    cupo: 60,
    plazas: { es: "60 habitaciones", va: "60 habitacions" }
  },

  {
    id: "hotel-ciutat-vella-valencia",
    nombre: "Hotel Ciutat Vella",
    tipo: "hotel", categoria: 4,
    destino: "València", provincia: "València",
    coords: [39.4750, -0.3760],
    web: "https://hosbec.com", telefono: "963 00 01 12", imagen: "assets/img/foto/alo-hotel-ciutat-vella-valencia.webp",
    claim: { es: "Vivir en València no es lo mismo que quedarte a dormir en ella.", va: "Viure a València no és el mateix que quedar-te a dormir-hi." },
    descripcion: {
      es: "Palacete del XIX entre la Lonja y el Mercat Central. Desayuno de mercado, ruta modernista y acceso a la azotea al atardecer.",
      va: "Palauet del XIX entre la Llotja i el Mercat Central. Esmorzar de mercat, ruta modernista i accés al terrat al capvespre."
    },
    oferta: {
      titulo: { es: "Noche modernista", va: "Nit modernista" },
      incluye: {
        es: ["Habitación en el palacete", "Ruta modernista guiada de 2 h", "Desayuno en el Mercat Central", "Copa en la azotea al atardecer"],
        va: ["Habitació al palauet", "Ruta modernista guiada de 2 h", "Esmorzar al Mercat Central", "Copa al terrat al capvespre"]
      },
      precioDesde: 118, precioOriginal: 195,
      unidad: { es: "por noche / hab. doble", va: "per nit / hab. doble" },
      dto: 39,
      condiciones: { es: "Ruta en castellano y valenciano. Aforo limitado.", va: "Ruta en castellà i valencià. Aforament limitat." }
    },
    experiencias: ["cultura", "gastronomia", "noche", "romantico"],
    servicios: ["terraza", "restaurante", "wifi", "vistas", "accesible"],
    destacado: true, nuevo: false,
    cupo: 16,
    plazas: { es: "16 habitaciones", va: "16 habitacions" }
  },

  {
    id: "apartamentos-far-de-cullera",
    nombre: "Apartamentos Far de Cullera",
    tipo: "apartamentos", categoria: 3,
    destino: "Cullera", provincia: "València",
    coords: [39.1646, -0.2519],
    web: "https://hosbec.com", telefono: "962 00 01 13", imagen: "assets/img/foto/alo-apartamentos-far-de-cullera.webp",
    claim: { es: "Donde el Xúquer se rinde al mar.", va: "On el Xúquer es rendeix a la mar." },
    descripcion: {
      es: "Al pie del castillo y del faro. Incluye paseo en barca por la desembocadura del Xúquer y cata de arroces de la Ribera.",
      va: "Al peu del castell i del far. Inclou passeig en barca per la desembocadura del Xúquer i tast d'arrossos de la Ribera."
    },
    oferta: {
      titulo: { es: "Río, arroz y faro", va: "Riu, arròs i far" },
      incluye: {
        es: ["Apartamento con terraza al mar", "Paseo en barca por el Xúquer", "Cata de tres arroces de la Ribera", "Entrada al Castillo de Cullera"],
        va: ["Apartament amb terrassa a la mar", "Passeig en barca pel Xúquer", "Tast de tres arrossos de la Ribera", "Entrada al Castell de Cullera"]
      },
      precioDesde: 68, precioOriginal: 110,
      unidad: { es: "por noche / hasta 4 personas", va: "per nit / fins a 4 persones" },
      dto: 38,
      condiciones: { es: "Barca sujeta a nivel del río. Mínimo 2 noches.", va: "Barca subjecta a nivell del riu. Mínim 2 nits." }
    },
    experiencias: ["gastronomia", "familia", "mar", "cultura"],
    servicios: ["piscina", "playa", "parking", "terraza", "familiar"],
    destacado: false, nuevo: false,
    cupo: 14,
    plazas: { es: "14 apartamentos", va: "14 apartaments" }
  },

  {
    id: "hotel-marjal-oliva",
    nombre: "Hotel Marjal d'Oliva",
    tipo: "hotel", categoria: 4,
    destino: "Oliva", provincia: "València",
    coords: [38.9187, -0.1188],
    web: "https://hosbec.com", telefono: "962 00 01 14", imagen: "assets/img/foto/alo-hotel-marjal-oliva.webp",
    claim: { es: "Doce kilómetros de arena y un humedal lleno de pájaros.", va: "Dotze quilòmetres d'arena i un aiguamoll ple d'ocells." },
    descripcion: {
      es: "Entre el marjal y la playa virgen de Oliva. Kayak por los canales del humedal y menú de temporada con producto de la Safor.",
      va: "Entre el marjal i la platja verge d'Oliva. Caiac pels canals de l'aiguamoll i menú de temporada amb producte de la Safor."
    },
    oferta: {
      titulo: { es: "Kayak entre cañas", va: "Caiac entre canyes" },
      incluye: {
        es: ["Habitación doble con media pensión", "Ruta en kayak por el marjal", "Guía naturalista", "Merienda de horchata y fartons"],
        va: ["Habitació doble amb mitja pensió", "Ruta en caiac pel marjal", "Guia naturalista", "Berenar d'orxata i fartons"]
      },
      precioDesde: 88, precioOriginal: 142,
      unidad: { es: "por noche / hab. doble", va: "per nit / hab. doble" },
      dto: 38,
      condiciones: { es: "Kayak para mayores de 12 años. Grupos de 8 personas.", va: "Caiac per a majors de 12 anys. Grups de 8 persones." }
    },
    experiencias: ["sostenible", "deporte", "familia", "gastronomia"],
    servicios: ["piscina", "playa", "restaurante", "parking", "mascotas"],
    destacado: false, nuevo: true,
    cupo: 28,
    plazas: { es: "28 habitaciones", va: "28 habitacions" }
  },

  {
    id: "bodega-hotel-utiel-requena",
    nombre: "Bodega Hotel Requena",
    tipo: "rural", categoria: 4,
    destino: "Requena", provincia: "València",
    coords: [39.4885, -1.1000],
    web: "https://hosbec.com", telefono: "962 00 01 15", imagen: "assets/img/foto/alo-bodega-hotel-utiel-requena.webp",
    claim: { es: "El interior también es costa. Solo que de viñedo.", va: "L'interior també és costa. Només que de vinya." },
    descripcion: {
      es: "Bodega familiar con habitaciones sobre las cuevas del siglo XV. Vendimia tardía, cata a ciegas y cena maridada en la sala de barricas.",
      va: "Celler familiar amb habitacions damunt de les coves del segle XV. Verema tardana, tast a cegues i sopar maridat a la sala de bótes."
    },
    oferta: {
      titulo: { es: "Dormir sobre las cuevas", va: "Dormir damunt de les coves" },
      incluye: {
        es: ["Habitación en la casa señorial", "Visita a las cuevas medievales", "Cata a ciegas de bobal", "Cena maridada en sala de barricas"],
        va: ["Habitació a la casa senyorial", "Visita a les coves medievals", "Tast a cegues de bobal", "Sopar maridat a sala de bótes"]
      },
      precioDesde: 105, precioOriginal: 175,
      unidad: { es: "por noche / hab. doble", va: "per nit / hab. doble" },
      dto: 40,
      condiciones: { es: "Solo mayores de edad para la cata. Transporte no incluido.", va: "Només majors d'edat per al tast. Transport no inclòs." }
    },
    experiencias: ["gastronomia", "cultura", "romantico", "sostenible"],
    servicios: ["restaurante", "parking", "vistas", "wifi", "terraza"],
    destacado: false, nuevo: false,
    cupo: 10,
    plazas: { es: "10 habitaciones", va: "10 habitacions" }
  },

  {
    id: "hotel-papa-luna-peniscola",
    nombre: "Hotel Papa Luna Peníscola",
    tipo: "hotel", categoria: 4,
    destino: "Peñíscola", provincia: "Castelló",
    coords: [40.3585, 0.4028],
    web: "https://hosbec.com", telefono: "964 00 01 16", imagen: "assets/img/foto/alo-hotel-papa-luna-peniscola.webp",
    claim: { es: "El castillo sin colas y la playa sin toallas.", va: "El castell sense cues i la platja sense tovalloles." },
    descripcion: {
      es: "A los pies de la ciudad amurallada. Visita teatralizada del castillo del Papa Luna en horario exclusivo para participantes de la Km0 Week.",
      va: "Als peus de la ciutat emmurallada. Visita teatralitzada del castell del Papa Luna en horari exclusiu per a participants de la Km0 Week."
    },
    oferta: {
      titulo: { es: "El Papa Luna, para ti solo", va: "El Papa Luna, per a tu a soles" },
      incluye: {
        es: ["Habitación con vistas al castillo", "Visita teatralizada en horario exclusivo", "Cena de suquet en el puerto", "Desayuno buffet"],
        va: ["Habitació amb vistes al castell", "Visita teatralitzada en horari exclusiu", "Sopar de suquet al port", "Esmorzar bufet"]
      },
      precioDesde: 79, precioOriginal: 135,
      unidad: { es: "por noche / hab. doble", va: "per nit / hab. doble" },
      dto: 41,
      condiciones: { es: "Visitas los días 15, 17 y 19 a las 19 h. Aforo 30 personas.", va: "Visites els dies 15, 17 i 19 a les 19 h. Aforament 30 persones." }
    },
    experiencias: ["cultura", "gastronomia", "familia", "mar"],
    servicios: ["piscina", "playa", "restaurante", "parking", "vistas", "accesible"],
    destacado: true, nuevo: false,
    cupo: 50,
    plazas: { es: "50 habitaciones", va: "50 habitacions" }
  },

  {
    id: "villa-benicassim",
    nombre: "Villa Benicàssim Rooms",
    tipo: "hotel", categoria: 3,
    destino: "Benicàssim", provincia: "Castelló",
    coords: [40.0546, 0.0653],
    web: "https://hosbec.com", telefono: "964 00 01 17", imagen: "assets/img/foto/alo-villa-benicassim.webp",
    claim: { es: "Las villas de los indianos, ahora con desayuno.", va: "Les vil·les dels indians, ara amb esmorzar." },
    descripcion: {
      es: "Villa modernista de la ruta de las Villas, restaurada. Vía Verde del Mar en bici hasta Oropesa y vermut en el paseo.",
      va: "Vil·la modernista de la ruta de les Vil·les, restaurada. Via Verda del Mar en bici fins a Orpesa i vermut al passeig."
    },
    oferta: {
      titulo: { es: "Vía Verde y vermut", va: "Via Verda i vermut" },
      incluye: {
        es: ["Habitación en villa modernista", "Bicis para recorrer la Vía Verde", "Vermut con encurtidos de la tierra", "Desayuno en el jardín"],
        va: ["Habitació en vil·la modernista", "Bicis per a recórrer la Via Verda", "Vermut amb encurtits de la terra", "Esmorzar al jardí"]
      },
      precioDesde: 66, precioOriginal: 105,
      unidad: { es: "por noche / hab. doble", va: "per nit / hab. doble" },
      dto: 37,
      condiciones: { es: "Bicis sujetas a disponibilidad. Casco incluido.", va: "Bicis subjectes a disponibilitat. Casc inclòs." }
    },
    experiencias: ["deporte", "cultura", "gastronomia", "mar"],
    servicios: ["piscina", "playa", "wifi", "terraza", "parking"],
    destacado: false, nuevo: false,
    cupo: 9,
    plazas: { es: "9 habitaciones", va: "9 habitacions" }
  },

  {
    id: "hostal-morella-muralla",
    nombre: "Hostal Muralla de Morella",
    tipo: "hostal", categoria: 2,
    destino: "Morella", provincia: "Castelló",
    coords: [40.6193, -0.1013],
    web: "https://hosbec.com", telefono: "964 00 01 18", imagen: "assets/img/foto/alo-hostal-morella-muralla.webp",
    claim: { es: "Niebla, piedra y un plato de olla a 1.000 metros.", va: "Boira, pedra i un plat d'olla a 1.000 metres." },
    descripcion: {
      es: "Dentro de la muralla, en una casa del siglo XVI. Ruta de las pinturas rupestres, manta morellana en la cama y olla de la abuela.",
      va: "Dins de la muralla, en una casa del segle XVI. Ruta de les pintures rupestres, manta morellana al llit i olla de l'àvia."
    },
    oferta: {
      titulo: { es: "Invierno en Els Ports", va: "Hivern als Ports" },
      incluye: {
        es: ["Habitación con manta morellana", "Ruta guiada de arte rupestre", "Cena de olla morellana", "Degustación de trufa negra"],
        va: ["Habitació amb manta morellana", "Ruta guiada d'art rupestre", "Sopar d'olla morellana", "Degustació de tòfona negra"]
      },
      precioDesde: 54, precioOriginal: 85,
      unidad: { es: "por noche / hab. doble", va: "per nit / hab. doble" },
      dto: 36,
      condiciones: { es: "Ruta con calzado de montaña. Mínimo 6 personas.", va: "Ruta amb calçat de muntanya. Mínim 6 persones." }
    },
    experiencias: ["cultura", "gastronomia", "sostenible"],
    servicios: ["restaurante", "wifi", "vistas", "parking"],
    destacado: false, nuevo: true,
    cupo: 8,
    plazas: { es: "8 habitaciones", va: "8 habitacions" }
  },

  {
    id: "resort-alcossebre-familias",
    nombre: "Alcossebre Family Resort",
    tipo: "apartamentos", categoria: 4,
    destino: "Alcossebre", provincia: "Castelló",
    coords: [40.2437, 0.2711],
    web: "https://hosbec.com", telefono: "964 00 01 19", imagen: "assets/img/foto/alo-resort-alcossebre-familias.webp",
    claim: { es: "Un fin de semana en el que los niños duermen agotados.", va: "Un cap de setmana en què els xiquets dormen esgotats." },
    descripcion: {
      es: "Apartamentos junto a la Sierra de Irta con programa infantil de naturaleza, piscina climatizada y taller de cocina para peques.",
      va: "Apartaments vora la Serra d'Irta amb programa infantil de natura, piscina climatitzada i taller de cuina per a menuts."
    },
    oferta: {
      titulo: { es: "Fin de semana de familia (de verdad)", va: "Cap de setmana de família (de veritat)" },
      incluye: {
        es: ["Apartamento familiar 2 dormitorios", "Programa infantil de naturaleza", "Taller de cocina para niños", "Piscina climatizada y club infantil"],
        va: ["Apartament familiar 2 dormitoris", "Programa infantil de natura", "Taller de cuina per a xiquets", "Piscina climatitzada i club infantil"]
      },
      precioDesde: 82, precioOriginal: 138,
      unidad: { es: "por noche / familia de 4", va: "per nit / família de 4" },
      dto: 41,
      condiciones: { es: "Programa infantil de 4 a 12 años. Sábados y domingos.", va: "Programa infantil de 4 a 12 anys. Dissabtes i diumenges." }
    },
    experiencias: ["familia", "deporte", "mar", "sostenible"],
    servicios: ["piscina", "playa", "familiar", "parking", "accesible", "restaurante"],
    destacado: false, nuevo: false,
    cupo: 25,
    plazas: { es: "25 apartamentos", va: "25 apartaments" }
  },

  {
    id: "hotel-grau-castello",
    nombre: "Hotel Grau de Castelló",
    tipo: "hotel", categoria: 3,
    destino: "Castelló de la Plana", provincia: "Castelló",
    coords: [39.9864, -0.0513],
    web: "https://hosbec.com", telefono: "964 00 01 20", imagen: "assets/img/foto/alo-hotel-grau-castello.webp",
    claim: { es: "El puerto, las Islas Columbretes y una tarde sin plan.", va: "El port, les Illes Columbretes i una vesprada sense pla." },
    descripcion: {
      es: "Junto al Planetario y al puerto pesquero. Incluye visita al Grau con marineros jubilados y clase de nudos marineros.",
      va: "Vora el Planetari i el port pesquer. Inclou visita al Grau amb mariners jubilats i classe de nusos mariners."
    },
    oferta: {
      titulo: { es: "El Grau contado por quien lo vivió", va: "El Grau contat per qui el va viure" },
      incluye: {
        es: ["Habitación doble con desayuno", "Paseo guiado por marineros del Grau", "Taller de nudos marineros", "Entrada al Planetario"],
        va: ["Habitació doble amb esmorzar", "Passeig guiat per mariners del Grau", "Taller de nusos mariners", "Entrada al Planetari"]
      },
      precioDesde: 59, precioOriginal: 95,
      unidad: { es: "por noche / hab. doble", va: "per nit / hab. doble" },
      dto: 38,
      condiciones: { es: "Paseo los sábados a las 11 h. Máximo 20 personas.", va: "Passeig els dissabtes a les 11 h. Màxim 20 persones." }
    },
    experiencias: ["cultura", "familia", "mar", "accesible"],
    servicios: ["restaurante", "wifi", "parking", "accesible", "playa"],
    destacado: false, nuevo: false,
    cupo: 32,
    plazas: { es: "32 habitaciones", va: "32 habitacions" }
  }

];

/* ===========================================================================
   AGENDA DE ACTIVIDADES ABIERTAS (opcional)
   Se muestra en la página Agenda. Mismo sistema: copia, pega y edita.
   dia: 1..17 (día 1 = 13 de noviembre; día 17 = 29 de noviembre)
   enlace: adónde va el botón «Quiero ir» → la web de quien organiza la
           actividad (el hotel, el ayuntamiento, la empresa). Si se deja
           vacío, se usa la web del alojamiento adherido de ese mismo
           destino y, en último caso, hosbec.com.
   Los fines de semana son los días 1-3, 8-10 y 15-17.
   =========================================================================== */
const AGENDA = [
  { dia: 1, hora: "12:00", lugar: "Benidorm", enlace: "https://hosbec.com", titulo: { es: "Acto inaugural en el Ayuntamiento", va: "Acte inaugural a l'Ajuntament" }, desc: { es: "Presentación oficial con hoteleros, ayuntamientos y Turisme CV. Entrada libre.", va: "Presentació oficial amb hotelers, ajuntaments i Turisme CV. Entrada lliure." }, tipo: "institucional", precio: { es: "Gratis", va: "Gratis" } },
  { dia: 1, hora: "19:30", lugar: "Alicante", enlace: "https://hosbec.com", titulo: { es: "Puertas abiertas: cocinas de hotel", va: "Portes obertes: cuines d'hotel" }, desc: { es: "Seis hoteles abren sus cocinas al público. Reserva previa.", va: "Sis hotels obrin les seues cuines al públic. Reserva prèvia." }, tipo: "gastronomia", precio: { es: "Gratis", va: "Gratis" } },
  { dia: 2, hora: "10:00", lugar: "Calpe", enlace: "https://hosbec.com", titulo: { es: "Flamencos al amanecer en las salinas", va: "Flamencs a l'alba a les salines" }, desc: { es: "Salida ornitológica guiada por biólogos del parque natural.", va: "Eixida ornitològica guiada per biòlegs del parc natural." }, tipo: "naturaleza", precio: { es: "12 €", va: "12 €" } },
  { dia: 2, hora: "18:00", lugar: "València", enlace: "https://hosbec.com", titulo: { es: "Ruta modernista de hoteles históricos", va: "Ruta modernista d'hotels històrics" }, desc: { es: "Tres palacetes convertidos en hotel, con acceso a zonas no visitables.", va: "Tres palauets convertits en hotel, amb accés a zones no visitables." }, tipo: "cultura", precio: { es: "8 €", va: "8 €" } },
  { dia: 3, hora: "11:00", lugar: "Dénia", enlace: "https://hosbec.com", titulo: { es: "Subasta de pescado + taller de arroz", va: "Subhasta de peix + taller d'arròs" }, desc: { es: "De la lonja al plato en tres horas, con cocineros de la Marina Alta.", va: "De la llotja al plat en tres hores, amb cuiners de la Marina Alta." }, tipo: "gastronomia", precio: { es: "25 €", va: "25 €" } },
  { dia: 3, hora: "20:00", lugar: "Peñíscola", enlace: "https://hosbec.com", titulo: { es: "Visita teatralizada al castillo", va: "Visita teatralitzada al castell" }, desc: { es: "Horario exclusivo Km0 Week, con el castillo cerrado al turismo general.", va: "Horari exclusiu Km0 Week, amb el castell tancat al turisme general." }, tipo: "cultura", precio: { es: "10 €", va: "10 €" } },
  { dia: 9, hora: "09:30", lugar: "Oliva", enlace: "https://hosbec.com", titulo: { es: "Kayak por el marjal", va: "Caiac pel marjal" }, desc: { es: "Ruta guiada de dos horas por los canales del humedal.", va: "Ruta guiada de dues hores pels canals de l'aiguamoll." }, tipo: "naturaleza", precio: { es: "18 €", va: "18 €" } },
  { dia: 6, hora: "17:00", lugar: "Benidorm", enlace: "https://hosbec.com", titulo: { es: "Mesa redonda: turismo y comunidad local", va: "Taula redona: turisme i comunitat local" }, desc: { es: "Hoteleros, vecinos y ayuntamientos debaten sobre convivencia. Abierto.", va: "Hotelers, veïns i ajuntaments debaten sobre convivència. Obert." }, tipo: "institucional", precio: { es: "Gratis", va: "Gratis" } },
  { dia: 10, hora: "10:30", lugar: "Elche", enlace: "https://hosbec.com", titulo: { es: "El Palmeral por dentro", va: "El Palmerar per dins" }, desc: { es: "Huertos históricos normalmente cerrados y demostración de palma blanca.", va: "Horts històrics normalment tancats i demostració de palma blanca." }, tipo: "cultura", precio: { es: "6 €", va: "6 €" } },
  { dia: 8, hora: "19:00", lugar: "Castelló de la Plana", enlace: "https://hosbec.com", titulo: { es: "El Grau contado por sus marineros", va: "El Grau contat pels seus mariners" }, desc: { es: "Paseo con marineros jubilados por el puerto pesquero.", va: "Passeig amb mariners jubilats pel port pesquer." }, tipo: "cultura", precio: { es: "Gratis", va: "Gratis" } },
  { dia: 16, hora: "11:00", lugar: "Altea", enlace: "https://hosbec.com", titulo: { es: "Taller de cerámica con artesanos", va: "Taller de ceràmica amb artesans" }, desc: { es: "Tres horas de torno y esmalte. Te llevas la pieza a casa.", va: "Tres hores de torn i esmalt. T'endús la peça a casa." }, tipo: "artesania", precio: { es: "30 €", va: "30 €" } },
  { dia: 9, hora: "21:00", lugar: "Torrevieja", enlace: "https://hosbec.com", titulo: { es: "Noche de habaneras en el hotel", va: "Nit d'havaneres a l'hotel" }, desc: { es: "Concierto abierto con coro local y cremaet.", va: "Concert obert amb cor local i cremaet." }, tipo: "musica", precio: { es: "Gratis", va: "Gratis" } },
  { dia: 17, hora: "12:00", lugar: "Gandia", enlace: "https://hosbec.com", titulo: { es: "Fideuà popular en el Grau", va: "Fideuà popular al Grau" }, desc: { es: "Cierre de la Km0 Week con fideuà para 400 personas. Inscripción previa.", va: "Tancament de la Km0 Week amb fideuà per a 400 persones. Inscripció prèvia." }, tipo: "gastronomia", precio: { es: "5 €", va: "5 €" } },
  { dia: 17, hora: "18:00", lugar: "Toda la Comunitat", enlace: "https://hosbec.com", titulo: { es: "Sorteo Pasaporte Km0", va: "Sorteig Passaport Km0" }, desc: { es: "Sorteo de 10 estancias entre quienes hayan completado el pasaporte.", va: "Sorteig de 10 estades entre qui haja completat el passaport." }, tipo: "institucional", precio: { es: "Gratis", va: "Gratis" } }
];

/* ===========================================================================
   CONFIGURACIÓN GENERAL DE LA EDICIÓN
   Cambia aquí las fechas y los contadores globales.
   =========================================================================== */
const CONFIG = {
  edicion: "2026",
  fechaInicio: "2026-11-13T00:00:00+01:00",
  fechaFin:    "2026-11-29T23:59:59+01:00",
  fechasTexto: { es: "13 – 29 de noviembre de 2026", va: "13 – 29 de novembre de 2026" },
  emailContacto: "km0week@hosbec.com",
  telefonoContacto: "965 85 55 16",
  webHosbec: "https://hosbec.com",
  // Cifras que se muestran en portada (edítalas cuando cambien)
  cifras: {
    alojamientos: 20,
    destinos: 17,
    experiencias: 14,
    dtoMedio: 39
  }
};

/* Exponer para los módulos de la web */
window.KM0 = { ALOJAMIENTOS, AGENDA, CONFIG };
