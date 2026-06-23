# Frontend Senna (Astro + Svelte)

- Sitio estático (SSG). Cada unidad se prerenderiza (`getStaticPaths`) → SEO.
- Interactividad solo en islas Svelte (`client:idle`). Hoy: el chat.
- Colores y tipografía SIEMPRE desde `src/styles/tokens.css`. No hardcodear hex.
- Datos en `src/data/unidades.ts`. Para migrar a Supabase: reemplazar el import
  por un `fetch` a la API; las páginas no cambian.
- Copy en español de Chile, sentence case en botones, tono directo no frío.
- Imágenes de la Unidad 1 viven en el WordPress de Senna (ver unidades.ts).

## Variables de entorno (PUBLIC_*)
- PUBLIC_API_URL  → backend FastAPI
- PUBLIC_WHATSAPP → número para enlaces wa.me
