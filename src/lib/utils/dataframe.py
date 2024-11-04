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

def create_or_read_df(path, columns=None, dtype=None):
    message(f"create_or_read_df")
    
    # Verifica se o arquivo existe
    if os.path.exists(path):
        # Verifica se o arquivo está vazio
        if os.path.getsize(path) > 0:
            message(f"read file: {path}")
            try:
                # Lê o arquivo CSV
                if dtype:
                    df = pd.read_csv(path, dtype=dtype)
                else:
                    df = pd.read_csv(path)
            except pd.errors.EmptyDataError:
                message(f"EmptyDataError: {path} is empty or corrupted.")
                df = pd.DataFrame(columns=columns)  # Cria um DataFrame vazio com as colunas fornecidas
                message(f"Creating new DataFrame with columns: {columns}")
                df.to_csv(path, index=False)
        else:
            message(f"{path} is empty. Creating new DataFrame.")
            df = pd.DataFrame(columns=columns)  # Cria um DataFrame vazio com as colunas fornecidas
            df.to_csv(path, index=False)
    else:
        message(f"create file: {path}")
        df = pd.DataFrame(columns=columns)  # Cria um DataFrame vazio com as colunas fornecidas
        df.to_csv(path, index=False)
    
    return df

def read_df(path, dtype=None):
    """
    Reads a DataFrame from a CSV file.

    Parameters:
    path (str): The path to the CSV file.
    dtype (dict, optional): A dictionary specifying column data types.

    Returns:
    DataFrame: The DataFrame read from the CSV file.
    """
    if path_exists(path):
        message(f"read file: {path}")
        if dtype:
            return pd.read_csv(path, dtype=dtype)
        else:
            return pd.read_csv(path)
    else:
        raise FileNotFoundError(f"The file '{path}' does not exist.")

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

def read_and_stack_historical_csvs_dataframes(history_data_path, get_only_last, dtype=None):
    # Usa glob para encontrar todos os arquivos CSV no diretório
    csv_files = glob(os.path.join(history_data_path, '*.csv'))
    csv_files = sorted(csv_files, reverse=True)
    
    if get_only_last and csv_files:
        # Encontra o arquivo CSV mais recentemente modificado
        latest_file = csv_files[0]
        message(latest_file)
        return read_df(latest_file, dtype)
    elif csv_files:
        # Lê todos os arquivos CSV e os concatena em um único DataFrame
        dfs = [read_df(file, dtype) for file in csv_files]
        return pd.concat(dfs, ignore_index=True)
    else:
        return pd.DataFrame()

def read_and_stack_csvs_dataframes(data_path: str, pages: list, file_name: str, dtype=None) -> pd.DataFrame:
    pages_path = [f"{data_path}/{page}" for page in pages]
    df_temp = []
    
    for path in pages_path:
        file_path = f"{path}/{file_name}"
        print(file_path)
        exit()
        
        if os.path.exists(file_path):
            df_temp.append(read_df(file_path, dtype))
        else:
            print(f"Arquivo {file_path} não encontrado, pulando para o próximo.")

    if df_temp:
        df = pd.concat(df_temp, ignore_index=True)
    else:
        df = pd.DataFrame()
    
    return df