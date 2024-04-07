import os
import statistics

import pandas as pd
from elasticsearch import helpers

from config.env import LOCAL
from shared.dataframe_functions import (drop_duplicates_for_columns,
                                        filter_dataframe_for_columns)
from shared.elasticsearch_functions import data_ingestion
from shared.elasticsearch_index import INDEX_SUPPLEMENT_BRAZIL
from utils.general_functions import get_all_origins, read_csvs_on_dir_and_union
from utils.log import message
from utils.wordlist import WORDLIST

CONF = {
    "name": "_set_history_price_",
    "data_path": f"{LOCAL}/data/supplement/brazil/_set_history_price_",
    "all_data_path": f"{LOCAL}/data/supplement/brazil",
    "brand": False,
    "pages_data_path": [
        # "adaptogen",
        # "atlhetica_nutrition",
        # "black_skull",
        # "boldsnacks",
        # "dark_lab",
        "darkness",
        "dux_nutrition_lab",
        "growth_supplements",
        "integralmedica",
        "iridium_labs",
        "max_titanium",
        "new_millen",
        "nutrata",
        "probiotica",
        "truesource",
        "under_labz",
        "vitafor"
    ]
}

def run(args):
    print("JOB_NAME: " + CONF["name"], end="")
    CONF.update(vars(args))

    job_type = CONF["job_type"]
    print(" - EXEC: " + job_type)
    
    global wordlist
    wordlist = WORDLIST["supplement"]
    all_data_path = CONF["all_data_path"]
    df_origin = get_all_origins(all_data_path, "origin_csl.csv")
    df_origin = df_origin.drop_duplicates(subset='ref').reset_index(drop=True)
    refs = df_origin['ref'].values
    cols = ["ref", "price", "price_numeric", "ing_date"]
    df_origin = df_origin[cols]
    
    dfs = [df_origin]
    for page_data_path in CONF["pages_data_path"]:
        dir = f"{all_data_path}/{page_data_path}/history"
        df_temp = read_csvs_on_dir_and_union(dir, False)
        df_temp = df_temp[cols]
        dfs.append(df_temp)
        
    df = pd.concat(dfs, ignore_index=True)
    df = drop_duplicates_for_columns(df, ["ref", "price", "price_numeric"])
    df = df[df["ref"].isin(refs)]

    refs_processed = []
    for idx, row in df.iterrows():
        ref = row['ref']
        if (ref in refs_processed):
            continue
        
        refs_processed.append(ref)
        
        df_price = df[df["ref"] == ref]
        last_price = df_price.sort_values("ing_date").tail(1)["price_numeric"].values[0]
        
        price = df_price["price_numeric"].values
        mean_price = statistics.mean(price)
        max_price = max(price)
        min_price = min(price)
        
        print(last_price)
        print(mean_price)
        print(max_price)
        print(min_price)
        
        exit()