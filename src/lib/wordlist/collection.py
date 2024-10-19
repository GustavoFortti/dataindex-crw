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
            "granola",
            "wafer",
            "bebida",
        ],
        "maybe_not": [
            "manteiga de amendoim",
        ],
        "default_collection": ["protein_see_all"],
        "promotion_collection": "whey_promotion",
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
        }
    },
    'whey_sache': {
        "product": [
            "whey",
        ],
        "features": [
            "hidrolisad",
            "concentrad",
            "iso",
            "veg",
            "sache",
        ],
        "ingredients": [
            "colageno",
        ],
        "flavor": {},
        "format": [],
        "is_not": [
            "kit",
            "barrinha",
            "crunch",
            "alfajor",
            "mass",
            "wafer",
            "bebida",
        ],
        "maybe_not": [
            "manteiga de amendoim",
        ],
        "default_collection": ["protein_see_all"],
        "promotion_collection": "whey_promotion",
        "indices_flavor": {
            "whey_flavor": {
                "product": "whey",
                "flavor": None
            },
        },
        "indices": {
            "whey_sache": {
                "product": "whey",
                "features": "sache",
            },
        }
    },
    'whey_kit': {
        "product": [
            "whey",
        ],
        "features": [
            "hidrolisad",
            "concentrad",
            "iso",
            "veg",
            "kit",
        ],
        "ingredients": [
            "colageno",
        ],
        "flavor": {},
        "format": [],
        "is_not": [
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
        "promotion_collection": None,
        "indices_flavor": {
            "whey_flavor": {
                "product": "whey",
                "flavor": None
            },
        },
        "indices": {
            "whey_kit_see_all": {
                "product": "whey",
                "features": "kit",
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
        "flavor": {},
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
        "promotion_collection": "whey_promotion",
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
            "sache",
            "wafer",
            "barbecue",
            "bebida",
        ],
        "maybe_not": [],
        "promotion_collection": "barrinha_promotion",
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
    'candy': {
        "product": [
            "crunch",
        ],
        "features": [
            "wafer",
            "alfajor",
        ],
        "ingredients": [
            "colageno",
        ],
        "flavor": KEYS_WORDLIST_FLAVOR,
        "format": [],
        "is_not": [
            "kit",
            "alfajor",
            "sache",
            "barbecue",
            "bebida",
        ],
        "maybe_not": [],
        "promotion_collection": None,
        "indices_flavor": {
            "candy_flavor": {
                "product": "crunch",
                "flavor": None
            },
        },
        "indices": {
            "candy_see_all": {
                "product": "crunch"
            },
            "candy_see_all": {
                "features": "wafer"
            },
            "candy_see_all": {
                "features": "alfajor"
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
            "hidrolisad",
            "concentrad",
            "iso",
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
        "promotion_collection": "creatina_promotion",
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
    'kit_creatina': {
        "product": [
            "creatina",
        ],
        "features": [
            "veg",
            "creapure",
            "kit"
        ],
        "ingredients": [
        ],
        "flavor": {},
        "format": [],
        "is_not": [
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
        "promotion_collection": None,
        "indices_flavor": [],
        "indices": {
            "kit_creatina": {
                "product": "creatina",
                "features": "kit",
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
            "cafein",
            "betaalanina",
            "arginin",
        ],
        "score_per_ingredients": True,
        "flavor": KEYS_WORDLIST_FLAVOR,
        "format": [],
        "is_not": [
            "kit",
            "whey",
            "barrinha",
            "mass",
            "alfajor",
            "granola",
            "wafer",
        ],
        "maybe_not": [],
        "promotion_collection": "pretreino_promotion",
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
            "sache",
            "alfajor",
            "pretreino",
            "wafer",
        ],
        "maybe_not": [],
        "default_collection": ["protein_see_all"],
        "promotion_collection": "protein_promotion",
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
            "sache",
            "mass",
            "alfajor",
            "wafer",
        ],
        "maybe_not": [],
        "default_collection": ["protein_see_all"],
        "promotion_collection": "protein_promotion",
        "indices_flavor": [],
        "indices": {
            "ervilha_see_all": {
                "product": "ervilha"
            },
        }
    },
    'rice': {
        "product": [
            "rice",
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
            "sache",
            "mass",
            "alfajor",
            "wafer",
        ],
        "maybe_not": [],
        "default_collection": ["protein_see_all"],
        "promotion_collection": "protein_promotion",
        "indices_flavor": [],
        "indices": {
            "rice_see_all": {
                "product": "rice"
            },
        }
    },
    'protein': {
        "product": [
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
            "soy",
            "ervilha",
            "rice",
            "barrinha",
            "sache",
            "mass",
            "alfajor",
            "wafer",
        ],
        "maybe_not": [],
        "default_collection": [],
        "promotion_collection": "protein_promotion",
        "indices_flavor": [],
        "indices": {
            "protein_see_all": {
                "product": "protein"
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
        "promotion_collection": "protein_promotion",
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
        "promotion_collection": "protein_promotion",
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
        "promotion_collection": "protein_promotion",
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
        "promotion_collection": "protein_promotion",
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
            "sache",
            "alfajor",
            "taurina",
            "wafer",
        ],
        "maybe_not": [],
        "default_collection": ["protein_see_all"],
        "promotion_collection": "protein_promotion",
        "indices_flavor": [],
        "indices": {
            "blend_see_all": {
                "product": "protein",
                "features": "blend"
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
        "promotion_collection": None,
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
            "pretreino",
        ],
        "maybe_not": [],
        "promotion_collection": None,
        "indices_flavor": [],
        "indices": {
            "manteiga_de_amendoim_see_all": {
                "product": "manteiga de amendoim",
            },
        }
    },
    'postreino': {
        "product": [
            "postreino",
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
            "pretreino",
        ],
        "maybe_not": [],
        "promotion_collection": None,
        "indices_flavor": [],
        "indices": {
            "postreino_see_all": {
                "product": "postreino",
            },
        }
    },
    'intratreino': {
        "product": [
            "intratreino",
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
            "pretreino",
        ],
        "maybe_not": [],
        "promotion_collection": None,
        "indices_flavor": [],
        "indices": {
            "intratreino_see_all": {
                "product": "intratreino",
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
        "promotion_collection": "carboidrato_promotion",
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
        "promotion_collection": "carboidrato_promotion",
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
        "promotion_collection": "carboidrato_promotion",
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
        "promotion_collection": "carboidrato_promotion",
        "indices_flavor": [],
        "indices": {
            "palatinose_see_all": {
                "product": "palatinose",
            },
        }
    },
    'bcaa': {
        "product": [
            "bcaa",
        ],
        "features": [],
        "ingredients": [],
        "flavor": KEYS_WORDLIST_FLAVOR,
        "format": [],
        "is_not": [
            "kit",
            "barrinha",
            "creatina",
            "glutamin",
            "betaalanina",
            "blend",
            "ervilha",
            "beef",
            "iso",
            "pretreino",
            "barbecue",
            "soy",
            "mass",
            "whey",
            "alfajor",
            "wafer",
        ],
        "maybe_not": [],
        "default_collection": ["aminoacidos_see_all"],
        "promotion_collection": "aminoacidos_promotion",
        "indices_flavor": [],
        "indices": {
            "bcaa_see_all": {
                "product": "bcaa",
            },
        }
    },
    'arginin': {
        "product": [
            "arginin",
        ],
        "features": [],
        "ingredients": [],
        "flavor": KEYS_WORDLIST_FLAVOR,
        "format": [],
        "is_not": [
            "kit",
            "barrinha",
            "creatina",
            "glutamin",
            "betaalanina",
            "blend",
            "ervilha",
            "beef",
            "iso",
            "pretreino",
            "barbecue",
            "soy",
            "mass",
            "whey",
            "alfajor",
            "wafer",
        ],
        "maybe_not": [],
        "default_collection": ["aminoacidos_see_all"],
        "promotion_collection": "aminoacidos_promotion",
        "indices_flavor": [],
        "indices": {
            "arginin_see_all": {
                "product": "arginin",
            },
        }
    },
    'glutamin': {
        "product": [
            "glutamin",
        ],
        "features": [],
        "ingredients": [],
        "flavor": KEYS_WORDLIST_FLAVOR,
        "format": [],
        "is_not": [
            "kit",
            "barrinha",
            "creatina",
            "arginin",
            "betaalanina",
            "blend",
            "ervilha",
            "beef",
            "iso",
            "pretreino",
            "barbecue",
            "soy",
            "mass",
            "whey",
            "alfajor",
            "wafer",
        ],
        "maybe_not": [],
        "default_collection": ["aminoacidos_see_all"],
        "promotion_collection": "aminoacidos_promotion",
        "indices_flavor": [],
        "indices": {
            "glutamin_see_all": {
                "product": "glutamin",
            },
        }
    },
    'betaalanina': {
        "product": [
            "betaalanina",
        ],
        "features": [],
        "ingredients": [],
        "flavor": KEYS_WORDLIST_FLAVOR,
        "format": [],
        "is_not": [
            "kit",
            "barrinha",
            "creatina",
            "glutamin",
            "bcaa",
            "blend",
            "ervilha",
            "beef",
            "iso",
            "barbecue",
            "soy",
            "mass",
            "whey",
            "alfajor",
            "wafer",
        ],
        "maybe_not": [],
        "default_collection": ["aminoacidos_see_all"],
        "promotion_collection": "aminoacidos_promotion",
        "indices_flavor": [],
        "indices": {
            "betaalanina_see_all": {
                "product": "betaalanina",
            },
        }
    },
    'taurina': {
        "product": [
            "taurina",
        ],
        "features": [],
        "ingredients": [],
        "flavor": KEYS_WORDLIST_FLAVOR,
        "format": [],
        "is_not": [
            "kit",
            "barrinha",
            "cafein",
            "creatina",
            "vitamina b",
            "glutamin",
            "bcaa",
            "blend",
            "ervilha",
            "beef",
            "iso",
            "barbecue",
            "soy",
            "mass",
            "whey",
            "alfajor",
            "wafer",
        ],
        "maybe_not": [],
        "default_collection": ["aminoacidos_see_all"],
        "promotion_collection": "aminoacidos_promotion",
        "indices_flavor": [],
        "indices": {
            "taurina_see_all": {
                "product": "taurina",
            },
        }
    },
    'multivitaminico': {
        "product": [
            "multivitaminico",
        ],
        "features": [],
        "ingredients": [],
        "flavor": KEYS_WORDLIST_FLAVOR,
        "format": [],
        "is_not": [
            "kit",
            "barrinha",
            "creatina",
            "glutamin",
            "bcaa",
            "blend",
            "ervilha",
            "beef",
            "bcaa",
            "iso",
            "barbecue",
            "soy",
            "mass",
            "whey",
            "alfajor",
            "wafer",
        ],
        "maybe_not": [],
        "default_collection": ["vitaminas_minerias_see_all"],
        "promotion_collection": "vitaminas_minerias_promotion",
        "indices_flavor": [],
        "indices": {
            "multivitaminico_see_all": {
                "product": "multivitaminico",
            },
        }
    },
    'vitamina_a': {
        "product": [
            "vitamina a",
        ],
        "features": [],
        "ingredients": [],
        "flavor": KEYS_WORDLIST_FLAVOR,
        "format": [],
        "is_not": [
            "kit",
            "barrinha",
            "creatina",
            "glutamin",
            "bcaa",
            "omega 3",
            "oleo",
            "blend",
            "ervilha",
            "beef",
            "bcaa",
            "iso",
            "barbecue",
            "soy",
            "mass",
            "whey",
            "alfajor",
            "wafer",
        ],
        "maybe_not": [],
        "default_collection": ["vitaminas_minerias_see_all"],
        "promotion_collection": "vitaminas_minerias_promotion",
        "indices_flavor": [],
        "indices": {
            "vitamina_a_see_all": {
                "product": "vitamina a",
            },
        }
    },
    'vitamina_b': {
        "product": [
            "vitamina b",
        ],
        "features": [],
        "ingredients": [
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
            "vitamina b9",
        ],
        "score_per_ingredients": True,
        "flavor": KEYS_WORDLIST_FLAVOR,
        "format": [],
        "is_not": [
            "kit",
            "barrinha",
            "creatina",
            "glutamin",
            "bcaa",
            "blend",
            "ervilha",
            "beef",
            "bcaa",
            "iso",
            "barbecue",
            "soy",
            "mass",
            "whey",
            "alfajor",
            "wafer",
        ],
        "maybe_not": [],
        "default_collection": ["vitaminas_minerias_see_all"],
        "promotion_collection": "vitaminas_minerias_promotion",
        "indices_flavor": [],
        "indices": {
            "vitamina_b_see_all": {
                "product": "vitamina b",
            },
        }
    },
    'biotina': {
        "product": [
            "biotina",
        ],
        "features": [],
        "ingredients": [],
        "flavor": KEYS_WORDLIST_FLAVOR,
        "format": [],
        "is_not": [
            "kit",
            "barrinha",
            "creatina",
            "glutamin",
            "bcaa",
            "blend",
            "ervilha",
            "beef",
            "bcaa",
            "iso",
            "barbecue",
            "soy",
            "mass",
            "whey",
            "alfajor",
            "wafer",
        ],
        "maybe_not": [],
        "default_collection": ["vitaminas_minerias_see_all"],
        "promotion_collection": "vitaminas_minerias_promotion",
        "indices_flavor": [],
        "indices": {
            "biotina_see_all": {
                "product": "biotina",
            },
        }
    },
    'vitamina_c': {
        "product": [
            "vitamina c",
        ],
        "features": [],
        "ingredients": [],
        "flavor": KEYS_WORDLIST_FLAVOR,
        "format": [],
        "is_not": [
            "kit",
            "barrinha",
            "creatina",
            "glutamin",
            "bcaa",
            "blend",
            "ervilha",
            "beef",
            "bcaa",
            "iso",
            "barbecue",
            "soy",
            "mass",
            "whey",
            "alfajor",
            "wafer",
        ],
        "maybe_not": [],
        "default_collection": ["vitaminas_minerias_see_all"],
        "promotion_collection": "vitaminas_minerias_promotion",
        "indices_flavor": [],
        "indices": {
            "vitamina_c_see_all": {
                "product": "vitamina c",
            },
        }
    },
    'vitamina_d': {
        "product": [
            "vitamina d",
        ],
        "features": [],
        "ingredients": [],
        "flavor": KEYS_WORDLIST_FLAVOR,
        "format": [],
        "is_not": [
            "kit",
            "barrinha",
            "creatina",
            "glutamin",
            "bcaa",
            "blend",
            "ervilha",
            "beef",
            "bcaa",
            "iso",
            "barbecue",
            "soy",
            "mass",
            "whey",
            "alfajor",
            "wafer",
        ],
        "maybe_not": [],
        "default_collection": ["vitaminas_minerias_see_all"],
        "promotion_collection": "vitaminas_minerias_promotion",
        "indices_flavor": [],
        "indices": {
            "vitamina_d_see_all": {
                "product": "vitamina d",
            },
        }
    },
    'vitamina_e': {
        "product": [
            "vitamina e",
        ],
        "features": [],
        "ingredients": [],
        "flavor": KEYS_WORDLIST_FLAVOR,
        "format": [],
        "is_not": [
            "kit",
            "barrinha",
            "creatina",
            "glutamin",
            "bcaa",
            "granola",
            "blend",
            "ervilha",
            "beef",
            "bcaa",
            "iso",
            "barbecue",
            "soy",
            "mass",
            "whey",
            "alfajor",
            "wafer",
        ],
        "maybe_not": [],
        "default_collection": ["vitaminas_minerias_see_all"],
        "promotion_collection": "vitaminas_minerias_promotion",
        "indices_flavor": [],
        "indices": {
            "vitamina_e_see_all": {
                "product": "vitamina e",
            },
        }
    },
    'vitamina_k': {
        "product": [
            "vitamina k",
        ],
        "features": [],
        "ingredients": [
            "vitamina k1",
            "vitamina k2",
            "vitamina k7",
        ],
        "score_per_ingredients": True,
        "flavor": KEYS_WORDLIST_FLAVOR,
        "format": [],
        "is_not": [
            "kit",
            "barrinha",
            "creatina",
            "glutamin",
            "bcaa",
            "blend",
            "ervilha",
            "beef",
            "bcaa",
            "iso",
            "barbecue",
            "soy",
            "mass",
            "whey",
            "alfajor",
            "wafer",
        ],
        "maybe_not": [],
        "default_collection": ["vitaminas_minerias_see_all"],
        "promotion_collection": "vitaminas_minerias_promotion",
        "indices_flavor": [],
        "indices": {
            "vitamina_k_see_all": {
                "product": "vitamina k",
            },
        }
    },
    'vitamina_q': {
        "product": [
            "vitamina q",
        ],
        "features": [],
        "ingredients": [],
        "score_per_ingredients": True,
        "flavor": KEYS_WORDLIST_FLAVOR,
        "format": [],
        "is_not": [
            "kit",
            "barrinha",
            "creatina",
            "glutamin",
            "bcaa",
            "blend",
            "ervilha",
            "beef",
            "bcaa",
            "iso",
            "barbecue",
            "soy",
            "mass",
            "whey",
            "alfajor",
            "wafer",
        ],
        "maybe_not": [],
        "default_collection": ["vitaminas_minerias_see_all"],
        "promotion_collection": "vitaminas_minerias_promotion",
        "indices_flavor": [],
        "indices": {
            "vitamina_q_see_all": {
                "product": "vitamina q",
            },
        }
    },
    'zinco': {
        "product": [
            "zinco",
        ],
        "features": [],
        "ingredients": [],
        "score_per_ingredients": True,
        "flavor": KEYS_WORDLIST_FLAVOR,
        "format": [],
        "is_not": [
            "kit",
            "barrinha",
            "creatina",
            "glutamin",
            "bcaa",
            "blend",
            "ervilha",
            "beef",
            "bcaa",
            "iso",
            "barbecue",
            "soy",
            "mass",
            "whey",
            "alfajor",
            "wafer",
        ],
        "maybe_not": [],
        "default_collection": ["vitaminas_minerias_see_all"],
        "promotion_collection": "vitaminas_minerias_promotion",
        "indices_flavor": [],
        "indices": {
            "zinco_see_all": {
                "product": "zinco",
            },
        }
    },
    'calcio': {
        "product": [
            "calcio",
        ],
        "features": [],
        "ingredients": [],
        "score_per_ingredients": True,
        "flavor": KEYS_WORDLIST_FLAVOR,
        "format": [],
        "is_not": [
            "kit",
            "barrinha",
            "creatina",
            "glutamin",
            "bcaa",
            "blend",
            "ervilha",
            "beef",
            "bcaa",
            "iso",
            "barbecue",
            "soy",
            "mass",
            "whey",
            "alfajor",
            "wafer",
        ],
        "maybe_not": [],
        "default_collection": ["vitaminas_minerias_see_all"],
        "promotion_collection": "vitaminas_minerias_promotion",
        "indices_flavor": [],
        "indices": {
            "calcio_see_all": {
                "product": "calcio",
            },
        }
    },
    'magnesio': {
        "product": [
            "magnesio",
        ],
        "features": [],
        "ingredients": [],
        "score_per_ingredients": True,
        "flavor": KEYS_WORDLIST_FLAVOR,
        "format": [],
        "is_not": [
            "kit",
            "barrinha",
            "creatina",
            "glutamin",
            "bcaa",
            "blend",
            "ervilha",
            "beef",
            "bcaa",
            "iso",
            "barbecue",
            "soy",
            "mass",
            "whey",
            "alfajor",
            "wafer",
        ],
        "maybe_not": [],
        "default_collection": ["vitaminas_minerias_see_all"],
        "promotion_collection": "vitaminas_minerias_promotion",
        "indices_flavor": [],
        "indices": {
            "magnesio_see_all": {
                "product": "magnesio",
            },
        }
    },
    'ferro': {
        "product": [
            "ferro",
        ],
        "features": [],
        "ingredients": [],
        "score_per_ingredients": True,
        "flavor": KEYS_WORDLIST_FLAVOR,
        "format": [],
        "is_not": [
            "kit",
            "barrinha",
            "creatina",
            "glutamin",
            "bcaa",
            "blend",
            "ervilha",
            "beef",
            "bcaa",
            "iso",
            "barbecue",
            "soy",
            "mass",
            "whey",
            "alfajor",
            "wafer",
        ],
        "maybe_not": [],
        "default_collection": ["vitaminas_minerias_see_all"],
        "promotion_collection": "vitaminas_minerias_promotion",
        "indices_flavor": [],
        "indices": {
            "ferro_see_all": {
                "product": "ferro",
            },
        }
    },
    'termogenico': {
        "product": [
            "termogenico",
        ],
        "features": [],
        "ingredients": [],
        "score_per_ingredients": True,
        "flavor": KEYS_WORDLIST_FLAVOR,
        "format": [],
        "is_not": [
            "kit",
            "barrinha",
            "creatina",
            "glutamin",
            "bcaa",
            "blend",
            "ervilha",
            "beef",
            "bcaa",
            "iso",
            "barbecue",
            "soy",
            "mass",
            "whey",
            "alfajor",
            "wafer",
        ],
        "maybe_not": [],
        "default_collection": ["termogenico_see_all"],
        "promotion_collection": "termogenico_promotion",
        "indices_flavor": [],
        "indices": {
            "termogenico_see_all": {
                "product": "termogenico",
            },
        }
    },
    'cafein': {
        "product": [
            "cafein",
        ],
        "features": [],
        "ingredients": [],
        "flavor": KEYS_WORDLIST_FLAVOR,
        "format": [],
        "is_not": [
            "kit",
            "barrinha",
            "creatina",
            "glutamin",
            "bcaa",
            "blend",
            "ervilha",
            "beef",
            "iso",
            "barbecue",
            "soy",
            "mass",
            "whey",
            "alfajor",
            "wafer",
        ],
        "maybe_not": [],
        "default_collection": ["termogenico_see_all"],
        "promotion_collection": "termogenico_promotion",
        "indices_flavor": [],
        "indices": {
            "cafein_see_all": {
                "product": "cafein",
            },
        }
    },
    'chaverde': {
        "product": [
            "chaverde",
        ],
        "features": [],
        "ingredients": [],
        "flavor": KEYS_WORDLIST_FLAVOR,
        "format": [],
        "is_not": [
            "kit",
            "barrinha",
            "creatina",
            "glutamin",
            "bcaa",
            "blend",
            "pretreino",
            "ervilha",
            "beef",
            "iso",
            "barbecue",
            "soy",
            "mass",
            "whey",
            "alfajor",
            "wafer",
        ],
        "maybe_not": [],
        "default_collection": ["termogenico_see_all"],
        "promotion_collection": "termogenico_promotion",
        "indices_flavor": [],
        "indices": {
            "chaverde_see_all": {
                "product": "chaverde",
            },
        }
    },
    'guarana': {
        "product": [
            "guarana",
        ],
        "features": [],
        "ingredients": [],
        "flavor": KEYS_WORDLIST_FLAVOR,
        "format": [],
        "is_not": [
            "kit",
            "barrinha",
            "creatina",
            "glutamin",
            "pretreino",
            "blend",
            "ervilha",
            "beef",
            "bcaa",
            "iso",
            "barbecue",
            "soy",
            "mass",
            "whey",
            "alfajor",
            "wafer",
        ],
        "maybe_not": [],
        "default_collection": ["termogenico_see_all"],
        "promotion_collection": "termogenico_promotion",
        "indices_flavor": [],
        "indices": {
            "guarana_see_all": {
                "product": "guarana",
            },
        }
    },
    'gengibre': {
        "product": [
            "gengibre",
        ],
        "features": [],
        "ingredients": [],
        "flavor": KEYS_WORDLIST_FLAVOR,
        "format": [],
        "is_not": [
            "kit",
            "barrinha",
            "creatina",
            "glutamin",
            "bcaa",
            "pretreino",
            "blend",
            "ervilha",
            "beef",
            "iso",
            "barbecue",
            "soy",
            "mass",
            "whey",
            "alfajor",
            "wafer",
        ],
        "maybe_not": [],
        "default_collection": ["termogenico_see_all"],
        "promotion_collection": "termogenico_promotion",
        "indices_flavor": [],
        "indices": {
            "gengibre_see_all": {
                "product": "gengibre",
            },
        }
    },
    'carnitin': {
        "product": [
            "carnitin",
        ],
        "features": [],
        "ingredients": [],
        "flavor": KEYS_WORDLIST_FLAVOR,
        "format": [],
        "is_not": [
            "kit",
            "barrinha",
            "creatina",
            "glutamin",
            "bcaa",
            "pretreino",
            "blend",
            "ervilha",
            "beef",
            "iso",
            "barbecue",
            "soy",
            "mass",
            "whey",
            "alfajor",
            "wafer",
        ],
        "maybe_not": [],
        "default_collection": ["termogenico_see_all"],
        "promotion_collection": "termogenico_promotion",
        "indices_flavor": [],
        "indices": {
            "carnitin_see_all": {
                "product": "carnitin",
            },
        }
    },
    'omega_3': {
        "product": [
            "omega 3",
        ],
        "features": [],
        "ingredients": [],
        "flavor": KEYS_WORDLIST_FLAVOR,
        "format": [],
        "is_not": [
            "kit",
            "barrinha",
            "creatina",
            "glutamin",
            "bcaa",
            "pretreino",
            "blend",
            "ervilha",
            "beef",
            "iso",
            "sache",
            "barbecue",
            "soy",
            "mass",
            "whey",
            "alfajor",
            "wafer",
        ],
        "maybe_not": [],
        "default_collection": ["oleos_see_all"],
        "promotion_collection": "oleos_promotion",
        "indices_flavor": [],
        "indices": {
            "omega_3_see_all": {
                "product": "omega 3",
            },
        }
    },
    'oleo_de_coco': {
        "product": [
            "oleo de coco",
        ],
        "features": [],
        "ingredients": [],
        "flavor": KEYS_WORDLIST_FLAVOR,
        "format": [],
        "is_not": [
            "kit",
            "barrinha",
            "creatina",
            "glutamin",
            "bcaa",
            "pretreino",
            "blend",
            "ervilha",
            "beef",
            "iso",
            "barbecue",
            "soy",
            "mass",
            "whey",
            "alfajor",
            "wafer",
        ],
        "maybe_not": [],
        "default_collection": ["oleos_see_all"],
        "promotion_collection": "oleos_promotion",
        "indices_flavor": [],
        "indices": {
            "oleo_de_coco_see_all": {
                "product": "oleo de coco",
            },
        }
    },
    'oleo_de_cartamo': {
        "product": [
            "oleo de cartamo",
        ],
        "features": [],
        "ingredients": [],
        "flavor": KEYS_WORDLIST_FLAVOR,
        "format": [],
        "is_not": [
            "kit",
            "barrinha",
            "creatina",
            "glutamin",
            "bcaa",
            "pretreino",
            "blend",
            "ervilha",
            "beef",
            "iso",
            "barbecue",
            "soy",
            "mass",
            "whey",
            "alfajor",
            "wafer",
        ],
        "maybe_not": [],
        "default_collection": ["oleos_see_all"],
        "promotion_collection": "oleos_promotion",
        "indices_flavor": [],
        "indices": {
            "oleo_de_cartamo_see_all": {
                "product": "oleo de cartamo",
            },
        }
    },
    'krill': {
        "product": [
            "krill",
        ],
        "features": [],
        "ingredients": [],
        "flavor": KEYS_WORDLIST_FLAVOR,
        "format": [],
        "is_not": [
            "kit",
            "barrinha",
            "creatina",
            "glutamin",
            "bcaa",
            "pretreino",
            "blend",
            "ervilha",
            "beef",
            "omega 3",
            "iso",
            "barbecue",
            "soy",
            "mass",
            "whey",
            "alfajor",
            "wafer",
        ],
        "maybe_not": [],
        "default_collection": ["oleos_see_all"],
        "promotion_collection": "oleos_promotion",
        "indices_flavor": [],
        "indices": {
            "krill_see_all": {
                "product": "krill",
            },
        }
    },
}
