// Datos de las unidades Senna. Hoy viven aquí (dos unidades caben perfecto en
// estático). Cuando crezca, esto se mueve a Supabase sin tocar las páginas:
// basta reemplazar este import por un fetch a la API.

export type Unidad = {
  slug: string;
  numero: string;            // "I" / "II" — son dos productos discretos, no decoración
  nombre: string;
  ubicacion: string;
  distribucion: string;
  equipamiento: 'Full' | 'Semifull';
  estadiaMinima: string;
  // Precio como texto ya formateado: soporta UF y pesos sin lógica en las páginas.
  precio: { monto: string; nota: string };
  resumen: string;
  amenidades: string[];
  galeria: { src: string; alt: string }[];
  destacada: { src: string; alt: string };
};

// Imágenes de la Unidad I alojadas en el WordPress de Senna.
const W = 'https://aparthotelsenna.wordpress.com/wp-content/uploads/2017/06';

export const UNIDADES: Unidad[] = [
  {
    slug: 'barrio-del-tenis',
    numero: 'I',
    nombre: 'Senna · Barrio del Tenis',
    ubicacion: 'Barrio del Tenis, Centro de Rancagua',
    distribucion: '1 dormitorio · walk-in closet · baño privado',
    equipamiento: 'Full',
    estadiaMinima: 'Desde 1 mes',
    precio: { monto: '12 UF', nota: 'al mes · todo incluido' },
    resumen:
      'Departamento completamente amoblado para profesionales que exigen confort, ' +
      'privacidad y una ubicación privilegiada en el corazón de Rancagua. Solo 20 ' +
      'unidades: atención personalizada y un ambiente de exclusividad.',
    amenidades: [
      'Completamente amoblado', 'WiFi de alta velocidad', 'TV Cable',
      'Estacionamiento incluido', 'Aseo 2 veces por semana', 'Conserjería de apoyo',
      'Walk-in closet y caja de seguridad', 'Música ambiental en áreas comunes',
      'Alta privacidad — ideal para parejas',
    ],
    destacada: { src: `${W}/img_0065.jpg`, alt: 'Dormitorio luminoso amoblado' },
    galeria: [
      { src: `${W}/img_0064.jpg`, alt: 'Edificio Senna' },
      { src: `${W}/img_0066.jpg`, alt: 'Living completamente amoblado' },
      { src: `${W}/img_0070.jpg`, alt: 'Sala de estar en el piso' },
      { src: `${W}/img_0071.jpg`, alt: 'Cocina equipada' },
      { src: `${W}/img_0073.jpg`, alt: 'Walk-in closet y caja de seguridad' },
      { src: `${W}/img_0074.jpg`, alt: 'Baño privado amplio' },
    ],
  },
  {
    slug: 'requinoa',
    numero: 'II',
    nombre: 'Senna · Requínoa',
    ubicacion: 'Centro de Requínoa · calle Comercio 15',
    distribucion: 'Estudio 35 m² · 1 dormitorio · baño con closet · living-comedor',
    equipamiento: 'Semifull',
    estadiaMinima: 'Arriendo mensual',
    precio: { monto: '$280.000', nota: '+ $50.000 gastos comunes · al mes' },
    resumen:
      'Acogedor departamento tipo estudio de 35 m² en pleno centro de Requínoa, ' +
      'calle Comercio 15. Sector tranquilo, a pasos de Cesfam, colegios y ' +
      'municipalidad, con salida directa a la carretera y a solo 15 minutos de ' +
      'Rancagua. Cocina con muebles, baño con closet y living-comedor; terraza y ' +
      'lavandería comunes.',
    amenidades: [
      '1 dormitorio', 'Baño con closet', 'Cocina con muebles', 'Living-comedor',
      'Terraza común', 'Lavandería común', 'Estacionamiento cercano',
      'A pasos de Cesfam, colegios y municipalidad', 'A 15 minutos de Rancagua',
    ],
    // Fotos locales (set DeptoRequinoa). Llevan marca de agua AnichPro: reemplazar
    // por versiones sin marca o de Senna cuando estén disponibles.
    destacada: { src: '/unidades/requinoa/dormitorio.jpg', alt: 'Dormitorio del estudio en Requínoa' },
    galeria: [
      { src: '/unidades/requinoa/acceso.jpg', alt: 'Acceso al condominio' },
      { src: '/unidades/requinoa/patio.jpg', alt: 'Terraza y quincho comunes' },
      { src: '/unidades/requinoa/living.jpg', alt: 'Living-comedor amoblado' },
      { src: '/unidades/requinoa/comedor.jpg', alt: 'Comedor' },
      { src: '/unidades/requinoa/cocina.jpg', alt: 'Cocina con muebles' },
      { src: '/unidades/requinoa/dormitorio-2.jpg', alt: 'Dormitorio, otro ángulo' },
      { src: '/unidades/requinoa/bano.jpg', alt: 'Baño con closet' },
      { src: '/unidades/requinoa/estar.jpg', alt: 'Estar con mural Senna' },
    ],
  },
];

export const porSlug = (slug: string) => UNIDADES.find((u) => u.slug === slug);
