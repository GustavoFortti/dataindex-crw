from datetime import datetime

import pandas as pd
from config.env import LOCAL
from lib.dataframe_functions import (drop_duplicates_for_columns,
                                     read_and_stack_csvs_dataframes,
                                     read_and_stack_historical_csvs_dataframes)
from lib.elasticsearch.elasticsearch_functions import batch_ingestion_by_field_values
from lib.elasticsearch.elasticsearch_index import INDEX_SUPPLEMENT_PRICE_BRAZIL
from lib.set_functions import get_pages_with_status_true
from utils.general_functions import DATE_FORMAT, create_directory_if_not_exists
from utils.log import message
from utils.wordlist import WORDLIST

CONF = {
    "name": "_set_history_price_",
    "data_path": f"{LOCAL}/data/supplement/brazil/_set_history_price_",
    "src_data_path": f"{LOCAL}/data/supplement/brazil",
    "pages_path": f"{LOCAL}/jobs/supplement/brazil/pages",
    "wordlist": False,
    "index_name": INDEX_SUPPLEMENT_PRICE_BRAZIL["index"]["history_price"],
    "index_type": INDEX_SUPPLEMENT_PRICE_BRAZIL["type"],
}

def run(args):
    print("JOB_NAME: " + CONF["name"], end="")
    CONF.update(vars(args))
    
    job_type = CONF["job_type"]
    message(" - EXEC: " + job_type)
    
    global WORDLIST
    WORDLIST = WORDLIST["supplement"]
    data_path = CONF["data_path"]
    src_data_path = CONF["src_data_path"]
    
    message("read data")
    create_directory_if_not_exists(data_path)
    pages_with_status_true = get_pages_with_status_true(CONF)
    df_origin = read_and_stack_csvs_dataframes(src_data_path, pages_with_status_true, "origin_csl.csv")
    df_origin = df_origin.drop_duplicates(subset='ref').reset_index(drop=True)
    refs = df_origin['ref'].values
    cols = ["ref", "price", "price_numeric", "ing_date", "brand"]
    df_origin = df_origin[cols]
    
    dfs = [df_origin]
    for page_data_path in pages_with_status_true:
        path = f"{src_data_path}/{page_data_path}/history"
        df_temp = read_and_stack_historical_csvs_dataframes(path, False)
        df_temp = df_temp[cols]
        dfs.append(df_temp)
        
    df = pd.concat(dfs, ignore_index=True)
    df = drop_duplicates_for_columns(df, ["ref", "price", "price_numeric"])
    df = df[df["ref"].isin(refs)]

    message("process prices")
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
        all_prices_dates.append({"ref": ref, "prices": str({"price": prices_dates[0][0], "date": prices_dates[0][1]}), "brand": brand, "price_discount_percent": str(price_discount_percent)})
    
    message("create dataframe")
    df = pd.DataFrame(all_prices_dates)
    date_today = datetime.today()
    df['ing_date'] = date_today.strftime(DATE_FORMAT)
    df.to_csv(f"{data_path}/history_price.csv", index=False)
    
    message("ingestion")
    brands_with_status_true = get_pages_with_status_true(CONF, False)
    batch_ingestion_by_field_values(CONF, df, "brand", brands_with_status_true)