import os
import pandas as pd
from elasticsearch import Elasticsearch, helpers
from utils.dry_functions import remove_nan_from_dict
from utils.wordlist import get_synonyms

os.environ['PYTHONWARNINGS'] = 'ignore'

def ingestion(conf):
    global CONF
    global SYNONYMS_LIST

    CONF = conf
    SYNONYMS_LIST = [", ".join(i) for i in get_synonyms(CONF['word_list'])]

    file_path = CONF['data_path']

    df = pd.read_csv(file_path + '/origin_csl.csv')

    create_connection()
    create_or_update_suply_document(df)

def create_connection():
    es_hosts = "https://localhost:9200"
    es_user = os.getenv('ES_USER')
    es_pass = os.getenv('ES_PASS')

    print(f"ES_HOSTS: {es_hosts}")
    print(f"ES_USER: {es_user}")
    print(f"ES_PASS: {es_pass}")

    global es
    es = Elasticsearch(
        [es_hosts],
        http_auth=(es_user, es_pass),
        verify_certs=False 
    )

    print(f"Elasticsearch connection... {es.ping()}")

def create_or_update_suply_document(df):
    global INDEX_NAME
    INDEX_NAME = 'suplementos'

    try:
        create_suply_index_if_not_exits()
        delete_docs_from_suply_by_marca_and_type()

        helpers.bulk(es, create_documents_with_pandas(df))
        print("Bulkload completed successfully")

    except Exception as e:
        print(f"Erro ao enviar dados para o Elasticsearch: {str(e)}")

def delete_docs_from_suply_by_marca_and_type():
    marca = CONF['marca']

    query = {
        "query": {
            "bool": {
                "must": [{
                    "term": {
                        "marca.keyword": marca
                    }
                }]
            }
        }
    }

    try:
        results = es.delete_by_query(index=INDEX_NAME, body=query)
        print(f"Documentos excluídos: {results['deleted']}")
    except Exception as e:
        print(f"Erro ao excluir documentos: {str(e)}")

def create_documents_with_pandas(df):
    for index, row in df.iterrows():
        yield {
            "_op_type": "create",
            "_index": INDEX_NAME,
            "_source": remove_nan_from_dict(row.to_dict()),
        }

def update_documents_with_pandas(df, hits):
    for index, row in df.iterrows():
        id = None
        for document in hits:
            if (document['ref'] == row['ref']):
                id = document['id']
                
        yield {
            "_op_type": "update",
            "_index": INDEX_NAME,
            "_id": id,
            "doc": remove_nan_from_dict(row.to_dict()),
        }

def create_suply_index_if_not_exits():
    index_settings = {
        "settings": {
            "analysis": {
                "filter": {
                    "sinonimo_filter": {
                        "type": "synonym",
                        "synonyms": SYNONYMS_LIST
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


    if not es.indices.exists(index=INDEX_NAME):
        es.indices.create(index=INDEX_NAME, body=index_settings)
        print(f"Índice '{INDEX_NAME}' criado.")
    else:
        print(f"Índice '{INDEX_NAME}' já existe.")