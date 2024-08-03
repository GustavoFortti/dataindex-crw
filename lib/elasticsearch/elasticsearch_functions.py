import os
from typing import Tuple

import pandas as pd
from elasticsearch import Elasticsearch, helpers

from lib.elasticsearch.elasticsearch_index import elasticsearch_index
from utils.general_functions import remove_nan_from_dict
from utils.log import message
from utils.wordlist import get_synonyms

os.environ['PYTHONWARNINGS'] = 'ignore'

def data_ingestion(df, conf):
    message("data_ingestion")

    synonyms_list = prepare_synonyms(conf)
    conf['synonyms_list'] = synonyms_list

    es = create_connection()
    insert_documents(es, conf, df)

def prepare_synonyms(conf):
    synonyms_list = []
    if (conf['wordlist']):
        synonyms_list = [", ".join(i) for i in get_synonyms(component_list=conf['wordlist'])]
        
    return synonyms_list

def create_connection():
    es_hosts = os.getenv('ES_HOSTS')
    es_user =  os.getenv('ES_USER')
    es_pass = os.getenv('ES_PASS')

    message(es_hosts)
    
    es = Elasticsearch(
        [es_hosts],
        http_auth=(es_user, es_pass),
        verify_certs=False,
    )

    message(f"Elasticsearch connection... {es.ping()}")
    return es

def insert_documents(es, conf, df):
    index_name = conf['index_name']
    index_type = conf['index_type']
    synonyms_list = conf['synonyms_list']
    
    create_index_if_not_exits(es, index_name, index_type, synonyms_list)
    
    if ("brand" in conf.keys()):
        message("delete by brand")
        delete_all_documents_on_index_by_field_value(es, index_name, "brand", conf['brand'])
    else:
        message("delete all")
        delete_all_documents_in_index(es, index_name)

    documents = create_documents_with_pandas(df, index_name)
    success, errors = helpers.bulk(es, documents)
    print(success, errors)

    message("Bulkload completed successfully")

def delete_all_documents_on_index_by_field_value(es, index_name, field, value):
    message("delete_all_documents_on_index_by_field_value")
    query = {
        "query": {
            "bool": {
                "must": [{ "match": { field: value }}]
            }
        }
    }

    try:
        results = es.delete_by_query(index=index_name, body=query)
        message(f"Documentos excluídos: {results['deleted']}")
    except Exception as e:
        message(f"Erro ao excluir documentos: {str(e)}")
        
def delete_all_documents_in_index(es, index_name: str) -> Tuple[int, str]:
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

def create_index_if_not_exits(es, index_name, index_type, synonyms_list):
    message("create_index_if_not_exits")
    index_settings = elasticsearch_index(index_type, synonyms_list)

    if not es.indices.exists(index=index_name):
        message("CREATING NEW INDEX")
        res = es.indices.create(index=index_name, body=index_settings)
        message(res)
        print(f"Índice '{index_name}' criado.")
    else:
        message("INDEX EXISTS")
        print(f"Índice '{index_name}' já existe.")
        
def check_elasticsearch_health(es) -> Tuple[str, dict]:
    """Check the health and indices of the Elasticsearch cluster."""
    try:
        # Fetching the overall health status of the Elasticsearch cluster.
        health = es.cluster.health()
        # Fetching a list of indices along with their details in a JSON format.
        indices = es.cat.indices(format="json")
        # Logging the health status of the Elasticsearch cluster.
        message(f"Elasticsearch Cluster Health Status: {health['status']}")
        # Returning the health status and a dictionary of indices with their details.
        return health['status'], {index['index']: index for index in indices}
    except Exception as e:
        # Logging the error message if the health check fails.
        message(f"Error checking Elasticsearch health and indices: {str(e)}")
        # Returning "error" status and an empty dictionary in case of an exception.
        return "error", {}

def list_all_indices(es) -> dict:
    """List all indices in the Elasticsearch cluster."""
    try:
        # Fetching a list of all indices and their details.
        indices = es.cat.indices(format="json")
        # Logging the action of listing all indices.
        message("Listing all indices in the Elasticsearch cluster.")
        # Returning a dictionary with index names and their details.
        for index in indices:
            message(index)
            message(index["index"])
    except Exception as e:
        # Logging the error if unable to list the indices.
        message(f"Error listing all indices: {str(e)}")
        # Returning an empty dictionary in case of an exception.
        return {}

def batch_ingestion_by_field_values(conf, df, field, values):
    for valeu in values:
        df_ing = df[df[field] == valeu]
        if (not df_ing.empty):
            message(f"history_price {field}: {valeu}")
            conf[field] = valeu
            data_ingestion(df_ing, conf)