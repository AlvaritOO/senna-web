-- Esquema Senna. Se ejecuta automáticamente al crear el contenedor de Postgres.
-- pgvector queda preparado pero NO se usa aún (dos unidades caben en contexto).

CREATE EXTENSION IF NOT EXISTS vector;   -- listo para el futuro (RAG/FAQ)

CREATE TABLE IF NOT EXISTS unidades (
  slug            TEXT PRIMARY KEY,
  numero          TEXT NOT NULL,
  nombre          TEXT NOT NULL,
  ubicacion       TEXT NOT NULL,
  distribucion    TEXT,
  equipamiento    TEXT CHECK (equipamiento IN ('Full', 'Semifull')),
  estadia_minima  TEXT,
  precio_valor    NUMERIC,
  precio_unidad   TEXT,          -- 'UF/mes' | 'UF/noche'
  precio_nota     TEXT,
  resumen         TEXT
);

CREATE TABLE IF NOT EXISTS disponibilidad (
  id      SERIAL PRIMARY KEY,
  slug    TEXT REFERENCES unidades(slug),
  desde   DATE NOT NULL,
  hasta   DATE NOT NULL,
  estado  TEXT DEFAULT 'ocupado' CHECK (estado IN ('ocupado', 'bloqueado'))
);

CREATE TABLE IF NOT EXISTS leads (
  id        SERIAL PRIMARY KEY,
  nombre    TEXT,
  contacto  TEXT NOT NULL,
  slug      TEXT,
  mensaje   TEXT,
  creado    TIMESTAMPTZ DEFAULT now()
);

-- Tabla preparada para cuando se active el conocimiento semántico (no usada hoy):
-- CREATE TABLE conocimiento (
--   id SERIAL PRIMARY KEY, titulo TEXT, contenido TEXT,
--   embedding vector(1536)
-- );

-- Semilla: Unidad 1 (datos reales del sitio actual).
INSERT INTO unidades (slug, numero, nombre, ubicacion, distribucion, equipamiento,
                      estadia_minima, precio_valor, precio_unidad, precio_nota, resumen)
VALUES
('barrio-del-tenis', 'I', 'Senna · Barrio del Tenis',
 'Barrio del Tenis, Centro de Rancagua',
 '1 dormitorio · walk-in closet · baño privado', 'Full',
 'Desde 1 mes', 12, 'UF/mes', 'Todo incluido',
 'Departamento completamente amoblado en el corazón de Rancagua.'),
('requinoa', 'II', 'Senna · Requínoa',
 'Centro de Requínoa, calle Comercio 15',
 'Estudio 35 m² · 1 dormitorio · baño con closet · living-comedor', 'Semifull',
 'Arriendo mensual', 280000, '$/mes', '+ $50.000 gastos comunes',
 'Estudio de 35 m² en el centro de Requínoa, a 15 min de Rancagua. Terraza y lavandería comunes.')
ON CONFLICT (slug) DO NOTHING;
