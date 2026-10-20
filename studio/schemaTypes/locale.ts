import { defineType, defineField } from 'sanity';

// Campos traducibles: cada texto tiene su versión en español y en inglés.
// El español es obligatorio. Si el inglés queda vacío, la web muestra el español.
export const localeString = defineType({
  name: 'localeString',
  title: 'Texto (ES / EN)',
  type: 'object',
  options: { columns: 2 },
  fields: [
    defineField({ name: 'es', title: 'Español', type: 'string', validation: (r) => r.required().error('Escribe el texto en español.') }),
    defineField({ name: 'en', title: 'English', type: 'string', validation: (r) => r.warning() }),
  ],
});

export const localeText = defineType({
  name: 'localeText',
  title: 'Texto largo (ES / EN)',
  type: 'object',
  fields: [
    defineField({ name: 'es', title: 'Español', type: 'text', rows: 3 }),
    defineField({ name: 'en', title: 'English', type: 'text', rows: 3 }),
  ],
});

export const localeSlug = defineType({
  name: 'localeSlug',
  title: 'Dirección web (URL)',
  type: 'object',
  description: 'Es la parte final de la dirección. Evita cambiarla después de publicar: los enlaces que ya se compartieron dejarían de funcionar.',
  fields: [
    defineField({ name: 'es', title: 'Español (/es/portafolios/…)', type: 'slug', options: { source: 'title.es', maxLength: 60 }, validation: (r) => r.required() }),
    defineField({ name: 'en', title: 'English (/en/portfolios/…)', type: 'slug', options: { source: 'title.en', maxLength: 60 }, description: 'Si está vacío, no se crea la página en inglés.' }),
  ],
});
