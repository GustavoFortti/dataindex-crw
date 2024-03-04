
def get_synonyms(component_list):
    keywords_list = []
    for component, attributes in component_list.items():
        keywords_list.append(attributes.get("subject"))
    return keywords_list

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

"""

"""

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
        "minimum_of_components": 2,
        "subject_required_in_components": True,
        "not_contain": []
    },
    "albumina": {
        "subject": [
            "albumina"
            "albumin"
            "albumi"
        ],
        "may_contain": [
            "egg",
        ],
        "minimum_of_components": 1,
        "subject_required_in_components": True,
        "not_contain": []
    },
    "alfajor": {
        "subject": [
            "alfajor"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "alho": {
        "subject": [
            "alho"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "aminoacido": {
        "subject": [
            "aminoacido"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "antiox": {
        "subject": [
            "antiox"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "antioxidante": {
        "subject": [
            "antioxidante"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
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
        "minimum_of_components": 1,
        "subject_required_in_components": True,
        "not_contain": []
    },
    "astaxantina": {
        "subject": [
            "astaxantina"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "barrinha": {
        "subject": [
            "barrinha",
            "barra",
            "bar",
            "crunch",
            "snack",
        ],
        "may_contain": [
            "protein",
            "whey",
        ],
        "minimum_of_components": 2,
        "subject_required_in_components": True,
        "not_contain": []
    },
    "batata doce": {
        "subject": [
            "batata doce"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "bcaa": {
        "subject": [
            "bcaa",
            "bca"
        ],
        "may_contain": [
            "aminoacido"
        ],
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "beauty": {
        "subject": [
            "beauty",
            "beleza"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
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
        "minimum_of_components": 1,
        "subject_required_in_components": True,
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
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "betacaroteno": {
        "subject": [
            "betacaroteno"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "biotina": {
        "subject": [
            "biotina"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "blend": {
        "subject": [
            "blend",
            "mistura"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "borragem": {
        "subject": [
            "borragem"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
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
        "minimum_of_components": None,
        "subject_required_in_components": False,
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
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "calcio": {
        "subject": [
            "calcio"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
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
        "minimum_of_components": None,
        "subject_required_in_components": False,
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
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "cartamo": {
        "subject": [
            "cartamo"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "caseinato": {
        "subject": [
            "caseinato"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "cha": {
        "subject": [
            "cha"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "cha verde": {
        "subject": [
            "cha verde"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "chia": {
        "subject": [
            "chia"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "chocolate": {
        "subject": [
            "chocolate"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "cistein": {
        "subject": [
            "cistein",
            "lcisteina"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "coco": {
        "subject": [
            "coco",
            "coco"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "colageno": {
        "subject": [
            "colageno",
            "colagen"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "complexo b": {
        "subject": [
            "complexo b",
            "vitamina b"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "concentrad": {
        "subject": [
            "concentrad"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
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
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "crisp": {
        "subject": [
            "crisp"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "cromo": {
        "subject": [
            "cromo",
            "cromo"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "curcuma": {
        "subject": [
            "curcuma",
            "acafrao"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "dextrose": {
        "subject": [
            "dextrose",
            "maltodextrose"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
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
        "minimum_of_components": None,
        "subject_required_in_components": False,
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
        "minimum_of_components": None,
        "subject_required_in_components": False,
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
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "espirulina": {
        "subject": [
            "espirulina"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "fibra": {
        "subject": [
            "fibra"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "fosfatidilserina": {
        "subject": [
            "fosfatidilserina"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "frutose": {
        "subject": [
            "frutose"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "gengibre": {
        "subject": [
            "gengibre"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "gergelim": {
        "subject": [
            "gergelim"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
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
        "minimum_of_components": 1,
        "subject_required_in_components": True,
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
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "hialuronico": {
        "subject": [
            "hialuronico"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "hidrolisad": {
        "subject": [
            "hidrolisad"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
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
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "imune": {
        "subject": [
            "imune",
            "imunidade"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
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
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "krill": {
        "subject": [
            "krill"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "lecitina": {
        "subject": [
            "lecitina"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
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
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "levagen": {
        "subject": [
            "levagen"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "linhaca": {
        "subject": [
            "linhaca"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "maca peruana": {
        "subject": [
            "maca peruana"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "magnesio": {
        "subject": [
            "magnesio",
            "magnesi"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "malto": {
        "subject": [
            "malto",
            "dextrina",
            "maltodextrina"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
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
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "melatonina": {
        "subject": [
            "melatonina",
            "melatonina"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "monohidratada": {
        "subject": [
            "monohidratada"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "multivitaminico": {
        "subject": [
            "multivitaminico",
            "polivitaminico"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "minerail": {
        "subject": [
            "minerai",
            "minerail"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "nail": {
        "subject": [
            "nail",
            "unha"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "oleo": {
        "subject": [
            "oleo"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "optimsm": {
        "subject": [
            "optimsm"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "palatinose": {
        "subject": [
            "palatinose"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "pastadeamendoim": {
        "subject": [
            "pasta de amendoim",
            "peanut",
            "amendoim"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
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
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "omega 6": {
        "subject": [
            "omega 6",
            "linoléico",
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "picolinato": {
        "subject": [
            "picolinato",
            "picolinato"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
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
        "minimum_of_components": 2,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "primula": {
        "subject": [
            "primula"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "propoli": {
        "subject": [
            "propoli"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
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
        "minimum_of_components": 2,
        "subject_required_in_components": True,
        "not_contain": []
    },
    "psyllium": {
        "subject": [
            "psyllium"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "quitosana": {
        "subject": [
            "quitosana"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "resveratrol": {
        "subject": [
            "resveratrol"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
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
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "semente": {
        "subject": [
            "semente"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "skin": {
        "subject": [
            "skin",
            "pele"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
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
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "spirulina": {
        "subject": [
            "spirulina"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
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
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "tempero": {
        "subject": [
            "tempero"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "termogenico": {
        "subject": [
            "termogenico"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "testofen": {
        "subject": [
            "testofen"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
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
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "transresveratrol": {
        "subject": [
            "transresveratrol"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "triptofano": {
        "subject": [
            "triptofano"
        ],
        "may_contain": [
            "aminoacido"
        ],
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "leucina": {
        "subject": [
            "leucina"
        ],
        "may_contain": [
            "aminoacido"
        ],
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "valina": {
        "subject": [
            "valina"
        ],
        "may_contain": [
            "aminoacido"
        ],
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "isoleucina": {
        "subject": [
            "isoleucina"
        ],
        "may_contain": [
            "aminoacido"
        ],
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "lisina": {
        "subject": [
            "lisina"
        ],
        "may_contain": [
            "aminoacido"
        ],
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "fenilalanina": {
        "subject": [
            "fenilalanina"
        ],
        "may_contain": [
            "aminoacido"
        ],
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "treonina": {
        "subject": [
            "treonina"
        ],
        "may_contain": [
            "aminoacido"
        ],
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "metionina": {
            "subject": [
            "metionina"
        ],
        "may_contain": [
            "aminoacido"
        ],
        "minimum_of_components": None,
        "subject_required_in_components": False,
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
        "minimum_of_components": None,
        "subject_required_in_components": False,
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
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "verisol": {
        "subject": [
            "verisol"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "vitamina": {
        "subject": [
            "vitamina",
            "vitamin"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "vitamina a": {
        "subject": [
            "vitamina a"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "vitamina b1": {
        "subject": [
            "vitamina b1",
            "tiamina"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "vitamina b10": {
        "subject": [
            "vitamina b10",
            "paraaminobenzoico"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "vitamina b11": {
        "subject": [
            "vitamina b11",
            "salicilico"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "vitamina b12": {
        "subject": [
            "vitamina b12",
            "cobalamina"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "vitamina b13": {
        "subject": [
            "vitamina b13",
            "orotico"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "vitamina b15": {
        "subject": [
            "vitamina b15",
            "pangamico"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "vitamina b17": {
        "subject": [
            "vitamina b17",
            "amigdalina"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "vitamina b2": {
        "subject": [
            "vitamina b2",
            "riboflavina"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "vitamina b22": {
        "subject": [
            "vitamina b22",
            "ratanhia"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "vitamina b3": {
        "subject": [
            "vitamina b3",
            "niacina"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "vitamina b4": {
        "subject": [
            "vitamina b4",
            "adenina"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "vitamina b5": {
        "subject": [
            "vitamina b5",
            "pantotenico"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "vitamina b6": {
        "subject": [
            "vitamina b6",
            "piridoxina"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "vitamina b7": {
        "subject": [
            "vitamina b7",
            "biotina"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "vitamina b8": {
        "subject": [
            "vitamina b8",
            "inositol"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "vitamina b9": {
        "subject": [
            "vitamina b9",
            "folico"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "vitamina c": {
        "subject": [
            "vitamina c",
            "ascorbico",
            "ascorbato",
            "ascorbila",
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "vitamina d": {
        "subject": [
            "vitamina d",
            "calciferol"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "vitamina e": {
        "subject": [
            "vitamina e",
            "tocoferol"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "vitamina f": {
        "subject": [
            "vitamina f",
            "graxos essenciais"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "vitamina g": {
        "subject": [
            "vitamina g",
            "monofosfato de nicotinamida"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "vitamina h": {
        "subject": [
            "vitamina h",
            "biotina"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "vitamina j": {
        "subject": [
            "vitamina j",
            "lipoico"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "vitamina k": {
        "subject": [
            "vitamina k",
            "filoquinona"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "vitamina k1": {
        "subject": [
            "vitamina k1",
            "fitoquinona"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "vitamina k2": {
        "subject": [
            "vitamina k2",
            "menaquinona"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "vitamina k7": {
        "subject": [
            "vitamina k7",
            "mk7"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "vitamina l": {
        "subject": [
            "vitamina l",
            "adipico"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "vitamina l1": {
        "subject": [
            "vitamina l1"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "vitamina l2": {
        "subject": [
            "vitamina l2"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "vitamina m": {
        "subject": [
            "vitamina m"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "vitamina n": {
        "subject": [
            "vitamina n",
            "pantotenico"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "vitamina o": {
        "subject": [
            "vitamina o"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "vitamina p": {
        "subject": [
            "vitamina p",
            "bioflavonoides"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "vitamina q": {
        "subject": [
            "vitamina q",
            "coenzima q10"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "vitamina r": {
        "subject": [
            "vitamina r",
            "flavina"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "vitamina s": {
        "subject": [
            "vitamina s",
            "aminobenzoico"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "vitamina t": {
        "subject": [
            "vitamina t",
            "bioflavonoides"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "vitamina w": {
        "subject": [
            "vitamina w"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
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
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "waxymaize": {
        "subject": [
            "waxy maize",
            "amido de milho"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
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
        "minimum_of_components": 2,
        "subject_required_in_components": True,
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
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "zeaxantina": {
        "subject": [
            "zeaxantina"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "zinco": {
        "subject": [
            "zinco",
            "zinco",
            "zinco"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
        "not_contain": []
    },
    "zma": {
        "subject": [
            "zma"
        ],
        "may_contain": [],
        "minimum_of_components": None,
        "subject_required_in_components": False,
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