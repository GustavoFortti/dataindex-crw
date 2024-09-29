import os
from datetime import datetime

import pandas as pd
from src.lib.utils.dataframe import (drop_duplicates_for_columns,
                                     read_and_stack_csvs_dataframes,
                                     read_and_stack_historical_csvs_dataframes)
from src.lib.utils.general_functions import get_pages_with_status_true
from src.lib.utils.file_system import DATE_FORMAT, create_directory_if_not_exists
from src.lib.utils.log import message
from src.lib.wordlist.wordlist import WORDLIST

def set_conf(args, local):
    conf = {}
    conf["local"] = local
    conf["job_name"] = args.job_name
    conf["page_name"] = args.page_name
    conf["page_type"] = args.page_type
    conf["country"] = args.country
    conf["src_data_path"] = f"{local}/data/{conf['page_type']}/{conf['country']}"
    conf["data_path"] = f"{conf['src_data_path']}/history_price"
    conf["pages_path"] = f"{local}/src/jobs/slave_page/pages/{conf['country']}"
    return conf

def run(args):
    global LOCAL
    
    LOCAL = os.getenv('LOCAL')
    conf = set_conf(args, LOCAL)

    print("JOB_NAME: " + conf["job_name"])
    conf.update(vars(args))
    src_data_path = conf["src_data_path"]
    data_path = conf['data_path']

    create_directory_if_not_exists(data_path)
    
    message("read data")
    pages_with_status_true = get_pages_with_status_true(conf)
    df_products_load_csl = read_and_stack_csvs_dataframes(src_data_path, pages_with_status_true, "products_load_csl.csv")
    df_products_load_csl = df_products_load_csl.drop_duplicates(subset='ref').reset_index(drop=True)
    refs = df_products_load_csl['ref'].values
    cols = ["ref", "price", "price_numeric", "ing_date", "brand"]
    df_products_load_csl = df_products_load_csl[cols]
    
    dfs = [df_products_load_csl]
    for page_data_path in pages_with_status_true:
        
        path = f"{src_data_path}/{page_data_path}/history"
        df_temp = read_and_stack_historical_csvs_dataframes(path, False)
        if (df_temp.empty):
            continue
        
        df_temp = df_temp[cols]
        dfs.append(df_temp)
    
    df = pd.concat(dfs, ignore_index=True)
    df = drop_duplicates_for_columns(df, ["ref", "price", "price_numeric"])
    df = df[df["ref"].isin(refs)]

    message("process prices")
    all_prices_dates = []
    data = []
    refs_processed = []
    for idx, row in df.iterrows():
        ref = row['ref']
        if (ref in refs_processed):
            continue
        
        refs_processed.append(ref)

        df_price = df[df["ref"] == ref].sort_values(by='ing_date', ascending=False)

        prices_dates = df_price[["price_numeric", "ing_date"]].values.tolist()
        prices = sum(df_price[["price_numeric"]].values.tolist(), [])

        price_discount_percent = False
        if (len(prices) > 1):
            price_variation = prices[0] / prices[1]
            if (price_variation < 0.95):
                price_discount_percent =  int((1 - price_variation) * 100)

        brand = df_price["brand"].values[0]

        for price, date in prices_dates:
            all_prices_dates.append({"price": price, "date": date})
            
        data.append({"ref": ref, "prices": all_prices_dates, "brand": brand, "price_discount_percent": price_discount_percent})
        
        all_prices_dates = []
    
    message("create dataframe")
    df = pd.DataFrame(data)
    date_today = datetime.today()
    df['ing_date'] = date_today.strftime(DATE_FORMAT)
    df.to_csv(f"{data_path}/history_price_csl.csv", index=False)