import re
from copy import deepcopy

from utils.general_functions import clean_text


def get_synonyms(component_list):
    keywords_list = []
    for component, attributes in component_list.items():
        keywords_list.append(attributes.get("subject"))
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

def find_subject_in_wordlist(word, wordlist):
    for values in wordlist.values():
        subject = values['subject']
        if (word in subject):
            return subject

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
        "subject": [
            "acetil",
            "nacetil",
            "n acetil",
            "cisteina",
            "l cisteina",
            "lcisteina",
            "nac",
        ],
        "product": True,
        "may_feature": False,
        "from": [
            "aminoacido",
            "antioxidante",
        ],
        "conflict": []
    },
    "albumina": {
        "subject": [
            "albumina",
            "albumin",
            "albumi",
        ],
        "product": True,
        "may_feature": False,
        "from": [
            "egg",
        ],
        "conflict": []
    },
    "alfajor": {
        "subject": [
            "alfajor"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "alho": {
        "subject": [
            "alho"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "aminoacido": {
        "subject": [
            "aminoacido"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "antioxidante": {
        "subject": [
            "antioxidante",
            "antiox"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "arginin": {
        "subject": [
            "arginin",
            "arginine",
            "arginina"
        ],
        "product": True,
        "may_feature": False,
        "from": [
            "aminoacido"
        ],
        "conflict": []
    },
    "astaxantina": {
        "subject": [
            "astaxantina"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "barrinha": {
        "subject": [
            "barrinha",
            "barra",
            "bar",
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "batata doce": {
        "subject": [
            "batata doce"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "bcaa": {
        "subject": [
            "bcaa",
            "bca"
        ],
        "product": True,
        "may_feature": False,
        "from": [
            "aminoacido",
            "leucina",
            "valina",
            "isoleucina",
        ],
        "conflict": []
    },
    "beauty": {
        "subject": [
            "beauty",
            "beleza"
        ],
        "product": False,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "beef": {
        "subject": [
            "beef",
            "carn",
            "carne"
        ],
        "product": True,
        "may_feature": False,
        "from": [
            "protein"
        ],
        "conflict": []
    },
    "betaalanina": {
        "subject": [
            "beta alanina",
            "betaalanina",
            "alanina",
            "alanine"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "betacaroteno": {
        "subject": [
            "betacaroteno"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "biotina": {
        "subject": [
            "biotina"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "blend": {
        "subject": [
            "blend",
            "mistura"
        ],
        "product": False,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "borragem": {
        "subject": [
            "borragem"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "cafein": {
        "subject": [
            "cafein",
            "cafe",
            "cafeina",
            "coffe",
            "caffe",
            "coffee"
        ],
        "product": True,
        "may_feature": True,
        "from": [
            "termogenico",
            "pretreino"
        ],
        "conflict": [
            "barrinha",
            "whey"
        ]
    },
    "termogenico": {
        "subject": [
            "termogenico",
            "termogênico",
            "termogenicos",
            "termogênicos",
        ],
        "product": True,
        "may_feature": False,
        "from": [
            "cafein",
        ],
        "conflict": []
    },
    "tcm": {
        "subject": [
            "tcm",
        ],
        "product": True,
        "may_feature": False,
        "from": [
            "cafein",
        ],
        "conflict": []
    },
    "calcio": {
        "subject": [
            "calcio"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "carboidrato": {
        "subject": [
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
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "carnitin": {
        "subject": [
            "carnitin",
            "carnitina",
            "lcarnitina",
            "l carnitina"
        ],
        "product": True,
        "may_feature": False,
        "from": [
            "aminoacido"
        ],
        "conflict": []
    },
    "cartamo": {
        "subject": [
            "cartamo"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "caseinato": {
        "subject": [
            "caseinato"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "cha": {
        "subject": [
            "cha"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "chaverde": {
        "subject": [
            "chaverde",
            "cha verde"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "chia": {
        "subject": [
            "chia"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "chocolate": {
        "subject": [
            "chocolate"
        ],
        "product": False,
        "may_feature": True,
        "from": [],
        "conflict": []
    },
    "cistein": {
        "subject": [
            "cistein",
            "lcisteina"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "coco": {
        "subject": [
            "coco",
        ],
        "product": False,
        "may_feature": True,
        "from": [],
        "conflict": []
    },
    "colageno": {
        "subject": [
            "colageno",
            "colagen"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "complexo b": {
        "subject": [
            "complexo b",
            "vitamina b"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "concentrad": {
        "subject": [
            "concentrad"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "creatina": {
        "subject": [
            "creatina",
            "creatine",
            "creatin",
            "creapure"
        ],
        "product": True,
        "may_feature": False,
        "from": [
            "monohidratada",
            "aminoacido"
        ],
        "conflict": []
    },
    "crisp": {
        "subject": [
            "crisp"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "cromo": {
        "subject": [
            "cromo",
            "cromo"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "curcuma": {
        "subject": [
            "curcuma",
            "acafrao"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "dextrose": {
        "subject": [
            "dextrose",
            "maltodextrose"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "dribose": {
        "subject": [
            "dribose",
            "d ribose",
            "ribose",
            "dribose"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "egg": {
        "subject": [
            "egg",
            "ovo"
        ],
        "product": True,
        "may_feature": False,
        "from": [
            "protein"
        ],
        "conflict": []
    },
    "ervilha": {
        "subject": [
            "ervilha",
            "pea"
        ],
        "product": True,
        "may_feature": False,
        "from": [
            "protein"
        ],
        "conflict": []
    },
    "espirulina": {
        "subject": [
            "espirulina"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "fibra": {
        "subject": [
            "fibra"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "fosfatidilserina": {
        "subject": [
            "fosfatidilserina"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "frutose": {
        "subject": [
            "frutose"
        ],
        "product": False,
        "may_feature": False,
        "from": [
            "carboidrato"
        ],
        "conflict": []
    },
    "gengibre": {
        "subject": [
            "gengibre"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "gergelim": {
        "subject": [
            "gergelim"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "glutamin": {
        "subject": [
            "glutamin",
            "glutamine",
            "glutamina",
            "lglutamina"
        ],
        "product": True,
        "may_feature": False,
        "from": [
            "aminoacido",
        ],
        "conflict": []
    },
    "hair": {
        "subject": [
            "hair",
            "cabelo"
        ],
        "product": False,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "hialuronico": {
        "subject": [
            "hialuronico"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "hidrolisad": {
        "subject": [
            "hidrolisad"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "hmb": {
        "subject": [
            "hmb",
            "hydroxymethylbutyrate"
        ],
        "product": True,
        "may_feature": False,
        "from": [
            "aminoacido"
        ],
        "conflict": []
    },
    "imune": {
        "subject": [
            "imune",
            "imunidade"
        ],
        "product": False,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "iso": {
        "subject": [
            "iso",
            "isolado",
            "isolate",
            "isolada"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "kit": {
        "subject": [
            "kit",
            "combo",
        ],
        "product": False,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "krill": {
        "subject": [
            "krill"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "lecitina": {
        "subject": [
            "lecitina"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "leucin": {
        "subject": [
            "leucin",
            "leucine",
            "lleucine"
        ],
        "product": True,
        "may_feature": False,
        "from": [
            "aminoacido"
        ],
        "conflict": []
    },
    "levagen": {
        "subject": [
            "levagen"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "linhaca": {
        "subject": [
            "linhaca"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "maca peruana": {
        "subject": [
            "maca peruana"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "magnesio": {
        "subject": [
            "magnesio",
            "magnesi"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "malto": {
        "subject": [
            "malto",
            "dextrina",
            "maltodextrina"
        ],
        "product": True,
        "may_feature": False,
        "from": [
            "carboidrato"
        ],
        "conflict": []
    },
    "mass": {
        "subject": [
            "mass",
            "hipercalorico"
        ],
        "product": True,
        "may_feature": False,
        "from": [
            "carboidrato",
            "malto",
            "waxymaize"
        ],
        "conflict": []
    },
    "melatonina": {
        "subject": [
            "melatonina",
            "melatonina"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "monohidratada": {
        "subject": [
            "monohidratada"
        ],
        "product": True,
        "may_feature": False,
        "from": [
            "creatina"
        ],
        "conflict": []
    },
    "multivitaminico": {
        "subject": [
            "multivitaminico",
            "polivitaminico"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "mineral": {
        "subject": [
            "minerai",
            "mineral",
        ],
        "product": False,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "nail": {
        "subject": [
            "nail",
            "unha"
        ],
        "product": False,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "oleo": {
        "subject": [
            "oleo"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "oleo de coco": {
        "subject": [
            "oleo de coco"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "ketchup": {
        "subject": [
            "ketchup"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "barbecue": {
        "subject": [
            "barbecue"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "mostarda": {
        "subject": [
            "mostarda"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "maionese": {
        "subject": [
            "mostarda"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "optimsm": {
        "subject": [
            "optimsm"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "palatinose": {
        "subject": [
            "palatinose",
            "isomaltulose"
        ],
        "product": True,
        "may_feature": False,
        "from": [
            "carboidrato"
        ],
        "conflict": []
    },
    "enzima": {
        "subject": [
            "enzima",
            "enzimas",
            "enzyme",
            "enzymes"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "protease": {
        "subject": [
            "protease",
            "proteasa",
            "protease"
        ],
        "product": True,
        "may_feature": False,
        "from": [
            "enzima"
        ],
        "conflict": []
    },
    "propolis": {
        "subject": [
            "propolis",
        ],
        "product": True,
        "may_feature": False,
        "from": [
            "enzima"
        ],
        "conflict": []
    },
    "lactase": {
        "subject": [
            "lactase",
            "lactasa",
            "lactase"
        ],
        "product": True,
        "may_feature": False,
        "from": [
            "enzima"
        ],
        "conflict": []
    },
    "lipase": {
        "subject": [
            "lipase",
            "lipasa",
            "lipase"
        ],
        "product": True,
        "may_feature": False,
        "from": [
            "enzima"
        ],
        "conflict": []
    },
    "bromelina": {
        "subject": [
            "bromelina",
            "bromelain",
            "bromelina"
        ],
        "product": True,
        "may_feature": False,
        "from": [
            "enzima"
        ],
        "conflict": []
    },
    "amilase": {
        "subject": [
            "amilase",
            "amylase",
            "amilasa"
        ],
        "product": True,
        "may_feature": False,
        "from": [
            "enzima"
        ],
        "conflict": []
    },
    "peanut": {
        "subject": [
            "pasta de amendoim",
            "peanut",
            "amendoim"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "omega 3": {
        "subject": [
            "peixe",
            "dha",
            "epa",
            "omega 3",
            "omega",
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "omega 6": {
        "subject": [
            "omega 6",
            "linoléico",
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "picolinato": {
        "subject": [
            "picolinato",
            "picolinato"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "pretreino": {
        "subject": [
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
        "product": True,
        "may_feature": False,
        "from": [
            "taurina",
            "betaalanina",
            "cafein",
            "arginin",
            "tyrosin",
            "termogenico"
        ],
        "conflict": []
    },
    "primula": {
        "subject": [
            "primula"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "propoli": {
        "subject": [
            "propoli"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "protein": {
        "subject": [
            "protein",
            "proteina",
            "proteica"
        ],
        "product": True,
        "may_feature": False,
        "from": [
            "concentrad", 
            "iso", 
            "hidrolisad",
        ],
        "conflict": []
    },
    "psyllium": {
        "subject": [
            "psyllium"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "quitosana": {
        "subject": [
            "quitosana"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "resveratrol": {
        "subject": [
            "resveratrol"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "rice": {
        "subject": [
            "rice",
            "arroz"
        ],
        "product": True,
        "may_feature": False,
        "from": [
            "protein"
        ],
        "conflict": []
    },
    "semente": {
        "subject": [
            "semente"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "skin": {
        "subject": [
            "skin",
            "pele"
        ],
        "product": False,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "soy": {
        "subject": [
            "soy",
            "soja"
        ],
        "product": True,
        "may_feature": False,
        "from": [
            "protein"
        ],
        "conflict": []
    },
    "spirulina": {
        "subject": [
            "spirulina"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "taurina": {
        "subject": [
            "taurina",
            "taurine",
            "taurin"
        ],
        "product": True,
        "may_feature": False,
        "from": [
            "aminoacido"
        ],
        "conflict": []
    },
    "tempero": {
        "subject": [
            "tempero"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "testofen": {
        "subject": [
            "testofen"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "tyrosin": {
        "subject": [
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
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "transresveratrol": {
        "subject": [
            "transresveratrol",
            "trans resveratrol"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "triptofano": {
        "subject": [
            "triptofano"
        ],
        "product": True,
        "may_feature": False,
        "from": [
            "aminoacido"
        ],
        "conflict": []
    },
    "leucina": {
        "subject": [
            "leucina"
        ],
        "product": True,
        "may_feature": False,
        "from": [
            "aminoacido"
        ],
        "conflict": []
    },
    "valina": {
        "subject": [
            "valina"
        ],
        "product": True,
        "may_feature": False,
        "from": [
            "aminoacido"
        ],
        "conflict": []
    },
    "isoleucina": {
        "subject": [
            "isoleucina"
        ],
        "product": True,
        "may_feature": False,
        "from": [
            "aminoacido"
        ],
        "conflict": []
    },
    "lisina": {
        "subject": [
            "lisina"
        ],
        "product": True,
        "may_feature": False,
        "from": [
            "aminoacido"
        ],
        "conflict": []
    },
    "fenilalanina": {
        "subject": [
            "fenilalanina"
        ],
        "product": True,
        "may_feature": False,
        "from": [
            "aminoacido"
        ],
        "conflict": []
    },
    "treonina": {
        "subject": [
            "treonina"
        ],
        "product": True,
        "may_feature": False,
        "from": [
            "aminoacido"
        ],
        "conflict": []
    },
    "metionina": {
            "subject": [
            "metionina"
        ],
        "product": True,
        "may_feature": False,
        "from": [
            "aminoacido",
        ],
        "conflict": []
    },
    "silimarina": {
            "subject": [
            "silimarina"
        ],
        "product": True,
        "may_feature": False,
        "from": [
            "aminoacido"
        ],
        "conflict": []
    },
    "histidina": {
        "subject": [
            "histidina",
            "lhistidina",
            "l histidina"
        ],
        "product": True,
        "may_feature": False,
        "from": [
            "aminoacido"
        ],
        "conflict": []
    },
    "veg": {
        "subject": [
            "veg",
            "vegan",
            "vegano",
            "vegie",
            "vegana"
        ],
        "product": False,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "vegetarian": {
        "subject": [
            "vegetarian",
            "vegetariano",
            "vegetariana",
            "veggie",
            "vegetarianismo"
        ],
        "product": False,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "verisol": {
        "subject": [
            "verisol"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "vitamina": {
        "subject": [
            "vitamina",
            "vitaminas",
            "vitamin"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "vitamina a": {
        "subject": [
            "vitamina a",
            "vitaminas a"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "vitamina b1": {
        "subject": [
            "vitamina b1",
            "vitaminas b1",
            "tiamina"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "vitamina b10": {
        "subject": [
            "vitamina b10",
            "vitaminas b10",
            "paraaminobenzoico"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "vitamina b11": {
        "subject": [
            "vitamina b11",
            "vitaminas b11",
            "salicilico"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "vitamina b12": {
        "subject": [
            "vitamina b12",
            "vitaminas b12",
            "cobalamina"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "vitamina b13": {
        "subject": [
            "vitamina b13",
            "vitaminas b13",
            "orotico"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "vitamina b15": {
        "subject": [
            "vitamina b15",
            "vitaminas b15",
            "pangamico"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "vitamina b17": {
        "subject": [
            "vitamina b17",
            "vitaminas b17",
            "amigdalina"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "vitamina b2": {
        "subject": [
            "vitamina b2",
            "vitaminas b2",
            "riboflavina"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "vitamina b22": {
        "subject": [
            "vitamina b22",
            "vitaminas b22",
            "ratanhia"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "vitamina b3": {
        "subject": [
            "vitamina b3",
            "vitaminas b3",
            "niacina"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "vitamina b4": {
        "subject": [
            "vitamina b4",
            "vitaminas b4",
            "adenina"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "vitamina b5": {
        "subject": [
            "vitamina b5",
            "vitaminas b5",
            "pantotenico"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "vitamina b6": {
        "subject": [
            "vitamina b6",
            "vitaminas b6",
            "piridoxina"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "vitamina b7": {
        "subject": [
            "vitamina b7",
            "vitaminas b7",
            "biotina"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "vitamina b8": {
        "subject": [
            "vitamina b8",
            "vitaminas b8",
            "inositol"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "vitamina b9": {
        "subject": [
            "vitamina b9",
            "vitaminas b9",
            "folico"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "vitamina c": {
        "subject": [
            "vitamina c",
            "vitaminas c",
            "ascorbico",
            "ascorbato",
            "ascorbila",
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "vitamina d": {
        "subject": [
            "vitamina d",
            "vitaminas d",
            "calciferol"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "vitamina e": {
        "subject": [
            "vitamina e",
            "vitaminas e",
            "tocoferol"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "vitamina f": {
        "subject": [
            "vitamina f",
            "vitaminas f",
            "graxos essenciais"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "vitamina g": {
        "subject": [
            "vitamina g",
            "vitaminas g",
            "monofosfato de nicotinamida"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "vitamina h": {
        "subject": [
            "vitamina h",
            "vitaminas h",
            "biotina"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "vitamina j": {
        "subject": [
            "vitamina j",
            "vitaminas j",
            "lipoico"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "vitamina k": {
        "subject": [
            "vitamina k",
            "vitaminas k",
            "filoquinona"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "vitamina k1": {
        "subject": [
            "vitamina k1",
            "vitaminas k1",
            "fitoquinona"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "vitamina k2": {
        "subject": [
            "vitamina k2"
            "vitaminas k2",
            "menaquinona"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "vitamina k7": {
        "subject": [
            "vitamina k7",
            "vitaminas k7",
            "mk7"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "vitamina l": {
        "subject": [
            "vitamina l",
            "vitaminas l",
            "adipico"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "vitamina l1": {
        "subject": [
            "vitamina l1",
            "vitaminas l1"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "vitamina l2": {
        "subject": [
            "vitamina l2",
            "vitaminas l2",
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "vitamina m": {
        "subject": [
            "vitamina m",
            "vitaminas m"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "vitamina n": {
        "subject": [
            "vitamina n",
            "vitaminas n",
            "pantotenico"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "vitamina o": {
        "subject": [
            "vitamina o",
            "vitaminas o",
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "vitamina p": {
        "subject": [
            "vitamina p",
            "vitaminas p",
            "bioflavonoides"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "vitamina q": {
        "subject": [
            "vitamina q",
            "vitaminas q",
            "coenzima q10"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "vitamina r": {
        "subject": [
            "vitamina r",
            "vitaminas r",
            "flavina"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "vitamina s": {
        "subject": [
            "vitamina s",
            "vitaminas s",
            "aminobenzoico"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "vitamina t": {
        "subject": [
            "vitamina t",
            "vitaminas t",
            "bioflavonoides"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "vitamina w": {
        "subject": [
            "vitamina w",
            "vitaminas w"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "wafer": {
        "subject": [
            "wafer",
            "bolacha",
            "biscoito",
            "cookie"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "waxymaize": {
        "subject": [
            "waxymaize",
            "waxy maize",
            "amido de milho"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "whey": {
        "subject": [
            "whey",
            "soro do leite"
        ],
        "product": True,
        "may_feature": False,
        "from": [
            "protein",
            "concentrad",
            "iso",
            "hidrolisad",
        ],
        "conflict": [
            "barrinha",
            "alfajor",
            "wafer",
        ]
    },
    "xylitol": {
        "subject": [
            "xylitol",
            "xilitol",
            "adocante",
            "adocante"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "zeaxantina": {
        "subject": [
            "zeaxantina"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "zinco": {
        "subject": [
            "zinco",
            "zinco",
            "zinco"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "selenio": {
        "subject": [
            "selenio",
            "seleni",
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
    },
    "zma": {
        "subject": [
            "zma"
        ],
        "product": True,
        "may_feature": False,
        "from": [],
        "conflict": []
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
    "brazil": BRAZIL_PRONOUNS
}

WORDLIST = {
    "supplement": SUPPLEMENT_COMPONENT_LIST,
}