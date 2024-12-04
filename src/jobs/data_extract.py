import importlib
import os
from typing import List

import pandas as pd

from src.jobs.pipeline import JobBase
from src.lib.extract.crawler import crawler
from src.lib.utils.data_quality import is_price
from src.lib.utils.dataframe import read_df
from src.lib.utils.file_system import (create_directory_if_not_exists,
                                       create_file_if_not_exists,
                                       delete_directory_and_contents,
                                       delete_file,
                                       file_modified_within_x_hours,
                                       get_old_files_by_percent,
                                       list_directory)
from src.lib.utils.log import message
from src.lib.utils.text_functions import find_in_text_with_wordlist
from src.lib.wordlist.wordlist import BLACK_LIST
from src.pages.page import Page


def run(job_base: JobBase) -> None:
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
        "update_all_products": update_all_products,
        "update_all_products_metadata": update_all_products_metadata,
        "update_old_products_metadata": update_old_products_metadata,
        "create_products_metadata_if_not_exist": create_products_metadata_if_not_exist,
        "check_if_job_is_ready": check_if_job_is_ready
    }
    
    control_options = {
        "update_all_products": job_base.control_update_all_products,
        "update_all_products_metadata": job_base.control_update_all_products_metadata,
        "update_old_products_metadata": job_base.control_update_old_products_metadata,
    }
    
    control_file = control_options.get(options, False)
    if control_file:
        checkpoint_extract_data(control_file)
    
    extract_functions.get(options)(job_base)
    

def create_new_page(job_base: JobBase) -> None:
    """
    Initializes a new page by resetting relevant configurations and performing updates.

    Args:
        job_base (JobBase): JobBase object containing configuration and state.

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


def update_all_products(job_base: JobBase) -> None:
    """
    Updates the products by crawling through seeds and extracting relevant data.

    Args:
        job_base (JobBase): JobBase object containing configuration and state.

    Returns:
        None
    """
    delete_file(job_base.path_extract_temp)

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
            # Safeguard to prevent infinite loop
            iteration_count += 1
            if iteration_count >= max_iterations:
                message(f"Reached maximum iterations ({max_iterations}) for seed index {index + 1}. Breaking the loop.")
                break

            message(f"Size items after crawling: {job_base.page.crawler_n_products_in_index}")

            if job_base.page.crawler_n_products_in_index == 0 or not crawler_index:
                message(f"number of products in index = {job_base.page.crawler_n_products_in_index}")
                message(f"index = {crawler_index}")
                message("proceeding to next seed due to index or crawler_n_products_in_index")
                break

        job_base.page.reset_index()
        
    message("page map completed")
    message(f"reading file: {job_base.path_extract_temp}")
    df_extract_temp: pd.DataFrame = read_df(job_base.path_extract_temp, dtype={'ref': str})
    df_extract_temp = df_extract_temp.drop_duplicates(subset='ref').reset_index(drop=True)
    df_extract_temp = df_extract_temp.dropna(subset=['price'])

    df_extract_temp = df_extract_temp[
        ~df_extract_temp['title'].apply(lambda x: find_in_text_with_wordlist(x, BLACK_LIST))
    ]
    df_extract_temp = df_extract_temp[df_extract_temp['price'].apply(is_price)]

    message(f"writing to origin: {job_base.path_extract_csl}")
    df_extract_temp.to_csv(job_base.path_extract_csl, index=False)
    delete_file(job_base.control_update_all_products)
    create_file_if_not_exists(job_base.control_update_all_products, "")


def update_all_products_metadata(job_base: JobBase) -> None:
    """
    Updates the products' metadata by crawling through product URLs and saving page sources.

    Args:
        job_base (JobBase): JobBase object containing configuration and state.

    Returns:
        None
    """
    message("update_all_products_metadata")
    df_extract_csl: pd.DataFrame = read_df(job_base.path_extract_csl, dtype={'ref': str})

    urls: List[str] = df_extract_csl['product_url'].values.tolist()
    total_urls: int = len(urls)
    for index, url in enumerate(urls):
        message(f"Processing URL: {url}")
        message(f"Index: {index + 1} / {total_urls}")
        crawler(job_base, url)

    delete_file(job_base.control_update_all_products_metadata)
    create_file_if_not_exists(job_base.control_update_all_products_metadata, "")


def update_old_products_metadata(job_base: JobBase) -> None:
    """
    Updates metadata for old product pages based on a percentage criterion.

    Args:
        page (Page): Page object containing configuration and state.
        config (Dict[str, Any]): Configuration dictionary.

    Returns:
        None
    """
    message("Updating metadata for old product pages")
    df_products_extract_csl: pd.DataFrame = read_df(job_base.path_extract_csl, dtype={'ref': str})

    products_path: str = os.path.join(job_base.data_path, "products")
    old_files: List[str] = get_old_files_by_percent(products_path, True, 5)
    refs: List[str] = [file.replace(".txt", "") for file in old_files]

    df_products_extract_csl = df_products_extract_csl[df_products_extract_csl['ref'].isin(refs)]

    refs_to_delete: List[str] = list(set(refs) - set(df_products_extract_csl['ref']))
    if refs_to_delete:
        for ref in refs_to_delete:
            file_path: str = os.path.join(products_path, f"{ref}.txt")
            delete_file(file_path)

    create_directory_if_not_exists(products_path)

    urls: List[str] = df_products_extract_csl['product_url'].values.tolist()
    total_urls: int = len(urls)
    for index, url in enumerate(urls):
        message(f"Processing URL: {url}")
        message(f"Index: {index + 1} / {total_urls}")
        crawler(job_base, url)

    delete_file(job_base.control_control_update_old_products_metadata)
    create_file_if_not_exists(job_base.control_control_update_old_products_metadata, "")


def check_if_job_is_ready(job_base: JobBase) -> None:
    """
    Performs a status job update by crawling product URLs with specific configurations.

    Args:
        job_base (JobBase): JobBase object containing configuration and state.

    Returns:
        None
    """
    message("performing status job update")
    # prepare page config
    job_base.page.html_scroll_page = False
    
    # prepare job config
    job_base.update_all_products = True
    job_base.check_if_job_is_ready = True
    
    update_all_products(job_base)


def create_products_metadata_if_not_exist(job_base: JobBase) -> None:
    """
    Creates metadata pages for products if they do not already exist.

    Args:
        job_base (JobBase): Page object containing configuration and state.

    Returns:
        None
    """
    message("Creating metadata pages if they do not exist")
    df_products_extract_csl: pd.DataFrame = read_df(job_base.extract_csl, dtype={'ref': str})

    products_path: str = os.path.join(job_base.data_path, "products")
    all_pages: List[str] = list_directory(products_path)
    refs: List[str] = [f"{ref}.txt" for ref in df_products_extract_csl['ref'].values]
    pages_to_create: List[str] = [ref.replace(".txt", "") for ref in refs if ref not in all_pages]

    df_products_extract_csl = df_products_extract_csl[df_products_extract_csl["ref"].isin(pages_to_create)]

    message(f"Pages to create: {pages_to_create}")

    create_directory_if_not_exists(products_path)

    urls: List[str] = df_products_extract_csl['product_url'].values.tolist()
    total_urls: int = len(urls)
    for index, url in enumerate(urls):
        message(f"Processing URL: {url}")
        message(f"Index: {index + 1} / {total_urls}")
        crawler(job_base, url)


def checkpoint_extract_data(control_file: str) -> bool:
    """
    Checks if the control file has been modified within the last 12 hours and if the environment flag is active.

    Args:
        control_file (str): Path to the control file.

    Returns:
        bool: False if the checkpoint is active and file modified within 12 hours, True otherwise.
    """
    message(f"checkpoint")
    file_modified: bool = file_modified_within_x_hours(control_file, 12)
    if file_modified:
        message(f"checkpoint_extract_data active - {control_file}")
        exit(1)