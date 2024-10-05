import os
from glob import glob
from typing import List, Optional

import pandas as pd
from src.lib.utils.file_system import path_exists
from src.lib.utils.log import message
from src.lib.utils.text_functions import DATE_FORMAT, levenshtein


def format_column_date(df, column):
    df[column] = pd.to_datetime(df[column], format=DATE_FORMAT, dayfirst=True)
    df[column] = df[column].dt.strftime(DATE_FORMAT)

    return df

def create_or_read_df(path, columns=None, dtypes=None):
    message(f"create_or_read_df")
    if path_exists(path):
        message(f"read file: {path}")
        if dtypes:
            df = pd.read_csv(path, dtype=dtypes)
        else:
            df = pd.read_csv(path)
    else:
        if columns is not None:
            df = pd.DataFrame(columns=columns)
        else:
            df = pd.DataFrame()
        message(f"create file: {path}")
        df.to_csv(path, index=False)
    
    return df

def filter_dataframe_for_columns(df: pd.DataFrame, columns: List[str], keywords: List[str], blacklist: Optional[List[str]] = None) -> pd.DataFrame:
    """Filters a DataFrame for specified columns based on keywords and an optional blacklist to exclude certain terms"""
    global_mask = pd.Series([False] * len(df), index=df.index)
    
    for col in columns:
        df[col] = df[col].astype(str).fillna('')
        global_mask |= df[col].str.contains('|'.join(keywords), case=False)
    
    filtered_df = df[global_mask]
    
    if blacklist:
        for col in columns:
            blacklist_mask = ~filtered_df[col].str.contains('|'.join(blacklist), case=False)
            filtered_df = filtered_df[blacklist_mask]
    
    filtered_df = filtered_df.drop_duplicates().reset_index(drop=True)
    
    return filtered_df


def drop_duplicates_for_columns(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    """Drop duplicates based on specific columns"""
    return df.drop_duplicates(subset=columns)

def calc_string_diff_in_df_col(title_x, title_y):
    distance = levenshtein(title_x, title_y)
    max_len = max(len(title_x), len(title_y))
    percent_diff = (distance / max_len) if max_len != 0 else 0
    return percent_diff


def read_and_stack_historical_csvs_dataframes(history_data_path, get_only_last):
    # Usa glob para encontrar todos os arquivos CSV no diretório
    csv_files = glob(os.path.join(history_data_path, '*.csv'))
    csv_files = sorted(csv_files, reverse=True)
    
    if get_only_last and csv_files:
        # Encontra o arquivo CSV mais recentemente modificado
        latest_file = csv_files[0]
        message(latest_file)
        return pd.read_csv(latest_file)
    elif csv_files:
        # Lê todos os arquivos CSV e os concatena em um único DataFrame
        dfs = [pd.read_csv(file) for file in csv_files]
        return pd.concat(dfs, ignore_index=True)
    else:
        return pd.DataFrame()


def read_and_stack_csvs_dataframes(data_path: str, pages: list, file_name: str) -> pd.DataFrame:
    pages_path = [f"{data_path}/{page}" for page in pages]
    df_temp = []
    
    for path in pages_path:
        file_path = f"{path}/{file_name}"
        
        if os.path.exists(file_path):
            df_temp.append(pd.read_csv(file_path))
        else:
            print(f"Arquivo {file_path} não encontrado, pulando para o próximo.")

    if df_temp:
        df = pd.concat(df_temp, ignore_index=True)
    else:
        df = pd.DataFrame()
    
    return df