/**
 * Carga del contenido del sitio.
 *
 * - Si existen las variables SANITY_PROJECT_ID y SANITY_DATASET, el contenido
 *   se lee de Sanity, solo la versión PUBLICADA (nunca borradores).
 * - Si no existen, se usa content/seed.json (contenido inicial tomado del PDF).
 *   Esto permite ver el sitio antes de conectar Sanity.
 *
 * La lectura ocurre solo durante la compilación: ninguna clave llega al navegador.
 */
import { createClient } from '@sanity/client';
import seed from '../../../content/seed.json';
import type { Localized } from './i18n';

export type PriceOption = {
  _key: string;
  amount: number;
  currency: string;
  unit?: 'perPerson' | 'perCouple' | 'none';
  label?: Localized;
  note?: Localized;
};
export type MenuItem = { _key: string; name: Localized; description?: Localized; quote?: Localized };
export type MenuSection = { _key: string; title: Localized; note?: Localized; items: MenuItem[] };
export type Plan = {
  _id: string;
  title: Localized;
  subtitle?: Localized;
  prices: PriceOption[];
  sections: MenuSection[];
  order: number;
  published: boolean;
  portfolioId: string;
};
export type Category = {
  _id: string;
  title: Localized;
  description?: Localized;
  order: number;
  published: boolean;
};
export type Portfolio = {
  _id: string;
  title: Localized;
  kicker?: Localized;
  intro?: Localized;
  slug: { es?: string; en?: string };
  categoryId?: string;
  theme: 'olive' | 'dark' | 'romantic';
  order: number;
  published: boolean;
  illustration?: string; // nombre de la ilustración incluida en el sitio
  imageUrl?: string; // imagen personalizada subida en Sanity (opcional)
  seoDescription?: Localized;
};
export type Settings = {
  siteName: string;
  tagline?: Localized;
  heroKicker?: Localized;
  heroTitle?: Localized;
  heroIntro?: Localized;
  whatsappNumber: string;
  whatsappDisplay?: string;
  whatsappMessage?: Localized;
  footerNote?: Localized;
  instagramUrl?: string;
  seoDescription?: Localized;
};
export type SiteContent = {
  source: 'sanity' | 'local';
  settings: Settings;
  categories: Category[];
  portfolios: Portfolio[];
  plans: Plan[];
};

const QUERY = `{
  "settings": *[_id == "siteSettings"][0],
  "categories": *[_type == "category"]{_id, title, description, order, published},
  "portfolios": *[_type == "portfolio"]{
    _id, title, kicker, intro, "slug": {"es": slug.es.current, "en": slug.en.current}, "categoryId": category._ref, theme, order, published,
    "illustration": illustrationKey, "imageUrl": customImage.asset->url, seoDescription
  },
  "plans": *[_type == "plan"]{
    _id, title, subtitle, prices, sections, order, published, "portfolioId": portfolio._ref
  }
}`;

function fromSeed(): SiteContent {
  const s: any = seed;
  return {
    source: 'local',
    settings: s.settings,
    categories: s.categories,
    portfolios: s.portfolios.map((p: any) => ({ ...p, categoryId: p.category?._ref })),
    plans: s.plans.map((p: any) => ({ ...p, portfolioId: p.portfolio?._ref })),
  };
}

let cache: Promise<SiteContent> | null = null;

export function getContent(): Promise<SiteContent> {
  if (!cache) cache = load();
  return cache;
}

async function load(): Promise<SiteContent> {
  const projectId = process.env.SANITY_PROJECT_ID;
  const dataset = process.env.SANITY_DATASET;
  if (!projectId || !dataset) {
    console.log('[contenido] Sin SANITY_PROJECT_ID/SANITY_DATASET: usando content/seed.json');
    return normalize(fromSeed());
  }
  const client = createClient({
    projectId,
    dataset,
    apiVersion: process.env.SANITY_API_VERSION || '2025-01-01',
    useCdn: false,
    perspective: 'published', // nunca borradores
    token: process.env.SANITY_READ_TOKEN || undefined, // solo si el dataset es privado
  });
  const data: any = await client.fetch(QUERY);
  if (!data?.settings) throw new Error('Sanity no devolvió la Configuración general (documento siteSettings).');
  console.log(`[contenido] Sanity ${projectId}/${dataset}: ${data.portfolios.length} portafolios, ${data.plans.length} planes`);
  return normalize({ source: 'sanity', ...data });
}

function normalize(c: SiteContent): SiteContent {
  const byOrder = (a: { order?: number }, b: { order?: number }) => (a.order ?? 99) - (b.order ?? 99);
  c.categories = (c.categories || []).map((x) => ({ ...x, published: x.published !== false })).sort(byOrder);
  c.portfolios = (c.portfolios || [])
    .filter((p) => p.slug?.es)
    .map((p) => ({ ...p, theme: p.theme || 'olive', published: p.published !== false }))
    .sort(byOrder);
  c.plans = (c.plans || [])
    .map((p) => ({ ...p, prices: p.prices || [], sections: p.sections || [], published: p.published !== false }))
    .sort(byOrder);
  return c;
}

/** Planes visibles de un portafolio. */
export function plansFor(c: SiteContent, portfolioId: string) {
  return c.plans.filter((p) => p.portfolioId === portfolioId && p.published);
}

/** Portafolios visibles (publicados y con categoría visible o sin categoría). */
export function visiblePortfolios(c: SiteContent) {
  const hidden = new Set(c.categories.filter((x) => !x.published).map((x) => x._id));
  return c.portfolios.filter((p) => p.published && !(p.categoryId && hidden.has(p.categoryId)));
}

/** Precio más bajo de un portafolio, para mostrar "Desde ...". */
export function lowestPrice(c: SiteContent, portfolioId: string) {
  const all = plansFor(c, portfolioId).flatMap((p) => p.prices.filter((x) => typeof x.amount === 'number'));
  if (!all.length) return null;
  return all.reduce((a, b) => (b.amount < a.amount ? b : a));
}

const ILLUSTRATIONS: Record<string, string> = {
  omakase: '/ilustraciones/omakase.png',
  brunch: '/ilustraciones/brunch.png',
  'corporativo-dinner': '/ilustraciones/corporativo-dinner.png',
  'corporativo-lunch': '/ilustraciones/corporativo-lunch.png',
  eventos: '/ilustraciones/eventos.png',
  'mix-night': '/ilustraciones/mix-night.png',
  celebracion: '/ilustraciones/celebracion.png',
  'romanticas-foto': '/ilustraciones/romanticas-foto.jpg',
};

export function illustrationFor(p: Portfolio): { src: string; kind: 'line' | 'photo' } | null {
  if (p.imageUrl) return { src: p.imageUrl + '?w=1200&auto=format', kind: 'photo' };
  if (p.illustration && ILLUSTRATIONS[p.illustration]) {
    return { src: ILLUSTRATIONS[p.illustration], kind: p.illustration.endsWith('foto') ? 'photo' : 'line' };
  }
  return null;
}

export function whatsappUrl(settings: Settings, text: string) {
  const n = (settings.whatsappNumber || '').replace(/\D/g, '');
  return `https://wa.me/${n}?text=${encodeURIComponent(text)}`;
}
