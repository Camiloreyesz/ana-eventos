import { defineCliConfig } from 'sanity/cli';

export default defineCliConfig({
  api: {
    projectId: process.env.SANITY_STUDIO_PROJECT_ID || 'reemplazar',
    dataset: process.env.SANITY_STUDIO_DATASET || 'production',
  },
  // Dirección del panel al publicarlo con `npm run deploy`: https://<studioHost>.sanity.studio
  studioHost: process.env.SANITY_STUDIO_HOST || 'ana-eventos',
});
