import importlib
from typing import Optional
from src.jobs.pipeline import JobBase
from src.lib.transform.product_info import create_product_info_columns
from src.lib.transform.transform_functions import (
    apply_generic_filters,
    apply_platform_data,
    create_history_price_column,
    create_price_discount_percent_col,
    create_quantity_column,
    filter_nulls,
    remove_blacklisted_products,
)
from src.lib.utils.log import message
from src.lib.utils.dataframe import read_df
from src.pages.page import Page


def run(job_base: JobBase) -> Optional[None]:
    """
    Executes the data transformation pipeline for a given job.

    Args:
        job_base (JobBase): An instance of JobBase containing job-specific configurations.

    Returns:
        Optional[None]: Exits the program after transformations and saves the result.
    """
    # Load the appropriate page module dynamically
    page_module = importlib.import_module(f"src.pages.{job_base.page_name}.page")
    page = Page(**page_module.page_arguments)
    job_base.set_page(page)

    message("Transformation process started.")
    df = read_df(job_base.path_extract_csl, dtype={'ref': str})

    # Apply various transformations and filters
    message("Filtering null values.")
    df = filter_nulls(df)

    message("Applying generic filters (name, price, brand).")
    df = apply_generic_filters(df, job_base)

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

    # Drop rows with critical missing values
    df = df.dropna(subset=["ref", "title", "price", "image_url", "product_url"], how="any")

    # Reorder and select relevant columns
    df = df[
        [
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
    ]

    # Display DataFrame info for debugging
    print(df.info())

    # Save historical price data
    df[["ref", "price_numeric", "ing_date"]].to_csv(
        job_base.path_history_price_file, index=False
    )

    message("Transformation process completed successfully.")
    return df
