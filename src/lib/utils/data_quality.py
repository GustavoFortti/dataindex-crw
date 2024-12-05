import os
import re
from datetime import date
from typing import Any, Dict, List, Optional, Tuple, Union

import pandas as pd
import requests

from src.jobs.pipeline import JobBase
from src.lib.utils.dataframe import (calc_string_diff_in_df_col,
                                     create_or_read_df,
                                     read_and_stack_historical_csvs_dataframes)
from src.lib.utils.file_system import (create_directory_if_not_exists,
                                       delete_file, has_files)
from src.lib.utils.general_functions import check_url_existence
from src.lib.utils.log import message


def check_if_job_is_ready(job_base: JobBase, data: Dict[str, Any], kill_job: bool = True) -> Optional[bool]:
    """
    Validates the provided data and determines the job status based on validation results.

    Args:
        job_base (JobBase): An object containing job configurations and paths.
        data (Dict[str, Any]): A dictionary containing data fields to validate.
        kill_job (bool, optional): Flag indicating whether to terminate the job on validation failure. Defaults to True.

    Returns:
        Optional[bool]: Returns False if validations fail and kill_job is False.
                         Returns True if validations pass and kill_job is False.
                         Returns None if the job is terminated.

    Raises:
        Exception: If any validation fails and kill_job is True.
    """
    errors: List[str] = []

    # Validate price format
    if not is_price(data.get("price", "")):
        errors.append("Error: Invalid price format.")

    # Validate image URL existence
    if not check_url_existence(data.get("image_url", "")):
        errors.append("Error: Image URL does not exist.")

    # Validate product URL existence
    if not check_url_existence(data.get("product_url", "")):
        errors.append("Error: Product URL does not exist.")

    if errors:
        for error in errors:
            message(error)

        if kill_job:
            message("Job terminated due to validation errors.")
            raise Exception(str(errors))
        else:
            return False

    message("All validations passed successfully.")
    if kill_job:
        df_products: pd.DataFrame = create_or_read_df(job_base.path_extract_csl, data.keys())
        if df_products.empty:
            delete_file(job_base.path_extract_csl)

        message("Terminating job as kill_job is True.")
        exit(0)
    else:
        message("Job continues to run.")
        return True


def data_history_analysis(conf: Dict[str, Any], df: pd.DataFrame) -> bool:
    """
    Analyzes the historical data against the current data to detect inconsistencies.

    Args:
        conf (Dict[str, Any]): Configuration dictionary containing paths and settings.
        df (pd.DataFrame): Current data DataFrame to analyze.

    Returns:
        bool: True if analysis is successful and no critical errors are found, else exits the program.

    Raises:
        SystemExit: Exits the program if corrupt data is detected.
    """
    history_path: str = f"{conf['data_path']}/history"

    # Ensure the history directory exists
    create_directory_if_not_exists(history_path)
    if not has_files(history_path):
        save_history_data(conf, df)
        return True

    message("Loading historical DataFrame...")
    message(f"History Path: {history_path}")
    df_history: pd.DataFrame = read_and_stack_historical_csvs_dataframes(
        history_path, combine=True, dtype={'ref': str}
    )

    message("Analyzing volume changes...")
    volume_error: bool
    volume_alert: bool
    volume_error, volume_alert = volume_analysis(df_history, df)

    message("Analyzing price changes...")
    price_error: bool
    price_alert: bool
    df_price: pd.DataFrame
    price_error, price_alert, df_price = price_analysis(df_history, df)

    is_success: bool = volume_error and price_error

    message(f"Volume Error: {volume_error}")
    message(f"Price Error: {price_error}")

    if not is_success:
        message("Error: Corrupt data detected during ingestion.")
        exit(1)

    return is_success


def volume_analysis(
    df_history: pd.DataFrame,
    df: pd.DataFrame,
    alert_threshold: float = 0.1,
    error_threshold: float = 0.2
) -> Tuple[bool, bool]:
    """
    Analyzes the change in volume between historical and current data.

    Args:
        df_history (pd.DataFrame): Historical data DataFrame.
        df (pd.DataFrame): Current data DataFrame.
        alert_threshold (float, optional): Threshold for triggering alerts. Defaults to 0.1.
        error_threshold (float, optional): Threshold for triggering errors. Defaults to 0.2.

    Returns:
        Tuple[bool, bool]: A tuple containing volume_error and volume_alert flags.
    """
    volume_history: int = len(df_history)
    volume_current: int = len(df)

    if volume_history == 0:
        return True, True

    volume_change: float = abs((volume_current / volume_history) - 1)
    message(f"Volume Change: {volume_change:.2f}")

    volume_error: bool = volume_change < error_threshold
    volume_alert: bool = volume_change < alert_threshold

    return volume_error, volume_alert


def title_analysis(df_history: pd.DataFrame, df: pd.DataFrame) -> Tuple[bool, bool, pd.DataFrame]:
    """
    Analyzes the differences in titles between historical and current data.

    Args:
        df_history (pd.DataFrame): Historical data DataFrame.
        df (pd.DataFrame): Current data DataFrame.

    Returns:
        Tuple[bool, bool, pd.DataFrame]: Flags indicating title errors and alerts, and the result DataFrame.

    Raises:
        ValueError: If the merged DataFrame is empty.
    """
    df_history_title: pd.DataFrame = df_history[["ref", "title"]]
    df_title: pd.DataFrame = df[["ref", "title"]]
    result_df_title: pd.DataFrame = df_history_title.merge(df_title, on='ref', how='inner')

    if result_df_title.empty:
        message("Error: Merged title DataFrame is empty.")
        return False, False, df

    # Calculate the percentage difference between titles
    result_df_title['diff_percent'] = result_df_title.apply(
        lambda row: calc_string_diff_in_df_col(row['title_x'], row['title_y']), axis=1
    ).astype(float)

    threshold_error: float = 0.60
    threshold_alert: float = 0.20
    result_df_title['title_error'] = result_df_title['diff_percent'] <= threshold_error
    result_df_title['title_alert'] = result_df_title['diff_percent'] <= threshold_alert

    message("Title Error DataFrame:")
    df_error: pd.DataFrame = result_df_title.sort_values('diff_percent')
    print(df_error[~df_error['title_error']][['ref', 'title_x', 'title_y', 'diff_percent', 'title_error', 'title_alert']])

    return (
        not result_df_title["title_error"].eq(False).any(),
        not result_df_title["title_alert"].eq(False).any(),
        result_df_title
    )


def price_analysis(df_history: pd.DataFrame, df: pd.DataFrame) -> Tuple[bool, bool, pd.DataFrame]:
    """
    Analyzes the differences in prices between historical and current data.

    Args:
        df_history (pd.DataFrame): Historical data DataFrame.
        df (pd.DataFrame): Current data DataFrame.

    Returns:
        Tuple[bool, bool, pd.DataFrame]: Flags indicating price errors and alerts, and the result DataFrame.
    """
    df_history_price: pd.DataFrame = df_history.groupby('ref')['price_numeric'].agg(['mean', 'max', 'min']).reset_index()
    df_price: pd.DataFrame = df[['ref', 'price_numeric']]
    result_df_price: pd.DataFrame = df_history_price.merge(df_price, on='ref', how='inner')

    result_df_price['diff_percent'] = abs((result_df_price['price_numeric'] / result_df_price['mean']) - 1)

    threshold_error: float = 0.70
    threshold_alert: float = 0.40
    result_df_price['price_error'] = result_df_price['diff_percent'] <= threshold_error
    result_df_price['price_alert'] = result_df_price['diff_percent'] <= threshold_alert

    message("Price Error DataFrame:")
    df_error: pd.DataFrame = result_df_price.sort_values('diff_percent')
    print(df_error)

    message("Filtered Price Errors:")
    print(df_error[~df_error['price_error']])

    message("Filtered Valid Prices:")
    print(df_error[df_error['price_error']])

    return (
        not result_df_price["price_error"].eq(False).any(),
        not result_df_price["price_alert"].eq(False).any(),
        result_df_price
    )


def save_history_data(conf: Dict[str, Any], df: pd.DataFrame) -> None:
    """
    Saves the current data as historical data for future analysis.

    Args:
        conf (Dict[str, Any]): Configuration dictionary containing paths and settings.
        df (pd.DataFrame): Current data DataFrame to save.
    """
    history_path: str = f"{conf['data_path']}/history"

    current_date: date = date.today()
    formatted_date: str = current_date.strftime(DATE_FORMAT)

    # Ensure the history directory exists
    create_directory_if_not_exists(history_path)

    # Save the DataFrame to a CSV file with the current date
    csv_path: str = f"{history_path}/products_load_csl_{formatted_date}.csv"
    df.to_csv(csv_path, index=False)
    message(f"Saved historical data to {csv_path}")


def is_price(string: Any) -> bool:
    """
    Validates if the provided string matches accepted price formats.

    Supported formats:
        - BRL: R$ 1.234,56
        - EUR: € 1.234,56
        - USD: $1,234.56
        - GBP: £1,234.56

    Args:
        string (Any): The string to validate as a price.

    Returns:
        bool: True if the string matches any of the supported price formats, else False.
    """
    if not isinstance(string, str):
        return False

    pattern: str = r"""
        ^(?:
            (R\$\s?\d{1,3}(?:\.\d{3})*[,.]\d{2})|  # BRL: R$ 1.234,56
            (€\s?\d{1,3}(?:\.\d{3})*,\d{2})|       # EUR: € 1.234,56
            (\$\s?\d{1,3}(?:,\d{3})*\.\d{2})|      # USD: $1,234.56
            (£\s?\d{1,3}(?:,\d{3})*\.\d{2})        # GBP: £1,234.56
        )$
    """

    return bool(re.match(pattern, string, re.VERBOSE | re.MULTILINE))