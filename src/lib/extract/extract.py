import os
from datetime import date
from typing import Any, Dict, List, Optional

import pandas as pd

from src.lib.extract.crawler import crawler
from src.lib.extract.page_elements import Page
from src.lib.utils.data_quality import is_price
from src.lib.utils.dataframe import (
    create_or_read_df,
    read_df
)
from src.lib.utils.file_system import (
    create_directory_if_not_exists,
    create_file_if_not_exists,
    DATE_FORMAT,
    delete_directory_and_contents,
    delete_file,
    file_modified_within_x_hours,
    get_old_files_by_percent,
    list_directory,
    read_json
)
from src.lib.utils.log import message
from src.lib.utils.text_functions import find_in_text_with_wordlist
from src.lib.wordlist.wordlist import BLACK_LIST


def extract(config: Dict[str, Any]) -> None:
    """
    Initiates the extraction process based on the provided configuration.

    Args:
        config (Dict[str, Any]): Configuration dictionary containing extraction parameters.

    Returns:
        None
    """
    message("STARTING EXTRACTION PROCESS")
    page: Page = Page(config)

    exec_flag: str = config.get('exec_flag', '').lower()

    if exec_flag == "new_page":
        create_new_page(config, page)
    elif exec_flag == "products_update" and checkpoint_extract_data(page.conf["control_products_update"]):
        perform_products_update(page, config)
    elif exec_flag == "products_metadata_update" and checkpoint_extract_data(page.conf["control_products_metadata_update"]):
        perform_products_metadata_update(page, config)
    elif exec_flag == "products_metadata_update_old_pages" and checkpoint_extract_data(page.conf["control_products_metadata_update_old_pages"]):
        products_metadata_update_old_pages_by_ref(page, config)
    elif exec_flag == "products_metadata_create_pages_if_not_exist":
        perform_products_metadata_create_pages_if_not_exist(page, config)
    elif exec_flag == "status_job" and checkpoint_extract_data(page.conf["control_products_update"]):
        perform_status_job_update(page, config)
    else:
        message(f"Unknown exec_flag: {exec_flag}. No action taken.")


def create_new_page(config: Dict[str, Any], page: Page) -> None:
    """
    Initializes a new page by resetting relevant configurations and performing updates.

    Args:
        config (Dict[str, Any]): Configuration dictionary.
        page (Page): Page object containing configuration and state.

    Returns:
        None
    """
    message("Initializing new page")
    data_path_pattern: str = f"{config['data_path']}/*"
    delete_directory_and_contents(data_path_pattern)

    config["products_update"] = True
    perform_products_update(page, config)

    config["products_update"] = False
    config["products_metadata_update"] = True
    page = Page(config)
    perform_products_metadata_update(page, config)


def update_all_products(page: Page, config: Dict[str, Any]) -> None:
    """
    Updates the products by crawling through seeds and extracting relevant data.

    Args:
        page (Page): Page object containing configuration and state.
        config (Dict[str, Any]): Configuration dictionary.

    Returns:
        None
    """
    seed_path: str = os.path.join(page.conf['seed_path'], "seed.json")
    seeds: List[Dict[str, Any]] = read_json(seed_path)

    delete_file(page.conf['path_products_extract_temp'])

    columns: List[str] = ["ref", "title", "price", "image_url", "product_url", "ing_date"]
    df_products: pd.DataFrame = create_or_read_df(page.conf['path_products_extract_csl'], columns)

    current_date: date = date.today()
    page.conf['formatted_date'] = current_date.strftime(DATE_FORMAT)
    page.conf['df_products'] = df_products

    page.conf["size_items"] = 0
    for index, seed in enumerate(seeds):
        message(f"Processing seed: {seed}")
        message(f"Seed index: {index + 1} / {len(seeds)}")
        page.conf["seed"] = seed

        iteration_count: int = 0  # Initialize iteration counter
        max_iterations: int = 100  # Define a maximum number of iterations

        while True:
            url: Optional[str] = page.get_url(seed)
            current_index: int = page.conf.get("index", 0)

            message(f"Current URL index: {current_index}")
            message(f"URL: {url}")

            if url is None:
                message("No more URLs to process for this seed.")
                break

            crawler(page, url)

            # Safeguard to prevent infinite loop
            iteration_count += 1
            if iteration_count >= max_iterations:
                message(f"Reached maximum iterations ({max_iterations}) for seed index {index + 1}. Breaking the loop.")
                break

            # Check if size_items has been updated correctly
            size_items: int = page.conf.get("size_items", -1)
            message(f"Size items after crawling: {size_items}")

            if size_items == 0 or not current_index:
                message(f"Size items = {size_items}")
                message(f"Index = {current_index}")
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


def update_all_products_metadata(page: Page, config: Dict[str, Any]) -> None:
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


def update_old_product_metadata(page: Page, config: Dict[str, Any]) -> None:
    """
    Updates metadata for old product pages based on a percentage criterion.

    Args:
        page (Page): Page object containing configuration and state.
        config (Dict[str, Any]): Configuration dictionary.

    Returns:
        None
    """
    message("Updating metadata for old product pages")
    products_extract_csl: str = os.path.join(config['data_path'], "products_extract_csl.csv")
    page.conf['path_products_extract_csl'] = products_extract_csl
    df_products_extract_csl: pd.DataFrame = read_df(products_extract_csl, dtype={'ref': str})

    products_path: str = os.path.join(config['data_path'], "products")
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
        crawler(page, url)

    delete_file(page.conf["control_products_metadata_update_old_pages"])
    create_file_if_not_exists(page.conf["control_products_metadata_update_old_pages"], "")


def create_products_metadata_if_not_exist(page: Page, config: Dict[str, Any]) -> None:
    """
    Creates metadata pages for products if they do not already exist.

    Args:
        page (Page): Page object containing configuration and state.
        config (Dict[str, Any]): Configuration dictionary.

    Returns:
        None
    """
    message("Creating metadata pages if they do not exist")
    products_extract_csl: str = os.path.join(config['data_path'], "products_extract_csl.csv")
    page.conf['path_products_extract_csl'] = products_extract_csl
    df_products_extract_csl: pd.DataFrame = read_df(products_extract_csl, dtype={'ref': str})

    products_path: str = os.path.join(config['data_path'], "products")
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
        crawler(page, url)


def check_if_job_is_ready(page: Page, config: Dict[str, Any]) -> None:
    """
    Performs a status job update by crawling product URLs with specific configurations.

    Args:
        page (Page): Page object containing configuration and state.
        config (Dict[str, Any]): Configuration dictionary.

    Returns:
        None
    """
    message("Performing status job update")
    config["scroll_page"] = False
    config["products_update"] = True
    config['status_job'] = True
    page = Page(config)
    update_all_products(page, config)


def checkpoint_extract_data(control_file: str) -> bool:
    """
    Checks if the control file has been modified within the last 12 hours and if the environment flag is active.

    Args:
        control_file (str): Path to the control file.

    Returns:
        bool: False if the checkpoint is active and file modified within 12 hours, True otherwise.
    """
    file_modified: bool = file_modified_within_x_hours(control_file, 12)
    message(f"CHECKPOINT_EXTRACT_DATA FLAG - {control_file}")
    checkpoint_flag: str = os.getenv('CHECKPOINT_EXTRACT_DATA', "false").lower()
    if file_modified and checkpoint_flag == "true":
        message(f"CHECKPOINT_EXTRACT_DATA ACTIVE - {control_file}")
        return False
    return True


def products_metadata_update_by_ref(config: Dict[str, Any], PageClass: Any, url: str) -> None:
    """
    Updates the metadata of a product page by its reference if the page has errors in tags.

    Args:
        config (Dict[str, Any]): Configuration dictionary.
        PageClass (Any): Page class to instantiate the Page object.
        url (str): URL of the product page to update.

    Returns:
        None
    """
    message("Updating old page by reference if page has errors in tags")
    config["scroll_page"] = True
    config["status_job"] = False
    config["products_metadata_update"] = True
    config["products_update"] = False

    page: Page = PageClass(config)
    message(f"Processing URL: {url}")
    crawler(page, url)
