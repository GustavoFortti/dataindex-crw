import re
from datetime import date

import pandas as pd

from src.lib.utils.dataframe import (calc_string_diff_in_df_col,
                                     create_or_read_df,
                                     read_and_stack_historical_csvs_dataframes)
from src.lib.utils.file_system import (create_directory_if_not_exists,
                                       delete_file, has_files)
from src.lib.utils.log import message
from src.lib.utils.text_functions import DATE_FORMAT
from src.lib.utils.web_functions import check_url_existence

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

def status_tag(page, data, kill_job=True):
    errors = []

    if not is_price(data["price"]):
        errors.append("ERRO: Invalid price format.")

    if not check_url_existence(data["image_url"]):
        errors.append("ERRO: Image URL does not exist.")

    if not check_url_existence(data["product_url"]):
        errors.append("ERRO: Product URL does not exist.")

    if errors:
        for error in errors:
            message(error)

        if (kill_job): 
            message("JOB KILLED BY FLAG WITH ERROR")
            raise Exception(str(errors))
        else: 
            return False
        
    message("status_tag: All validations passed successfully.")
    if (kill_job): 
        df_products = create_or_read_df(page.conf['path_products_extract_csl'], data.keys())
        if (df_products.empty):
            delete_file(page.conf['path_products_extract_csl'])
        
        message("Kill job")
        exit(0)
    else: 
        message("job running")
        return True

def data_history_analysis(conf, df):
    history_path = conf['data_path'] + "/history"

    create_directory_if_not_exists(history_path)
    if (not has_files(history_path)):
        save_history_data(conf, df)
        return True

    message("CARREGANDO DATAFRAME HISTORICO...")
    message(history_path)
    df_history = read_and_stack_historical_csvs_dataframes(history_path, True, dtype={'ref': str})

    message("ANALISE volume")
    volume_erro, volume_alert = volume_analysis(df_history, df)
    message("ANALISE price")
    price_erro, price_alert, df_price = price_analysis(df_history, df)

    is_success = (price_erro & 
                  volume_erro)

    message(f"price_erro: {price_erro}")
    message(f"volume_erro: {volume_erro}")

    if (not is_success):
        message("Ingestion.py - Error: corrupt data")
        exit(1)       

    return is_success

def volume_analysis(df_history, df, alert_threshold=0.1, error_threshold=0.2):
    volume_history = len(df_history)
    volume_current = len(df)

    if volume_history == 0:
        return True, True
    
    volume_change = abs((volume_current / volume_history) - 1)
    message(f"volume_change: {volume_change}")

    volume_error = volume_change < error_threshold
    volume_alert = volume_change < alert_threshold

    return volume_error, volume_alert

def title_analysis(df_history, df):
    df_history_title = df_history[["ref", "title"]]
    df_title = df[["ref", "title"]]
    result_df_title = df_history_title.merge(df_title, on='ref', how='inner')

    if (result_df_title.empty):
        message("ERRO RESULT_DF_TITLE.EMPTY")
        return False, False, df

    result_df_title['diff_percent'] = result_df_title.apply(lambda row: calc_string_diff_in_df_col(row['title_x'], row['title_y']), axis=1).astype(float)

    threshold_erro = 0.60
    threshold_alert = 0.20
    result_df_title['title_erro'] = result_df_title['diff_percent'] <= threshold_erro
    result_df_title['title_alert'] = result_df_title['diff_percent'] <= threshold_alert

    message("TITLE ERROR DATAFRAME")
    df_erro = result_df_title.sort_values('diff_percent')
    print(df_erro[~df_erro['title_erro']][['ref', 'title_x', 'title_y', 'diff_percent', 'title_erro', 'title_alert']])

    return  [
                not (result_df_title["title_erro"] == False).any(),
                not (result_df_title["title_alert"] == False).any(),
                result_df_title
            ]

def price_analysis(df_history, df):
    df_history_price = df_history.groupby('ref')['price_numeric'].agg(['mean', 'max', 'min']).reset_index()
    df_price = df[['ref', 'price_numeric']]
    result_df_price = df_history_price.merge(df_price, on='ref', how='inner')

    result_df_price['diff_percent'] = abs((result_df_price['price_numeric'] / result_df_price['mean']) - 1)

    threshold_erro = 0.70
    threshold_alert = 0.40
    result_df_price['price_erro'] = result_df_price['diff_percent'] <= threshold_erro
    result_df_price['price_alert'] = result_df_price['diff_percent'] <= threshold_alert

    df_erro = result_df_price.sort_values('diff_percent')
    print(df_erro)
    message("PRICE ERROR DATAFRAME")
    print(df_erro[~df_erro['price_erro']])
    message("PRICE DATAFRAME")
    print(df_erro[df_erro['price_erro']])

    return  [
                not (result_df_price["price_erro"] == False).any(),
                not (result_df_price["price_alert"] == False).any(),
                result_df_price
            ]

def save_history_data(conf, df):
    history_path = conf['data_path'] + "/history"

    data_atual = date.today()
    formatted_date = data_atual.strftime(DATE_FORMAT)
    
    create_directory_if_not_exists(history_path)

    df.to_csv(f"{history_path}/products_load_csl_{formatted_date}.csv", index=False)
    message(f"Saved historical data in {history_path}/products_load_csl_{formatted_date}.csv")
    

def is_price(string):
    if not isinstance(string, str):
        return False

    pattern = r"""
    (R\$\s?\d{1,3}(?:\.\d{3})*[,.]\d{2})|  # BRL: R$
    (€\s?\d{1,3}(?:\.\d{3})*,\d{2})|       # EUR: €
    (\$\s?\d{1,3}(?:,\d{3})*\.\d{2})|      # USD: $
    (£\s?\d{1,3}(?:,\d{3})*\.\d{2})        # GBP: £
    """

    return bool(re.match(pattern, string, re.VERBOSE))