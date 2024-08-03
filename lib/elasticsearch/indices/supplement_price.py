def get_index(synonyms):
    return {
        "mappings": {
            "properties": {
                "ref": {
                    "type": "keyword"
                },
                "prices": {
                    "type": "object"
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