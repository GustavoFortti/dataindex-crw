from src.lib.wordlist.wordlist_flavor import WORDLIST_FLAVOR

KEYS_WORDLIST_FLAVOR = WORDLIST_FLAVOR.keys()

COLLECTIONS = {
    'whey': {
        "product": [
            "whey",
        ],
        "features": [
            "hidrolisad",
            "concentrad",
            "iso",
            "veg",
        ],
        "ingredients": [
            "colageno",
        ],
        "flavor": KEYS_WORDLIST_FLAVOR,
        "format": [],
        "is_not": [
            "kit",
            "sache",
            "barrinha",
            "crunch",
            "alfajor",
            "wafer",
            "bebida",
        ],
        "maybe_not": [
            "manteiga de amendoim",
        ],
        "indices_flavor": {
            "whey_flavor": {
                "product": "whey",
                "flavor": None
            },
        },
        "indices": {
            "whey_ver_todos": {
                "product": "whey"
            },
            "whey_concentrado": {
                "product": "whey",
                "features": "concentrad",
            },
            "whey_hidrolisado": {
                "product": "whey",
                "features": "hidrolisad",
            },
            "whey_isolado": {
                "product": "whey",
                "features": "iso",
            },
            "whey_vegano": {
                "product": "whey",
                "features": "veg",
            },
        }
    },
    'barrinha': {
        "product": [
            "barrinha",
        ],
        "features": [
            "veg",
        ],
        "ingredients": [
            "colageno",
        ],
        "flavor": KEYS_WORDLIST_FLAVOR,
        "format": [],
        "is_not": [
            "kit",
            "alfajor",
            "wafer",
            "bebida",
        ],
        "maybe_not": [],
        "indices_flavor": {
            "barrinha_flavor": {
                "product": "barrinha",
                "flavor": None
            },
        },
        "indices": {
            "barrinha_ver_todos": {
                "product": "barrinha"
            },
            "barrinha_vegano": {
                "product": "barrinha",
                "features": "veg",
            },
        }
    },
    'creatina': {
        "product": [
            "creatina",
        ],
        "features": [
            "veg",
            "creapure",
        ],
        "ingredients": [
        ],
        "flavor": KEYS_WORDLIST_FLAVOR,
        "format": [],
        "is_not": [
            "kit",
            "whey",
            "barrinha",
            "pretreino",
            "mass",
            "alfajor",
            "wafer",
            "bebida",
        ],
        "maybe_not": [],
        "rule_fields": [
            {
                "field": "quantity",
                "name": "1kg",
                "range": [999, 10000],
            },
            {
                "field": "quantity",
                "name": "500g",
                "range": [499, 999],
            },
        ],
        "indices_flavor": [],
        "indices": {
            "creatina_ver_todos": {
                "product": "creatina"
            },
            "creatina_vegano": {
                "product": "creatina",
                "features": "veg",
            },
            "creatina_creapure": {
                "product": "creatina",
                "features": "creapure",
            },
        }
    },
    'pretreino': {
        "product": [
            "pretreino",
        ],
        "features": [
            "veg",
        ],
        "ingredients": [
        ],
        "flavor": KEYS_WORDLIST_FLAVOR,
        "format": [],
        "is_not": [
            "kit",
            "whey",
            "barrinha",
            "mass",
            "alfajor",
            "wafer",
        ],
        "maybe_not": [],
        "indices_flavor": [],
        "indices": {
            "pretreino_ver_todos": {
                "product": "pretreino"
            },
            "pretreino_vegano": {
                "product": "pretreino",
                "features": "veg",
            },
        }
    }
}
