# Genera content/seed.json a partir del Portafolio Ana 2026 (PDF).
# Fuente unica del contenido inicial: se usa para la vista previa local
# y para cargar Sanity la primera vez (studio/scripts/seed.mjs).
import json, re, os

def L(es, en=None):
    return {"_type": "localeString", "es": es, "en": en if en is not None else ""}

def slugify(s):
    s = s.lower()
    for a, b in zip("áéíóúñü", "aeiouna"):
        s = s.replace(a, b)
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")

counter = [0]
def key():
    counter[0] += 1
    return f"k{counter[0]:04d}"

def item(name_es, name_en, desc_es="", desc_en="", quote_es="", quote_en=""):
    d = {"_key": key(), "_type": "menuItem", "name": L(name_es, name_en)}
    if desc_es: d["description"] = L(desc_es, desc_en)
    if quote_es: d["quote"] = L(quote_es, quote_en)
    return d

def section(title_es, title_en, items, note_es="", note_en=""):
    s = {"_key": key(), "_type": "menuSection", "title": L(title_es, title_en), "items": items}
    if note_es: s["note"] = L(note_es, note_en)
    return s

def price(amount, unit, label_es="", label_en="", note_es="", note_en=""):
    p = {"_key": key(), "_type": "priceOption", "amount": amount, "currency": "COP", "unit": unit}
    if label_es: p["label"] = L(label_es, label_en)
    if note_es: p["note"] = L(note_es, note_en)
    return p

def ref(id_):
    return {"_type": "reference", "_ref": id_}

BEB_EVENTOS = lambda: section("Bebidas", "Drinks", [
    item("1 cóctel de bienvenida", "1 welcome cocktail"),
    item("1 botella de agua", "1 bottle of water"),
    item("1 copa de vino", "1 glass of wine")])

settings = {
    "_id": "siteSettings", "_type": "siteSettings",
    "siteName": "Ana Caribe + Asia",
    "tagline": L("Ana is a feeling", "Ana is a feeling"),
    "heroTitle": L("Eventos con sabor a Caribe y Asia", "Events with a Caribbean + Asian soul"),
    "heroIntro": L(
        "Menús para celebrar, reunirte y compartir en Cartagena. Elige la experiencia y escríbenos por WhatsApp para reservar.",
        "Menus to celebrate, meet and share in Cartagena. Choose your experience and message us on WhatsApp to book."),
    "whatsappNumber": "573126604133",
    "whatsappDisplay": "312 660 4133",
    "whatsappMessage": L("Hola Ana, quiero información sobre", "Hi Ana, I'd like information about"),
    "footerNote": L("Precios en pesos colombianos (COP). Sujetos a confirmación al reservar.",
                    "Prices in Colombian pesos (COP). Subject to confirmation when booking."),
    "instagramUrl": "",
    "seoDescription": L(
        "Portafolio de eventos de Ana Caribe + Asia en Cartagena: omakase, menús corporativos, brunch, eventos, celebraciones románticas y más.",
        "Ana Caribe + Asia events portfolio in Cartagena: omakase, corporate menus, brunch, events, romantic celebrations and more."),
}

categories = [
    {"_id": "cat-experiencias", "title": L("Experiencias de autor", "Signature experiences"),
     "description": L("Menús de degustación que cuentan la historia del Caribe y Asia en cada tiempo.",
                      "Tasting menus that tell the Caribbean + Asia story course by course."), "order": 1},
    {"_id": "cat-corporativos", "title": L("Corporativos", "Corporate"),
     "description": L("Almuerzos y cenas para equipos, clientes y reuniones de trabajo.",
                      "Lunches and dinners for teams, clients and business meetings."), "order": 2},
    {"_id": "cat-eventos", "title": L("Eventos y reuniones", "Events & gatherings"),
     "description": L("Menús para grupos, noches de canapés y cócteles, y brunch para compartir.",
                      "Group menus, canapé and cocktail nights, and brunch to share."), "order": 3},
    {"_id": "cat-celebraciones", "title": L("Celebraciones", "Celebrations"),
     "description": L("Cenas en pareja y detalles para cumpleaños y fechas especiales.",
                      "Dinners for two and touches for birthdays and special dates."), "order": 4},
]
for c in categories:
    c.update({"_type": "category", "published": True})

portfolios = [
    dict(_id="pf-omakase", title=L("Omakase", "Omakase"), kicker=L("Menu by Ana", "Menu by Ana"),
         slug={"es": "omakase", "en": "omakase"}, category="cat-experiencias", theme="olive", order=1,
         illustration="omakase",
         intro=L("Metamorfosis en 7 tiempos (Caribe – Asia).", "A metamorphosis in 7 courses (Caribbean – Asia).")),
    dict(_id="pf-corporativo", title=L("Menú corporativo", "Corporate menu"), kicker=L("Lunch · Dinner", "Lunch · Dinner"),
         slug={"es": "menu-corporativo", "en": "corporate-menu"}, category="cat-corporativos", theme="dark", order=2,
         illustration="corporativo-dinner",
         intro=L("Dos opciones de almuerzo y una de cena, con entrada, fuerte a elegir, postre y bebidas.",
                 "Two lunch options and one dinner, with starter, choice of main, dessert and drinks.")),
    dict(_id="pf-eventos", title=L("Eventos", "Events"), kicker=L("Menu by Ana", "Menu by Ana"),
         slug={"es": "menus-para-eventos", "en": "event-menus"}, category="cat-eventos", theme="olive", order=3,
         illustration="eventos",
         intro=L("Tres menús especiales para tu evento, con entrada, fuerte a elegir, postre y bebidas.",
                 "Three special menus for your event, with starter, choice of main, dessert and drinks.")),
    dict(_id="pf-mix-night", title=L("The Mix Night", "The Mix Night"), kicker=L("Menu by Ana", "Menu by Ana"),
         slug={"es": "the-mix-night", "en": "the-mix-night"}, category="cat-eventos", theme="olive", order=4,
         illustration="mix-night",
         intro=L("12 opciones de canapés para elegir 6, con 3 cócteles. Piqueo charoleado (o servido a la mesa).",
                 "12 canapé options to choose 6, with 3 cocktails. Passed bites (or served at the table).")),
    dict(_id="pf-brunch", title=L("Brunch", "Brunch"), kicker=L("Menu by Ana", "Menu by Ana"),
         slug={"es": "brunch", "en": "brunch"}, category="cat-eventos", theme="olive", order=5,
         illustration="brunch",
         intro=L("Servido a la mesa o en formato buffet.", "Served at the table or buffet style.")),
    dict(_id="pf-romanticas", title=L("Celebraciones románticas", "Romantic celebrations"),
         kicker=L("Experiencia celebraciones", "Celebration experience"),
         slug={"es": "celebraciones-romanticas", "en": "romantic-celebrations"}, category="cat-celebraciones",
         theme="romantic", order=6, illustration="romanticas-foto",
         intro=L("Dos menús para compartir en pareja: Menú de Mar «Mares encendidos» y Menú de Tierra «Fuego y raíces».",
                 "Two menus to share as a couple: Sea Menu “Mares encendidos” and Land Menu “Fuego y raíces”.")),
    dict(_id="pf-celebracion", title=L("Paquete de celebración", "Celebration package"), kicker=L("By Ana", "By Ana"),
         slug={"es": "paquete-de-celebracion", "en": "celebration-package"}, category="cat-celebraciones",
         theme="olive", order=7, illustration="celebracion",
         intro=L("Tortas para celebrar tu fecha especial. Cada tamaño incluye torta y detalle.",
                 "Cakes to celebrate your special day. Each size includes cake and a special touch.")),
]
for p in portfolios:
    p["_type"] = "portfolio"
    p["published"] = True
    p["category"] = ref(p["category"])

plans = []
def plan(id_, pf, order, title, subtitle, prices, sections, note=""):
    d = {"_id": id_, "_type": "plan", "portfolio": ref(pf), "order": order, "published": True,
         "title": title, "prices": prices, "sections": sections}
    if subtitle: d["subtitle"] = subtitle
    if note: d["internalNote"] = note
    plans.append(d)

# --- OMAKASE ---
plan("plan-omakase", "pf-omakase", 1,
     L("Metamorfosis en 7 tiempos", "Metamorphosis in 7 courses"), L("Caribe – Asia", "Caribbean – Asia"),
     [price(220000, "none", "Sin maridaje", "Without pairing"),
      price(280000, "none", "Con maridaje de coctelería", "With cocktail pairing")],
     [section("7 tiempos", "7 courses", [
        item("Tiempo 1 · El Origen", "Course 1 · The Origin",
             "Base de arroz de sushi, tartar de trucha sellado, teriyaki de tamarindo, ralladura de limón mandarino.",
             "Sushi rice base, seared trout tartare, tamarind teriyaki, mandarin lime zest.",
             "Un bocado semilla: arroz de sushi y trucha, abrazados por tamarindo y cítricos del Caribe.",
             "A seed bite: sushi rice and trout, embraced by tamarind and Caribbean citrus."),
        item("Tiempo 2 · Mares encontrados", "Course 2 · Meeting seas",
             "Ceviche de camarón, leche de tigre de coco, puré de batata.",
             "Shrimp ceviche, coconut tiger's milk, sweet potato purée.",
             "Camarón del Caribe en leche de tigre de coco, con batata y un helado que recuerda la brisa marina.",
             "Caribbean shrimp in coconut tiger's milk, with sweet potato and an ice cream that recalls the sea breeze."),
        item("Tiempo 3 · Raíces y memorias", "Course 3 · Roots and memories",
             "Papa rellena de posta cartagenera en tempura de achiote, alioli de ajo negro, cebolla quemada.",
             "Potato stuffed with Cartagena-style posta in annatto tempura, black garlic aioli, charred onion.",
             "Una memoria costeña vestida de tempura: posta dulce-salada dentro de una papa crujiente, ajo negro y humo.",
             "A coastal memory dressed in tempura: sweet-savory posta inside a crispy potato, black garlic and smoke."),
        item("Tiempo 4 · Fuego en movimiento", "Course 4 · Fire in motion",
             "Maki de pescado blanco y aguacate; cobertura de pescado blanco sellado en mantequilla batayaki; salsa acevichada (mayonesa acevichada de coco).",
             "White fish and avocado maki; topped with white fish seared in batayaki butter; acevichada sauce (coconut acevichada mayo).",
             "Un bocado semilla: arroz de sushi y trucha, abrazados por tamarindo y cítricos del Caribe.",
             "A seed bite: sushi rice and trout, embraced by tamarind and Caribbean citrus."),
        item("Tiempo 5 · Mares encontrados", "Course 5 · Meeting seas",
             "Ceviche de camarón, leche de tigre de coco, puré de batata.",
             "Shrimp ceviche, coconut tiger's milk, sweet potato purée.",
             "Blanco sobre blanco: rollo ligero con baño acevichado, donde Asia y el Caribe se unen con el fuego.",
             "White on white: a light roll with an acevichada glaze, where Asia and the Caribbean meet over fire."),
        item("Tiempo 6 · El Encuentro: ramen caribeño", "Course 6 · The Encounter: Caribbean ramen",
             "Caldo marino de coco y lemongrass, noodles, pescado blanco al panko, huevo marinado en miso, cebolla morada encurtida, aceite de chiles y carcasa.",
             "Coconut and lemongrass sea broth, noodles, panko white fish, miso-marinated egg, pickled red onion, chili oil and carcass.",
             "Ramen de corrientes tropicales: coco, lemongrass y mar de Cartagena.",
             "A ramen of tropical currents: coconut, lemongrass and the Cartagena sea."),
        item("Tiempo 7 · Eterno retorno", "Course 7 · Eternal return",
             "Arroz con leche al jengibre, frutos rojos y crumble.",
             "Ginger rice pudding, red berries and crumble.",
             "Memoria de arroz con leche que vuelve nueva: jengibre, frutos rojos.",
             "A rice pudding memory made new: ginger, red berries."),
     ])],
     note="PENDIENTE: en el PDF el Tiempo 5 repite el Tiempo 2 y la frase del Tiempo 4 repite la del Tiempo 1 ('Blanco sobre blanco' parece ser del Tiempo 4). Confirmar textos y si el valor es por persona.")

# --- CORPORATIVO ---
plan("plan-lunch-1", "pf-corporativo", 1, L("Menú 1 · Lunch", "Menu 1 · Lunch"),
     L("Todos los días, 12:00 p. m. a 5:00 p. m.", "Every day, 12:00 p.m. to 5:00 p.m."),
     [price(120000, "perPerson")],
     [section("Entrada", "Starter", [item("Arepa de arroz crocante", "Crispy rice arepa", "Con costilla ahumada.", "With smoked rib.")]),
      section("Fuertes", "Mains", [
          item("Pechuga en salsa de pimientas", "Chicken breast in pepper sauce", "Con vegetales y papa salteada en finas hierbas.", "With vegetables and potatoes sautéed in fine herbs."),
          item("Arroz al wok", "Wok rice", "Con cerdo salteado al estilo oriental.", "With Asian-style stir-fried pork.")], "1 a elegir", "Choose 1"),
      section("Postre", "Dessert", [item("Torta de banano", "Banana cake", "Con ganache de chocolate negro, crema de ron y almendras.", "With dark chocolate ganache, rum cream and almonds.")]),
      section("Bebidas", "Drinks", [item("1 mocktail de bienvenida", "1 welcome mocktail"), item("1 softdrink", "1 soft drink")])])
plan("plan-lunch-2", "pf-corporativo", 2, L("Menú 2 · Lunch", "Menu 2 · Lunch"),
     L("Todos los días, 12:00 p. m. a 5:00 p. m.", "Every day, 12:00 p.m. to 5:00 p.m."),
     [price(150000, "perPerson")],
     [section("Entrada", "Starter", [item("Canastas de plátano", "Plantain baskets", "Rellenas de salsa criolla y aguacate con queso costeño.", "Filled with criolla sauce and avocado with costeño cheese.")]),
      section("Fuertes", "Mains", [
          item("Costillas ahumadas", "Smoked ribs", "De cerdo con salsa teriyaki, puré de papa y coliflor.", "Pork, with teriyaki sauce, potato and cauliflower purée."),
          item("Pesca blanca", "White fish", "En salsa encocada con vegetales salteados.", "In coconut sauce with sautéed vegetables.")], "1 a elegir", "Choose 1"),
      section("Postre", "Dessert", [item("Enyucado", "Enyucado (cassava cake)")]),
      section("Bebidas", "Drinks", [item("1 mocktail de bienvenida", "1 welcome mocktail"), item("1 copa de vino", "1 glass of wine")])],
     note="Confirmar 'Pesca blanca' (¿pescado blanco?).")
plan("plan-dinner", "pf-corporativo", 3, L("Menú Dinner", "Dinner menu"),
     L("Domingos a miércoles", "Sunday to Wednesday"),
     [price(180000, "perPerson")],
     [section("Entrada", "Starter", [item("Croquetas de titoté", "Titoté croquettes", "Rellenas de salsa criolla y camarón.", "Filled with criolla sauce and shrimp.")]),
      section("Fuertes", "Mains", [
          item("Salmón y humus", "Salmon and hummus", "Glaseado, con humus de frijol palomito, aceite de ajonjolí y mix asiático.", "Glazed, with black-eyed pea hummus, sesame oil and Asian greens."),
          item("Lomo en vino", "Beef loin in wine", "Aromatizado con especias, puré y vegetales salteados.", "Spiced, with purée and sautéed vegetables.")], "1 a elegir", "Choose 1"),
      section("Postre", "Dessert", [item("Pie de coco", "Coconut pie")]),
      section("Bebidas", "Drinks", [item("1 mocktail de bienvenida", "1 welcome mocktail"), item("1 softdrink", "1 soft drink"), item("1 softdrink", "1 soft drink")])],
     note="PENDIENTE: el PDF lista '1 softdrink' dos veces. ¿Son 2 softdrinks o es un error?")

# --- EVENTOS ---
plan("plan-eventos-1", "pf-eventos", 1, L("Menú 1", "Menu 1"), L("Menú especial", "Special menu"), [price(295000, "perPerson")],
     [section("Entrada", "Starter", [item("Satay de pollo y tocineta", "Chicken and bacon satay", "Con melado de panela kogui.", "With Kogui panela syrup.")]),
      section("Fuertes", "Mains", [
          item("Pechuga y taré", "Chicken breast and tare", "En láminas de champiñón, tare de cebolla caramelizada, puré de papa y coliflor.", "With sliced mushrooms, caramelized onion tare, potato and cauliflower purée."),
          item("Salmón encocado", "Coconut salmon", "Con camarón, salsa de coco, chiles y arroz cremoso de cilantro.", "With shrimp, coconut sauce, chilies and creamy cilantro rice.")], "1 opción a elegir", "Choose 1"),
      section("Postre", "Dessert", [item("Torta de banano", "Banana cake", "Con ganache de chocolate negro, crema de ron y almendras.", "With dark chocolate ganache, rum cream and almonds.")]),
      BEB_EVENTOS()],
     note="En el PDF las páginas de Eventos tienen el pie 'OMAKASE. by ana restaurante' (no afecta la web).")
plan("plan-eventos-2", "pf-eventos", 2, L("Menú 2", "Menu 2"), L("Menú especial", "Special menu"), [price(335000, "perPerson")],
     [section("Entrada", "Starter", [item("Ceviche afrutado", "Fruity ceviche", "Camarones con zumo de maracuyá, limón criollo, mango, fresa, kiwi y cebolla roja.", "Shrimp with passion fruit juice, local lime, mango, strawberry, kiwi and red onion.")]),
      section("Fuertes", "Mains", [
          item("Róbalo", "Snook", "Filete de pescado con chimichurri, arroz cremoso de champiñones y miso.", "Fish fillet with chimichurri, creamy mushroom and miso rice."),
          item("Picaña", "Picanha", "Con risoni de miso, ajo y espárragos.", "With miso risoni, garlic and asparagus.")], "1 opción a elegir", "Choose 1"),
      section("Postre", "Dessert", [item("Torta de mandoca", "Mandoca cake", "Con helado de vainilla.", "With vanilla ice cream.")]),
      BEB_EVENTOS()])
plan("plan-eventos-3", "pf-eventos", 3, L("Menú 3", "Menu 3"), L("Menú especial", "Special menu"), [price(380000, "perPerson")],
     [section("Entrada", "Starter", [item("Taco", "Taco", "Con costilla ahumada.", "With smoked rib.")]),
      section("Fuertes", "Mains", [
          item("Lomo al trapo", "Lomo al trapo (cloth-roasted beef loin)", "Con salsa de pimientas, milhoja de papa y vegetales salteados.", "With pepper sauce, potato mille-feuille and sautéed vegetables."),
          item("Timbal de mariscos", "Seafood timbale", "Camarón, calamar, pescado y cola de langosta en salsa cremosa de coco y ají amarillo.", "Shrimp, squid, fish and lobster tail in a creamy coconut and yellow chili sauce.")], "1 opción a elegir", "Choose 1"),
      section("Postre", "Dessert", [item("Merengue y matcha", "Meringue and matcha", "Bizcocho de mandarina, merengue y helado de té matcha.", "Mandarin sponge cake, meringue and matcha tea ice cream.")]),
      BEB_EVENTOS()])

# --- MIX NIGHT ---
plan("plan-mix-night", "pf-mix-night", 1, L("Canapés y cócteles", "Canapés and cocktails"),
     L("12 opciones de canapés para elegir 6, con 3 cócteles", "12 canapé options to choose 6, with 3 cocktails"),
     [price(335000, "perPerson")],
     [section("Canapés", "Canapés", [
        item("Canastilla de plátano", "Plantain basket", "Con cóctel de camarón (o en salsa criolla, salsa de aguacate y queso costeño).", "With shrimp cocktail (or with criolla sauce, avocado sauce and costeño cheese)."),
        item("Satay de lomo y tocineta", "Beef loin and bacon satay", "Glaseado con panela.", "Glazed with panela."),
        item("Tortilla de maíz", "Corn tortilla", "Con costilla de cerdo ahumada.", "With smoked pork rib."),
        item("Lumpias", "Lumpia", "De pechuga, vegetales y chile dulce (o de solo vegetales).", "Chicken, vegetables and sweet chili (or vegetables only)."),
        item("Taco nori", "Nori taco", "Alga tempurizada con arroz para sushi, salmón, atún y cebolla puerro.", "Tempura seaweed with sushi rice, salmon, tuna and leek."),
        item("Croquetas de salmón", "Salmon croquettes", "Con topping de kanikama y mayospicy.", "Topped with kanikama and spicy mayo."),
        item("Mini hamburguesa de salmón", "Mini salmon burger", "Jaiba con queso mozzarella y salsa tártara.", "Crab with mozzarella cheese and tartar sauce."),
        item("Nigiri de salmón", "Salmon nigiri", "Con crema de parmesano (o de tomate seco, quinua y queso crema).", "With parmesan cream (or sun-dried tomato, quinoa and cream cheese)."),
        item("Sushi roll: spicy tuna", "Sushi roll: spicy tuna", "3 unidades.", "3 pieces."),
        item("Papa rellena de posta cartagenera", "Potato stuffed with Cartagena-style posta", "Con alioli de ajo.", "With garlic aioli."),
        item("Ceviche afrutado", "Fruity ceviche", "Camarón, fresa, kiwi, mango, cebolla y zumo de maracuyá.", "Shrimp, strawberry, kiwi, mango, onion and passion fruit juice."),
        item("Di búfala", "Di bufala", "Tomate, queso mozzarella, pesto y jamón serrano con reducción de balsámico.", "Tomato, mozzarella, pesto and serrano ham with balsamic reduction."),
      ], "Elegir 6 opciones", "Choose 6"),
      section("Cócteles", "Cocktails", [item("Mojito", "Mojito"), item("Mezcal paloma", "Mezcal paloma"), item("Lemon drop", "Lemon drop"), item("Gin tonic", "Gin & tonic")], "Elegir 3 opciones", "Choose 3")])

# --- BRUNCH ---
plan("plan-brunch-mesa", "pf-brunch", 1, L("Servido a la mesa", "Served at the table"), L("Opción 1", "Option 1"), [price(130000, "perPerson")],
     [section("Incluye", "Includes", [
        item("Pan de bono, croissant, pan integral", "Pan de bono, croissant, whole wheat bread"),
        item("Mantequilla y mermelada", "Butter and jam"),
        item("Tostada con jamón, queso y aguacate", "Toast with ham, cheese and avocado"),
        item("Omelette ranchero criollo", "Ranchero criollo omelette"),
        item("Bowl de granola", "Granola bowl"),
        item("Mimosa", "Mimosa"),
        item("Café, latte, té", "Coffee, latte, tea"),
        item("Jugo de estación", "Seasonal juice")])])
plan("plan-brunch-buffet", "pf-brunch", 2, L("Buffet", "Buffet"), L("Opción 1", "Option 1"), [price(150000, "perPerson")],
     [section("Incluye", "Includes", [
        item("Pan de bono, croissant, pan integral", "Pan de bono, croissant, whole wheat bread"),
        item("Frutas de estación", "Seasonal fruit"),
        item("Arepa de maíz y queso", "Corn and cheese arepa"),
        item("Mini carimañolas de queso y empanadas de carne", "Mini cheese carimañolas and beef empanadas"),
        item("Satay de pollo", "Chicken satay"),
        item("Mimosa", "Mimosa"),
        item("Café, latte, té", "Coffee, latte, tea"),
        item("Jugo de estación", "Seasonal juice")])])

# --- ROMANTICAS ---
BEB_ROM = lambda: section("Bebidas", "Drinks", [item("Mocktail de bienvenida", "Welcome mocktail"), item("2 copas de vino", "2 glasses of wine")])
plan("plan-menu-mar", "pf-romanticas", 1, L("Menú de Mar", "Sea Menu"), L("«Mares encendidos»", "“Mares encendidos”"),
     [price(390000, "perCouple")],
     [section("Entradas", "Starters", [
        item("Ostra en batayaki y encocado de kimchi (2 und.)", "Oyster in batayaki with kimchi encocado (2 pcs)",
             "Ostra tibia sellada en mantequilla batayaki, terminada con un encocado ligero infusionado en kimchi, limón mandarino.",
             "Warm oyster seared in batayaki butter, finished with a light kimchi-infused coconut sauce, mandarin lime."),
        item("Nigiri dúo del Caribe (4 und.)", "Caribbean nigiri duo (4 pcs)",
             "Atún + mayo de soya y togarashi. Salmón sellado + mantequilla parmesano + ralladura de limón tropical.",
             "Tuna + soy mayo and togarashi. Seared salmon + parmesan butter + tropical lime zest.")],
        "Elegir una opción para compartir", "Choose one to share"),
      section("Fuerte", "Main", [item("Pasta Renacer", "Pasta Renacer",
             "Pasta fresca teñida en coral (salsa roja de ají dulce, tomate y chorizo), coronada con queso costeño y langostinos en mantequilla de gochujang y un toque de limón kaffir.",
             "Fresh pasta dyed coral (red sauce of sweet pepper, tomato and chorizo), topped with costeño cheese and prawns in gochujang butter with a hint of kaffir lime.")],
             "Para compartir", "To share"),
      section("Postre", "Dessert", [item("Pie de coco", "Coconut pie", "Cremoso pie de coco, crema montada de ron, coco tostado.", "Creamy coconut pie, rum whipped cream, toasted coconut.")]),
      BEB_ROM()],
     note="El PDF dice 'toharashi'; se escribió 'togarashi'. Confirmar.")
plan("plan-menu-tierra", "pf-romanticas", 2, L("Menú de Tierra", "Land Menu"), L("«Fuego y raíces»", "“Fuego y raíces”"),
     [price(390000, "perCouple")],
     [section("Entradas", "Starters", [
        item("Gyoza de cerdo o pollo (4 und.)", "Pork or chicken gyoza (4 pcs)", "Fritas, rellenas de vegetales, con salsa ponzu.", "Fried, filled with vegetables, with ponzu sauce."),
        item("Nigiri de tierra (2 und.)", "Land nigiri (2 pcs)", "Res angus sellada + mayo de ajo negro + trufa.", "Seared Angus beef + black garlic mayo + truffle.")]),
      section("Fuerte", "Main", [item("Pasta estilo tobanyaki", "Tobanyaki-style pasta",
             "Pasta fresca en crema con hongos shiitake y setas caribeñas, perfumada con trufa, terminada con lomo en mantequilla batayaki.",
             "Fresh pasta in cream with shiitake and Caribbean mushrooms, scented with truffle, finished with beef loin in batayaki butter.")],
             "Para compartir", "To share"),
      section("Postre", "Dessert", [item("Postre de banano y café (2 und.)", "Banana and coffee dessert (2 pcs)",
             "Torta de banana bañada en café con ganache de chocolate, almendras y crema montada de ron.",
             "Banana cake soaked in coffee with chocolate ganache, almonds and rum whipped cream.")]),
      BEB_ROM()],
     note="En el PDF las entradas del Menú de Tierra no dicen 'elegir una opción'. Confirmar si se sirven ambas.")

# --- CELEBRACION ---
plan("plan-tortas", "pf-celebracion", 1, L("Tortas", "Cakes"), None,
     [price(80000, "none", "Media libra", "Half pound", "Incluye torta y detalle.", "Includes cake and a special touch."),
      price(120000, "none", "Libra", "One pound", "Incluye torta y detalle.", "Includes cake and a special touch."),
      price(140000, "none", "Libra y media", "Pound and a half", "Incluye torta y detalle.", "Includes cake and a special touch.")],
     [section("Sabores", "Flavors", [item("Chocolate", "Chocolate"), item("Zanahoria", "Carrot"), item("Naranja", "Orange")]),
      section("Crema", "Frosting", [item("Ganache de chocolate negro", "Dark chocolate ganache"), item("Crema con frutos rojos", "Red berry cream"), item("Crema cítrica", "Citrus cream")])])

for p in plans:
    if p.get("subtitle") is None: p.pop("subtitle", None)

out = {"settings": settings, "categories": categories, "portfolios": portfolios, "plans": plans}
path = os.path.join(os.path.dirname(__file__), "..", "content", "seed.json")
with open(path, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
print("ok", len(categories), len(portfolios), len(plans))
