import os
from glob import glob
from typing import Any, Dict, List, Optional, Union

import pandas as pd

from src.lib.utils.file_system import file_or_path_exists
from src.lib.utils.log import message
from src.lib.utils.text_functions import levenshtein


def create_or_read_df(
    path: str,
    columns: Optional[List[str]] = None,
    dtype: Optional[Dict[str, Any]] = None
) -> pd.DataFrame:
    """
    Cria um novo DataFrame ou lê um existente de um arquivo CSV.
    Se o arquivo não existir ou estiver vazio, um novo DataFrame é criado com as colunas especificadas.

    Args:
        path (str): O caminho para o arquivo CSV.
        columns (Optional[List[str]]): Lista de nomes de colunas para o DataFrame.
        dtype (Optional[Dict[str, Any]]): Dicionário especificando os tipos de dados das colunas.

    Returns:
        pd.DataFrame: O DataFrame lido do arquivo CSV ou um novo DataFrame.
    """
    message("create_or_read_df")

    # Verifica se o arquivo existe
    if os.path.exists(path):
        # Verifica se o arquivo não está vazio
        if os.path.getsize(path) > 0:
            message(f"read file: {path}")
            try:
                # Lê o arquivo CSV
                df: pd.DataFrame
                if dtype:
                    df = pd.read_csv(path, dtype=dtype)
                else:
                    df = pd.read_csv(path)
            except pd.errors.EmptyDataError:
                message(f"EmptyDataError: {path} está vazio ou corrompido.")
                df = pd.DataFrame(columns=columns if columns else [])
                message(f"Creating new DataFrame with columns: {columns}")
                df.to_csv(path, index=False)
        else:
            message(f"{path} está vazio. Criando novo DataFrame.")
            df = pd.DataFrame(columns=columns if columns else [])
            df.to_csv(path, index=False)
    else:
        message(f"create file: {path}")
        df = pd.DataFrame(columns=columns if columns else [])
        df.to_csv(path, index=False)

    return df


def read_df(path: str, dtype: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
    """
    Lê um DataFrame de um arquivo CSV.

    Args:
        path (str): O caminho para o arquivo CSV.
        dtype (Optional[Dict[str, Any]]): Dicionário especificando os tipos de dados das colunas.

    Returns:
        pd.DataFrame: O DataFrame lido do arquivo CSV.

    Raises:
        FileNotFoundError: Se o arquivo não existir.
    """
    if file_or_path_exists(path):
        message(f"read file: {path}")
        if dtype:
            return pd.read_csv(path, dtype=dtype)
        else:
            return pd.read_csv(path)
    else:
        raise FileNotFoundError(f"O arquivo '{path}' não existe.")


def filter_dataframe_for_columns(
    df: pd.DataFrame,
    columns: List[str],
    keywords: List[str],
    blacklist: Optional[List[str]] = None
) -> pd.DataFrame:
    """
    Filtra um DataFrame com base em palavras-chave nas colunas especificadas e exclui linhas contendo termos da blacklist.

    Args:
        df (pd.DataFrame): O DataFrame a ser filtrado.
        columns (List[str]): Lista de nomes de colunas para aplicar o filtro.
        keywords (List[str]): Lista de palavras-chave para procurar nas colunas.
        blacklist (Optional[List[str]]): Lista de termos para excluir dos resultados.

    Returns:
        pd.DataFrame: O DataFrame filtrado.
    """
    global_mask: pd.Series = pd.Series([False] * len(df), index=df.index)

    for col in columns:
        df[col] = df[col].astype(str).fillna('')
        global_mask |= df[col].str.contains('|'.join(keywords), case=False, regex=True, na=False)

    filtered_df: pd.DataFrame = df[global_mask]

    if blacklist:
        for col in columns:
            blacklist_mask: pd.Series = ~filtered_df[col].str.contains('|'.join(blacklist), case=False, regex=True, na=False)
            filtered_df = filtered_df[blacklist_mask]

    filtered_df = filtered_df.drop_duplicates().reset_index(drop=True)
    return filtered_df


def drop_duplicates_for_columns(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    """
    Remove linhas duplicadas com base em colunas específicas.

    Args:
        df (pd.DataFrame): O DataFrame a ser processado.
        columns (List[str]): Lista de nomes de colunas para identificar duplicatas.

    Returns:
        pd.DataFrame: O DataFrame sem duplicatas.
    """
    return df.drop_duplicates(subset=columns)


def calc_string_diff_in_df_col(title_x: str, title_y: str) -> float:
    """
    Calcula a diferença percentual entre duas strings usando a distância de Levenshtein.

    Args:
        title_x (str): A primeira string para comparar.
        title_y (str): A segunda string para comparar.

    Returns:
        float: A diferença percentual entre as duas strings.
    """
    distance: int = levenshtein(title_x, title_y)
    max_len: int = max(len(title_x), len(title_y))
    percent_diff: float = (distance / max_len) if max_len != 0 else 0.0
    return percent_diff


def read_and_stack_historical_csvs_dataframes(
    history_data_path: str,
    get_only_last: bool,
    dtype: Optional[Dict[str, Any]] = None
) -> pd.DataFrame:
    """
    Lê e empilha DataFrames históricos de arquivos CSV de um diretório.

    Args:
        history_data_path (str): Caminho para o diretório contendo arquivos CSV históricos.
        get_only_last (bool): Se True, apenas o arquivo mais recente será lido.
        dtype (Optional[Dict[str, Any]]): Dicionário especificando os tipos de dados das colunas.

    Returns:
        pd.DataFrame: O DataFrame concatenado dos arquivos CSV históricos.
    """
    # Usa glob para encontrar todos os arquivos CSV no diretório
    csv_files: List[str] = glob(os.path.join(history_data_path, '*.csv'))
    csv_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)

    if get_only_last and csv_files:
        # Encontra o arquivo CSV mais recentemente modificado
        latest_file: str = csv_files[0]
        message(f"Reading latest file: {latest_file}")
        return read_df(latest_file, dtype)
    elif csv_files:
        # Lê todos os arquivos CSV e concatena em um único DataFrame
        dfs: List[pd.DataFrame] = [read_df(file, dtype) for file in csv_files]
        return pd.concat(dfs, ignore_index=True)
    else:
        return pd.DataFrame()


def read_and_stack_csvs_dataframes(
    data_path: str,
    pages: List[str],
    file_name: str,
    dtype: Optional[Dict[str, Any]] = None
) -> pd.DataFrame:
    """
    Lê e concatena arquivos CSV de múltiplos diretórios especificados por páginas.

    Args:
        data_path (str): O caminho base dos dados.
        pages (List[str]): Lista de diretórios de páginas para ler os arquivos.
        file_name (str): O nome do arquivo CSV a ser lido em cada diretório.
        dtype (Optional[Dict[str, Any]]): Dicionário especificando os tipos de dados das colunas.

    Returns:
        pd.DataFrame: O DataFrame concatenado dos arquivos CSV especificados.
    """
    pages_path: List[str] = [os.path.join(data_path, page) for page in pages]
    df_temp: List[pd.DataFrame] = []

    for path in pages_path:
        file_path: str = os.path.join(path, file_name)

        if os.path.exists(file_path):
            df_temp.append(read_df(file_path, dtype))
        else:
            message(f"Arquivo {file_path} não encontrado, pulando para o próximo.")

    if df_temp:
        df: pd.DataFrame = pd.concat(df_temp, ignore_index=True)
    else:
        df = pd.DataFrame()

    return df
