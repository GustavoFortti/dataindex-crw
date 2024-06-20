def get_index(synonyms):
    return {
        "settings": {
            "analysis": {
                "filter": {
                    "sinonimo_filter": {
                        "type": "synonym",
                        "synonyms": synonyms
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