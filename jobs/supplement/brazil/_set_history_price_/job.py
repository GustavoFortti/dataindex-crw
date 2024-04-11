import importlib
import os
from copy import deepcopy
from datetime import datetime

import pandas as pd
from elasticsearch import helpers

from config.env import LOCAL
from lib.dataframe_functions import drop_duplicates_for_columns
from lib.elasticsearch.elasticsearch_functions import data_ingestion
from lib.elasticsearch.elasticsearch_index import INDEX_SUPPLEMENT_PRICE_BRAZIL
from utils.general_functions import (DATE_FORMAT,
                                     create_directory_if_not_exists,
                                     list_directory,
                                     read_csvs_on_dir_and_union)
from utils.log import message
from utils.wordlist import WORDLIST

CONF = {
    "name": "_set_history_price_",
    "data_path": f"{LOCAL}/data/supplement/brazil/_set_history_price_",
    "all_data_path": f"{LOCAL}/data/supplement/brazil",
    "all_pages_path": f"{LOCAL}/jobs/supplement/brazil/pages",
    "wordlist": False,
    "index_name": INDEX_SUPPLEMENT_PRICE_BRAZIL["index"]["history_price"],
    "index_type": INDEX_SUPPLEMENT_PRICE_BRAZIL["type"],
    "pages_data_path": []
}

def get_pages_data_path():
    pages = (list_directory(CONF["all_pages_path"]))
    page_type = CONF["page_type"]
    country = CONF["country"]
    
    pages_data_path = []
    for page in pages:
        module_name = f"jobs.{page_type}.{country}.pages.{page}.conf"
        page_conf = importlib.import_module(module_name)
        if (page_conf.STATUS):
            pages_data_path.append(page)
            
    return sorted(pages_data_path)

def run(args):
    print("JOB_NAME: " + CONF["name"], end="")
    CONF.update(vars(args))

    job_type = CONF["job_type"]
    print(" - EXEC: " + job_type)
    
    data_path = CONF["data_path"]
    create_directory_if_not_exists(data_path)
    CONF["pages_data_path"] = get_pages_data_path()
    
    global wordlist
    
    wordlist = WORDLIST["supplement"]
    all_data_path = CONF["all_data_path"]
    pages_path = [f"{all_data_path}/{page_path}" for page_path in CONF["pages_data_path"]]
    df_origin_temp = []
    for path in pages_path:
        df_origin_temp.append(pd.read_csv(f"{path}/origin_csl.csv"))

    df_origin = pd.concat(df_origin_temp, ignore_index=True)
    df_origin = df_origin.drop_duplicates(subset='ref').reset_index(drop=True)
    refs = df_origin['ref'].values
    cols = ["ref", "price", "price_numeric", "ing_date", "brand"]
    df_origin = df_origin[cols]
    
    dfs = [df_origin]
    for page_data_path in CONF["pages_data_path"]:
        path = f"{all_data_path}/{page_data_path}/history"
        df_temp = read_csvs_on_dir_and_union(path, False)
        df_temp = df_temp[cols]
        dfs.append(df_temp)
        
    df = pd.concat(dfs, ignore_index=True)
    df = drop_duplicates_for_columns(df, ["ref", "price", "price_numeric"])
    df = df[df["ref"].isin(refs)]

    all_prices_dates = []
    refs_processed = []
    for idx, row in df.iterrows():
        ref = row['ref']
        if (ref in refs_processed):
            continue
        
        refs_processed.append(ref)
        
        df_price = df[df["ref"] == ref]
        
        prices_dates = df_price[["price_numeric", "ing_date"]].values.tolist()
        
        prices = df_price["price_numeric"].values
        
        price_discount_percent = 0.0
        if (len(prices) > 1):
            price_discount_percent = -round((prices[0] - prices[1]) / prices[1], 2)
        
        brand = df_price["brand"].values[0]
        all_prices_dates.append({"ref": ref, "prices": prices_dates, "brand": brand, "price_discount_percent": price_discount_percent})
    
    df = pd.DataFrame(all_prices_dates)
    date_today = datetime.today()
    df['ing_date'] = date_today.strftime(DATE_FORMAT)
    df.to_csv(f"{data_path}/history_price.csv", index=False)
    
    batch_ingestion(df)

def batch_ingestion(df):
    conf = deepcopy(CONF)
    
    for brand in conf['pages_data_path']:
        df_ing = df[df['brand'] == brand]
        if (not df_ing.empty):
            message(f"history_price brand: {brand}")
            conf["brand"] = brand
            data_ingestion(df_ing, conf)