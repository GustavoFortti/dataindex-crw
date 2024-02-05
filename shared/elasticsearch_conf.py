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
                    "spec": {
                        "type": "text",
                        "analyzer": "title_analyzer",
                        "fields": {
                            "keyword": {
                                "type": "keyword",
                                "ignore_above": 256
                            }
                        }
                    },
                    "spec_route": {
                        "type": "text",
                        "analyzer": "title_analyzer",
                        "fields": {
                            "keyword": {
                                "type": "keyword",
                                "ignore_above": 256
                            }
                        }
                    },
                    "ing_date": {
                        "type": "date",
                        "format": "yyyy-MM-dd"
                    },
                    "image_url": {
                        "type": "keyword"
                    },
                    "image_url_srv": {
                        "type": "keyword"
                    },
                    "product_url": {
                        "type": "keyword"
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
                    "name": {
                        "type": "text",
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
                    "price_numeric": {
                        "type": "float"
                    },
                    "quantity": {
                        "type": "integer"
                    },
                    "preco_qnt": {
                        "type": "float"
                    },
                    "quantity_format": {
                        "type": "integer"
                    },
                    "format": {
                        "type": "text"
                    }
                }
            }
        }
    
    return index[product]