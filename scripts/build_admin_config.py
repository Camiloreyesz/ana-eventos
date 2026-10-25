# Genera web/public/admin/config.yml (configuración del panel Decap CMS).
# Se escribe con Python para no repetir a mano los campos Español / English.
# Uso: python3 scripts/build_admin_config.py
import os, json

REPO = "Camiloreyesz/ana-eventos"

def txt(label, name, required=False, long=False, hint=None):
    """Campo traducible: un grupo con Español y English."""
    w = "text" if long else "string"
    f = {
        "label": label, "name": name, "widget": "object", "collapsed": False, "required": required,
        "summary": "{{fields.es}}",
        "fields": [
            {"label": "Español", "name": "es", "widget": w, "required": required},
            {"label": "English", "name": "en", "widget": w, "required": False},
        ],
    }
    if hint: f["hint"] = hint
    return f

visible = {"label": "Visible en el sitio", "name": "published", "widget": "boolean", "default": True,
           "hint": "Apágalo para ocultarlo de la web sin borrarlo."}
order = {"label": "Orden", "name": "order", "widget": "number", "value_type": "int", "default": 10,
         "hint": "Número menor = aparece primero."}

ILL = [
    {"label": "Omakase (manos y nigiris)", "value": "omakase"},
    {"label": "Corporativos (cubiertos y copa)", "value": "corporativo-dinner"},
    {"label": "Cubiertos sin copa", "value": "corporativo-lunch"},
    {"label": "Eventos (personas brindando)", "value": "eventos"},
    {"label": "Mesa larga (grupos)", "value": "mix-night"},
    {"label": "Brunch (pancakes)", "value": "brunch"},
    {"label": "Celebración (velas y vino)", "value": "celebracion"},
    {"label": "Románticas (foto de fondo)", "value": "romanticas-foto"},
]

def img(label, name, hint=None):
    f = {"label": label, "name": name, "widget": "image", "required": True}
    if hint: f["hint"] = hint
    return f

# Ilustraciones disponibles para las tarjetas de categoría de la portada.
CAT_ILL = [x for x in ILL if x["value"] in ("mix-night", "corporativo-dinner", "corporativo-lunch", "omakase", "celebracion", "eventos", "brunch")]

portada = {
    "name": "portada", "label": "Portada (página de inicio)",
    "description": "Textos y fotos de la página de inicio. Cada texto tiene Español e English.",
    "files": [{
        "name": "portada", "label": "Portada",
        "file": "web/content/portada.json", "format": "json",
        "fields": [
            {"label": "1. Inicio (foto grande)", "name": "hero", "widget": "object", "collapsed": True, "fields": [
                txt("Título", "title", required=True),
                txt("Texto", "intro", long=True),
                img("Foto", "image", "Mejor vertical, mínimo 900 px de ancho."),
                txt("Descripción de la foto (para personas que no la ven)", "imageAlt", required=True),
            ]},
            {"label": "2. Presentación (ilustración y frase)", "name": "presentation", "widget": "object", "collapsed": True, "fields": [
                txt("Frase destacada", "lead", long=True, required=True),
                txt("Texto", "text", long=True),
                img("Ilustración", "image", "Formato horizontal 4:3."),
                txt("Descripción de la imagen", "imageAlt", required=True),
            ]},
            {"label": "3. Experiencias (título de las categorías)", "name": "experiences", "widget": "object", "collapsed": True,
             "hint": "Los nombres y descripciones de las tarjetas se editan en «Categorías».", "fields": [
                txt("Título", "title", required=True),
                txt("Texto", "intro", long=True),
            ]},
            {"label": "4. La noche (música, drinks y comida)", "name": "night", "widget": "object", "collapsed": True, "fields": [
                txt("Título", "title", required=True),
                {"label": "Datos (capacidad, menú, shows…)", "label_singular": "dato", "name": "rows", "widget": "list",
                 "summary": "{{fields.label.es}}: {{fields.value.es}}", "fields": [
                    txt("Etiqueta", "label", required=True, hint="Ej.: Capacidad"),
                    txt("Valor", "value", required=True, hint="Ej.: Hasta 120 personas"),
                ]},
                txt("Nota final", "note", long=True),
                img("Foto izquierda", "photoA", "Vertical 4:5."),
                txt("Descripción de la foto izquierda", "photoAAlt", required=True),
                img("Foto derecha", "photoB", "Vertical 4:5."),
                txt("Descripción de la foto derecha", "photoBAlt", required=True),
            ]},
            {"label": "5. Cata de aguardiente", "name": "tasting", "widget": "object", "collapsed": True, "fields": [
                txt("Título", "title", required=True),
                {"label": "Párrafos", "label_singular": "párrafo", "name": "paragraphs", "widget": "list",
                 "summary": "{{fields.es}}", "fields": [
                    {"label": "Español", "name": "es", "widget": "text"},
                    {"label": "English", "name": "en", "widget": "text", "required": False},
                ]},
                img("Foto", "image", "Vertical."),
                txt("Descripción de la foto", "imageAlt", required=True),
            ]},
            {"label": "6. Franja de tarifa especial", "name": "banner", "widget": "object", "collapsed": True, "fields": [
                {"label": "Mostrar la franja", "name": "visible", "widget": "boolean", "default": True},
                txt("Texto", "text", required=True),
            ]},
            {"label": "7. Contacto y dirección", "name": "contact", "widget": "object", "collapsed": True, "fields": [
                txt("Título", "title", required=True),
                txt("Texto", "text", long=True),
                txt("Zona", "location", required=True, hint="Ej.: Cartagena de Indias, Centro"),
                txt("Dirección", "address", hint="Se muestra bajo la zona. Si lo dejas vacío, no aparece."),
            ]},
        ],
    }],
}

price = {
    "label": "Precios", "label_singular": "precio", "name": "prices", "widget": "list", "collapsed": False,
    "summary": "${{fields.amount}} {{fields.label.es}}",
    "hint": "Si el plan tiene un solo precio, deja un solo ítem sin nombre.",
    "fields": [
        {"label": "Valor", "name": "amount", "widget": "number", "value_type": "int", "min": 0,
         "hint": "Solo el número, sin puntos ni signo. Ej.: 120000"},
        {"label": "Moneda", "name": "currency", "widget": "select", "default": "COP",
         "options": [{"label": "Pesos colombianos (COP)", "value": "COP"}, {"label": "Dólares (USD)", "value": "USD"}]},
        {"label": "Se cobra", "name": "unit", "widget": "select", "default": "perPerson",
         "options": [{"label": "Por persona", "value": "perPerson"}, {"label": "Por pareja", "value": "perCouple"},
                     {"label": "Sin unidad (no mostrar)", "value": "none"}]},
        txt("Nombre del precio", "label", hint='Ej.: "Sin maridaje", "Libra".'),
        txt("Nota", "note", hint='Ej.: "Incluye torta y detalle."'),
    ],
}

section = {
    "label": "Menú", "label_singular": "sección", "name": "sections", "widget": "list",
    "summary": "{{fields.title.es}}",
    "fields": [
        txt("Título de la sección", "title", required=True, hint="Ej.: Entrada, Fuertes, Postre, Bebidas."),
        txt("Nota", "note", hint='Ej.: "1 a elegir", "Para compartir".'),
        {"label": "Ítems", "label_singular": "ítem", "name": "items", "widget": "list", "summary": "{{fields.name.es}}",
         "fields": [
             txt("Nombre", "name", required=True),
             txt("Descripción", "description"),
             txt("Frase en cursiva", "quote"),
         ]},
    ],
}

plan = {
    "label": "Planes", "label_singular": "plan", "name": "plans", "widget": "list",
    "summary": "{{fields.title.es}}",
    "hint": "Arrastra para cambiar el orden.",
    "fields": [
        txt("Nombre del plan", "title", required=True),
        txt("Subtítulo / horario", "subtitle", hint='Ej.: "Domingos a miércoles", "Opción 1".'),
        visible,
        price,
        section,
        {"label": "Nota interna (no se publica)", "name": "internalNote", "widget": "text", "required": False,
         "hint": "Para el equipo: dudas o cambios por confirmar."},
    ],
}

config = {
    "backend": {
        "name": "github",
        "repo": REPO,
        "branch": "main",
        "commit_messages": {
            "create": "Crear {{collection}} “{{slug}}”",
            "update": "Actualizar {{collection}} “{{slug}}”",
            "delete": "Borrar {{collection}} “{{slug}}”",
            "uploadMedia": "Subir imagen “{{path}}”",
            "deleteMedia": "Borrar imagen “{{path}}”",
        },
    },
    # Solo se usa al probar en el computador (localhost); en la web real se ignora.
    "local_backend": True,
    "locale": "es",
    "site_url": "https://ana-eventos.netlify.app",
    "display_url": "https://ana-eventos.netlify.app",
    "logo_url": "/logo-ana.png",
    "media_folder": "web/public/uploads",
    "public_folder": "/uploads",
    "editor": {"preview": False},
    "collections": [
        portada,
        {
            "name": "portafolios", "label": "Portafolios", "label_singular": "Portafolio",
            "description": "Cada portafolio es una página de la web, con sus planes y precios.",
            "folder": "web/content/portafolios", "extension": "json", "format": "json",
            "create": True, "delete": True,
            "slug": "{{fields.slug.es}}", "identifier_field": "title.es",
            "summary": "{{title.es}}",
            "sortable_fields": ["order", "title.es"],
            "fields": [
                txt("Nombre", "title", required=True),
                txt("Etiqueta", "kicker", hint='Texto pequeño bajo el nombre. Ej.: "Menu by Ana".'),
                txt("Introducción", "intro", long=True),
                plan,
                {"label": "Dirección web", "name": "slug", "widget": "object", "collapsed": True,
                 "hint": "Final de la dirección. Evita cambiarla después de publicar: los enlaces ya compartidos dejarían de funcionar.",
                 "fields": [
                     {"label": "Español (/es/portafolios/…)", "name": "es", "widget": "string",
                      "pattern": ["^[a-z0-9-]+$", "Solo minúsculas, números y guiones"]},
                     {"label": "English (/en/portfolios/…)", "name": "en", "widget": "string", "required": False,
                      "pattern": ["^[a-z0-9-]*$", "Solo minúsculas, números y guiones"],
                      "hint": "Si está vacío, no se crea la página en inglés."},
                 ]},
                {"label": "Categoría", "name": "category", "widget": "relation", "collection": "categorias",
                 "search_fields": ["title.es"], "value_field": "{{slug}}", "display_fields": ["title.es"]},
                order,
                visible,
                {"label": "Estilo", "name": "theme", "widget": "select", "default": "olive",
                 "options": [{"label": "Oliva (general)", "value": "olive"}, {"label": "Tinta (corporativo)", "value": "dark"},
                             {"label": "Rojo romántico", "value": "romantic"}]},
                {"label": "Ilustración", "name": "illustration", "widget": "select", "required": False, "options": ILL},
                {"label": "Imagen propia", "name": "image", "widget": "image", "required": False,
                 "hint": "Reemplaza la ilustración. Úsala solo con piezas aprobadas por marca."},
                txt("Descripción para Google", "seoDescription", long=True),
            ],
        },
        {
            "name": "categorias", "label": "Categorías", "label_singular": "Categoría",
            "folder": "web/content/categorias", "extension": "json", "format": "json",
            "create": True, "delete": True,
            "slug": "{{fields.title.es}}", "identifier_field": "title.es",
            "summary": "{{title.es}}",
            "sortable_fields": ["order"],
            "fields": [
                txt("Nombre", "title", required=True), txt("Descripción", "description", long=True),
                {"label": "Ilustración de la tarjeta en la portada", "name": "illustration", "widget": "select",
                 "required": False, "options": CAT_ILL},
                order, visible,
            ],
        },
        {
            "name": "configuracion", "label": "Configuración general",
            "files": [{
                "name": "general", "label": "Datos generales y contacto",
                "file": "web/content/configuracion.json", "format": "json",
                "fields": [
                    {"label": "Nombre del sitio", "name": "siteName", "widget": "string"},
                    {"label": "WhatsApp (con indicativo, solo números)", "name": "whatsappNumber", "widget": "string",
                     "pattern": ["^\\d{10,15}$", "Solo números con indicativo. Ej.: 573126604133"]},
                    {"label": "WhatsApp como se muestra", "name": "whatsappDisplay", "widget": "string", "hint": "Ej.: 312 660 4133"},
                    txt("Inicio del mensaje de WhatsApp", "whatsappMessage",
                        hint='Se completa con el nombre del portafolio. Ej.: "Hola Ana, quiero información sobre"'),
                    {"label": "Instagram (enlace completo)", "name": "instagramUrl", "widget": "string", "required": False},
                    {"label": "Web de Ana (enlace completo)", "name": "webUrl", "widget": "string", "required": False,
                     "hint": "Se muestra como botón «Web de Ana» en el contacto."},
                    txt("Nota del pie de página", "footerNote"),
                    txt("Descripción para Google", "seoDescription", long=True),
                ],
            }],
        },
    ],
}

out = os.path.join(os.path.dirname(__file__), "..", "web", "public", "admin", "config.yml")
os.makedirs(os.path.dirname(out), exist_ok=True)
# JSON es YAML válido; así se evita depender de una librería YAML.
with open(out, "w", encoding="utf-8") as f:
    f.write("# Archivo generado por scripts/build_admin_config.py. Edita el script, no este archivo.\n")
    json.dump(config, f, ensure_ascii=False, indent=2)
    f.write("\n")
print("ok", out)
