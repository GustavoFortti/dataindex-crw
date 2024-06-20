def get_index(synonyms):
    return {
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