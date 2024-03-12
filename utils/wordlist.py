import re
from copy import deepcopy

from utils.general_functions import clean_text

def get_synonyms(component_list):
    keywords_list = []
    for component, attributes in component_list.items():
        keywords_list.append(attributes.get("subject"))
    return keywords_list

def get_word_index_in_text(word, text):
    text_temp = deepcopy(text)
    word_clean = clean_text(word, False, False, False)
    matches = re.finditer(" " + word_clean, text_temp)

    locations = []
    for match in matches:
        start_index = match.start()
        locations.append(start_index)

    return locations

def get_back_words(text, text_accents, locations, word_size):
    size_max = 30
    slice_min = lambda value: value if value >= 0 else 0
    slice_max = lambda value: value if value <= len(text) else len(text)

    import pandas as pd
    df = pd.DataFrame(columns=['back_words', 'back_words_original'])

    for location in locations:
        start = slice_min(location - size_max)
        end = slice_max(location + (word_size + 1))

        back_words = (text[start:end].replace("\n", ""))
        back_words_original = (text_accents[start:end].replace("\n", ""))

        back_words = back_words.split(" ")
        back_words_original = back_words_original.split(" ")

        df = df._append({'back_words': back_words, 'back_words_original': back_words_original}, ignore_index=True)

    df.to_csv('back_words.csv', index=False)
        # print(text[start:location + 1].split(" "))
        # print(text_accents[start:location + 1].split(" "))

        # is_only_one_word = False
        # first_chat = (back_words[-word_size:])
        # if (not first_chat.isalpha()):
        #     is_only_one_word = True

        # context_words = [i for i in back_words[:-word_size].split(" ") if i != '']
        # print(context_words)

    return

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
        "may_contain": [
            "aminoacido",
            "antioxidante",
        ],
        "not_contain": []
    },
    "albumina": {
        "subject": [
            "albumina",
            "albumin",
            "albumi",
        ],
        "may_contain": [
            "egg",
        ],
        "not_contain": []
    },
    "alfajor": {
        "subject": [
            "alfajor"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "alho": {
        "subject": [
            "alho"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "aminoacido": {
        "subject": [
            "aminoacido"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "antiox": {
        "subject": [
            "antiox"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "antioxidante": {
        "subject": [
            "antioxidante"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "arginin": {
        "subject": [
            "arginin",
            "arginine",
            "arginina"
        ],
        "may_contain": [
            "aminoacido"
        ],
        "not_contain": []
    },
    "astaxantina": {
        "subject": [
            "astaxantina"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "barrinha": {
        "subject": [
            "barrinha",
            "barra",
            "bar",
        ],
        "may_contain": [
            "protein",
            "whey",
        ],
        "not_contain": []
    },
    "batata doce": {
        "subject": [
            "batata doce"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "bcaa": {
        "subject": [
            "bcaa",
            "bca"
        ],
        "may_contain": [
            "aminoacido",
            "leucina",
            "valina",
            "isoleucina",
        ],
        "not_contain": []
    },
    "beauty": {
        "subject": [
            "beauty",
            "beleza"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "beef": {
        "subject": [
            "beef",
            "carn",
            "carne"
        ],
        "may_contain": [
            "protein"
        ],
        "not_contain": []
    },
    "betaalanina": {
        "subject": [
            "beta alanina",
            "betaalanina",
            "alanina",
            "alanine"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "betacaroteno": {
        "subject": [
            "betacaroteno"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "biotina": {
        "subject": [
            "biotina"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "blend": {
        "subject": [
            "blend",
            "mistura"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "borragem": {
        "subject": [
            "borragem"
        ],
        "may_contain": [],
        "not_contain": []
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
        "may_contain": [],
        "not_contain": []
    },
    "termogenico": {
        "subject": [
            "termogenico",
            "termogênico",
            "termogenicos",
            "termogênicos",
            "cut",
            "cutting",
            "emagrece",
        ],
        "may_contain": [
            "cafein",
        ],
        "not_contain": []
    },
    "calcio": {
        "subject": [
            "calcio"
        ],
        "may_contain": [],
        "not_contain": []
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
        "may_contain": [],
        "not_contain": []
    },
    "carnitin": {
        "subject": [
            "carnitin",
            "carnitina",
            "lcarnitina"
            "l carnitina"
        ],
        "may_contain": [
            "aminoacido"
        ],
        "not_contain": []
    },
    "cartamo": {
        "subject": [
            "cartamo"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "caseinato": {
        "subject": [
            "caseinato"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "cha": {
        "subject": [
            "cha"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "chaverde": {
        "subject": [
            "chaverde",
            "cha verde"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "chia": {
        "subject": [
            "chia"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "chocolate": {
        "subject": [
            "chocolate"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "cistein": {
        "subject": [
            "cistein",
            "lcisteina"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "coco": {
        "subject": [
            "coco",
            "coco"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "colageno": {
        "subject": [
            "colageno",
            "colagen"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "complexo b": {
        "subject": [
            "complexo b",
            "vitamina b"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "concentrad": {
        "subject": [
            "concentrad"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "creatina": {
        "subject": [
            "creatina",
            "creatine",
            "creatin",
            "creapure"
        ],
        "may_contain": [
            "monohidratada",
            "aminoacido"
        ],
        "not_contain": []
    },
    "crisp": {
        "subject": [
            "crisp"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "cromo": {
        "subject": [
            "cromo",
            "cromo"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "curcuma": {
        "subject": [
            "curcuma",
            "acafrao"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "dextrose": {
        "subject": [
            "dextrose",
            "maltodextrose"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "dribose": {
        "subject": [
            "dribose",
            "d ribose",
            "ribose",
            "dribose"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "egg": {
        "subject": [
            "egg",
            "ovo"
        ],
        "may_contain": [
            "protein"
        ],
        "not_contain": []
    },
    "ervilha": {
        "subject": [
            "ervilha",
            "pea"
        ],
        "may_contain": [
            "protein"
        ],
        "not_contain": []
    },
    "espirulina": {
        "subject": [
            "espirulina"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "fibra": {
        "subject": [
            "fibra"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "fosfatidilserina": {
        "subject": [
            "fosfatidilserina"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "frutose": {
        "subject": [
            "frutose"
        ],
        "may_contain": [
            "carboidrato"
        ],
        "not_contain": []
    },
    "gengibre": {
        "subject": [
            "gengibre"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "gergelim": {
        "subject": [
            "gergelim"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "glutamin": {
        "subject": [
            "glutamin",
            "glutamine",
            "glutamina",
            "lglutamina"
        ],
        "may_contain": [
            "aminoacido",
        ],
        "not_contain": [
            "whey"
        ]
    },
    "hair": {
        "subject": [
            "hair",
            "cabelo"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "hialuronico": {
        "subject": [
            "hialuronico"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "hidrolisad": {
        "subject": [
            "hidrolisad"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "hmb": {
        "subject": [
            "hmb",
            "hydroxymethylbutyrate"
        ],
        "may_contain": [
            "aminoacido"
        ],
        "not_contain": []
    },
    "imune": {
        "subject": [
            "imune",
            "imunidade"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "iso": {
        "subject": [
            "iso",
            "isolado",
            "isolate",
            "isolada"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "kit": {
        "subject": [
            "kit",
            "combo",
        ],
        "may_contain": [],
        "not_contain": []
    },
    "krill": {
        "subject": [
            "krill"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "lecitina": {
        "subject": [
            "lecitina"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "leucin": {
        "subject": [
            "leucin",
            "leucine",
            "lleucine"
        ],
        "may_contain": [
            "aminoacido"
        ],
        "not_contain": []
    },
    "levagen": {
        "subject": [
            "levagen"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "linhaca": {
        "subject": [
            "linhaca"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "maca peruana": {
        "subject": [
            "maca peruana"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "magnesio": {
        "subject": [
            "magnesio",
            "magnesi"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "malto": {
        "subject": [
            "malto",
            "dextrina",
            "maltodextrina"
        ],
        "may_contain": [
            "carboidrato"
        ],
        "not_contain": []
    },
    "mass": {
        "subject": [
            "mass",
            "hipercalorico"
        ],
        "may_contain": [
            "carboidrato",
            "malto",
            "waxymaize"
        ],
        "not_contain": []
    },
    "melatonina": {
        "subject": [
            "melatonina",
            "melatonina"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "monohidratada": {
        "subject": [
            "monohidratada"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "multivitaminico": {
        "subject": [
            "multivitaminico",
            "polivitaminico"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "minerail": {
        "subject": [
            "minerai",
            "minerail"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "nail": {
        "subject": [
            "nail",
            "unha"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "oleo": {
        "subject": [
            "oleo"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "optimsm": {
        "subject": [
            "optimsm"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "palatinose": {
        "subject": [
            "palatinose",
            "isomaltulose"
        ],
        "may_contain": [
            "carboidrato"
        ],
        "not_contain": []
    },
    "enzima": {
        "subject": [
            "enzima",
            "enzimas",
            "enzyme",
            "enzymes"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "protease": {
        "subject": [
            "protease",
            "proteasa",
            "protease"
        ],
        "may_contain": [
            "enzima"
        ],
        "not_contain": []
    },
    "lactase": {
        "subject": [
            "lactase",
            "lactasa",
            "lactase"
        ],
        "may_contain": [
            "enzima"
        ],
        "not_contain": []
    },
    "lipase": {
        "subject": [
            "lipase",
            "lipasa",
            "lipase"
        ],
        "may_contain": [
            "enzima"
        ],
        "not_contain": []
    },
    "bromelina": {
        "subject": [
            "bromelina",
            "bromelain",
            "bromelina"
        ],
        "may_contain": [
            "enzima"
        ],
        "not_contain": []
    },
    "amilase": {
        "subject": [
            "amilase",
            "amylase",
            "amilasa"
        ],
        "may_contain": [
            "enzima"
        ],
        "not_contain": []
    },
    "peanut": {
        "subject": [
            "pasta de amendoim",
            "peanut",
            "amendoim"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "omega 3": {
        "subject": [
            "peixe",
            "dha",
            "epa",
            "omega 3",
        ],
        "may_contain": [],
        "not_contain": []
    },
    "omega 6": {
        "subject": [
            "omega 6",
            "linoléico",
        ],
        "may_contain": [],
        "not_contain": []
    },
    "picolinato": {
        "subject": [
            "picolinato",
            "picolinato"
        ],
        "may_contain": [],
        "not_contain": []
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
        "may_contain": [
            "taurina",
            "betaalanina",
            "cafein",
            "arginin",
            "tyrosin",
            "pretreino",
        ],
        "not_contain": []
    },
    "primula": {
        "subject": [
            "primula"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "propoli": {
        "subject": [
            "propoli"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "protein": {
        "subject": [
            "protein",
            "proteina",
            "proteica"
        ],
        "may_contain": [
            "concentrad", 
            "iso", 
            "hidrolisad",
        ],
        "not_contain": []
    },
    "psyllium": {
        "subject": [
            "psyllium"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "quitosana": {
        "subject": [
            "quitosana"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "resveratrol": {
        "subject": [
            "resveratrol"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "rice": {
        "subject": [
            "rice",
            "arroz"
        ],
        "may_contain": [
            "protein"
        ],
        "not_contain": []
    },
    "semente": {
        "subject": [
            "semente"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "skin": {
        "subject": [
            "skin",
            "pele"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "soy": {
        "subject": [
            "soy",
            "soja"
        ],
        "may_contain": [
            "protein"
        ],
        "not_contain": []
    },
    "spirulina": {
        "subject": [
            "spirulina"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "taurina": {
        "subject": [
            "taurina",
            "taurine",
            "taurin"
        ],
        "may_contain": [
            "aminoacido"
        ],
        "not_contain": []
    },
    "tempero": {
        "subject": [
            "tempero"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "testofen": {
        "subject": [
            "testofen"
        ],
        "may_contain": [],
        "not_contain": []
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
        "may_contain": [],
        "not_contain": []
    },
    "transresveratrol": {
        "subject": [
            "transresveratrol",
            "trans resveratrol"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "triptofano": {
        "subject": [
            "triptofano"
        ],
        "may_contain": [
            "aminoacido"
        ],
        "not_contain": []
    },
    "leucina": {
        "subject": [
            "leucina"
        ],
        "may_contain": [
            "aminoacido"
        ],
        "not_contain": []
    },
    "valina": {
        "subject": [
            "valina"
        ],
        "may_contain": [
            "aminoacido"
        ],
        "not_contain": []
    },
    "isoleucina": {
        "subject": [
            "isoleucina"
        ],
        "may_contain": [
            "aminoacido"
        ],
        "not_contain": []
    },
    "lisina": {
        "subject": [
            "lisina"
        ],
        "may_contain": [
            "aminoacido"
        ],
        "not_contain": []
    },
    "fenilalanina": {
        "subject": [
            "fenilalanina"
        ],
        "may_contain": [
            "aminoacido"
        ],
        "not_contain": []
    },
    "treonina": {
        "subject": [
            "treonina"
        ],
        "may_contain": [
            "aminoacido"
        ],
        "not_contain": []
    },
    "metionina": {
            "subject": [
            "metionina"
        ],
        "may_contain": [
            "aminoacido",
        ],
        "not_contain": []
    },
    "silimarina": {
            "subject": [
            "silimarina"
        ],
        "may_contain": [
            "aminoacido"
        ],
        "not_contain": []
    },
    "histidina": {
        "subject": [
            "histidina",
            "lhistidina"
            "l histidina"
        ],
        "may_contain": [
            "aminoacido"
        ],
        "not_contain": []
    },
    "veg": {
        "subject": [
            "veg",
            "vegan",
            "vegano",
            "vegie",
            "vegana"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "verisol": {
        "subject": [
            "verisol"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "vitamina": {
        "subject": [
            "vitamina",
            "vitaminas",
            "vitamin"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "vitamina a": {
        "subject": [
            "vitamina a"
            "vitaminas a"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "vitamina b1": {
        "subject": [
            "vitamina b1",
            "vitaminas b1",
            "tiamina"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "vitamina b10": {
        "subject": [
            "vitamina b10",
            "vitaminas b10",
            "paraaminobenzoico"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "vitamina b11": {
        "subject": [
            "vitamina b11",
            "vitaminas b11",
            "salicilico"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "vitamina b12": {
        "subject": [
            "vitamina b12",
            "vitaminas b12",
            "cobalamina"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "vitamina b13": {
        "subject": [
            "vitamina b13",
            "vitaminas b13",
            "orotico"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "vitamina b15": {
        "subject": [
            "vitamina b15",
            "vitaminas b15",
            "pangamico"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "vitamina b17": {
        "subject": [
            "vitamina b17",
            "vitaminas b17",
            "amigdalina"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "vitamina b2": {
        "subject": [
            "vitamina b2",
            "vitaminas b2",
            "riboflavina"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "vitamina b22": {
        "subject": [
            "vitamina b22",
            "vitaminas b22",
            "ratanhia"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "vitamina b3": {
        "subject": [
            "vitamina b3",
            "vitaminas b3",
            "niacina"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "vitamina b4": {
        "subject": [
            "vitamina b4",
            "vitaminas b4",
            "adenina"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "vitamina b5": {
        "subject": [
            "vitamina b5",
            "vitaminas b5",
            "pantotenico"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "vitamina b6": {
        "subject": [
            "vitamina b6",
            "vitaminas b6",
            "piridoxina"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "vitamina b7": {
        "subject": [
            "vitamina b7",
            "vitaminas b7",
            "biotina"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "vitamina b8": {
        "subject": [
            "vitamina b8",
            "vitaminas b8",
            "inositol"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "vitamina b9": {
        "subject": [
            "vitamina b9",
            "vitaminas b9",
            "folico"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "vitamina c": {
        "subject": [
            "vitamina c",
            "vitaminas c",
            "ascorbico",
            "ascorbato",
            "ascorbila",
        ],
        "may_contain": [],
        "not_contain": []
    },
    "vitamina d": {
        "subject": [
            "vitamina d",
            "vitaminas d",
            "calciferol"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "vitamina e": {
        "subject": [
            "vitamina e",
            "vitaminas e",
            "tocoferol"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "vitamina f": {
        "subject": [
            "vitamina f",
            "vitaminas f",
            "graxos essenciais"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "vitamina g": {
        "subject": [
            "vitamina g",
            "vitaminas g",
            "monofosfato de nicotinamida"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "vitamina h": {
        "subject": [
            "vitamina h",
            "vitaminas h",
            "biotina"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "vitamina j": {
        "subject": [
            "vitamina j",
            "vitaminas j",
            "lipoico"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "vitamina k": {
        "subject": [
            "vitamina k",
            "vitaminas k",
            "filoquinona"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "vitamina k1": {
        "subject": [
            "vitamina k1",
            "vitaminas k1",
            "fitoquinona"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "vitamina k2": {
        "subject": [
            "vitamina k2",
            "vitaminas k2",
            "menaquinona"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "vitamina k7": {
        "subject": [
            "vitamina k7",
            "vitaminas k7",
            "mk7"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "vitamina l": {
        "subject": [
            "vitamina l",
            "vitaminas l",
            "adipico"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "vitamina l1": {
        "subject": [
            "vitamina l1"
            "vitaminas l1"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "vitamina l2": {
        "subject": [
            "vitamina l2"
            "vitaminas l2"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "vitamina m": {
        "subject": [
            "vitamina m"
            "vitaminas m"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "vitamina n": {
        "subject": [
            "vitamina n",
            "vitaminas n",
            "pantotenico"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "vitamina o": {
        "subject": [
            "vitamina o"
            "vitaminas o"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "vitamina p": {
        "subject": [
            "vitamina p",
            "vitaminas p",
            "bioflavonoides"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "vitamina q": {
        "subject": [
            "vitamina q",
            "vitaminas q",
            "coenzima q10"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "vitamina r": {
        "subject": [
            "vitamina r",
            "vitaminas r",
            "flavina"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "vitamina s": {
        "subject": [
            "vitamina s",
            "vitaminas s",
            "aminobenzoico"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "vitamina t": {
        "subject": [
            "vitamina t",
            "vitaminas t",
            "bioflavonoides"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "vitamina w": {
        "subject": [
            "vitamina w"
            "vitaminas w"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "wafer": {
        "subject": [
            "wafer",
            "bolacha",
            "biscoito",
            "cookie"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "waxymaize": {
        "subject": [
            "waxymaize",
            "waxy maize",
            "amido de milho"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "whey": {
        "subject": [
            "whey",
            "soro do leite"
        ],
        "may_contain": [
            "protein",
            "concentrad",
            "iso",
            "hidrolisad",
        ],
        "not_contain": [
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
        "may_contain": [],
        "not_contain": []
    },
    "zeaxantina": {
        "subject": [
            "zeaxantina"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "zinco": {
        "subject": [
            "zinco",
            "zinco",
            "zinco"
        ],
        "may_contain": [],
        "not_contain": []
    },
    "zma": {
        "subject": [
            "zma"
        ],
        "may_contain": [],
        "not_contain": []
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

PRONOUNS = {
    "brazil": BRAZIL_PRONOUNS
}

WORDLIST = {
    "supplement": SUPPLEMENT_COMPONENT_LIST,
}