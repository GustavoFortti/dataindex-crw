import importlib
from typing import Optional

import pandas as pd

from src.jobs.job_manager import JobBase
from src.lib.transform.product_info import create_product_info_columns
from src.lib.transform.transform_functions import (
    creates_new_columns_from_dirty_columns, apply_platform_data, create_history_price_column,
    create_price_discount_percent_col, create_quantity_column, filter_nulls,
    remove_blacklisted_products)
from src.lib.utils.dataframe import read_df
from src.lib.utils.log import message
from src.pages.page import Page


def run(job_base: JobBase) -> Optional[None]:
    """
    Executes the data transformation pipeline for a given job.

    Args:
        job_base (JobBase): An instance of JobBase containing job-specific configurations.

    Returns:
        Optional[None]: Exits the program after transformations and saves the result.
    """
    # Step 1: Initialize and load the page
    message("Transformation process started.")

    page_module = importlib.import_module(f"src.pages.{job_base.page_name}.page")
    page: Page = Page(**page_module.page_arguments)
    job_base.set_page(page)

    # Step 2: Read the extracted data
    df: pd.DataFrame = read_df(job_base.path_extract_csl, dtype={'ref': str})

    # Step 3: Apply transformations and filters
    message("Filtering null values.")
    df = filter_nulls(df)

    message("Create (name, price, brand).")
    df = creates_new_columns_from_dirty_columns(df, job_base)

    message("Applying platform-specific data (coupons, links).")
    df = apply_platform_data(df, job_base)

    message("Creating quantity column.")
    df = create_quantity_column(df)

    message("Removing blacklisted products.")
    df = remove_blacklisted_products(df)

    message("Creating discount percentage column.")
    df = create_price_discount_percent_col(df, job_base.data_path)

    message("Creating historical prices column.")
    df = create_history_price_column(df, job_base)

    message("Creating product information columns (product_definition, collections).")
    df = create_product_info_columns(df, job_base)

    # Step 4: Drop rows with critical missing values
    df = df.dropna(subset=["ref", "title", "price", "image_url", "product_url"], how="any")

    # Step 5: Reorder and select relevant columns
    selected_columns: list[str] = [
        'ref',
        'title',
        'title_extract',
        'title_terms',
        'name',
        'brand',
        'page_name',
        'image_url',
        'product_url',
        'price_numeric',
        'price',
        'prices',
        'compare_at_price',
        'price_discount_percent',
        'quantity',
        'unit_of_measure',
        'price_per_quantity',
        'product_tags',
        'collections',
        'product_score',
        'affiliate_url',
        'affiliate_coupon',
        'affiliate_coupon_discount_percentage',
        'ing_date',
    ]
    df = df[selected_columns]

    # Step 6: Display DataFrame info for debugging
    message("Displaying DataFrame info:")
    print(df.info())

    # Step 7: Save historical price data
    historical_price_columns: list[str] = ["ref", "price_numeric", "ing_date"]
    df[historical_price_columns].to_csv(
        job_base.file_path_history_price, index=False
    )

    # Step 8: Save the transformed data
    message("Transformation process completed successfully.")
    df.to_csv(job_base.path_transform_csl, index=False)