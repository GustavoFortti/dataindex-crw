INDEX_SUPPLEMENT_BRAZIL = {
    "index": "brazil_supplement_09042024",
    "type": "supplement",
    "set": {
        "history_price": "brazil_supplement_history_price_09042024",
        "whey": "brazil_supplement_whey_09042024",
        "bar": "brazil_supplement_bar_09042024",
        "preworkout": "brazil_supplement_preworkout_09042024",
        "promocoes": "brazil_supplement_promocoes_09042024",
        "whey_protein": "brazil_supplement_whey_protein_09042024",
        "creatina": "brazil_supplement_creatina_09042024",
        "proteinas": "brazil_supplement_proteinas_09042024",
        "barrinhas_de_proteina": "brazil_supplement_barrinhas_de_proteina_09042024",
        "pre_treino": "brazil_supplement_pre_treino_09042024",
        "cafeina": "brazil_supplement_cafeina_09042024",
        "energia": "brazil_supplement_energia_09042024",
        "resistencia": "brazil_supplement_resistencia_09042024",
        "imunidade": "brazil_supplement_imunidade_09042024",
        "hipercalorico": "brazil_supplement_hipercalorico_09042024",
        "carboidratos": "brazil_supplement_carboidratos_09042024",
        "beta_alanina": "brazil_supplement_beta_alanina_09042024",
        "termogenico": "brazil_supplement_termogenico_09042024",
        "oleos": "brazil_supplement_oleos_09042024",
        "temperos": "brazil_supplement_temperos_09042024",
        "adocantes": "brazil_supplement_adocantes_09042024",
        "pasta_de_amendoim": "brazil_supplement_pasta_de_amendoim_09042024",
        "vegano": "brazil_supplement_vegano_09042024",
        "vegetariano": "brazil_supplement_vegetariano_09042024",
        "vitaminas": "brazil_supplement_vitaminas_09042024",
        "minerais": "brazil_supplement_minerais_09042024",
        "sono": "brazil_supplement_sono_09042024",
        "magnesio": "brazil_supplement_magnesio_09042024",
        "pele": "brazil_supplement_pele_09042024",
        "cabelo": "brazil_supplement_cabelo_09042024",
        "omega": "brazil_supplement_omega_09042024",
        "colageno": "brazil_supplement_colageno_09042024",
        "combos": "brazil_supplement_combos_09042024",
    },
}

def elasticsearch_index(product, synonyms_list):
    index = {}
    
    index['supplement'] = {
        "settings": {
            "analysis": {
                "filter": {
                    "sinonimo_filter": {
                        "type": "synonym",
                        "synonyms": synonyms_list
                    },
                    "especial_char_filter": {
                        "type": "pattern_replace",
                        "pattern": "[^\\w\\s]",
                        "replacement": ""
                    }
                },
                "analyzer": {
                    "title_analyzer": {
                        "type": "custom",
                        "tokenizer": "standard",
                        "filter": [
                            "lowercase",
                            "asciifolding",
                            "stop",
                            "porter_stem",
                            "sinonimo_filter",
                            "especial_char_filter"
                        ]
                    }
                }
            }
        },
        "mappings": {
            "properties": {
                "ref": {
                    "type": "keyword"
                },
                "title": {
                    "type": "text",
                    "analyzer": "title_analyzer",
                    "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 256
                        }
                    }
                },
                "price": {
                    "type": "text"
                },
                "image_url": {
                    "type": "keyword"
                },
                "product_url": {
                    "type": "keyword"
                },
                "ing_date": {
                    "type": "date",
                    "format": "yyyy-MM-dd"
                },
                "name": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 256
                        }
                    }
                },
                "brand": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 256
                        }
                    }
                },
                "price_numeric": {
                    "type": "float"
                },
                "price_discount_percent": {
                    "type": "float"
                },
                "quantity": {
                    "type": "integer"
                },
                "preco_qnt": {
                    "type": "float"
                },
                "product_def": {
                    "type": "text",
                    "analyzer": "title_analyzer",
                    "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 256
                        }
                    }
                },
                "product_def_pred": {
                    "type": "text",
                    "analyzer": "title_analyzer",
                    "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 256
                        }
                    }
                },
                "image_url_srv": {
                    "type": "keyword"
                },
            }
        }
    }
    
    index['supplement_prices'] = {
        "mappings": {
            "properties": {
                "ref": {
                    "type": "keyword"
                },
                "prices": {
                    "type": "text"
                },
                "price_discount_percent": {
                    "type": "float"
                },
                "brand": {
                    "type": "text"
                },
                "ing_date": {
                    "type": "date",
                    "format": "yyyy-MM-dd"
                },
            }
        }
    }
    
    return index[product]