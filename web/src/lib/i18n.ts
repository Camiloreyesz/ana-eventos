export const LANGS = ['es', 'en'] as const;
export type Lang = (typeof LANGS)[number];

/** Segmento de la URL de portafolios en cada idioma. */
export const PORTFOLIO_SEGMENT: Record<Lang, string> = { es: 'portafolios', en: 'portfolios' };
/** Segmento de la URL de las categorías en cada idioma. */
export const CATEGORY_SEGMENT: Record<Lang, string> = { es: 'categorias', en: 'categories' };

/** Textos fijos de la interfaz (botones, etiquetas, mensajes del sistema). */
export const UI = {
  es: {
    navPortfolios: 'Portafolios',
    navContact: 'Reservar',
    langLabel: 'Idioma',
    langSwitch: 'English',
    skip: 'Saltar al contenido',
    from: 'Desde',
    perPerson: 'Por persona',
    perCouple: 'Por pareja',
    currencyNote: 'COP',
    viewPortfolio: 'Ver portafolio',
    quote: 'Cotizar por WhatsApp',
    quoteShort: 'Escríbenos',
    bookNow: 'Book now',
    bookText: 'Cuéntanos la fecha, cuántas personas son y qué experiencia te interesa.',
    related: 'Otras experiencias',
    allPortfolios: 'Ver todos los portafolios',
    plans: 'Planes',
    retiredTitle: 'Este portafolio no está disponible por ahora',
    retiredText: 'Mira las otras experiencias que tenemos para tu evento.',
    notFoundTitle: 'No encontramos esta página',
    notFoundText: 'Puede que el enlace haya cambiado. Vuelve al inicio para ver todos los portafolios.',
    backHome: 'Volver al inicio',
    menu: 'Menú',
    close: 'Cerrar',
    footerRights: 'Todos los derechos reservados.',
    openWhatsapp: 'Abrir WhatsApp',
    newTab: '(se abre en una pestaña nueva)',
    navExperiences: 'Experiencias',
    navNight: 'La noche',
    navTasting: 'Cata de aguardiente',
    navContactSection: 'Contacto',
    mainNav: 'Principal',
    homeLabel: 'Inicio',
    openMenu: 'Abrir menú',
    closeMenu: 'Cerrar menú',
    heroCta: 'Reservar por WhatsApp',
    heroLink: 'Ver experiencias',
    viewPortfolios: 'Ver portafolios',
    consultWhatsapp: 'Consultar por WhatsApp',
    writeWhatsapp: 'Escribir por WhatsApp',
    callLabel: 'Teléfono',
    webLabel: 'Web de Ana',
    instagramLabel: 'Instagram',
    waTopicEvents: 'los eventos',
    waTopicTasting: 'la cata de aguardiente',
    categoryCount: 'portafolios',
    categoryEmpty: 'Por ahora no hay portafolios publicados en esta categoría.',
    allCategories: 'Ver todas las experiencias',
    quoteThis: 'Cotizar este menú',
    compareTitle: 'Menús de este portafolio',
    compareHint: 'Toca un menú para ver su detalle.',
    fromShort: 'Desde',
  },
  en: {
    navPortfolios: 'Portfolios',
    navContact: 'Book',
    langLabel: 'Language',
    langSwitch: 'Español',
    skip: 'Skip to content',
    from: 'From',
    perPerson: 'Per person',
    perCouple: 'Per couple',
    currencyNote: 'COP',
    viewPortfolio: 'View portfolio',
    quote: 'Get a quote on WhatsApp',
    quoteShort: 'Message us',
    bookNow: 'Book now',
    bookText: 'Tell us the date, how many guests and which experience you like.',
    related: 'Other experiences',
    allPortfolios: 'See all portfolios',
    plans: 'Plans',
    retiredTitle: 'This portfolio is not available right now',
    retiredText: 'Take a look at our other experiences for your event.',
    notFoundTitle: 'We couldn’t find this page',
    notFoundText: 'The link may have changed. Go back home to see all portfolios.',
    backHome: 'Back to home',
    menu: 'Menu',
    close: 'Close',
    footerRights: 'All rights reserved.',
    openWhatsapp: 'Open WhatsApp',
    newTab: '(opens in a new tab)',
    navExperiences: 'Experiences',
    navNight: 'The night',
    navTasting: 'Aguardiente tasting',
    navContactSection: 'Contact',
    mainNav: 'Main',
    homeLabel: 'Home',
    openMenu: 'Open menu',
    closeMenu: 'Close menu',
    heroCta: 'Book on WhatsApp',
    heroLink: 'See experiences',
    viewPortfolios: 'See portfolios',
    consultWhatsapp: 'Ask on WhatsApp',
    writeWhatsapp: 'Message us on WhatsApp',
    callLabel: 'Phone',
    webLabel: 'Ana’s website',
    instagramLabel: 'Instagram',
    waTopicEvents: 'events',
    waTopicTasting: 'the aguardiente tasting',
    categoryCount: 'portfolios',
    categoryEmpty: 'There are no published portfolios in this category right now.',
    allCategories: 'See all experiences',
    quoteThis: 'Get a quote for this menu',
    compareTitle: 'Menus in this portfolio',
    compareHint: 'Tap a menu to see its details.',
    fromShort: 'From',
  },
} satisfies Record<Lang, Record<string, string>>;

export type Localized = { es?: string; en?: string } | null | undefined;

/**
 * Devuelve el texto en el idioma pedido. Si falta la traducción al inglés,
 * usa el español y lo marca (`fallback: true`) para poner lang="es" en el HTML
 * y que no haya una mezcla de idiomas sin señalar.
 */
export function tr(value: Localized, lang: Lang): string {
  if (!value) return '';
  return (value[lang] || value.es || '').trim();
}
export function isFallback(value: Localized, lang: Lang): boolean {
  return !!value && lang === 'en' && !value.en?.trim() && !!value.es?.trim();
}

export function otherLang(lang: Lang): Lang {
  return lang === 'es' ? 'en' : 'es';
}

/** Formato de precio sin convertir moneda: $220.000 (separador de miles con punto). */
export function formatPrice(amount: number): string {
  return '$' + Math.round(amount).toString().replace(/\B(?=(\d{3})+(?!\d))/g, '.');
}

export function unitLabel(unit: string | undefined, lang: Lang): string {
  if (unit === 'perPerson') return UI[lang].perPerson;
  if (unit === 'perCouple') return UI[lang].perCouple;
  return '';
}

export function homePath(lang: Lang) {
  return `/${lang}/`;
}
export function portfolioPath(lang: Lang, slug: string) {
  return `/${lang}/${PORTFOLIO_SEGMENT[lang]}/${slug}/`;
}
export function categoryPath(lang: Lang, id: string) {
  return `/${lang}/${CATEGORY_SEGMENT[lang]}/${id}/`;
}
