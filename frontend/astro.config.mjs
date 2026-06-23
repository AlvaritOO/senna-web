import { defineConfig } from 'astro/config';
import svelte from '@astrojs/svelte';

// Sitio estático (SSG) + islas Svelte para lo interactivo (chat).
// Ideal para SEO inmobiliario: cada unidad se prerenderiza como HTML.
export default defineConfig({
  site: 'https://senna.cl',
  integrations: [svelte()],
});
