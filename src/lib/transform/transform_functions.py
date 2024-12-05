import json
import os
import re
from copy import deepcopy
from typing import Any, Dict, List, Optional, Tuple

import imagehash
import numpy as np
import pandas as pd
from PIL import Image

from src.jobs.pipeline import JobBase
from src.lib.utils.dataframe import read_and_stack_historical_csvs_dataframes
from src.lib.utils.file_system import (
    create_directory_if_not_exists,
    file_or_path_exists,
    list_directory,
    save_file,
)
from src.lib.utils.image_functions import calculate_precise_image_hash, convert_image
from src.lib.utils.log import message
from src.lib.utils.text_functions import clean_text, find_in_text_with_wordlist, remove_spaces
from src.lib.wordlist.wordlist import BLACK_LIST


def ensure_columns_exist(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    """
    Ensures that the specified columns exist in the DataFrame.
    If a column does not exist, it is added with NaN values.

    Args:
        df (pd.DataFrame): The DataFrame to modify.
        columns (List[str]): List of column names to ensure.

    Returns:
        pd.DataFrame: The modified DataFrame with the specified columns.
    """
    for column in columns:
        if column not in df.columns:
            df[column] = np.nan  # Add the column with NaN (null) values
    return df


def filter_nulls(df: pd.DataFrame) -> pd.DataFrame:
    """
    Filters out rows with null values in 'title', 'price', or 'image_url' columns.

    Args:
        df (pd.DataFrame): The DataFrame to filter.

    Returns:
        pd.DataFrame: The filtered DataFrame with reset index.
    """
    return df.dropna(subset=['title', 'price', 'image_url']).reset_index(drop=True)


def creates_new_columns_from_dirty_columns(df: pd.DataFrame, job_base: JobBase) -> pd.DataFrame:
    """
    Applies various data cleaning and transformation filters to the DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame to process.
        job_base (JobBase): An instance of JobBase containing job configurations.

    Returns:
        pd.DataFrame: The transformed DataFrame.
    """
    df['title_extract'] = df['title']
    df['name'] = df['title'].str.lower()
    df['price'] = df['price'].str.replace(r'[R$]', '', regex=True).str.replace(' ', '')
    df['brand'] = job_base.page.brand
    df['page_name'] = job_base.page_name

    # Remove thousands separator dots and replace comma with dot
    df['price_numeric'] = df['price'].str.replace(',', '.').astype(float)

    df['title'] = df['title'].apply(clean_text).apply(remove_spaces)
    return df


def apply_platform_data(df: pd.DataFrame, job_base: JobBase) -> pd.DataFrame:
    """
    Applies platform-specific data to the DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame to process.
        job_base (JobBase): An instance of JobBase containing job configurations.

    Returns:
        pd.DataFrame: The DataFrame with platform data applied.
    """
    df['affiliate_coupon'] = job_base.page.affiliate_coupon
    df['affiliate_coupon_discount_percentage'] = job_base.page.affiliate_coupon_discount_percentage
    df['affiliate_url'] = None
    if job_base.page.affiliate_url:
        df['affiliate_url'] = job_base.page.affiliate_url

    return df


def create_quantity_column(df: pd.DataFrame) -> pd.DataFrame:
    """
    Extracts and converts quantity information into a uniform format.

    Args:
        df (pd.DataFrame): The DataFrame to process.

    Returns:
        pd.DataFrame: The DataFrame with quantity information added.
    """
    # Ensure we always return two elements to avoid column size error
    df['quantity_unit'] = df['name'].apply(lambda text: find_pattern_for_quantity(text))

    # Split 'quantity_unit' column into 'quantity' and 'unit_of_measure'
    df[['quantity', 'unit_of_measure']] = pd.DataFrame(df['quantity_unit'].tolist(), index=df.index)

    # Apply conversion to grams
    df['quantity'] = df[['quantity', 'unit_of_measure']].apply(convert_to_grams, axis=1)

    # Calculate price per quantity
    df['price_per_quantity'] = df.apply(calculate_price_per_quantity, axis=1)

    # Replace invalid values with NaN
    df['quantity'] = df['quantity'].apply(lambda x: np.nan if x == -1 else x)

    return df


def remove_blacklisted_products(df: pd.DataFrame) -> pd.DataFrame:
    """
    Removes products based on a blacklist.

    Args:
        df (pd.DataFrame): The DataFrame to filter.

    Returns:
        pd.DataFrame: The filtered DataFrame without blacklisted products.
    """
    return df[~df['title'].apply(lambda x: find_in_text_with_wordlist(x, BLACK_LIST))]


def find_pattern_for_quantity(text: str) -> Tuple[Optional[float], Optional[str]]:
    """
    Finds quantity and unit patterns in the given text.

    Args:
        text (str): The text to search for quantity patterns.

    Returns:
        Tuple[Optional[float], Optional[str]]: The quantity and unit found, or (None, None) if not found.
    """
    # Add liquid measurement units (ml and l) and also capsules/comprimidos
    pattern = r'(\d+[.,]?\d*)\s*(kg|g|gr|gramas|ml|l|litro|litros|cápsula|capsula|capsule|cap|caps|comprimido|comp|comps)'
    matches = re.findall(pattern, text, re.IGNORECASE)

    quantity = None
    unit = None
    if len(matches) == 1:
        quantity_str, unit = matches[0]
        quantity_str = str(quantity_str).replace(',', '.')

        # Adjust gram and milliliter units to integers when necessary
        if unit.lower() in ['g', 'gr', 'gramas', 'ml'] and "." in quantity_str:
            quantity_str = quantity_str.replace(".", "")

        try:
            quantity = float(quantity_str)
        except ValueError:
            quantity = None

        # Check for multiples of units, like '3x'
        multiply_pattern = r'(\d+)x'
        matches_multiply = re.findall(multiply_pattern, text)
        if len(matches_multiply) == 1 and quantity is not None:
            quantity *= float(matches_multiply[0])

    return quantity, unit


def convert_to_grams(row: pd.Series) -> float:
    """
    Converts the quantity to grams based on the unit of measure.

    Args:
        row (pd.Series): A row from the DataFrame containing 'quantity' and 'unit_of_measure'.

    Returns:
        float: The quantity converted to grams, or -1 if invalid.
    """
    value = row['quantity']
    unit = row['unit_of_measure']

    if pd.notna(value):
        if unit in ['kg']:
            value = float(value) * 1000
        try:
            value = int(float(value))
        except ValueError:
            pass
    else:
        value = -1

    return value


def calculate_price_per_quantity(row: pd.Series) -> Optional[float]:
    """
    Calculates the price per quantity unit.

    Args:
        row (pd.Series): A row from the DataFrame containing 'price_numeric' and 'quantity'.

    Returns:
        Optional[float]: The price per quantity unit, or NaN if invalid.
    """
    if row['quantity'] > 0:
        result = row['price_numeric'] / row['quantity']
    else:
        result = -1
    if result < 0:
        return np.nan
    return round(result, 3)


def image_processing(df: pd.DataFrame, data_path: str) -> None:
    """
    Processes images by generating hashes, comparing with existing hashes, and converting images as needed.

    Args:
        df (pd.DataFrame): DataFrame containing product references.
        data_path (str): The base path where images and other data are stored.

    Raises:
        Exception: If there is a mismatch between expected and found images.
    """
    message("Starting image processing")
    path_img_temp = os.path.join(data_path, "img_tmp")
    path_img_hash = os.path.join(data_path, "img_hash")
    path_img_csl = os.path.join(data_path, "img_csl")
    create_directory_if_not_exists(path_img_hash)
    create_directory_if_not_exists(path_img_csl)

    refs = sorted(df['ref'])

    images_in_temp = list_directory(path_img_temp)
    dict_images = {filename.split(".")[0]: filename for filename in images_in_temp if filename.split(".")[0] in refs}
    dict_images = dict(sorted(dict_images.items(), key=lambda item: item[1]))

    if not set(dict_images.keys()).issubset(refs):
        difference = set(dict_images.keys()) - set(refs)
        message(f"Missing references in images: {difference}")
        raise Exception("ERROR IMAGE PROCESSING")

    message("Loading images")

    def describe_image(image: Image.Image, img_path: str) -> Dict[str, Any]:
        width, height = image.size
        file_size = os.path.getsize(img_path)
        return {
            "dimensions": (width, height),
            "size": file_size,
            "img_path": img_path
        }

    images_info: Dict[str, Dict[str, Any]] = {}

    for index, (ref, img_file_name) in enumerate(dict_images.items()):
        img_path = os.path.join(path_img_temp, img_file_name)
        image = Image.open(img_path)
        new_image_hash = calculate_precise_image_hash(img_path)
        new_image_hash_str = str(new_image_hash)
        new_image_hash = imagehash.hex_to_hash(new_image_hash_str)

        path_ref_img_hash = os.path.join(path_img_hash, f"{ref}.txt")
        if file_or_path_exists(path_ref_img_hash):
            with open(path_ref_img_hash, "r") as file:
                old_image_hash_str = file.read()
                old_image_hash = imagehash.hex_to_hash(old_image_hash_str)

            if new_image_hash != old_image_hash:
                save_file(new_image_hash_str, path_ref_img_hash)
                images_info[ref] = describe_image(image, img_path)
        else:
            save_file(new_image_hash_str, path_ref_img_hash)
            images_info[ref] = describe_image(image, img_path)

    for ref, image_info in images_info.items():
        save_path = os.path.join(path_img_csl, ref)
        img_path = image_info["img_path"]
        convert_image(img_path, save_path)
    message("Image processing completed successfully")


def filter_price_changes(df: pd.DataFrame, refs: List[str]) -> pd.DataFrame:
    """
    Filters the DataFrame to include only rows where the price has changed for each reference.

    Args:
        df (pd.DataFrame): The DataFrame containing price information.
        refs (List[str]): List of product references to process.

    Returns:
        pd.DataFrame: The filtered DataFrame containing only price changes.
    """
    for ref in refs:
        df_temp = df[df["ref"] == ref].sort_values('ing_date')

        last_price = None
        for idx, row in df_temp.iterrows():
            price = row['price_numeric']
            is_price_changed = False

            if last_price is None or last_price != price:
                last_price = price
                is_price_changed = True

            df.loc[idx, "is_price_changed"] = is_price_changed

    df = df[df['is_price_changed']]
    return df


def create_price_discount_percent_col(df: pd.DataFrame, data_path: str) -> pd.DataFrame:
    """
    Creates a 'price_discount_percent' column in the DataFrame based on historical prices.

    Args:
        df (pd.DataFrame): The current DataFrame.
        data_path (str): The base path where historical price data is stored.

    Returns:
        pd.DataFrame: The DataFrame with 'price_discount_percent' and 'compare_at_price' columns added.
    """
    df_new = deepcopy(df)
    refs = df['ref'].values

    path = os.path.join(data_path, "history")
    df_temp = read_and_stack_historical_csvs_dataframes(path, False, dtype={'ref': str})

    if df_temp.empty:
        df_new["price_discount_percent"] = 0.0
        df_new["compare_at_price"] = None
        return df_new

    df_temp = df_temp[df_temp["ref"].isin(refs)]
    df_price = pd.concat([df, df_temp], ignore_index=True)

    df_price_temp = filter_price_changes(df_price, refs)
    df_price_temp = df_price_temp[['ref', 'price_numeric', 'ing_date']]

    refs_processed = []

    for ref in refs:
        if ref in refs_processed:
            continue
        refs_processed.append(ref)

        df_price_temp_sorted = df_price_temp[df_price_temp["ref"] == ref].sort_values('ing_date', ascending=False)
        prices = df_price_temp_sorted["price_numeric"].values

        price_discount_percent = 0.0
        compare_at_price = None
        if len(prices) > 1:
            price_ratio = prices[0] / prices[1]
            if price_ratio < 1.0:
                compare_at_price = prices[1]
                price_discount_percent = round(1.0 - price_ratio, 2)

        df_new.loc[df_new['ref'] == ref, "price_discount_percent"] = price_discount_percent
        df_new.loc[df_new['ref'] == ref, "compare_at_price"] = compare_at_price

    return df_new


def create_history_price_column(df: pd.DataFrame, job_base: JobBase) -> pd.DataFrame:
    """
    Adds a 'prices' column to the DataFrame containing historical price data.

    Args:
        df (pd.DataFrame): The current DataFrame.
        job_base (JobBase): An instance of JobBase containing job configurations.

    Returns:
        pd.DataFrame: The DataFrame with the 'prices' column added.
    """
    df_new = deepcopy(df)
    df_new["prices"] = None

    df_historical_prices = read_and_stack_historical_csvs_dataframes(
        job_base.path_history_price, False, dtype={'ref': str}
    )

    if df_historical_prices.empty:
        return df_new

    message("Processing historical prices")
    for idx, row in df_new.iterrows():
        ref = row['ref']

        df_price = df_historical_prices[df_historical_prices["ref"] == ref].sort_values(by='ing_date', ascending=False)

        if df_price.empty:
            continue

        prices_dates = df_price[["price_numeric", "ing_date"]].values.tolist()
        filtered_prices_dates = []

        for i in range(len(prices_dates)):
            price, date = prices_dates[i]
            if i == len(prices_dates) - 1 or price != prices_dates[i + 1][0]:
                filtered_prices_dates.append({'price': price, 'date': date})

        if len(filtered_prices_dates) >= 2:
            df_new.loc[idx, "prices"] = str(filtered_prices_dates)

    return df_new
