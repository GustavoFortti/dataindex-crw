import re
from copy import deepcopy

from src.lib.utils.text_functions import clean_text


def get_synonyms(component_list):
    keywords_list = []
    for component, attributes in component_list.items():
        keywords_list.append(attributes.get("synonyms"))
    return keywords_list

def get_word_index_in_text(word, text, add_space_firts):
    text_temp = deepcopy(text)
    word_clean = clean_text(word, False, False, False, True, False)
    space = " " if not add_space_firts else ""
    matches = re.finditer(space + word_clean, text_temp)

    locations = []
    for match in matches:
        start_index = match.start()
        locations.append(start_index)

    return locations

def get_back_words(text_accents, locations):
    size_max = 30
    slice_min = lambda value: value if value >= 0 else 0
    back_words = []
    for location in locations:
        start = slice_min(location - size_max)

        back_words_aux = (text_accents[start:location].replace("\n", ""))
        back_words_aux = [i for i in back_words_aux.split(" ") if i != '']
        back_words.append(back_words_aux)

    return back_words

def find_synonym_in_wordlist(word, wordlist):
    for values in wordlist.values():
        synonym = values['synonym']
        if (word in synonym):
            return synonym

def remove_prepositions_pronouns(text, pronouns):
    pronouns = set(pronouns)

    for pronoun in pronouns:
        space_pronoun = " " * len(pronoun)
        text = text.replace(pronoun, space_pronoun)
    
    return text

BLACK_LIST = [
    "regata",
    "camiseta",
    "coqueteleira",
    "mochila",
    "garraf",
    "bone",
    "marmita",
    "marmiteira",
    "galao",
    "baby look",
    "mascara",
    "porta capsulas",
    "shoulder bag",
    "frisbee",
    "bottle",
    "shorts",
    "jaqueta",
    "calça",
    "legging",
    "blusa",
    "top dux",
    "viseira",
    "bermuda",
    "necessaire",
    "bolsa",
    "moletom"
]

SUPPLEMENT_COMPONENT_LIST = {
    "nac": {
        "synonyms": [
            "acetil",
            "nacetil",
            "n acetil",
            "cisteina",
            "l cisteina",
            "lcisteina",
            "nac",
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "NAC",
    },
    "albumina": {
        "synonyms": [
            "albumina",
            "albumin",
            "albumi",
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "albumina",
    },
    "alfajor": {
        "synonyms": [
            "alfajor"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "alfajor",
    },
    "alho": {
        "synonyms": [
            "alho"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "alho",
    },
    "aminoacido": {
        "synonyms": [
            "aminoacido"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "aminoácido",
    },
    "antioxidante": {
        "synonyms": [
            "antioxidante",
            "antiox"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "antioxidante",
    },
    "arginin": {
        "synonyms": [
            "arginin",
            "arginine",
            "arginina"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "arginina",
    },
    "astaxantina": {
        "synonyms": [
            "astaxantina"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "astaxantina",
    },
    "barrinha": {
        "synonyms": [
            "barrinha",
            "barra",
            "bar",
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "barrinha",
    },
    "batata doce": {
        "synonyms": [
            "batata doce"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "batata doce",
    },
    "bcaa": {
        "synonyms": [
            "bcaa",
            "bca"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "BCAA",
    },
    "beauty": {
        "synonyms": [
            "beauty",
            "beleza"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "beleza",
    },
    "beef": {
        "synonyms": [
            "beef",
            "carn",
            "carne"
        ],
        "conflict": ["carnitin"],
        "exact_term": True,
        "brazil": "carne",
    },
    "betaalanina": {
        "synonyms": [
            "beta alanina",
            "betaalanina",
            "alanina",
            "alanine"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "beta-alanina",
    },
    "betacaroteno": {
        "synonyms": [
            "betacaroteno"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "betacaroteno",
    },
    "biotina": {
        "synonyms": [
            "biotina"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "biotina",
    },
    "blend": {
        "synonyms": [
            "blend",
            "mistura"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "mistura",
    },
    "borragem": {
        "synonyms": [
            "borragem"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "borragem",
    },
    "cafein": {
        "synonyms": [
            "cafein",
            "cafe",
            "cafeina",
            "coffe",
            "caffe",
            "coffee"
        ],
        "conflict": [
        ],
        "exact_term": False,
        "brazil": "cafeína",
    },
    "termogenico": {
        "synonyms": [
            "termogenico",
            "termogênico",
            "termogenicos",
            "termogênicos",
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "termogênico",
    },
    "tcm": {
        "synonyms": [
            "tcm",
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "TCM",
    },
    "calcio": {
        "synonyms": [
            "calcio"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "cálcio",
    },
    "carboidrato": {
        "synonyms": [
            "carboidrato",
            "carbohidrato",
            "carbohydrate",
            "kohlenhydrat",
            "carboidrati",
            "carbo",
            "karbohydrat",
            "glucide",
            "carbohydrates",
            "carbs",
            "carb",
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "carboidrato",
    },
    "carnitin": {
        "synonyms": [
            "carnitin",
            "carnitina",
            "lcarnitina",
            "l carnitina",
            "l carn",
        ],
        "conflict": ["beef"],
        "exact_term": False,
        "brazil": "carnitina",
    },
    "cartamo": {
        "synonyms": [
            "cartamo"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "cártamo",
    },
    "caseinato": {
        "synonyms": [
            "caseinato"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "caseinato",
    },
    "cha": {
        "synonyms": [
            "cha"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "chá",
    },
    "chaverde": {
        "synonyms": [
            "chaverde",
            "cha verde"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "chá verde",
    },
    "chia": {
        "synonyms": [
            "chia"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "chia",
    },
    "cistein": {
        "synonyms": [
            "cistein",
            "lcisteina"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "cisteína",
    },
    "colageno": {
        "synonyms": [
            "colageno",
            "colagen"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "colágeno",
    },
    "vitamina b": {
        "synonyms": [
            "complexo b",
            "vitamina b"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "vitamina B",
    },
    "concentrad": {
        "synonyms": [
            "wpc",
            "concentrad",
            "concentrado"
        ],
        "conflict": [],
        "exact_term": True,
        "brazil": "concentrado",
    },
    "po": {
        "synonyms": [
            "po",
            "em po"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "pó",
    },
    "crunch": {
        "synonyms": ["crunch", "crunchy", "crunch flavor", "crunch powder"],
        "conflict": [],
        "exact_term": False,
        "brazil": "crunch"
    },
    "creatina": {
        "synonyms": [
            "creatina",
            "creatine",
            "creatin",
            "creapure"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "creatina",
    },
    "crisp": {
        "synonyms": [
            "crisp"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "crisp",
    },
    "cromo": {
        "synonyms": [
            "cromo",
            "cromo"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "cromo",
    },
    "curcuma": {
        "synonyms": [
            "curcuma",
            "acafrao"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "cúrcuma",
    },
    "dextrose": {
        "synonyms": [
            "dextrose",
            "maltodextrose"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "dextrose",
    },
    "dribose": {
        "synonyms": [
            "dribose",
            "d ribose",
            "ribose",
            "dribose"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "ribose",
    },

    "ervilha": {
        "synonyms": [
            "ervilha",
            "pea"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "ervilha",
    },
    "espirulina": {
        "synonyms": [
            "espirulina"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "espirulina",
    },
    "fibra": {
        "synonyms": [
            "fibra"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "fibra",
    },
    "fosfatidilserina": {
        "synonyms": [
            "fosfatidilserina"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "fosfatidilserina",
    },
    "frutose": {
        "synonyms": [
            "frutose"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "frutose",
    },
    "gengibre": {
        "synonyms": [
            "gengibre"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "gengibre",
    },
    "gergelim": {
        "synonyms": [
            "gergelim"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "gergelim",
    },
    "glutamin": {
        "synonyms": [
            "glutamin",
            "glutamine",
            "glutamina",
            "lglutamina"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "glutamina",
    },
    "hair": {
        "synonyms": [
            "hair",
            "cabelo"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "cabelo",
    },
    "hialuronico": {
        "synonyms": [
            "hialuronico"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "hialurônico",
    },
    "hidrolisad": {
        "synonyms": [
            "hidrolisad",
            "hidrolisado",
            "hydro",
            "wph"
        ],
        "conflict": [],
        "exact_term": True,
        "brazil": "hidrolisado",
    },
    "churros": {
        "synonyms": [
            "churros",
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "churros",
    },
    "hmb": {
        "synonyms": [
            "hmb",
            "hydroxymethylbutyrate"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "HMB",
    },
    "imune": {
        "synonyms": [
            "imune",
            "imunidade"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "imunidade",
    },
    "iso": {
        "synonyms": [
            "iso",
            "wpi",
            "isolado",
            "isolate",
            "isolada"
        ],
        "conflict": [],
        "exact_term": True,
        "brazil": "isolado",
    },
    "kit": {
        "synonyms": [
            "kit",
            "combo",
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "kit",
    },
    "krill": {
        "synonyms": [
            "krill"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "krill",
    },
    "lecitina": {
        "synonyms": [
            "lecitina"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "lecitina",
    },
    "leucin": {
        "synonyms": [
            "leucin",
            "leucine",
            "lleucine"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "leucina",
    },
    "levagen": {
        "synonyms": [
            "levagen"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "levagen",
    },
    "linhaca": {
        "synonyms": [
            "linhaca"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "linhaça",
    },
    "maca peruana": {
        "synonyms": [
            "maca peruana"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "maca peruana",
    },
    "magnesio": {
        "synonyms": [
            "magnesio",
            "magnesi"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "magnésio",
    },
    "malto": {
        "synonyms": [
            "malto",
            "dextrina",
            "maltodextrina",
            "maltodextrin"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "maltodextrina",
    },
    "mass": {
        "synonyms": [
            "mass",
            "hipercalorico"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "Hipercalórico",
    },
    "melatonina": {
        "synonyms": [
            "melatonina",
            "melatonina",
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "melatonina",
    },
    "monohidratada": {
        "synonyms": [
            "monohidratada"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "monohidratada",
    },
    "creapure": {
        "synonyms": [
            "creapure"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "creapure",
    },
    "multivitaminico": {
        "synonyms": [
            "multivitaminico",
            "polivitaminico"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "multivitamínico",
    },
    "mineral": {
        "synonyms": [
            "minerai",
            "mineral",
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "mineral",
    },
    "nail": {
        "synonyms": [
            "nail",
            "unha"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "unha",
    },
    "oleo": {
        "synonyms": [
            "oleo"
        ],
        "conflict": [
            "oleo de coco"
        ],
        "exact_term": False,
        "brazil": "óleo",
    },
    "oleo de coco": {
        "synonyms": [
            "oleo de coco"
        ],
        "conflict": [
            "coco"
        ],
        "exact_term": False,
        "brazil": "óleo de coco",
    },
    "ketchup": {
        "synonyms": [
            "ketchup"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "ketchup",
    },
    "barbecue": {
        "synonyms": [
            "barbecue"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "barbecue",
    },
    "mostarda": {
        "synonyms": [
            "mostarda"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "mostarda",
    },
    "maionese": {
        "synonyms": [
            "maionese"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "maionese",
    },
    "optimsm": {
        "synonyms": [
            "optimsm"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "optimsm",
    },
    "palatinose": {
        "synonyms": [
            "palatinose",
            "isomaltulose"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "palatinose",
    },
    "enzima": {
        "synonyms": [
            "enzima",
            "enzimas",
            "enzyme",
            "enzymes"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "enzima",
    },
    "protease": {
        "synonyms": [
            "protease",
            "proteasa",
            "protease"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "protease",
    },
    "propolis": {
        "synonyms": [
            "propolis",
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "própolis",
    },
    "lactase": {
        "synonyms": [
            "lactase",
            "lactasa",
            "lactase"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "lactase",
    },
    "lipase": {
        "synonyms": [
            "lipase",
            "lipasa",
            "lipase"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "lipase",
    },
    "bromelina": {
        "synonyms": [
            "bromelina",
            "bromelain",
            "bromelina"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "bromelina",
    },
    "amilase": {
        "synonyms": [
            "amilase",
            "amylase",
            "amilasa"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "amilase",
    },
    "manteiga de amendoim": {
        "synonyms": [
            "pasta de amendoim",
            "manteiga de amendoim",
            "peanut butter",
            "peanutbutter",
            "peanut butter flavor"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "pasta de amendoim"
    },
    "amendoim": {
        "synonyms": [
            "amendoim",
            "peanut",
            "almonds",
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "amendoim"
    },
    "omega 3": {
        "synonyms": [
            "peixe",
            "dha",
            "epa",
            "omega 3",
            "omega",
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "ômega 3",
    },
    "omega 6": {
        "synonyms": [
            "omega 6",
            "linoléico",
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "ômega 6",
    },
    "picolinato": {
        "synonyms": [
            "picolinato",
            "picolinato"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "picolinato",
    },
    "pretreino": {
        "synonyms": [
            "pretreino",
            "pre treino",
            "pre-treino",
            "workout",
            "work out",
            "pretrein",
            "pre trein",
            "preworkout",
            "pre workout"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "pré-treino",
    },
    "primula": {
        "synonyms": [
            "primula"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "prímula",
    },
    "propoli": {
        "synonyms": [
            "propoli"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "própolis",
    },
    "sache": {
        "synonyms": ["sache", "saco", "sachet"],
        "conflict": [],
        "exact_term": False,
        "brazil": "sache"
    },
    "protein": {
        "synonyms": [
            "protein",
            "proteina",
            "proteica"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "proteina",
    },
    "psyllium": {
        "synonyms": [
            "psyllium"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "psílio",
    },
    "quitosana": {
        "synonyms": [
            "quitosana"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "quitosana",
    },
    "resveratrol": {
        "synonyms": [
            "resveratrol"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "resveratrol",
    },
    "rice": {
        "synonyms": [
            "rice",
            "arroz"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "arroz",
    },
    "semente": {
        "synonyms": [
            "semente"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "semente",
    },
    "skin": {
        "synonyms": [
            "skin",
            "pele"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "pele",
    },
    "soy": {
        "synonyms": [
            "soy",
            "soja"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "soja",
    },
    "spirulina": {
        "synonyms": [
            "spirulina"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "spirulina",
    },
    "taurina": {
        "synonyms": [
            "taurina",
            "taurine",
            "taurin"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "taurina",
    },
    "tempero": {
        "synonyms": [
            "tempero"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "tempero",
    },
    "testofen": {
        "synonyms": [
            "testofen"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "testofen",
    },
    "tyrosin": {
        "synonyms": [
            "tyrosin",
            "tirosin",
            "tyrosine",
            "tirosina",
            "tirosine",
            "l tyrosine",
            "ltyrosine",
            "l tirosina",
            "l tirosine",
            "ltirosina",
            "ltirosine",
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "tirosina",
    },
    "transresveratrol": {
        "synonyms": [
            "transresveratrol",
            "trans resveratrol"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "trans-resveratrol",
    },
    "triptofano": {
        "synonyms": [
            "triptofano"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "triptofano",
    },
    "leucina": {
        "synonyms": [
            "leucina"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "leucina",
    },
    "valina": {
        "synonyms": [
            "valina"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "valina",
    },
    "isoleucina": {
        "synonyms": [
            "isoleucina"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "isoleucina",
    },
    "lisina": {
        "synonyms": [
            "lisina"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "lisina",
    },
    "fenilalanina": {
        "synonyms": [
            "fenilalanina"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "fenilalanina",
    },
    "treonina": {
        "synonyms": [
            "treonina"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "treonina",
    },
    "metionina": {
        "synonyms": [
            "metionina"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "metionina",
    },
    "silimarina": {
        "synonyms": [
            "silimarina"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "silimarina",
    },
    "histidina": {
        "synonyms": [
            "histidina",
            "lhistidina",
            "l histidina"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "histidina",
    },
    "veg": {
        "synonyms": [
            "veg",
            "vegan",
            "vegano",
            "vegie",
            "vegana"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "vegano",
    },
    "vegetarian": {
        "synonyms": [
            "vegetarian",
            "vegetariano",
            "vegetariana",
            "veggie",
            "vegetarianismo"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "vegetariano",
    },
    "verisol": {
        "synonyms": [
            "verisol"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "verisol",
    },
    "vitamina": {
        "synonyms": [
            "vitamina",
            "vitaminas",
            "vitamin"
        ],
        "conflict": [
            "vitamina a",
            "vitamina b1",
            "vitamina b10",
            "vitamina b11",
            "vitamina b12",
            "vitamina b13",
            "vitamina b15",
            "vitamina b17",
            "vitamina b2",
            "vitamina b22",
            "vitamina b3",
            "vitamina b4",
            "vitamina b5",
            "vitamina b6",
            "vitamina b7",
            "vitamina b8",
            "vitamina b9",
            "vitamina c",
            "vitamina d",
            "vitamina e",
            "vitamina f",
            "vitamina g",
            "vitamina h",
            "vitamina j",
            "vitamina k",
            "vitamina k1",
            "vitamina k2",
            "vitamina k7",
            "vitamina q"
        ],
        "exact_term": False,
        "brazil": "vitamina",
    },
    "vitamina a": {
        "synonyms": [
            "vitamina a",
            "vitaminas a",
            "retinol",
            "retinal",
            "ácido retinoico"
        ],
        "conflict": ["vitamina"],
        "exact_term": False,
        "brazil": "vitamina A",
    },
    "vitamina b1": {
        "synonyms": [
            "vitamina b1",
            "vitaminas b1",
            "tiamina"
        ],
        "conflict": [
            "vitamina",
            "vitamina b10",
            "vitamina b11",
            "vitamina b12",
            "vitamina b13",
            "vitamina b15",
            "vitamina b17",
            "vitamina b2",
            "vitamina b22",
            "vitamina b3",
            "vitamina b4",
            "vitamina b5",
            "vitamina b6",
            "vitamina b7",
            "vitamina b8",
            "vitamina b9"
        ],
        "exact_term": False,
        "brazil": "vitamina B1",
    },
    "vitamina b10": {
        "synonyms": [
            "vitamina b10",
            "vitaminas b10",
            "paraaminobenzoico"
        ],
        "conflict": [
            "vitamina",
            "vitamina b1",
            "vitamina b11",
            "vitamina b12",
            "vitamina b13",
            "vitamina b15",
            "vitamina b17",
            "vitamina b2",
            "vitamina b22",
            "vitamina b3",
            "vitamina b4",
            "vitamina b5",
            "vitamina b6",
            "vitamina b7",
            "vitamina b8",
            "vitamina b9"
        ],
        "exact_term": False,
        "brazil": "vitamina B10",
    },
    "vitamina b11": {
        "synonyms": [
            "vitamina b11",
            "vitaminas b11",
            "salicilico"
        ],
        "conflict": [
            "vitamina",
            "vitamina b1",
            "vitamina b10",
            "vitamina b12",
            "vitamina b13",
            "vitamina b15",
            "vitamina b17",
            "vitamina b2",
            "vitamina b22",
            "vitamina b3",
            "vitamina b4",
            "vitamina b5",
            "vitamina b6",
            "vitamina b7",
            "vitamina b8",
            "vitamina b9"
        ],
        "exact_term": False,
        "brazil": "vitamina B11",
    },
    "vitamina b12": {
        "synonyms": [
            "vitamina b12",
            "vitaminas b12",
            "cobalamina"
        ],
        "conflict": [
            "vitamina",
            "vitamina b1",
            "vitamina b10",
            "vitamina b11",
            "vitamina b13",
            "vitamina b15",
            "vitamina b17",
            "vitamina b2",
            "vitamina b22",
            "vitamina b3",
            "vitamina b4",
            "vitamina b5",
            "vitamina b6",
            "vitamina b7",
            "vitamina b8",
            "vitamina b9"
        ],
        "exact_term": False,
        "brazil": "vitamina B12",
    },
    "vitamina b13": {
        "synonyms": [
            "vitamina b13",
            "vitaminas b13",
            "orotico"
        ],
        "conflict": [
            "vitamina",
            "vitamina b1",
            "vitamina b10",
            "vitamina b11",
            "vitamina b12",
            "vitamina b15",
            "vitamina b17",
            "vitamina b2",
            "vitamina b22",
            "vitamina b3",
            "vitamina b4",
            "vitamina b5",
            "vitamina b6",
            "vitamina b7",
            "vitamina b8",
            "vitamina b9"
        ],
        "exact_term": False,
        "brazil": "vitamina B13",
    },
    "vitamina b15": {
        "synonyms": [
            "vitamina b15",
            "vitaminas b15",
            "pangamico"
        ],
        "conflict": [
            "vitamina",
            "vitamina b1",
            "vitamina b10",
            "vitamina b11",
            "vitamina b12",
            "vitamina b13",
            "vitamina b17",
            "vitamina b2",
            "vitamina b22",
            "vitamina b3",
            "vitamina b4",
            "vitamina b5",
            "vitamina b6",
            "vitamina b7",
            "vitamina b8",
            "vitamina b9"
        ],
        "exact_term": False,
        "brazil": "vitamina B15",
    },
    "vitamina b17": {
        "synonyms": [
            "vitamina b17",
            "vitaminas b17",
            "amigdalina"
        ],
        "conflict": [
            "vitamina",
            "vitamina b1",
            "vitamina b10",
            "vitamina b11",
            "vitamina b12",
            "vitamina b13",
            "vitamina b15",
            "vitamina b2",
            "vitamina b22",
            "vitamina b3",
            "vitamina b4",
            "vitamina b5",
            "vitamina b6",
            "vitamina b7",
            "vitamina b8",
            "vitamina b9"
        ],
        "exact_term": False,
        "brazil": "vitamina B17",
    },
    "vitamina b2": {
        "synonyms": [
            "vitamina b2",
            "vitaminas b2",
            "riboflavina"
        ],
        "conflict": [
            "vitamina",
            "vitamina b1",
            "vitamina b10",
            "vitamina b11",
            "vitamina b12",
            "vitamina b13",
            "vitamina b15",
            "vitamina b17",
            "vitamina b22",
            "vitamina b3",
            "vitamina b4",
            "vitamina b5",
            "vitamina b6",
            "vitamina b7",
            "vitamina b8",
            "vitamina b9"
        ],
        "exact_term": False,
        "brazil": "vitamina B2",
    },
    "vitamina b22": {
        "synonyms": [
            "vitamina b22",
            "vitaminas b22",
            "ratanhia"
        ],
        "conflict": [
            "vitamina",
            "vitamina b1",
            "vitamina b10",
            "vitamina b11",
            "vitamina b12",
            "vitamina b13",
            "vitamina b15",
            "vitamina b17",
            "vitamina b2",
            "vitamina b3",
            "vitamina b4",
            "vitamina b5",
            "vitamina b6",
            "vitamina b7",
            "vitamina b8",
            "vitamina b9"
        ],
        "exact_term": False,
        "brazil": "vitamina B22",
    },
    "vitamina b3": {
        "synonyms": [
            "vitamina b3",
            "vitaminas b3",
            "niacina"
        ],
        "conflict": [
            "vitamina",
            "vitamina b1",
            "vitamina b10",
            "vitamina b11",
            "vitamina b12",
            "vitamina b13",
            "vitamina b15",
            "vitamina b17",
            "vitamina b2",
            "vitamina b22",
            "vitamina b4",
            "vitamina b5",
            "vitamina b6",
            "vitamina b7",
            "vitamina b8",
            "vitamina b9"
        ],
        "exact_term": False,
        "brazil": "vitamina B3",
    },
    "vitamina b4": {
        "synonyms": [
            "vitamina b4",
            "vitaminas b4",
            "adenina"
        ],
        "conflict": [
            "vitamina",
            "vitamina b1",
            "vitamina b10",
            "vitamina b11",
            "vitamina b12",
            "vitamina b13",
            "vitamina b15",
            "vitamina b17",
            "vitamina b2",
            "vitamina b22",
            "vitamina b3",
            "vitamina b5",
            "vitamina b6",
            "vitamina b7",
            "vitamina b8",
            "vitamina b9"
        ],
        "exact_term": False,
        "brazil": "vitamina B4",
    },
    "vitamina b5": {
        "synonyms": [
            "vitamina b5",
            "vitaminas b5",
            "pantotenico"
        ],
        "conflict": [
            "vitamina",
            "vitamina b1",
            "vitamina b10",
            "vitamina b11",
            "vitamina b12",
            "vitamina b13",
            "vitamina b15",
            "vitamina b17",
            "vitamina b2",
            "vitamina b22",
            "vitamina b3",
            "vitamina b4",
            "vitamina b6",
            "vitamina b7",
            "vitamina b8",
            "vitamina b9"
        ],
        "exact_term": False,
        "brazil": "vitamina B5",
    },
    "vitamina b6": {
        "synonyms": [
            "vitamina b6",
            "vitaminas b6",
            "piridoxina"
        ],
        "conflict": [
            "vitamina",
            "vitamina b1",
            "vitamina b10",
            "vitamina b11",
            "vitamina b12",
            "vitamina b13",
            "vitamina b15",
            "vitamina b17",
            "vitamina b2",
            "vitamina b22",
            "vitamina b3",
            "vitamina b4",
            "vitamina b5",
            "vitamina b7",
            "vitamina b8",
            "vitamina b9"
        ],
        "exact_term": False,
        "brazil": "vitamina B6",
    },
    "vitamina b7": {
        "synonyms": [
            "vitamina b7",
            "vitaminas b7",
            "biotina"
        ],
        "conflict": [
            "vitamina",
            "vitamina b1",
            "vitamina b10",
            "vitamina b11",
            "vitamina b12",
            "vitamina b13",
            "vitamina b15",
            "vitamina b17",
            "vitamina b2",
            "vitamina b22",
            "vitamina b3",
            "vitamina b4",
            "vitamina b5",
            "vitamina b6",
            "vitamina b8",
            "vitamina b9"
        ],
        "exact_term": False,
        "brazil": "vitamina B7",
    },
    "vitamina b8": {
        "synonyms": [
            "vitamina b8",
            "vitaminas b8",
            "inositol"
        ],
        "conflict": [
            "vitamina",
            "vitamina b1",
            "vitamina b10",
            "vitamina b11",
            "vitamina b12",
            "vitamina b13",
            "vitamina b15",
            "vitamina b17",
            "vitamina b2",
            "vitamina b22",
            "vitamina b3",
            "vitamina b4",
            "vitamina b5",
            "vitamina b6",
            "vitamina b7",
            "vitamina b9"
        ],
        "exact_term": False,
        "brazil": "vitamina B8",
    },
    "vitamina b9": {
        "synonyms": [
            "vitamina b9",
            "vitaminas b9",
            "folico"
        ],
        "conflict": [
            "vitamina",
            "vitamina b1",
            "vitamina b10",
            "vitamina b11",
            "vitamina b12",
            "vitamina b13",
            "vitamina b15",
            "vitamina b17",
            "vitamina b2",
            "vitamina b22",
            "vitamina b3",
            "vitamina b4",
            "vitamina b5",
            "vitamina b6",
            "vitamina b7",
            "vitamina b8"
        ],
        "exact_term": False,
        "brazil": "vitamina B9",
    },
    "vitamina c": {
        "synonyms": [
            "vitamina c",
            "vitaminas c",
            "ascorbico",
            "ascorbato",
            "ascorbila",
            "ácido ascórbico",
            "vitamina C",
            "ácido L-ascórbico",
            "L-ascorbico",
            "L-ascorbato",
            "L-ascorbila"
        ],
        "conflict": ["vitamina"],
        "exact_term": False,
        "brazil": "vitamina C",
    },
    "vitamina d": {
        "synonyms": [
            "vitamina d",
            "vitaminas d",
            "calciferol",
            "colecalciferol",
            "ergocalciferol",
            "vitamina D",
            "ácido calciferólico",
            "D3",
            "D2"
        ],
        "conflict": ["vitamina"],
        "exact_term": False,
        "brazil": "vitamina D",
    },
    "vitamina e": {
        "synonyms": [
            "vitamina e",
            "vitaminas e",
            "tocoferol",
            "tocoquinona",
            "vitamina E",
            "d-alfa-tocoferol",
            "dl-tocoferol"
        ],
        "conflict": ["vitamina"],
        "exact_term": False,
        "brazil": "vitamina E",
    },
    "vitamina f": {
        "synonyms": [
            "vitamina f",
            "vitaminas f",
            "graxos essenciais",
            "ácidos graxos essenciais"
        ],
        "conflict": ["vitamina"],
        "exact_term": False,
        "brazil": "vitamina F",
    },
    "vitamina g": {
        "synonyms": [
            "vitamina g",
            "vitaminas g",
            "monofosfato de nicotinamida",
            "nicotinamida monofosfato"
        ],
        "conflict": ["vitamina"],
        "exact_term": False,
        "brazil": "vitamina G",
    },
    "vitamina h": {
        "synonyms": [
            "vitamina h",
            "vitaminas h",
            "biotina"
        ],
        "conflict": ["vitamina"],
        "exact_term": False,
        "brazil": "vitamina H",
    },
    "vitamina j": {
        "synonyms": [
            "vitamina j",
            "vitaminas j",
            "lipoico",
            "ácido lipoico"
        ],
        "conflict": ["vitamina"],
        "exact_term": False,
        "brazil": "vitamina J",
    },
    "vitamina k": {
        "synonyms": [
            "vitamina k",
            "vitaminas k",
            "filoquinona",
            "vitamina K",
            "fitoquinona"
        ],
        "conflict": [
            "vitamina k1",
            "vitamina k2",
            "vitamina k7",
            "vitamina"
        ],
        "exact_term": False,
        "brazil": "vitamina K",
    },
    "vitamina k1": {
        "synonyms": [
            "vitamina k1",
            "vitaminas k1",
            "fitoquinona",
            "phylloquinona"
        ],
        "conflict": [
            "vitamina k",
            "vitamina k2",
            "vitamina k7",
            "vitamina"
        ],
        "exact_term": False,
        "brazil": "vitamina K1",
    },
    "vitamina k2": {
        "synonyms": [
            "vitamina k2",
            "vitaminas k2",
            "menaquinona",
            "MK-7",
            "MK-4"
        ],
        "conflict": [
            "vitamina k",
            "vitamina k1",
            "vitamina k7",
            "vitamina"
        ],
        "exact_term": False,
        "brazil": "vitamina K2",
    },
    "vitamina k7": {
        "synonyms": [
            "vitamina k7",
            "vitaminas k7",
            "mk7",
            "menaquinona-7"
        ],
        "conflict": [
            "vitamina k",
            "vitamina k1",
            "vitamina k2",
            "vitamina"
        ],
        "exact_term": False,
        "brazil": "vitamina K7",
    },
    "vitamina q": {
        "synonyms": [
            "vitamina q",
            "vitaminas q",
            "coenzima q10",
            "ubiquinona",
            "ubiquinol"
        ],
        "conflict": ["vitamina"],
        "exact_term": False,
        "brazil": "vitamina Q",
    },
    "wafer": {
        "synonyms": [
            "wafer",
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "wafer",
    },
    "bebida": {
        "synonyms": ["bebida", "drink", "liquid"],
        "conflict": [],
        "exact_term": False,
        "brazil": "bebida"
    },
    "biscuit": {
        "synonyms": ["biscuit", "biscoito", "bolacha", "cookie"],
        "conflict": [],
        "exact_term": False,
        "brazil": "cookie"
    },
    "waxymaize": {
        "synonyms": [
            "waxymaize",
            "waxy maize",
            "amido de milho"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "waxymaize",
    },
    "whey": {
        "synonyms": [
            "whey",
            "soro do leite"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "whey",
    },
    "xylitol": {
        "synonyms": [
            "xylitol",
            "xilitol",
            "adocante",
            "adocante"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "xilitol",
    },
    "zeaxantina": {
        "synonyms": [
            "zeaxantina"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "zeaxantina",
    },
    "zinco": {
        "synonyms": [
            "zinco",
            "zinco",
            "zinco"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "zinco",
    },
    "selenio": {
        "synonyms": [
            "selenio",
            "seleni",
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "selênio",
    },
    "zma": {
        "synonyms": [
            "zma"
        ],
        "conflict": [],
        "exact_term": False,
        "brazil": "ZMA",
    }
}

personal_pronouns = ["Eu", "Tu", "Ele", "Ela", "Nós", "Vós", "Eles", "Elas", "Mim", "Ti", "Si", "Consigo"]
oblique_pronouns = ["Me", "Te", "Se", "Nos", "Vos", "O", "A", "Lhe", "Os", "As", "Nos", "Vos", "Se", "Convosco", "Lhes", "Contigo"]
demonstrative_pronouns = ["Este", "Esse", "Aquele", "Esta", "Essa", "Aquela", "Isto", "Isso", "Aquilo", "Estes", "Esses", "Aqueles", "Estas", "Essas", "Aquelas", "Iste"]
possessive_pronouns = ["Meu", "Teu", "Seu", "Nosso", "Vosso", "Seu", "Minha", "Tua", "Sua", "Nossa", "Vossa", "Sua", "Meus", "Teus", "Seus", "Nossos", "Vossos", "Minhas", "Tuas", "Suas", "Nossas", "Vossas"]
indefinite_pronouns = ["Alguém", "Ninguém", "Todo", "Algum", "Nenhum", "Outro", "Muito", "Pouco", "Tanto", "Cada", "Algo", "Tudo", "Nada", "Cada um", "Qualquer", "Poucos", "Muitos", "Vários", "Outrem"]
relative_pronouns = ["Que", "Qual", "Quem", "Onde", "Cujo", "O qual", "Cuja", "Quanto"]
interrogative_pronouns = ["Quem", "O que", "Qual", "Quanto", "Onde", "Quando", "Como", "Por que", "Qualquer coisa", "Quanto a"]
prepositions = ["A", "Ante", "Até", "Após", "Com", "Contra", "De", "Desde", "Em", "Entre", "Para", "Por", "Perante", "Sem", "Sob", "Sobre", "Trás", "Conforme", "Contudo", "Durante", "Exceto", "Mediant", "Menos", "Salvo", "Segundo", "Visto"]

BRAZIL_PRONOUNS = personal_pronouns + oblique_pronouns + demonstrative_pronouns + possessive_pronouns + indefinite_pronouns + relative_pronouns + interrogative_pronouns + prepositions
BRAZIL_CONECTORES = ['a', 'o', 'e', 'ou', 'nem', 'mas', 'porque', 'como', 'apesar', 'além', 'entretanto', 'porém', 'todavia', 'logo', 'portanto', 'assim', 'contudo', 'embora', 'ainda', 'também', 'quer', 'seja', 'isto', 'aquilo']

PRONOUNS = {
    "exact_term": False,
    "brazil": BRAZIL_PRONOUNS,
}

WORDLIST = {
    "supplement": SUPPLEMENT_COMPONENT_LIST,
}