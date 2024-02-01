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
                        "titulo_analyzer": {
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
                    "titulo": {
                        "type": "text",
                        "analyzer": "titulo_analyzer",
                        "fields": {
                            "keyword": {
                                "type": "keyword",
                                "ignore_above": 256
                            }
                        }
                    },
                    "especificacao": {
                        "type": "text",
                        "analyzer": "titulo_analyzer",
                        "fields": {
                            "keyword": {
                                "type": "keyword",
                                "ignore_above": 256
                            }
                        }
                    },
                    "especificacao_rota": {
                        "type": "text",
                        "analyzer": "titulo_analyzer",
                        "fields": {
                            "keyword": {
                                "type": "keyword",
                                "ignore_above": 256
                            }
                        }
                    },
                    "ing_date": {
                        "type": "date",
                        "format": "dd/MM/yyyy"
                    },
                    "link_imagem": {
                        "type": "keyword"
                    },
                    "link_imagem_srv": {
                        "type": "keyword"
                    },
                    "link_produto": {
                        "type": "keyword"
                    },
                    "marca": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword",
                                "ignore_above": 256
                            }
                        }
                    },
                    "nome": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword",
                                "ignore_above": 256
                            }
                        }
                    },
                    "preco": {
                        "type": "text"
                    },
                    "preco_numeric": {
                        "type": "float"
                    },
                    "quantidade": {
                        "type": "integer"
                    },
                    "preco_qnt": {
                        "type": "float"
                    },
                    "quantidade_formato": {
                        "type": "integer"
                    },
                    "formato": {
                        "type": "text"
                    }
                }
            }
        }
    
    return index[product]