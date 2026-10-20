import { defineConfig } from 'astro/config';

// URL pública del sitio. En Netlify se toma de la variable URL que Netlify
// define en cada compilación; SITE_URL permite forzar el dominio propio.
const site = process.env.SITE_URL || process.env.URL || 'http://localhost:4321';

export default defineConfig({
  site,
  output: 'static',
  trailingSlash: 'always',
  build: { format: 'directory' },
  // Mantiene los espacios entre elementos en línea (comportamiento previo a Astro 7).
  compressHTML: true,
});
