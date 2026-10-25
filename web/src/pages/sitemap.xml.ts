import type { APIRoute } from 'astro';
import { getContent, visiblePortfolios } from '../lib/content';
import { portfolioPath, categoryPath } from '../lib/i18n';

// Sitemap propio con enlaces alternativos por idioma (hreflang).
// Solo incluye categorías y portafolios publicados.
export const GET: APIRoute = async ({ site }) => {
  const c = await getContent();
  const abs = (p: string) => new URL(p, site).href;
  const groups: { es?: string; en?: string }[] = [{ es: '/es/', en: '/en/' }];
  const vis = visiblePortfolios(c);
  for (const cat of c.categories.filter((x) => x.published && vis.some((p) => p.categoryId === x._id))) {
    groups.push({ es: categoryPath('es', cat._id), en: categoryPath('en', cat._id) });
  }
  for (const p of vis) {
    groups.push({
      es: p.slug.es ? portfolioPath('es', p.slug.es) : undefined,
      en: p.slug.en ? portfolioPath('en', p.slug.en) : undefined,
    });
  }
  const urls = groups.flatMap((g) =>
    (['es', 'en'] as const).filter((l) => g[l]).map((l) => {
      const alts = (['es', 'en'] as const).filter((x) => g[x])
        .map((x) => `<xhtml:link rel="alternate" hreflang="${x}" href="${abs(g[x]!)}"/>`).join('');
      return `<url><loc>${abs(g[l]!)}</loc>${alts}</url>`;
    }),
  );
  const xml = `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">${urls.join('')}</urlset>`;
  return new Response(xml, { headers: { 'Content-Type': 'application/xml; charset=utf-8' } });
};
