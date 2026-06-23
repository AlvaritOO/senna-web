# Senna — Sitio multi-unidad de departamentos amoblados

Sitio de Senna (Rancagua, Chile): departamentos amoblados con dos unidades
distintas por ubicación, distribución, tiempo de estadía y nivel de
equipamiento (full / semifull). Objetivo del sitio: vitrina + captación de
leads, con un asistente por chat web y WhatsApp.

## Convenciones (IMPORTANTES)
- Todo el código, comentarios, commits y nombres de variables en **español**.
- Marca dark-luxury editorial. Respetar SIEMPRE los tokens de marca (ver
  `frontend/src/styles/tokens.css`). No introducir colores fuera de la paleta.
- Tipografía: DM Serif Display (display) + Inter (texto). No cambiarlas.
- Tono de copy: directo y profesional, nunca frío. Sentence case en botones.

## Paleta Senna
- Noche    #0F1923  (fondo principal)
- Profundo #1E2D3D  (superficies elevadas)
- Oro      #C9A84C  (acento único — usar con moderación)
- Marfil   #F5F4F0  (texto sobre oscuro)
- Acero    #8A9BAD  (texto secundario)

## Arquitectura
- `frontend/`  Astro + Svelte (islas). Despliega en Vercel. SSG + SSR.
- `backend/`   FastAPI dockerizado. Cerebro del asistente + webhook WhatsApp.
- Datos: Supabase (Postgres). pgvector preparado pero NO requerido aún
  (dos unidades caben en el contexto del asistente). Activarlo solo al crecer.

## Comandos
- Frontend:  `cd frontend && npm install && npm run dev` (build: `npm run build`)
- Backend:   `docker compose up --build`  (levanta API + Postgres + Redis)
- Esquema:   `backend/sql/001_schema.sql`

## Reglas para el asistente IA
- Nunca inventar disponibilidad ni precios: siempre vía tools que consultan la DB.
- Si no sabe algo, deriva a WhatsApp humano (+569 6607 8526).
- Responde corto, en español de Chile, sin sonar robótico.

## Estado / pendientes
- Unidad I (Barrio del Tenis): datos e imágenes reales (fotos en WordPress).
- Unidad II (Requínoa): datos reales (Comercio 15, 35 m², $280.000 + $50.000 GC) y
  fotos en /public/unidades/requinoa. NOTA: las fotos llevan marca AnichPro;
  reemplazar por versiones sin marca o de Senna.
- WhatsApp: webhook agnóstico listo; falta configurar Meta Cloud API (token + número).
