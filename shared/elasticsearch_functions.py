import os
import pandas as pd

from elasticsearch import Elasticsearch, helpers

from shared.elasticsearch_conf import elasticsearch_index

from utils.general_functions import remove_nan_from_dict
from utils.wordlist import get_synonyms

os.environ['PYTHONWARNINGS'] = 'ignore'

def data_ingestion(conf):
    global CONF
    global SYNONYMS_LIST

    CONF = conf
    SYNONYMS_LIST = [", ".join(i) for i in get_synonyms(CONF['word_list'])]

    file_path = CONF['data_path']
    index_name = CONF['index_name']

    df = pd.read_csv(file_path + '/origin_csl.csv')

    create_connection()
    insert_documents(df, index_name)

def create_connection():
    es_hosts = os.getenv('ES_HOSTS')
    es_user =  os.getenv('ES_USER')
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
    return es

def insert_documents(df, index_name):
    try:
        create_index_if_not_exits(index_name)
        field, value = "marca", CONF['marca']
        delete_all_documents_on_index_by_field_value(index_name, field, value)

        helpers.bulk(es, create_documents_with_pandas(df, index_name))
        print("Bulkload completed successfully")

    except Exception as e:
        print(f"Erro ao enviar dados para o Elasticsearch: {str(e)}")

def delete_all_documents_on_index_by_field_value(index_name, field, value):
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
        print(f"Documentos excluídos: {results['deleted']}")
    except Exception as e:
        print(f"Erro ao excluir documentos: {str(e)}")

def create_documents_with_pandas(df, index_name):
    for index, row in df.iterrows():
        yield {
            "_op_type": "create",
            "_index": index_name,
            "_source": remove_nan_from_dict(row.to_dict()),
        }

def create_index_if_not_exits(index_name):
    index_settings = elasticsearch_index(CONF['index_type'], SYNONYMS_LIST)

    if not es.indices.exists(index=index_name):
        es.indices.create(index=index_name, body=index_settings)
        print(f"Índice '{index_name}' criado.")
    else:
        print(f"Índice '{index_name}' já existe.")