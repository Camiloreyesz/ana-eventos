# Ana Caribe + Asia · Portafolio de eventos

Sitio web bilingüe (español / inglés) con los portafolios de eventos de Ana y un panel en `/admin` para cambiar precios, planes y textos sin tocar código.

Solo usa **GitHub** y **Netlify**. No hay base de datos ni otro servicio.

```
ana-eventos/
├── web/
│   ├── content/               ← TODO el contenido (lo edita el panel)
│   │   ├── configuracion.json   textos generales y WhatsApp
│   │   ├── categorias/          una categoría por archivo
│   │   └── portafolios/         un portafolio por archivo, con sus planes y precios
│   ├── public/admin/          ← el panel (Decap CMS)
│   ├── public/ilustraciones/  ← ilustraciones extraídas de los PDF
│   └── src/                   ← diseño y páginas (Astro)
├── scripts/build_admin_config.py   genera web/public/admin/config.yml
└── netlify.toml
```

## Cómo funciona

1. Entras a `https://<tu-sitio>/admin/` e inicias sesión con tu cuenta de GitHub.
2. Abres un portafolio, cambias un precio o un plato y pulsas **Publicar → Publicar ahora**.
3. El panel guarda el cambio en GitHub.
4. Netlify detecta el cambio y vuelve a construir la web. Tarda 1 a 2 minutos; no es instantáneo.
5. Recargas la web y ves el cambio.

Mientras no pulses Publicar, nada cambia en la web. El panel conserva lo que estabas editando en ese navegador si cierras sin publicar.

## Rutas

| Página | Español | Inglés |
|---|---|---|
| Inicio | `/es/` | `/en/` |
| Portafolio | `/es/portafolios/<dirección>/` | `/en/portfolios/<dirección>/` |
| Panel | `/admin/` | |
| Raíz `/` | redirige a `/es/` o `/en/` según el idioma del navegador | |

Portafolios (orden de los PDF): brunch · menu-corporativo-almuerzo · menu-corporativo-cena · paquete-de-celebracion · menus-para-eventos · menu-a-elegir · omakase · celebraciones-romanticas.

## Puesta en marcha (una sola vez)

### 1. Conectar Netlify con GitHub
Ya existe el proyecto **ana-eventos** en Netlify, vacío y privado (solo tu equipo de Netlify lo ve).

1. Netlify → **ana-eventos** → Project configuration → Build & deploy → Continuous deployment → **Link repository** → GitHub → `Camiloreyesz/ana-eventos`.
2. Netlify lee `netlify.toml`: carpeta base `web`, comando `npm run build`, salida `dist`. No hay que escribir nada.
3. Rama de producción: `main`. Guarda y espera el primer deploy.

No hacen falta variables de entorno. Opcional: `SITE_URL` con el dominio propio cuando se conecte.

### 2. Activar el inicio de sesión del panel (GitHub OAuth)
1. En GitHub: Settings → Developer settings → **OAuth Apps** → New OAuth App
   (o https://github.com/settings/developers).
   - Application name: `Ana Panel`
   - Homepage URL: `https://ana-eventos.netlify.app`
   - Authorization callback URL: `https://api.netlify.com/auth/done`
2. Copia el **Client ID** y genera un **Client secret** (guárdalo, GitHub no lo vuelve a mostrar).
3. En Netlify: ana-eventos → Project configuration → Security → **OAuth** → Authentication providers → **Install provider** → GitHub → pega ID y secret.
4. Entra a `https://ana-eventos.netlify.app/admin/` → **Iniciar sesión con GitHub**.

Solo pueden entrar las cuentas de GitHub con permiso de escritura en el repositorio. Para sumar a alguien del equipo: GitHub → repositorio → Settings → Collaborators → Add people.

### 3. Hacer pública la web
Mientras el proyecto esté privado, solo tú (con sesión en Netlify) ves la web. Cuando quieras publicarla: Project configuration → Access & security → **Visitor access** → quita la protección.

### 4. Conectar el dominio de Ana (Hostinger)
No hace falta transferir el dominio ni cambiar los nameservers. El correo sigue igual.

1. Recomendado: un **subdominio**, por ejemplo `eventos.dominiodeana.com`, que no toca la web actual.
2. Netlify → Domain management → **Add a domain** → escribe el subdominio.
3. Hostinger → Dominios → DNS / Nameservers → **Administrar registros DNS**:
   - Antes de tocar nada, toma una captura de todos los registros.
   - Agrega un registro **CNAME**: nombre `eventos`, valor `ana-eventos.netlify.app`.
   - **No borres ni edites** registros MX, TXT (SPF, DKIM, DMARC) ni los demás: son del correo y de la web actual.
4. Espera la propagación (de minutos a unas horas). Netlify activa HTTPS solo; revísalo en Domain management → HTTPS.
5. En Netlify → Environment variables agrega `SITE_URL=https://eventos.dominiodeana.com` y vuelve a desplegar.
6. Actualiza `site_url` y `display_url` en `scripts/build_admin_config.py` y genera de nuevo el `config.yml`.

## Guía de uso del panel

**Cambiar un precio**
Portafolios → abre el portafolio → **Planes** → despliega el plan (flecha ›) → **Precios** → **Valor** (solo números, ej. `135000`) → Publicar → Publicar ahora.

**Cambiar un plato o descripción**
Plan → **Menú** → sección (Entrada, Fuertes…) → **Ítems**. Cada texto tiene Español y English.

**Ocultar sin borrar**
Apaga **Visible en el sitio** (en el plan, el portafolio o la categoría) y publica. Los datos quedan guardados para volver a activarlo.
Un portafolio oculto muestra "Este portafolio no está disponible por ahora" con enlaces a los demás, para que no quede un enlace roto.

**Borrar definitivamente**
Botón **Eliminar entrada**. Su dirección pasa a dar error 404. (GitHub conserva el historial, así que se puede recuperar.)

**Agregar un plan**
Dentro del portafolio → Planes → **Add plan**. El orden en la web es el orden de la lista (arrastra para mover).

**Agregar un portafolio**
Portafolios → **+ Portafolio**. Llena nombre, dirección web (solo minúsculas y guiones), categoría, estilo e ilustración.

**Orden de portafolios y categorías**
Campo **Orden**: el número más bajo aparece primero.

**Traducciones**
Si el inglés de un texto queda vacío, la web en inglés muestra el español (marcado como español para Google). Si un portafolio no tiene dirección en inglés, no se crea su página en inglés.

**Notas internas**
Campo "Nota interna" de cada plan: dudas por confirmar. No se publica.

## Trabajo local (opcional)

Requiere Node 22.12 o superior.

```bash
cd web && npm install && npm run dev      # http://localhost:4321
# Panel sin GitHub, sobre los archivos locales:
npx decap-server                          # desde la raíz del repo, en otra terminal
# luego abre http://localhost:4321/admin/
```

Para cambiar los campos del panel: edita `scripts/build_admin_config.py` y ejecuta `python3 scripts/build_admin_config.py`.

## Seguridad
- No hay claves en el código. El inicio de sesión lo hace Netlify con GitHub (OAuth); el secreto queda guardado en Netlify.
- Solo las cuentas de GitHub con permiso de escritura en el repositorio pueden editar.
- El panel tiene `noindex` para que Google no lo muestre.

## Decisiones técnicas
- **Astro estático + Decap CMS + Netlify + GitHub.** Se descartó Sanity para no sumar otro servicio.
- **Fuentes**: el PDF usa Rexton, Holland Title y Androgy (de pago). La web usa equivalentes libres alojadas en el propio sitio: Krona One, DM Sans e Italiana. Si Ana tiene licencia web de las originales, se cambian en `web/src/styles/global.css`.
- **Ilustraciones**: extraídas de los PDF como trazos (no redibujadas).
- **WhatsApp**: todos los botones abren WhatsApp al 312 660 4133 con un mensaje que nombra el portafolio y el plan.
