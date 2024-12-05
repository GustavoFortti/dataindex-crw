import importlib
from copy import deepcopy
from typing import List, Optional

import pandas as pd

from src.jobs.pipeline import JobBase
from src.lib.load.shopify import process_and_ingest_products
from src.lib.utils.dataframe import (create_or_read_df,
                                     read_and_stack_csvs_dataframes)
from src.lib.utils.file_system import (create_directory_if_not_exists,
                                       delete_file, file_or_path_exists,
                                       list_directory)
from src.lib.utils.log import message
from src.lib.utils.page_functions import get_pages_with_status_true
from src.pages.page import Page


def run(job_base: JobBase) -> Optional[None]:
    """
    Executes the data load pipeline for a given job.

    Args:
        job_base (JobBase): An instance of JobBase containing job-specific configurations.

    Returns:
        Optional[None]: Exits the program after processing data and saving results.
    """
    # Step 1: Initialize and load pages
    message("Load process started.")

    pages: List[str] = list_directory(job_base.pages_path)
    pages = [page for page in pages if ("." not in page) and ("__" not in page)]
    
    for page_name in pages:
        page_module = importlib.import_module(f"src.pages.{page_name}.page")
        page: Page = Page(**page_module.page_arguments)
        job_base.append_pages(page)
    
    create_directory_if_not_exists(job_base.load_data_path)
    
    # Step 2: Read transformed data
    message("Reading data.")
    pages_with_status_true: List[Page] = get_pages_with_status_true(job_base)
    df_products_transform_csl: pd.DataFrame = read_and_stack_csvs_dataframes(
        job_base.src_data_path,
        pages_with_status_true,
        "transform_csl.csv",
        dtype={'ref': str}
    )
    df_products_transform_csl = df_products_transform_csl.drop_duplicates(subset='ref').reset_index(drop=True)
    df_products_transform_csl = df_products_transform_csl.sample(frac=1).reset_index(drop=True)

    # Add column 'is_transform_data' to indicate new data
    columns: List[str] = df_products_transform_csl.columns.tolist()
    df_products_transform_csl['is_transform_data'] = 1

    # Step 3: Load last processed data
    df_last_load: pd.DataFrame = create_or_read_df(job_base.path_memory_shopify)
    if df_last_load.empty:
        message("Flag - Loading initial df_last_load.")
        df_last_load = create_or_read_df(job_base.path_load_csl, df_products_transform_csl.columns)

    if not df_last_load.empty:
        df_last_load['is_transform_data'] = 0

        # Concatenate DataFrames
        df_union: pd.DataFrame = pd.concat([df_products_transform_csl, df_last_load], ignore_index=True)

        # Remove duplicates and keep only new transform data
        df_union_no_transform: pd.DataFrame = df_union.drop(
            columns=['is_transform_data', 'ing_date'],
            errors='ignore'
        )
        duplicates: pd.Index = df_union_no_transform[df_union_no_transform.duplicated(keep=False)].index

        # Filter out duplicates from the original DataFrame
        df: pd.DataFrame = df_union.drop(duplicates).query("is_transform_data == 1").reset_index(drop=True)
    else:
        df = deepcopy(df_products_transform_csl)

    # Remove the helper column and revert to original column order
    df = df.drop(columns=['is_transform_data'])
    df = df[columns]
    df_products_transform_csl = df_products_transform_csl.drop(columns=['is_transform_data'])

    # Step 4: Process data with Shopify
    brands: List[str] = [page.brand for page in job_base.pages]

    if not df.empty:
        refs: List[str] = df_products_transform_csl["ref"].tolist()
        process_and_ingest_products(job_base, df, refs, brands)
        exit()
        df.to_csv(job_base.path_shopify_csl, index=False)
        message(f"path_shopify_csl - {file_or_path_exists(job_base.path_shopify_csl)}")
    
    # Step 5: Save updated data and clean up
    df_products_transform_csl.to_csv(job_base.path_load_csl, index=False)
    delete_file(job_base.path_memory_shopify)
    message(f"path_load_csl - {file_or_path_exists(job_base.path_load_csl)}")
    message("LOAD END")
