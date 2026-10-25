# Contexto del proyecto · Web de portafolios de eventos de Ana

*Documento de traspaso. Estado al 25 de octubre de 2026. Léelo antes de trabajar en esta web.*

> ## Enlaces clave
> - **Página para editar el contenido (panel):** https://ana-eventos.netlify.app/admin/
>   Se entra con **Iniciar sesión con GitHub** (cuenta de Camilo: `Camiloreyesz`). Ahí se cambian precios, platos, textos, categorías y el WhatsApp. Al pulsar **Publicar → Publicar ahora**, la web se actualiza en 1–2 minutos.
> - **Web pública:** https://ana-eventos.netlify.app
> - **Código (GitHub):** https://github.com/Camiloreyesz/ana-eventos
> - **Hosting (Netlify):** https://app.netlify.com/projects/ana-eventos

## 1. Qué es

Landing pública y bilingüe (español / inglés) que reúne los **portafolios de eventos de Ana Caribe + Asia**, restaurante del Grupo Empresarial Munay en Cartagena (sede Centro). Reemplaza el envío de 8 PDF por separado: un solo enlace, siempre actualizado, que se ve bien en el celular y lleva al cliente directo a WhatsApp.

- **Responsable:** Camilo Reyes, diseñador gráfico y líder creativo del grupo. Hoy es el único que edita.
- **Web pública:** https://ana-eventos.netlify.app (redirige a `/es/` o `/en/` según el idioma del navegador)
- **Panel de edición:** https://ana-eventos.netlify.app/admin/ (inicio de sesión con GitHub)
- **Código:** https://github.com/Camiloreyesz/ana-eventos (rama `main`)
- **Hosting:** Netlify, proyecto `ana-eventos`

## 2. Estado actual

| Tema | Estado |
|---|---|
| Sitio publicado | ✅ Público. La versión principal está abierta; las versiones de prueba (deploy previews) solo las ve el equipo de Netlify. |
| Despliegue automático | ✅ Cada cambio en `main` de GitHub publica solo en Netlify (1–2 min). |
| Panel `/admin` | ✅ Funciona con login de GitHub (OAuth configurado en Netlify). Probado por Camilo. |
| Contenido | ✅ Revisado contra los 8 PDF separados. No quedan dudas abiertas. |
| Responsive | ✅ Revisado sin desbordes en 16 anchos (320 px a 1440 px). |
| Dominio propio | ⏳ Pendiente de decidir. Recomendado: subdominio tipo `eventos.<dominio de Ana>` vía CNAME en Hostinger. |
| Seguridad | ⚠️ Verificar que el Client secret de la OAuth App de GitHub se rotó (el original se pegó en un chat). |

## 3. Decisiones tomadas (no reabrir sin que Camilo lo pida)

1. **Sin suscripciones ni servicios extra.** Solo GitHub + Netlify. Se descartó Sanity por esto. No proponer CMS de pago, bases de datos ni servidores.
2. **Panel: Decap CMS** (gratis, open source), en `/admin`, con backend GitHub y login vía el proveedor OAuth de Netlify. No usar Netlify Identity + Git Gateway: Git Gateway está en retiro.
3. **Contacto solo por WhatsApp: 312 660 4133** (`573126604133`). Sin formulario. Cada botón abre WhatsApp con el nombre del portafolio y del plan ya escritos. El PDF de Románticas trae otro número (311 391 8067); se decidió usar 312 660 4133 en todo el sitio.
4. **Diseño fiel a los PDF:** gráfico y editorial, con ilustraciones de trazo extraídas de los PDF (no redibujadas). Sin fotos genéricas. Precios y textos son texto real, nunca imágenes.
5. **Bilingüe con rutas separadas:** `/es/portafolios/<slug>/` y `/en/portfolios/<slug>/`. Si falta el inglés de un texto se muestra el español, marcado con `lang="es"`. Precios en COP, sin convertir.
6. **Portafolio oculto ≠ borrado:** si se oculta, su URL muestra "no está disponible por ahora" (con `noindex`) y enlaces a los demás. Si se borra, da 404.

## 4. Contenido vigente

Precios en COP. Fuente: los 8 PDF separados de Camilo (20 oct 2026), con sus ajustes confirmados.

| # | Portafolio (archivo) | Categoría | Planes y precios |
|---|---|---|---|
| 1 | Brunch (`brunch`) | Eventos y grupos | Servido a la mesa $130.000 · Buffet $150.000, por persona |
| 2 | Corporativos · Almuerzo (`menu-corporativo-almuerzo`) | Corporativos | Menú 1 $120.000 · Menú 2 $150.000, por persona. Todos los días de 12:00 a 5:00 p. m. |
| 3 | Corporativos · Cena (`menu-corporativo-cena`) | Corporativos | Menú cena $180.000 por persona. Domingos a miércoles |
| 4 | Paquete de celebración (`paquete-de-celebracion`) | Celebraciones | Tortas: media libra $80.000 · libra $120.000 · libra y media $140.000 (incluyen torta y detalle) |
| 5 | Eventos (`menus-para-eventos`) | Eventos y grupos | Menú 1 $295.000 · Menú 2 $335.000 · Menú 3 $380.000, por persona |
| 6 | Menú a elegir · Grupos (`menu-a-elegir`) | Eventos y grupos | 12 canapés para elegir 6 + 3 cócteles: $335.000 por persona |
| 7 | Omakase (`omakase`) | Experiencias de autor | Metamorfosis en **6 tiempos**: sin maridaje $220.000 · con maridaje de coctelería $280.000, por persona |
| 8 | Celebraciones románticas (`celebraciones-romanticas`) | Celebraciones | Menú de Mar «Mares encendidos» y Menú de Tierra «Fuego y raíces»: $390.000 por pareja cada uno |

Ajustes confirmados por Camilo frente a los PDF:
- **Omakase:** se quitó el tiempo repetido (el Tiempo 5 repetía el 2) y quedó en 6 tiempos. La frase "Blanco sobre blanco" pasó al Tiempo 4. El valor es por persona.
- **Cena:** lleva un solo softdrink (el PDF lo repetía).
- **Eventos:** Menú 1, postre pie de coco con helado. Menú 2, entraña y "Brûlée de maracuyá". Menú 3, postre Oblea Ana.
- **Románticas:** se escribe "togarashi" (no "toharashi"). Las entradas de los dos menús dicen "Elegir una opción para compartir".
- **Almuerzo 2:** "Pesca blanca" es correcto.
- **Ortografía corregida:** croissant, ganache, almendras.

Las traducciones al inglés y los textos de portada y categorías los escribió Claude (incluida la portada nueva). Camilo no los ha revisado a fondo.

## 5. Arquitectura técnica

- **Astro 7**, sitio 100 % estático. Node ≥ 22.12. Dependencias: `astro` y las fuentes `@fontsource` (Krona One, DM Sans, Italiana), alojadas en el propio sitio.
- **Contenido en JSON dentro del repo**, que es lo que edita el panel:
  - `web/content/configuracion.json`: WhatsApp, Instagram, web de Ana, pie, SEO
  - `web/content/portada.json`: textos y fotos de la página de inicio (colección **Portada** del panel); fotos en `web/public/fotos/`
  - `web/content/categorias/*.json`: una categoría por archivo (`title`, `description`, `illustration`, `order`, `published`); cada una tiene su página `/es/categorias/<id>/` y `/en/categories/<id>/`
  - `web/content/portafolios/*.json`: un portafolio por archivo, con `plans[]`, cada plan con `prices[]` y `sections[] → items[]`
  - Todo campo de texto es `{ "es": "...", "en": "..." }`. Precio: `amount` (entero), `currency` (`COP`), `unit` (`perPerson` | `perCouple` | `none`), `label` y `note` opcionales.
- **Panel:** `web/public/admin/index.html` carga Decap CMS 3.17.1 desde unpkg. `web/public/admin/config.yml` **se genera** con `python3 scripts/build_admin_config.py`: edita el script, no el YAML.
- **Lectura del contenido:** `web/src/lib/content.ts` (solo en compilación).
- **Textos fijos de la interfaz** (botones, 404, etc.): `web/src/lib/i18n.ts`.
- **Componentes:** `web/src/components/` (`HomeView`, `CategoryView`, `PortfolioView`, `PortfolioCard`, `PlanCard`, `BookNow`, `Header`, `Footer`). Estilos de la portada en `web/src/styles/home.css`.
- **Rutas:** `web/src/pages/` (`es/`, `en/`, `404`, `sitemap.xml`, `robots.txt`, raíz con redirección).
- **SEO:** canonical, hreflang (es, en, x-default), Open Graph, sitemap con alternates, 404 bilingüe, `noindex` en `/admin` y en portafolios ocultos.
- **Netlify** (`netlify.toml`): base `web`, comando `npm run build`, salida `dist`, Node 22, redirección de `/` por idioma y cabeceras de seguridad.

## 6. Identidad visual

Tomada de los PDF 2026 y del Manual de Marca de Ana (2022).

| Token | Valor | Uso |
|---|---|---|
| `--cream` | `#e5e7d3` | Fondo (color de los PDF) |
| `--paper` / `--cream-soft` | `#f3f4e8` / `#eceedc` | Tarjetas |
| `--ink` | `#2a321a` | Texto y botones (verde muy oscuro del manual) |
| `--olive` | `#6b8756` | Acento (oliva del PDF `#789563`, oscurecido para contraste) |
| `--red` | `#b51d04` | Solo en Celebraciones románticas |

- **Tipografía:** los PDF usan Rexton, Holland Title y Androgy (de pago). En la web se usan sustitutos libres: Krona One para títulos anchos en mayúscula, DM Sans para el cuerpo e Italiana para el título serif de Románticas. Si Ana tiene licencia web de las originales, se cambian en `global.css`.
- **Recursos gráficos:** etiqueta verde con letras espaciadas ("MENU BY [ANA]"), estrella de 4 puntas como viñeta, línea "ANA IS ——— A FEELING", bloque "BOOK NOW" con el teléfono.
- **Temas por portafolio:** `olive` (general), `dark` (corporativos) y `romantic` (rojo, serif, foto tenue de fondo).
- **Archivos:** logo en `web/public/logo-ana.png`. Ilustraciones en `web/public/ilustraciones/`: omakase, corporativo-dinner, corporativo-lunch, eventos, mix-night, brunch, celebracion y romanticas-foto.

## 7. Cómo trabajar en este proyecto

**Cambios de contenido** (precios, platos, textos): los hace Camilo desde el panel https://ana-eventos.netlify.app/admin/, o se editan los JSON y se suben a `main`. Netlify publica en 1–2 minutos.

Ruta típica en el panel para cambiar un precio: **Portafolios** → abrir el portafolio → **Planes** → desplegar el plan (flecha ›) → **Precios** → **Valor** (solo números, ej. `135000`) → **Publicar → Publicar ahora**. Para ocultar sin borrar, apagar **Visible en el sitio**.

**Cambios de diseño o código:**
1. Clonar el repo y ejecutar `cd web && npm install && npm run dev` (http://localhost:4321).
2. Antes de subir, ejecutar `npm run build`, que debe generar 28 páginas sin errores (2 portadas, 8 categorías, 16 portafolios, 404, raíz, sitemap, robots; cambia si se agregan o ocultan portafolios).
3. Revisar el responsive (sin scroll horizontal de 320 a 1440 px) y ambos idiomas.
4. Subir a `main`. No hay ramas de revisión configuradas.

**Panel en local sin GitHub:** ejecutar `npx decap-server` en la raíz y abrir `http://localhost:4321/admin/`.

**Cuidado con:**
- No exponer claves en el repo. El secreto de OAuth vive solo en Netlify.
- El entorno de Claude no puede subir directo a Netlify (red bloqueada). Siempre se publica a través de GitHub.
- La app de Claude tiene permiso de escritura en el repo `Camiloreyesz/ana-eventos`.

## 8. Pendientes e ideas

**Pendientes:**
- Decidir y conectar el dominio propio. Pasos en el README: CNAME en Hostinger sin tocar MX/SPF/DKIM/DMARC y sin cambiar nameservers. Después, `SITE_URL` en Netlify y `site_url` en `build_admin_config.py`.
- Confirmar que el Client secret de la OAuth App se rotó.
- Que Camilo revise las traducciones al inglés.

**Ideas (no aprobadas):** agregar el Instagram de Ana (campo ya disponible en Configuración general), medir clics a WhatsApp, y reutilizar esta misma base para otras landings del grupo (por ejemplo, la de fidelización con Comeback).

## 9. Estilo de trabajo con Camilo

- Español de Colombia, claro y directo, sin tecnicismos innecesarios.
- Dar opciones con una recomendación. Si algo puede salir caro o complicado, decirlo con respeto.
- No inventar datos comerciales: precios, platos y condiciones salen de sus PDF o de su confirmación.
- Al terminar: una o dos frases sobre qué quedó hecho y qué falta.
