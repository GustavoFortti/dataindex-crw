import os

import pandas as pd
from config.env import LOCAL
from elasticsearch import helpers
from shared.dataframe_functions import filter_dataframe_for_columns
from shared.elasticsearch_functions import data_ingestion
from shared.elasticsearch_index import INDEX_SUPPLEMENT_BRAZIL
from shared.set_functions import get_all_origins
from utils.log import message
from utils.wordlist import WORDLIST

CONF = {
    "name": "_set_history_price_",
    "data_path": f"{LOCAL}/data/supplement/brazil/_set_history_price_",
    "all_data_path": f"{LOCAL}/data/supplement/brazil/",
    "brand": False
}

def run(args):
    print("JOB_NAME: " + CONF["name"], end="")
    CONF.update(vars(args))

    job_type = CONF["job_type"]
    print(" - EXEC: " + job_type)
    
    global wordlist
    wordlist = WORDLIST["supplement"]
    df = get_all_origins(CONF['all_data_path'], "origin_csl.csv")
    df = df.drop_duplicates(subset='ref').reset_index(drop=True)
    
    # print(df)