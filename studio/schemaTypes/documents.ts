import { defineType, defineField, defineArrayMember } from 'sanity';

const visible = defineField({
  name: 'published',
  title: 'Visible en el sitio',
  type: 'boolean',
  initialValue: true,
  description: 'Apágalo para ocultarlo de la web sin borrarlo. Los datos se conservan.',
});
const order = defineField({ name: 'order', title: 'Orden', type: 'number', description: 'Número menor = aparece primero.', initialValue: 10 });

export const ILLUSTRATIONS = [
  { title: 'Omakase (manos y nigiris)', value: 'omakase' },
  { title: 'Corporativo dinner (cubiertos y copa)', value: 'corporativo-dinner' },
  { title: 'Corporativo lunch (cubiertos)', value: 'corporativo-lunch' },
  { title: 'Eventos (personas brindando)', value: 'eventos' },
  { title: 'The Mix Night (mesa larga)', value: 'mix-night' },
  { title: 'Brunch (pancakes)', value: 'brunch' },
  { title: 'Celebración (velas y vino)', value: 'celebracion' },
  { title: 'Románticas (foto de fondo)', value: 'romanticas-foto' },
];

export const siteSettings = defineType({
  name: 'siteSettings',
  title: 'Configuración general',
  type: 'document',
  groups: [{ name: 'portada', title: 'Portada', default: true }, { name: 'contacto', title: 'Contacto' }, { name: 'seo', title: 'Buscadores' }],
  fields: [
    defineField({ name: 'siteName', title: 'Nombre del sitio', type: 'string', group: 'portada', validation: (r) => r.required() }),
    defineField({ name: 'heroTitle', title: 'Título de la portada', type: 'localeString', group: 'portada' }),
    defineField({ name: 'heroIntro', title: 'Texto de la portada', type: 'localeText', group: 'portada' }),
    defineField({ name: 'tagline', title: 'Frase de marca', type: 'localeString', group: 'portada' }),
    defineField({ name: 'whatsappNumber', title: 'WhatsApp (con indicativo, solo números)', type: 'string', group: 'contacto', description: 'Ej.: 573126604133', validation: (r) => r.required().regex(/^\d{10,15}$/, { name: 'número' }) }),
    defineField({ name: 'whatsappDisplay', title: 'WhatsApp como se muestra', type: 'string', group: 'contacto', description: 'Ej.: 312 660 4133' }),
    defineField({ name: 'whatsappMessage', title: 'Inicio del mensaje de WhatsApp', type: 'localeString', group: 'contacto', description: 'Se completa con el nombre del portafolio. Ej.: "Hola Ana, quiero información sobre"' }),
    defineField({ name: 'instagramUrl', title: 'Instagram (enlace completo)', type: 'url', group: 'contacto' }),
    defineField({ name: 'footerNote', title: 'Nota del pie de página', type: 'localeString', group: 'contacto' }),
    defineField({ name: 'seoDescription', title: 'Descripción para Google', type: 'localeText', group: 'seo', description: 'Unas 150 letras.' }),
  ],
  preview: { prepare: () => ({ title: 'Configuración general' }) },
});

export const category = defineType({
  name: 'category',
  title: 'Categoría',
  type: 'document',
  fields: [
    defineField({ name: 'title', title: 'Nombre', type: 'localeString', validation: (r) => r.required() }),
    defineField({ name: 'description', title: 'Descripción', type: 'localeText' }),
    order,
    visible,
  ],
  orderings: [{ title: 'Orden', name: 'order', by: [{ field: 'order', direction: 'asc' }] }],
  preview: {
    select: { title: 'title.es', published: 'published', order: 'order' },
    prepare: ({ title, published, order }) => ({ title, subtitle: `${order ?? ''} · ${published === false ? 'Oculta' : 'Visible'}` }),
  },
});

export const portfolio = defineType({
  name: 'portfolio',
  title: 'Portafolio',
  type: 'document',
  groups: [{ name: 'contenido', title: 'Contenido', default: true }, { name: 'diseno', title: 'Diseño' }, { name: 'seo', title: 'Buscadores' }],
  fields: [
    defineField({ name: 'title', title: 'Nombre', type: 'localeString', group: 'contenido', validation: (r) => r.required() }),
    defineField({ name: 'kicker', title: 'Etiqueta', type: 'localeString', group: 'contenido', description: 'Texto pequeño bajo el nombre. Ej.: "Menu by Ana".' }),
    defineField({ name: 'intro', title: 'Introducción', type: 'localeText', group: 'contenido' }),
    defineField({ name: 'slug', title: 'Dirección web', type: 'localeSlug', group: 'contenido', validation: (r) => r.required() }),
    defineField({ name: 'category', title: 'Categoría', type: 'reference', to: [{ type: 'category' }], group: 'contenido' }),
    order,
    visible,
    defineField({ name: 'theme', title: 'Estilo', type: 'string', group: 'diseno', initialValue: 'olive', options: { list: [{ title: 'Oliva (general)', value: 'olive' }, { title: 'Tinta (corporativo)', value: 'dark' }, { title: 'Rojo romántico', value: 'romantic' }], layout: 'radio' } }),
    defineField({ name: 'illustrationKey', title: 'Ilustración', type: 'string', group: 'diseno', options: { list: ILLUSTRATIONS } }),
    defineField({ name: 'customImage', title: 'Imagen propia (opcional)', type: 'image', group: 'diseno', description: 'Reemplaza la ilustración. Úsala solo si tienes una pieza aprobada por marca.' }),
    defineField({ name: 'seoDescription', title: 'Descripción para Google', type: 'localeText', group: 'seo' }),
  ],
  orderings: [{ title: 'Orden', name: 'order', by: [{ field: 'order', direction: 'asc' }] }],
  preview: {
    select: { title: 'title.es', cat: 'category.title.es', published: 'published' },
    prepare: ({ title, cat, published }) => ({ title, subtitle: `${cat || 'Sin categoría'} · ${published === false ? 'Oculto' : 'Visible'}` }),
  },
});

export const plan = defineType({
  name: 'plan',
  title: 'Plan',
  type: 'document',
  fields: [
    defineField({ name: 'portfolio', title: 'Portafolio', type: 'reference', to: [{ type: 'portfolio' }], validation: (r) => r.required() }),
    defineField({ name: 'title', title: 'Nombre del plan', type: 'localeString', validation: (r) => r.required() }),
    defineField({ name: 'subtitle', title: 'Subtítulo / horario', type: 'localeString', description: 'Ej.: "Domingos a miércoles", "Opción 1".' }),
    defineField({ name: 'prices', title: 'Precios', type: 'array', of: [defineArrayMember({ type: 'priceOption' })], validation: (r) => r.min(1).warning('El plan no tiene precio.') }),
    defineField({ name: 'sections', title: 'Menú', type: 'array', of: [defineArrayMember({ type: 'menuSection' })] }),
    order,
    visible,
    defineField({ name: 'internalNote', title: 'Nota interna (no se publica)', type: 'text', rows: 3, description: 'Para el equipo: dudas, cambios por confirmar, etc.' }),
  ],
  orderings: [{ title: 'Orden', name: 'order', by: [{ field: 'order', direction: 'asc' }] }],
  preview: {
    select: { title: 'title.es', pf: 'portfolio.title.es', amount: 'prices.0.amount', published: 'published', note: 'internalNote' },
    prepare: ({ title, pf, amount, published, note }) => ({
      title: `${note ? '⚠︎ ' : ''}${title}`,
      subtitle: [pf, amount ? `$${amount.toLocaleString('es-CO')}` : 'Sin precio', published === false ? 'Oculto' : ''].filter(Boolean).join(' · '),
    }),
  },
});
