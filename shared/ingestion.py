import shared.elasticsearch_functions as es
import shared.image_server_functions as image_srv

def ingestion(conf):

    image_srv.data_ingestion(conf)
    # es.data_ingestion(conf)