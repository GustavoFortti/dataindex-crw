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
    Creates a new DataFrame or reads an existing one from a CSV file.
    If the file does not exist or is empty, a new DataFrame is created with the specified columns.

    Args:
        path (str): The path to the CSV file.
        columns (Optional[List[str]]): List of column names for the DataFrame.
        dtype (Optional[Dict[str, Any]]): Dictionary specifying the data types of the columns.

    Returns:
        pd.DataFrame: The DataFrame read from the CSV file or a new DataFrame.
    """
    message("create_or_read_df")

    # Check if the file exists
    if os.path.exists(path):
        # Check if the file is not empty
        if os.path.getsize(path) > 0:
            message(f"read file: {path}")
            try:
                # Read the CSV file
                df: pd.DataFrame
                if dtype:
                    df = pd.read_csv(path, dtype=dtype)
                else:
                    df = pd.read_csv(path)
            except pd.errors.EmptyDataError:
                message(f"EmptyDataError: {path} is empty or corrupted.")
                df = pd.DataFrame(columns=columns if columns else [])
                message(f"Creating new DataFrame with columns: {columns}")
                df.to_csv(path, index=False)
        else:
            message(f"{path} is empty. Creating new DataFrame.")
            df = pd.DataFrame(columns=columns if columns else [])
            df.to_csv(path, index=False)
    else:
        message(f"create file: {path}")
        df = pd.DataFrame(columns=columns if columns else [])
        df.to_csv(path, index=False)

    return df


def read_df(path: str, dtype: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
    """
    Reads a DataFrame from a CSV file.

    Args:
        path (str): The path to the CSV file.
        dtype (Optional[Dict[str, Any]]): Dictionary specifying the data types of the columns.

    Returns:
        pd.DataFrame: The DataFrame read from the CSV file.

    Raises:
        FileNotFoundError: If the file does not exist.
    """
    if file_or_path_exists(path):
        message(f"read file: {path}")
        if dtype:
            return pd.read_csv(path, dtype=dtype)
        else:
            return pd.read_csv(path)
    else:
        raise FileNotFoundError(f"The file '{path}' does not exist.")


def filter_dataframe_for_columns(
    df: pd.DataFrame,
    columns: List[str],
    keywords: List[str],
    blacklist: Optional[List[str]] = None
) -> pd.DataFrame:
    """
    Filters a DataFrame based on keywords in specified columns and excludes rows containing blacklist terms.

    Args:
        df (pd.DataFrame): The DataFrame to filter.
        columns (List[str]): List of column names to apply the filter.
        keywords (List[str]): List of keywords to search for in the columns.
        blacklist (Optional[List[str]]): List of terms to exclude from the results.

    Returns:
        pd.DataFrame: The filtered DataFrame.
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
    Removes duplicate rows based on specific columns.

    Args:
        df (pd.DataFrame): The DataFrame to process.
        columns (List[str]): List of column names to identify duplicates.

    Returns:
        pd.DataFrame: The DataFrame without duplicates.
    """
    return df.drop_duplicates(subset=columns)


def calc_string_diff_in_df_col(title_x: str, title_y: str) -> float:
    """
    Calculates the percentage difference between two strings using Levenshtein distance.

    Args:
        title_x (str): The first string to compare.
        title_y (str): The second string to compare.

    Returns:
        float: The percentage difference between the two strings.
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
    Reads and stacks historical CSV DataFrames from a directory.

    Args:
        history_data_path (str): Path to the directory containing historical CSV files.
        get_only_last (bool): If True, only the most recent file will be read.
        dtype (Optional[Dict[str, Any]]): Dictionary specifying the data types of the columns.

    Returns:
        pd.DataFrame: The concatenated DataFrame from historical CSV files.
    """
    # Use glob to find all CSV files in the directory
    csv_files: List[str] = glob(os.path.join(history_data_path, '*.csv'))
    csv_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)

    if get_only_last and csv_files:
        # Find the most recently modified CSV file
        latest_file: str = csv_files[0]
        message(f"Reading latest file: {latest_file}")
        return read_df(latest_file, dtype)
    elif csv_files:
        # Read all CSV files and concatenate them into a single DataFrame
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
    Reads and concatenates CSV files from multiple directories specified by pages.

    Args:
        data_path (str): The base data path.
        pages (List[str]): List of page directories to read files from.
        file_name (str): The name of the CSV file to read in each directory.
        dtype (Optional[Dict[str, Any]]): Dictionary specifying the data types of the columns.

    Returns:
        pd.DataFrame: The concatenated DataFrame from the specified CSV files.
    """
    pages_path: List[str] = [os.path.join(data_path, page) for page in pages]
    df_temp: List[pd.DataFrame] = []

    for path in pages_path:
        file_path: str = os.path.join(path, file_name)

        if os.path.exists(file_path):
            df_temp.append(read_df(file_path, dtype))
        else:
            message(f"File {file_path} not found, skipping to the next.")

    if df_temp:
        df: pd.DataFrame = pd.concat(df_temp, ignore_index=True)
    else:
        df = pd.DataFrame()

    return df
