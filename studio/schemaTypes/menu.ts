import { defineType, defineField, defineArrayMember } from 'sanity';

export const priceOption = defineType({
  name: 'priceOption',
  title: 'Precio',
  type: 'object',
  fields: [
    defineField({ name: 'amount', title: 'Valor', type: 'number', description: 'Solo el número, sin puntos ni signo. Ej.: 120000', validation: (r) => r.required().integer().positive() }),
    defineField({ name: 'currency', title: 'Moneda', type: 'string', initialValue: 'COP', options: { list: [{ title: 'Pesos colombianos (COP)', value: 'COP' }, { title: 'Dólares (USD)', value: 'USD' }], layout: 'radio', direction: 'horizontal' }, validation: (r) => r.required() }),
    defineField({ name: 'unit', title: 'Se cobra', type: 'string', initialValue: 'perPerson', options: { list: [{ title: 'Por persona', value: 'perPerson' }, { title: 'Por pareja', value: 'perCouple' }, { title: 'Sin unidad (no mostrar)', value: 'none' }], layout: 'radio' } }),
    defineField({ name: 'label', title: 'Nombre del precio (opcional)', type: 'localeString', description: 'Úsalo cuando el plan tiene varios precios. Ej.: "Sin maridaje" / "Con maridaje de coctelería".' }),
    defineField({ name: 'note', title: 'Nota (opcional)', type: 'localeString', description: 'Ej.: "Incluye torta y detalle."' }),
  ],
  preview: {
    select: { amount: 'amount', label: 'label.es', unit: 'unit' },
    prepare: ({ amount, label, unit }) => ({
      title: `$${(amount || 0).toLocaleString('es-CO')}`,
      subtitle: [label, unit === 'perPerson' ? 'por persona' : unit === 'perCouple' ? 'por pareja' : ''].filter(Boolean).join(' · '),
    }),
  },
});

export const menuItem = defineType({
  name: 'menuItem',
  title: 'Plato o ítem',
  type: 'object',
  fields: [
    defineField({ name: 'name', title: 'Nombre', type: 'localeString', validation: (r) => r.required() }),
    defineField({ name: 'description', title: 'Descripción (opcional)', type: 'localeString' }),
    defineField({ name: 'quote', title: 'Frase (opcional)', type: 'localeString', description: 'Texto en cursiva, como en el Omakase.' }),
  ],
  preview: { select: { title: 'name.es', subtitle: 'description.es' } },
});

export const menuSection = defineType({
  name: 'menuSection',
  title: 'Sección del menú',
  type: 'object',
  fields: [
    defineField({ name: 'title', title: 'Título', type: 'localeString', description: 'Ej.: Entrada, Fuertes, Postre, Bebidas.', validation: (r) => r.required() }),
    defineField({ name: 'note', title: 'Nota (opcional)', type: 'localeString', description: 'Ej.: "1 a elegir", "Para compartir".' }),
    defineField({ name: 'items', title: 'Ítems', type: 'array', of: [defineArrayMember({ type: 'menuItem' })] }),
  ],
  preview: {
    select: { title: 'title.es', note: 'note.es', items: 'items' },
    prepare: ({ title, note, items }) => ({ title, subtitle: [note, `${items?.length || 0} ítems`].filter(Boolean).join(' · ') }),
  },
});
