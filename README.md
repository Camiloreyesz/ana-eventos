# Ana Caribe + Asia · Portafolio de eventos

Sitio web bilingüe (español / inglés) que reúne los portafolios de eventos de Ana, con un panel visual (Sanity Studio) para que el equipo cambie precios, planes y textos sin tocar código.

```
ana-eventos/
├── web/        Sitio público (Astro). Se publica en Netlify.
├── studio/     Panel de administración (Sanity Studio), en español.
├── content/    seed.json: contenido inicial tomado del Portafolio Ana 2026 (PDF).
├── scripts/    build_seed.py: genera seed.json (solo para la carga inicial).
└── netlify.toml
```

## Cómo funciona

1. El equipo entra al panel (`https://ana-eventos.sanity.studio` o la dirección que elijan) con su cuenta de Sanity.
2. Cambia un precio, un plato o un texto. Sanity guarda un **borrador** automáticamente.
3. Pulsa **Publicar**.
4. Sanity avisa a Netlify (webhook) y Netlify **vuelve a compilar el sitio**. Tarda normalmente 1 a 2 minutos. No es instantáneo.
5. Se recarga la web y se ve el cambio.

Los borradores **nunca** se muestran en la web: el sitio solo lee contenido publicado.

## Rutas

| Página | Español | Inglés |
|---|---|---|
| Inicio | `/es/` | `/en/` |
| Portafolio | `/es/portafolios/<slug>/` | `/en/portfolios/<slug>/` |
| Raíz | `/` redirige a `/es/` o `/en/` según el idioma del navegador | |

Portafolios iniciales: omakase · menu-corporativo · menus-para-eventos · the-mix-night · brunch · celebraciones-romanticas · paquete-de-celebracion (y sus equivalentes en inglés).

## Puesta en marcha (una sola vez)

### 1. Subir el código a GitHub
1. Crea un repositorio privado, por ejemplo `ana-eventos`.
2. Desde esta carpeta:
   ```bash
   git remote add origin https://github.com/<tu-usuario>/ana-eventos.git
   git push -u origin main
   ```

### 2. Crear el proyecto en Sanity
1. Entra a https://www.sanity.io/manage y crea un proyecto (plan gratuito) con un dataset llamado `production` (visibilidad **Public**: solo lectura del contenido publicado).
2. Copia el **Project ID**.
3. En la carpeta `studio/`, copia `.env.example` como `.env` y escribe el Project ID.
4. Instala y publica el panel:
   ```bash
   cd studio
   npm install
   npm run deploy        # te pedirá iniciar sesión en Sanity
   ```
5. Carga el contenido inicial del PDF:
   - En sanity.io/manage → API → Tokens, crea un token **Editor**.
   - Ponlo en `studio/.env` como `SANITY_WRITE_TOKEN`.
   - Ejecuta `npm run seed`.
   - **Borra el token** de `.env` y de sanity.io/manage al terminar.
6. Invita al equipo en sanity.io/manage → Members (rol **Editor**). Solo quien tenga cuenta invitada puede entrar al panel.
7. En sanity.io/manage → API → CORS origins agrega la dirección del panel si Sanity lo pide.

### 3. Conectar Netlify
Ya existe un proyecto vacío llamado **ana-eventos** (https://ana-eventos.netlify.app), creado por Claude, privado (solo el equipo de Netlify puede verlo).

1. En Netlify → ana-eventos → Project configuration → Build & deploy → **Link repository** y elige el repositorio de GitHub.
2. Netlify lee `netlify.toml`: carpeta base `web`, comando `npm run build`, carpeta de salida `dist`. No hay que escribirlo a mano.
3. En **Environment variables** agrega:

   | Variable | Valor | ¿Secreta? |
   |---|---|---|
   | `SANITY_PROJECT_ID` | el Project ID | No |
   | `SANITY_DATASET` | `production` | No |
   | `SANITY_API_VERSION` | `2025-01-01` | No |
   | `SANITY_READ_TOKEN` | solo si el dataset es privado (token **Viewer**) | Sí |
   | `SITE_URL` | el dominio propio cuando se conecte | No |

   Sin `SANITY_PROJECT_ID` el sitio se publica con el contenido de `content/seed.json`.
4. Lanza un deploy (Deploys → Trigger deploy).
5. Cuando quieras que el público lo vea: Project configuration → Access & security → Visitor access, quita la protección.

### 4. Publicar automáticamente al cambiar el contenido
1. Netlify → Project configuration → Build & deploy → **Build hooks** → Add build hook (nombre: `Sanity`). Copia la URL.
2. Sanity (sanity.io/manage → API → **Webhooks**) → Create webhook:
   - URL: la del build hook.
   - Dataset: `production`.
   - Trigger on: Create, Update, Delete.
   - Filter: `_type in ["siteSettings","category","portfolio","plan"]`
   - HTTP method: POST. Sin "drafts" (así solo dispara al publicar).
3. Prueba: cambia un precio en el panel, publica, espera 1–2 minutos y recarga la web.

### 5. Conectar el dominio de Ana (Hostinger)
No hace falta transferir el dominio ni cambiar los nameservers. Se agrega un registro DNS en Hostinger y el correo sigue igual.

1. Decide la dirección. Recomendado: un **subdominio**, por ejemplo `eventos.dominiodeana.com`, que no toca la web actual.
2. Netlify → Domain management → **Add a domain** → escribe el subdominio. Netlify te mostrará el registro que necesita.
3. Hostinger → Dominios → DNS / Nameservers → **Administrar registros DNS**:
   - Antes de tocar nada, toma una captura de todos los registros.
   - Agrega un registro **CNAME**: nombre `eventos`, valor `ana-eventos.netlify.app`.
   - **No borres ni edites** registros MX, TXT (SPF, DKIM, DMARC) ni los demás: son del correo y de la web actual.
4. Espera la propagación (minutos a unas horas). Netlify activa HTTPS solo (Let's Encrypt). Verifica en Domain management → HTTPS.
5. Pon `SITE_URL=https://eventos.dominiodeana.com` en Netlify y vuelve a desplegar para que los enlaces de Google usen el dominio.

Si prefieren el dominio principal (sin subdominio), habría que reemplazar la web que hoy está ahí. Eso se decide aparte.

## Guía para el equipo: editar desde el panel

**Cambiar un precio**
Planes por portafolio → elige el portafolio → abre el plan → Precios → toca el precio → cambia **Valor** (solo números, ej. `135000`) → **Publicar**.

**Cambiar un plato o una descripción**
Abre el plan → Menú → sección (Entrada, Fuertes…) → ítem. Cada texto tiene Español y English. Publica.

**Ocultar un plan o portafolio sin borrarlo**
Apaga **Visible en el sitio** y publica. Desaparece de la web y los datos quedan guardados para volver a activarlo.
Si un portafolio se oculta, su dirección muestra "Este portafolio no está disponible por ahora" con enlaces a los demás (no queda un enlace roto).

**Borrar definitivamente**
Menú de los tres puntos → Eliminar. No se puede deshacer desde la web; si se elimina un portafolio, su dirección da error 404.

**Agregar un plan nuevo**
Planes por portafolio → portafolio → botón **+**. Completa nombre, precio y menú. Publica.

**Ordenar**
Campo **Orden**: el número más bajo aparece primero.

**Traducciones**
Si un texto en inglés queda vacío, la web en inglés muestra el texto en español (marcado como español para Google). Si un portafolio no tiene dirección en inglés, no se crea su página en inglés.

**Notas internas**
Los planes con ⚠︎ en la lista tienen una **Nota interna** con algo por confirmar. Esa nota no aparece en la web.

## Trabajo local

Requiere Node 22.12 o superior.

```bash
cd web && npm install && npm run dev     # http://localhost:4321  (usa seed.json si no hay .env)
cd studio && npm install && npm run dev  # http://localhost:3333
```

## Seguridad
- Ninguna clave va en el código. El sitio lee Sanity solo durante la compilación en Netlify; el navegador no recibe tokens.
- El panel exige iniciar sesión con una cuenta invitada al proyecto de Sanity.
- `.env` está en `.gitignore`.

## Decisiones técnicas
- **Astro estático + Sanity + Netlify**, como pedía el brief. Sin servidor ni base de datos propia.
- **Fuentes**: el PDF usa Rexton, Holland Title y Androgy (de pago). La web usa equivalentes libres alojados en el propio sitio: Krona One, DM Sans e Italiana. Si Ana tiene licencia web de las originales, se pueden cambiar en `web/src/styles/global.css`.
- **Ilustraciones**: extraídas del PDF como trazos (no se redibujaron). Están en `web/public/ilustraciones/`.
- **WhatsApp**: todos los botones abren WhatsApp al 312 660 4133 con un mensaje que nombra el portafolio y el plan.
- **Sin formulario**: la cotización va directo a WhatsApp, por decisión del cliente.
