from lib.elasticsearch.indices import supplement, supplement_price

INDEX_DATE = "09042024"

INDEX_SUPPLEMENT_PRICE_BRAZIL = {
    "type": "supplement_price",
    "index": {
        "history_price": f"brazil_supplement_history_price_{INDEX_DATE}",
    }
}

INDEX_SUPPLEMENT_BRAZIL = {
    "type": "supplement",
    "index": {
        "product": f"brazil_supplement_{INDEX_DATE}",
        "whey": f"brazil_supplement_whey_{INDEX_DATE}",
        "bar": f"brazil_supplement_bar_{INDEX_DATE}",
        "preworkout": f"brazil_supplement_preworkout_{INDEX_DATE}",
        "promocoes": f"brazil_supplement_promocoes_{INDEX_DATE}",
        "whey_protein": f"brazil_supplement_whey_protein_{INDEX_DATE}",
        "creatina": f"brazil_supplement_creatina_{INDEX_DATE}",
        "proteinas": f"brazil_supplement_proteinas_{INDEX_DATE}",
        "barrinhas_de_proteina": f"brazil_supplement_barrinhas_de_proteina_{INDEX_DATE}",
        "pre_treino": f"brazil_supplement_pre_treino_{INDEX_DATE}",
        "cafeina": f"brazil_supplement_cafeina_{INDEX_DATE}",
        "energia": f"brazil_supplement_energia_{INDEX_DATE}",
        "resistencia": f"brazil_supplement_resistencia_{INDEX_DATE}",
        "imunidade": f"brazil_supplement_imunidade_{INDEX_DATE}",
        "hipercalorico": f"brazil_supplement_hipercalorico_{INDEX_DATE}",
        "carboidratos": f"brazil_supplement_carboidratos_{INDEX_DATE}",
        "beta_alanina": f"brazil_supplement_beta_alanina_{INDEX_DATE}",
        "termogenico": f"brazil_supplement_termogenico_{INDEX_DATE}",
        "oleos": f"brazil_supplement_oleos_{INDEX_DATE}",
        "temperos": f"brazil_supplement_temperos_{INDEX_DATE}",
        "adocantes": f"brazil_supplement_adocantes_{INDEX_DATE}",
        "pasta_de_amendoim": f"brazil_supplement_pasta_de_amendoim_{INDEX_DATE}",
        "vegano": f"brazil_supplement_vegano_{INDEX_DATE}",
        "vegetariano": f"brazil_supplement_vegetariano_{INDEX_DATE}",
        "vitaminas": f"brazil_supplement_vitaminas_{INDEX_DATE}",
        "minerais": f"brazil_supplement_minerais_{INDEX_DATE}",
        "sono": f"brazil_supplement_sono_{INDEX_DATE}",
        "magnesio": f"brazil_supplement_magnesio_{INDEX_DATE}",
        "pele": f"brazil_supplement_pele_{INDEX_DATE}",
        "cabelo": f"brazil_supplement_cabelo_{INDEX_DATE}",
        "omega": f"brazil_supplement_omega_{INDEX_DATE}",
        "colageno": f"brazil_supplement_colageno_{INDEX_DATE}",
        "combos": f"brazil_supplement_combos_{INDEX_DATE}",
    }
}

ALL_INDEXS = [
    INDEX_SUPPLEMENT_PRICE_BRAZIL,
    INDEX_SUPPLEMENT_BRAZIL
]

def elasticsearch_index(index_type, synonyms_list):
    index = {}
    
    indices = {
        "supplement": supplement.get_index,
        "supplement_price": supplement_price.get_index 
    }
    
    module = indices.get(index_type)
    index = module(synonyms_list)
    
    return index