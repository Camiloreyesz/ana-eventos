// Carga el contenido inicial (content/seed.json, tomado del PDF) en Sanity.
// Uso: SANITY_STUDIO_PROJECT_ID=xxx SANITY_WRITE_TOKEN=yyy npm run seed
// Se puede repetir: reemplaza los documentos con el mismo _id (no toca otros).
import { createClient } from '@sanity/client';
import { readFileSync, existsSync } from 'node:fs';

if (existsSync('.env')) {
  for (const line of readFileSync('.env', 'utf8').split('\n')) {
    const m = line.match(/^\s*([A-Z_]+)\s*=\s*(.*)\s*$/);
    if (m && !process.env[m[1]]) process.env[m[1]] = m[2];
  }
}
const projectId = process.env.SANITY_STUDIO_PROJECT_ID;
const dataset = process.env.SANITY_STUDIO_DATASET || 'production';
const token = process.env.SANITY_WRITE_TOKEN;
if (!projectId || !token) {
  console.error('Faltan SANITY_STUDIO_PROJECT_ID o SANITY_WRITE_TOKEN (ver .env.example).');
  process.exit(1);
}
const client = createClient({ projectId, dataset, token, apiVersion: '2025-01-01', useCdn: false });
const seed = JSON.parse(readFileSync(new URL('../../content/seed.json', import.meta.url), 'utf8'));

const slug = (v) => (v ? { _type: 'slug', current: v } : undefined);
const docs = [
  seed.settings,
  ...seed.categories,
  ...seed.portfolios.map(({ illustration, slug: s, ...p }) => ({
    ...p,
    illustrationKey: illustration,
    slug: { _type: 'localeSlug', es: slug(s.es), en: slug(s.en) },
  })),
  ...seed.plans,
];

const tx = client.transaction();
for (const d of docs) tx.createOrReplace(d);
const res = await tx.commit();
console.log(`Listo: ${docs.length} documentos cargados en ${projectId}/${dataset} (transacción ${res.transactionId}).`);
