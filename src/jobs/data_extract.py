import importlib
import os
from datetime import date
from typing import Any, Dict, List, Optional

import pandas as pd

from src.lib.extract.crawler import crawler
from src.lib.utils.data_quality import is_price
from src.lib.utils.dataframe import create_or_read_df, read_df
from src.lib.utils.file_system import (create_file_if_not_exists,
                                       delete_directory_and_contents,
                                       delete_file)
from src.lib.utils.log import message
from src.lib.utils.text_functions import find_in_text_with_wordlist
from src.lib.wordlist.wordlist import BLACK_LIST
from src.pages.page import Page


def run(job_base: classmethod) -> None:
    message("extract start")

    page_module = importlib.import_module(f"src.pages.{job_base.page_name}.page")
    page = Page(**page_module.page_arguments)
    
    job_base.set_page(page)
    job_base.page.set_seeds(f"{job_base.local}/src/pages/{job_base.page.brand}/seed.json")
    job_base.page.set_page_functions(
        f"src.pages.{job_base.page_name}.page_elements",
        f"src.pages.{job_base.page_name}.page_url"
    )
    
    options = job_base.options
    extract_functions = {
        "create_new_page": create_new_page,
        "update_all_products": update_all_products
        # "update_all_products_metadata": update_products_metadata
        # "update_old_product_metadata": update_old_product_metadata
        # "create_products_metadata_if_not_exist": create_products_metadata_if_not_exist
        # "check_if_job_is_ready": check_if_job_is_ready
    }
    
    extract_functions.get(options)(job_base)
    

def create_new_page(job_base: classmethod) -> None:
    """
    Initializes a new page by resetting relevant configurations and performing updates.

    Args:
        config (Dict[str, Any]): Configuration dictionary.
        page (Page): Page object containing configuration and state.

    Returns:
        None
    """
    message("Initializing new page")
    data_path_pattern: str = f"{job_base.data_path}/*"
    delete_directory_and_contents(data_path_pattern)

    job_base.update_all_products = True
    update_all_products(job_base)

    job_base.update_all_products = False
    job_base.update_all_products_metadata = True
    update_all_products_metadata(job_base)

def update_all_products(job_base: classmethod) -> None:
    """
    Updates the products by crawling through seeds and extracting relevant data.

    Args:
        page (Page): Page object containing configuration and state.
        config (Dict[str, Any]): Configuration dictionary.

    Returns:
        None
    """
    delete_file(job_base.path_extract_temp)

    df_products: pd.DataFrame = create_or_read_df(job_base.path_extract_csl, job_base.df_columns)
    
    seeds = job_base.page.seeds
    for index, seed in enumerate(seeds):
        message(f"seed index: {index + 1} / {len(seeds)}")
        job_base.page.seed = seed

        iteration_count: int = 0
        max_iterations: int = 100
        
        while True:
            url: str = job_base.page.get_url()
            crawler_index: int = job_base.page.crawler_index

            message(f"current url index: {crawler_index}")
            message(f"url: {url}")

            if url is None:
                message("No more URLs to process for this seed.")
                break

            crawler(job_base, url)
            exit()

            # Safeguard to prevent infinite loop
            iteration_count += 1
            if iteration_count >= max_iterations:
                message(f"Reached maximum iterations ({max_iterations}) for seed index {index + 1}. Breaking the loop.")
                break

            # Check if size_items has been updated correctly
            size_items: int = page.conf.get("size_items", -1)
            message(f"Size items after crawling: {size_items}")

            if size_items == 0 or not crawler_index:
                message(f"Size items = {size_items}")
                message(f"Index = {crawler_index}")
                message("Proceeding to next seed due to index or size_items")
                break

        page.reset_index()

    message(f"Reading file: {page.conf['path_products_extract_temp']}")
    df_products_extract_temp: pd.DataFrame = read_df(page.conf['path_products_extract_temp'], dtype={'ref': str})
    df_products_extract_temp = df_products_extract_temp.drop_duplicates(subset='ref').reset_index(drop=True)
    df_products_extract_temp = df_products_extract_temp.dropna(subset=['price'])

    df_products_extract_temp = df_products_extract_temp[
        ~df_products_extract_temp['title'].apply(lambda x: find_in_text_with_wordlist(x, BLACK_LIST))
    ]
    df_products_extract_temp = df_products_extract_temp[df_products_extract_temp['price'].apply(is_price)]

    message(f"Writing to origin: {page.conf['path_products_extract_csl']}")
    df_products_extract_temp.to_csv(page.conf['path_products_extract_csl'], index=False)
    delete_file(page.conf["control_products_update"])
    create_file_if_not_exists(page.conf["control_products_update"], "")


def update_all_products_metadata(job_base: classmethod) -> None:
    """
    Updates the products' metadata by crawling through product URLs and saving page sources.

    Args:
        page (Page): Page object containing configuration and state.
        config (Dict[str, Any]): Configuration dictionary.

    Returns:
        None
    """
    message("Updating products metadata")
    products_extract_csl: str = os.path.join(config['data_path'], "products_extract_csl.csv")
    page.conf['path_products_extract_csl'] = products_extract_csl
    df_products_extract_csl: pd.DataFrame = read_df(products_extract_csl, dtype={'ref': str})

    urls: List[str] = df_products_extract_csl['product_url'].values.tolist()
    total_urls: int = len(urls)
    for index, url in enumerate(urls):
        message(f"Processing URL: {url}")
        message(f"Index: {index + 1} / {total_urls}")
        crawler(page, url)

    delete_file(page.conf["control_products_metadata_update"])
    create_file_if_not_exists(page.conf["control_products_metadata_update"], "")
