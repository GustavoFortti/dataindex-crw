import os

import pandas as pd

import lib.data_quality as dq
import lib.elasticsearch.elasticsearch_functions as es
import lib.image_server_functions as image_srv
from utils.log import message

def ingestion(conf):
    print(conf['data_path'])
    df = pd.read_csv(conf['data_path'] + '/origin_dry.csv')

    if (conf['option'] == "data_quality"):
        message("Running Data Quality...")
        dq.data_history_analysis(conf, df)
        exit(0)

    dq.save_history_data(conf, df)
    message("Data ready for ingestion")

    message("START IMAGE INGESTION")
    df = image_srv.data_ingestion(df, conf)

    if not os.path.exists(conf['data_path']):
        os.makedirs(conf['data_path'])

    df.to_csv(conf['data_path'] + "/origin_csl.csv", index=False)

    message("START BULKLOAD")
    es.data_ingestion(df, conf)