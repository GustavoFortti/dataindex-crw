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
            "mass",
            "dose",
            "wafer",
            "bebida",
        ],
        "maybe_not": [
            "manteiga de amendoim",
        ],
        "default_collection": ["protein_see_all"],
        "indices_flavor": {
            "whey_flavor": {
                "product": "whey",
                "flavor": None
            },
        },
        "indices": {
            "whey_see_all": {
                "product": "whey",
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
    'whey_drink': {
        "product": [
            "whey",
            "bebida",
        ],
        "features": [
            "bebida",
            "hidrolisad",
            "concentrad",
            "iso",
            "veg",
        ],
        "ingredients": [],
        "flavor": KEYS_WORDLIST_FLAVOR,
        "format": [],
        "is_not": [
            "kit",
            "sache",
            "barrinha",
            "crunch",
            "alfajor",
            "wafer",
        ],
        "maybe_not": [
            "manteiga de amendoim",
        ],
        "default_collection": ["protein_see_all"],
        "indices_flavor": {
            "whey_flavor": {
                "product": "whey",
                "flavor": None
            },
        },
        "indices": {
            "whey_drink": {
                "product": "bebida",
                "features": "whey"
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
            "barbecue",
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
            "barrinha_see_all": {
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
            "beef",
            "soy",
            "ervilha",
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
            "creatina_see_all": {
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
            "pretreino_see_all": {
                "product": "pretreino"
            },
            "pretreino_vegano": {
                "product": "pretreino",
                "features": "veg",
            },
        }
    },
    'soy': {
        "product": [
            "soy",
            "protein",
        ],
        "features": [
            "veg",
        ],
        "ingredients": [],
        "flavor": KEYS_WORDLIST_FLAVOR,
        "format": [],
        "is_not": [
            "kit",
            "whey",
            "barrinha",
            "mass",
            "alfajor",
            "pretreino",
            "wafer",
        ],
        "maybe_not": [],
        "default_collection": ["protein_see_all"],
        "indices_flavor": [],
        "indices": {
            "soy_see_all": {
                "product": "soy"
            },
        }
    },
    'ervilha': {
        "product": [
            "ervilha",
            "protein",
        ],
        "features": [
            "veg",
        ],
        "ingredients": [],
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
        "default_collection": ["protein_see_all"],
        "indices_flavor": [],
        "indices": {
            "ervilha_see_all": {
                "product": "ervilha"
            },
        }
    },
    'colageno': {
        "product": [
            "colageno",
        ],
        "features": [
        ],
        "ingredients": [],
        "flavor": KEYS_WORDLIST_FLAVOR,
        "format": [],
        "is_not": [
            "kit",
            "whey",
            "barrinha",
            "mass",
            "alfajor",
            "beef",
            "wafer",
        ],
        "maybe_not": [],
        "default_collection": ["protein_see_all"],
        "indices_flavor": [],
        "indices": {
            "colageno_see_all": {
                "product": "colageno"
            },
        }
    },
    'casein': {
        "product": [
            "casein",
        ],
        "features": [],
        "ingredients": [],
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
        "default_collection": ["protein_see_all"],
        "indices_flavor": [],
        "indices": {
            "casein_see_all": {
                "product": "casein"
            },
        }
    },
    'albumina': {
        "product": [
            "albumina",
        ],
        "features": [],
        "ingredients": [],
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
        "default_collection": ["protein_see_all"],
        "indices_flavor": [],
        "indices": {
            "albumina_see_all": {
                "product": "albumina"
            },
        }
    },
    'beef': {
        "product": [
            "beef",
            "protein"
        ],
        "features": [
            "beef"
        ],
        "ingredients": [],
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
        "default_collection": ["protein_see_all"],
        "indices_flavor": [],
        "indices": {
            "beef_see_all": {
                "product": "protein",
                "features": "beef"
            },
        }
    },
    'blend': {
        "product": [
            "blend",
            "protein"
        ],
        "features": [
            "blend"
        ],
        "ingredients": [],
        "flavor": KEYS_WORDLIST_FLAVOR,
        "format": [],
        "is_not": [
            "kit",
            "barrinha",
            "mass",
            "leucin",
            "alfajor",
            "taurina",
            "wafer",
        ],
        "maybe_not": [],
        "default_collection": ["protein_see_all"],
        "indices_flavor": [],
        "indices": {
            "blend_see_all": {
                "product": "protein",
                "features": "blend"
            },
        }
    },
    'rice': {
        "product": [
            "rice",
            "protein"
        ],
        "features": [
            "rice"
        ],
        "ingredients": [],
        "flavor": KEYS_WORDLIST_FLAVOR,
        "format": [],
        "is_not": [
            "kit",
            "barrinha",
            "mass",
            "leucin",
            "alfajor",
            "taurina",
            "wafer",
        ],
        "maybe_not": [],
        "default_collection": ["protein_see_all"],
        "indices_flavor": [],
        "indices": {
            "rice_see_all": {
                "product": "protein",
                "features": "rice"
            },
        }
    },
    'mass': {
        "product": [
            "mass",
        ],
        "features": [
            "protein"
        ],
        "ingredients": [],
        "flavor": KEYS_WORDLIST_FLAVOR,
        "format": [],
        "is_not": [
            "kit",
            "barrinha",
            "alfajor",
            "wafer",
        ],
        "maybe_not": [],
        "indices_flavor": [],
        "indices": {
            "mass_see_all": {
                "product": "mass",
            },
        }
    },
    'manteiga_de_amendoim': {
        "product": [
            "manteiga de amendoim",
        ],
        "features": [],
        "ingredients": [],
        "flavor": KEYS_WORDLIST_FLAVOR,
        "format": [],
        "is_not": [
            "kit",
            "barrinha",
            "alfajor",
            "wafer",
        ],
        "maybe_not": [],
        "indices_flavor": [],
        "indices": {
            "manteiga_de_amendoim_see_all": {
                "product": "manteiga de amendoim",
            },
        }
    },
    'waxymaize': {
        "product": [
            "waxymaize",
        ],
        "features": [],
        "ingredients": [],
        "flavor": KEYS_WORDLIST_FLAVOR,
        "format": [],
        "is_not": [
            "kit",
            "barrinha",
            "creatina",
            "whey",
            "alfajor",
            "wafer",
        ],
        "maybe_not": [],
        "default_collection": ["carboidrato_see_all"],
        "indices_flavor": [],
        "indices": {
            "waxymaize_see_all": {
                "product": "waxymaize",
            },
        }
    },
    'maltodextrina': {
        "product": [
            "maltodextrina",
        ],
        "features": [],
        "ingredients": [],
        "flavor": KEYS_WORDLIST_FLAVOR,
        "format": [],
        "is_not": [
            "kit",
            "barrinha",
            "creatina",
            "whey",
            "alfajor",
            "wafer",
        ],
        "maybe_not": [],
        "default_collection": ["carboidrato_see_all"],
        "indices_flavor": [],
        "indices": {
            "maltodextrina_see_all": {
                "product": "maltodextrina",
            },
        }
    },
    'dextrose': {
        "product": [
            "dextrose",
        ],
        "features": [],
        "ingredients": [],
        "flavor": KEYS_WORDLIST_FLAVOR,
        "format": [],
        "is_not": [
            "kit",
            "barrinha",
            "creatina",
            "whey",
            "alfajor",
            "wafer",
        ],
        "maybe_not": [],
        "default_collection": ["carboidrato_see_all"],
        "indices_flavor": [],
        "indices": {
            "dextrose_see_all": {
                "product": "dextrose",
            },
        }
    },
    'palatinose': {
        "product": [
            "palatinose",
        ],
        "features": [],
        "ingredients": [],
        "flavor": KEYS_WORDLIST_FLAVOR,
        "format": [],
        "is_not": [
            "kit",
            "barrinha",
            "creatina",
            "whey",
            "alfajor",
            "wafer",
        ],
        "maybe_not": [],
        "default_collection": ["carboidrato_see_all"],
        "indices_flavor": [],
        "indices": {
            "palatinose_see_all": {
                "product": "palatinose",
            },
        }
    },
}
