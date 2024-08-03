def get_index(synonyms):
    return {
        "mappings": {
            "properties": {
                "ref": {
                    "type": "keyword"
                },
                "prices": {
                    "type": "object",
                    "properties": {
                        "price": {
                            "type": "float"
                        },
                        "date": {
                            "type": "date",
                            "format": "yyyy-MM-dd"
                        }
                    }
                },
                "brand": {
                    "type": "text"
                },
                "ing_date": {
                    "type": "date",
                    "format": "yyyy-MM-dd"
                }
            }
        }
    }
