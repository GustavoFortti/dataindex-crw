from datetime import date
import pandas as pd
from utils.log import message

from utils import (DATE_FORMAT,
                   check_url_existence, 
                   is_price, 
                   read_csvs_on_dir_and_union,
                   calc_string_diff_in_df_col,
                   has_files,
                   create_directory_if_not_exists)

def status_tag(data, kill_job=True):
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
            exit(1)
        else: return False
        
    message("status_tag: All validations passed successfully.")
    if (kill_job): 
        message("Kill job")
        exit(0)
    else: 
        message("job running")
        return True

def data_history_analysis(conf, df):
    history_path = conf['data_path'] + "/history"

    create_directory_if_not_exists(history_path)
    if (not has_files(history_path)):
        data_history_save(conf, df)
        return True

    df_history = read_csvs_on_dir_and_union(history_path, True)

    volume_erro, volume_alert = volume_analysis(df_history, df)
    price_erro, price_alert, df_price = price_analysis(df_history, df)
    title_erro, title_alert, df_title = title_analysis(df_history, df)

    is_success = (price_erro & 
                  title_erro & 
                  volume_erro)

    if (not is_success):
        message("Ingestion.py - Error: corrupt data")
        exit(1)
    else:
        data_history_save(conf, df)
        message("Data ready for ingestion")

    return is_success

def volume_analysis(df_history, df, alert_threshold=0.2, error_threshold=0.5):
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

    result_df_title['diff_percent'] = result_df_title.apply(calc_string_diff_in_df_col, axis=1)

    threshold_erro = 0.60
    threshold_alert = 0.20
    result_df_title['title_erro'] = result_df_title['diff_percent'] <= threshold_erro
    result_df_title['title_alert'] = result_df_title['diff_percent'] <= threshold_alert

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

    return  [
                not (result_df_price["price_erro"] == False).any(),
                not (result_df_price["price_alert"] == False).any(),
                result_df_price
            ]

def data_history_save(conf, df):
    history_path = conf['data_path'] + "/history"

    data_atual = date.today()
    formatted_date = data_atual.strftime(DATE_FORMAT)

    df.to_csv(f"{history_path}/origin_csl_{formatted_date}.csv", index=False)
    message(f"Saved historical data in {history_path}/origin_csl_{formatted_date}.csv")