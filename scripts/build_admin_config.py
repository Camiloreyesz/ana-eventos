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
            "fields": [txt("Nombre", "title", required=True), txt("Descripción", "description", long=True), order, visible],
        },
        {
            "name": "configuracion", "label": "Configuración general",
            "files": [{
                "name": "general", "label": "Textos generales y contacto",
                "file": "web/content/configuracion.json", "format": "json",
                "fields": [
                    {"label": "Nombre del sitio", "name": "siteName", "widget": "string"},
                    txt("Título de la portada", "heroTitle"),
                    txt("Texto de la portada", "heroIntro", long=True),
                    txt("Frase de marca", "tagline"),
                    {"label": "WhatsApp (con indicativo, solo números)", "name": "whatsappNumber", "widget": "string",
                     "pattern": ["^\\d{10,15}$", "Solo números con indicativo. Ej.: 573126604133"]},
                    {"label": "WhatsApp como se muestra", "name": "whatsappDisplay", "widget": "string", "hint": "Ej.: 312 660 4133"},
                    txt("Inicio del mensaje de WhatsApp", "whatsappMessage",
                        hint='Se completa con el nombre del portafolio. Ej.: "Hola Ana, quiero información sobre"'),
                    {"label": "Instagram (enlace completo)", "name": "instagramUrl", "widget": "string", "required": False},
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
