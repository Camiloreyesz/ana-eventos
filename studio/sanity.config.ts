import { defineConfig } from 'sanity';
import { structureTool, type StructureResolver } from 'sanity/structure';
import { esESLocale } from '@sanity/locale-es-es';
import { schemaTypes } from './schemaTypes';

const projectId = process.env.SANITY_STUDIO_PROJECT_ID || 'reemplazar';
const dataset = process.env.SANITY_STUDIO_DATASET || 'production';
const SINGLETONS = new Set(['siteSettings']);

const structure: StructureResolver = (S) =>
  S.list()
    .title('Ana · Portafolio de eventos')
    .items([
      S.listItem().title('Configuración general').id('siteSettings')
        .child(S.document().schemaType('siteSettings').documentId('siteSettings').title('Configuración general')),
      S.divider(),
      S.documentTypeListItem('category').title('Categorías'),
      S.documentTypeListItem('portfolio').title('Portafolios'),
      S.listItem().title('Planes por portafolio').child(
        S.documentTypeList('portfolio').title('Elige un portafolio').child((id) =>
          S.documentList().title('Planes').schemaType('plan')
            .filter('_type == "plan" && portfolio._ref == $id').params({ id })
            .defaultOrdering([{ field: 'order', direction: 'asc' }])
            .initialValueTemplates([S.initialValueTemplateItem('plan-en-portafolio', { portfolioId: id })]),
        ),
      ),
      S.documentTypeListItem('plan').title('Todos los planes'),
    ]);

export default defineConfig({
  name: 'ana-eventos',
  title: 'Ana · Portafolio de eventos',
  projectId,
  dataset,
  plugins: [structureTool({ structure }), esESLocale()],
  schema: {
    types: schemaTypes,
    templates: (prev) => [
      ...prev.filter((t) => !SINGLETONS.has(t.schemaType)),
      {
        id: 'plan-en-portafolio',
        title: 'Plan en este portafolio',
        schemaType: 'plan',
        parameters: [{ name: 'portfolioId', type: 'string' }],
        value: (p: { portfolioId: string }) => ({ portfolio: { _type: 'reference', _ref: p.portfolioId }, published: true }),
      },
    ],
  },
  document: {
    // La Configuración general no se puede duplicar ni borrar.
    actions: (prev, ctx) =>
      SINGLETONS.has(ctx.schemaType) ? prev.filter((a) => !['duplicate', 'delete', 'unpublish'].includes(a.action || '')) : prev,
    newDocumentOptions: (prev) => prev.filter((i) => !SINGLETONS.has(i.templateId)),
  },
});
