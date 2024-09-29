import os

import pandas as pd
import src.lib.utils.data_quality as dq
from src.lib.load.image_ingestion import image_ingestion
from src.lib.utils.log import message
from src.lib.load.connection.shopify import process_and_ingest_products

def load(conf):
    print(conf['data_path'])
    df = pd.read_csv(conf['data_path'] + '/products_transform_csl.csv')
    
    if (conf['exec_flag'] == "data_quality"):
        message("Running Data Quality...")
        dq.data_history_analysis(conf, df)
        exit(0)

    dq.save_history_data(conf, df)
    message("Data ready for ingestion")
    
    process_and_ingest_products(df)
    exit()

    message("START IMAGE INGESTION")
    df = image_ingestion(df, conf)

    if not os.path.exists(conf['data_path']):
        os.makedirs(conf['data_path'])


    message("START BULKLOAD")
    df.to_csv(conf['data_path'] + "/products_load_csl.csv", index=False)