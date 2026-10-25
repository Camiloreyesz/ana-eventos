/**
 * Carga del contenido del sitio.
 *
 * El contenido vive en archivos JSON dentro del repositorio (web/content/).
 * El panel /admin (Decap CMS) edita esos archivos y guarda los cambios en GitHub;
 * Netlify detecta el cambio y vuelve a compilar el sitio.
 *
 *   web/content/configuracion.json      → datos generales, WhatsApp, Instagram y web
 *   web/content/portada.json            → textos y fotos de la página de inicio
 *   web/content/categorias/*.json       → una categoría por archivo
 *   web/content/portafolios/*.json      → un portafolio por archivo, con sus planes
 *
 * La lectura ocurre solo durante la compilación.
 */
import { readFileSync, readdirSync, existsSync } from 'node:fs';
import { join, resolve } from 'node:path';
import type { Localized } from './i18n';

export type PriceOption = {
  amount: number;
  currency: string;
  unit?: 'perPerson' | 'perCouple' | 'none';
  label?: Localized;
  note?: Localized;
};
export type MenuItem = { name: Localized; description?: Localized; quote?: Localized };
export type MenuSection = { title: Localized; note?: Localized; items: MenuItem[] };
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
  illustration?: string; // ilustración de la tarjeta en la portada
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
  illustration?: string; // ilustración incluida en el sitio
  imageUrl?: string; // imagen propia subida desde el panel (opcional)
  seoDescription?: Localized;
};
export type Settings = {
  siteName: string;
  whatsappNumber: string;
  whatsappDisplay?: string;
  whatsappMessage?: Localized;
  footerNote?: Localized;
  instagramUrl?: string;
  webUrl?: string;
  seoDescription?: Localized;
};

/** Textos y fotos de la página de inicio (web/content/portada.json). */
export type Portada = {
  hero: { title: Localized; intro: Localized; image: string; imageAlt: Localized };
  experiences: { title: Localized; intro: Localized };
  night: {
    title: Localized;
    rows: { label: Localized; value: Localized }[];
    note: Localized;
    photoA: string;
    photoAAlt: Localized;
    photoB: string;
    photoBAlt: Localized;
  };
  tasting: { title: Localized; paragraphs: Localized[]; image: string; imageAlt: Localized };
  banner: { visible?: boolean; text: Localized };
  contact: { title: Localized; text: Localized; location: Localized; address?: Localized };
};
export type SiteContent = {
  settings: Settings;
  categories: Category[];
  portfolios: Portfolio[];
  plans: Plan[];
};

// web/content, tanto en local como en Netlify (la compilación corre dentro de web/).
const CONTENT_DIR = resolve(process.env.CONTENT_DIR || join(process.cwd(), 'content'));

function readJson(path: string): any {
  try {
    return JSON.parse(readFileSync(path, 'utf8'));
  } catch (e) {
    throw new Error(`[contenido] No se pudo leer ${path}: ${(e as Error).message}`);
  }
}
function readFolder(name: string): { id: string; data: any }[] {
  const dir = join(CONTENT_DIR, name);
  if (!existsSync(dir)) return [];
  return readdirSync(dir)
    .filter((f) => f.endsWith('.json'))
    .map((f) => ({ id: f.replace(/\.json$/, ''), data: readJson(join(dir, f)) }));
}

let cache: Promise<SiteContent> | null = null;
let portadaCache: Portada | null = null;

/** Contenido de la portada. */
export function getPortada(): Portada {
  if (!portadaCache) portadaCache = readJson(join(CONTENT_DIR, 'portada.json')) as Portada;
  return portadaCache;
}

export function getContent(): Promise<SiteContent> {
  if (!cache) cache = Promise.resolve(load());
  return cache;
}

function load(): SiteContent {
  const settings = readJson(join(CONTENT_DIR, 'configuracion.json'));
  const categories: Category[] = readFolder('categorias').map(({ id, data }) => ({ ...data, _id: id }));
  const plans: Plan[] = [];
  const portfolios: Portfolio[] = readFolder('portafolios').map(({ id, data }) => {
    const { plans: pls = [], category, image, ...rest } = data;
    (pls as any[]).forEach((pl, i) => plans.push({ ...pl, _id: `${id}-${i + 1}`, order: pl.order ?? i + 1, portfolioId: id }));
    return { ...rest, _id: id, categoryId: category || undefined, imageUrl: image || undefined };
  });
  console.log(`[contenido] ${portfolios.length} portafolios, ${plans.length} planes, ${categories.length} categorías`);
  return normalize({ settings, categories, portfolios, plans });
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
  if (p.imageUrl) return { src: p.imageUrl, kind: 'photo' };
  if (p.illustration && ILLUSTRATIONS[p.illustration]) {
    return { src: ILLUSTRATIONS[p.illustration], kind: p.illustration.endsWith('foto') ? 'photo' : 'line' };
  }
  return null;
}

export function categoryIllustration(cat: Category): string | null {
  return (cat.illustration && ILLUSTRATIONS[cat.illustration]) || null;
}

export function whatsappUrl(settings: Settings, text: string) {
  const n = (settings.whatsappNumber || '').replace(/\D/g, '');
  return `https://wa.me/${n}?text=${encodeURIComponent(text)}`;
}
