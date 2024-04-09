import os
from typing import Tuple

import pandas as pd
from elasticsearch import Elasticsearch, helpers

from shared.elasticsearch_index import elasticsearch_index
from utils.general_functions import remove_nan_from_dict
from utils.log import message
from utils.wordlist import get_synonyms

os.environ['PYTHONWARNINGS'] = 'ignore'

def data_ingestion(df, conf):
    message("data_ingestion")
    global CONF
    global SYNONYMS_LIST

    CONF = conf
    
    SYNONYMS_LIST = []
    if (CONF['wordlist']):
        SYNONYMS_LIST = [", ".join(i) for i in get_synonyms(component_list=CONF['wordlist'])]
    
    index_name = CONF['index_name']

    create_connection()
    insert_documents(df, index_name)

def create_connection():

    es_hosts = os.getenv('ES_HOSTS')
    es_user =  os.getenv('ES_USER')
    es_pass = os.getenv('ES_PASS')

    message(es_hosts)
    
    global es
    es = Elasticsearch(
        [es_hosts],
        http_auth=(es_user, es_pass),
        verify_certs=False 
    )

    message(f"Elasticsearch connection... {es.ping()}")
    return es

def insert_documents(df, index_name):
    create_index_if_not_exits(index_name)
    
    field, value = "brand", CONF['brand']
    if (value):
        delete_all_documents_on_index_by_field_value(index_name, field, value)
    else:
        delete_all_documents_in_index(index_name)

    documents = create_documents_with_pandas(df, index_name)
    success, errors = helpers.bulk(es, documents)
    print(success, errors)

    message("Bulkload completed successfully")

def delete_all_documents_on_index_by_field_value(index_name, field, value):
    message("delete_all_documents_on_index_by_field_value")
    query = {
        "query": {
            "bool": {
                "must": [{
                    "term": {
                        f"{field}.keyword": value
                    }
                }]
            }
        }
    }

    try:
        results = es.delete_by_query(index=index_name, body=query)
        message(f"Documentos excluídos: {results['deleted']}")
    except Exception as e:
        message(f"Erro ao excluir documentos: {str(e)}")
        
def delete_all_documents_in_index(index_name: str) -> Tuple[int, str]:
    message("delete_all_documents_in_index")
    query = {"query": {"match_all": {}}}

    try:
        results = es.delete_by_query(index=index_name, body=query)
        message(f"Documentos excluídos: {results['deleted']}")
    except Exception as e:
        message(f"Erro ao excluir documentos: {str(e)}")

def create_documents_with_pandas(df, index_name):
    for index, row in df.iterrows():

        document = {
            "_op_type": "create",
            "_index": index_name,
            "_source": remove_nan_from_dict(row.to_dict()),
        }
        
        yield document

def create_index_if_not_exits(index_name):
    message("create_index_if_not_exits")
    index_settings = elasticsearch_index(CONF['index_type'], SYNONYMS_LIST)

    if not es.indices.exists(index=index_name):
        message("CREATING NEW INDEX")
        res = es.indices.create(index=index_name, body=index_settings)
        message(res)
        print(f"Índice '{index_name}' criado.")
    else:
        message("INDEX EXISTS")
        print(f"Índice '{index_name}' já existe.")