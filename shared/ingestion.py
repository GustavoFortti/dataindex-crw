import os
import pandas as pd

import shared.elasticsearch_functions as es
import shared.image_server_functions as image_srv

def ingestion(conf):
    print(conf['data_path'])
    df = pd.read_csv(conf['data_path'] + '/origin_dry.csv')

    print("START IMAGE INGESTION")
    df = image_srv.data_ingestion(df, conf)

    if not os.path.exists(conf['data_path']):
        os.makedirs(conf['data_path'])

    df.to_csv(conf['data_path'] + "/origin_csl.csv", index=False)
    
    print("START BULKLOAD")
    es.data_ingestion(df, conf)