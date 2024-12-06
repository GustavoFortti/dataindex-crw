import time
from typing import Any, Dict, List, Optional

import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver.remote.webdriver import WebDriver

import src.lib.extract.selenium_service as se
from src.jobs.job_manager import JobBase
from src.lib.utils.data_quality import check_if_job_is_ready
from src.lib.utils.dataframe import create_or_read_df
from src.lib.utils.file_system import read_file, save_file
from src.lib.utils.log import message
from src.lib.utils.text_functions import clean_string_break_line, generate_hash


def crawler(job_base: JobBase, url: str) -> None:
    """
    Initiates the crawling process for a given page and URL.

    Args:
        job_base (JobBase): The page object containing configuration and state.
        url (str): The URL to crawl.

    Returns:
        None
    """
    
    message("executing crawler")
    if not bool(job_base.driver):
        job_base.driver = se.initialize_selenium(job_base)
    load_page(job_base, url)


def load_page(job_base: JobBase, url: str) -> None:
    """
    Loads the specified URL using the configured Selenium driver and performs necessary updates.

    Args:
        job_base (JobBase): The page object containing configuration and state.
        url (str): The URL to load.

    Returns:
        None
    """
    message("executing load_page")

    if job_base.update_all_products:
        handle_update_all_products(job_base, url)

    if job_base.update_all_products_metadata:
        handle_update_all_products_metadata(job_base, url)


def handle_update_all_products(job_base: JobBase, url: str) -> None:
    """
    Handles the products update process, including loading the URL, dynamic scrolling,
    and data extraction.

    Args:
        job_base (JobBase): The page object containing configuration and state.
        driver (Any): The Selenium driver instance.
        url (str): The URL to load.

    Returns:
        None
    """
    driver: WebDriver = job_base.driver
    message("update_all_products")
    se.load_url(driver, url)

    apply_dynamic_scroll(job_base)

    if job_base.check_if_job_is_ready:
        perform_additional_scroll(driver)

    soup, _ = se.get_page_source(driver)
    extract_data(job_base, soup)


def apply_dynamic_scroll(job_base: JobBase) -> None:
    """
    Applies dynamic scrolling based on the provided configuration.

    Args:
        job_base (JobBase): The page object containing configuration and state.

    Returns:
        None
    """
    time_sleep: float = job_base.page.html_dynamic_scroll["time_sleep"]
    scroll_step: int = job_base.page.html_dynamic_scroll["scroll_step"]
    percentage: float = job_base.page.html_dynamic_scroll["percentage"]
    return_percentage: float = job_base.page.html_dynamic_scroll["return_percentage"]
    max_return: int = job_base.page.html_dynamic_scroll["max_return"]
    max_attempts: int = job_base.page.html_dynamic_scroll["max_attempts"]
    start_time_sleep: float = job_base.page.html_dynamic_scroll["start_time_sleep"]
    
    message(f"{start_time_sleep} seconds")
    time.sleep(start_time_sleep)
    
    if job_base.page.html_scroll_page:
        se.dynamic_scroll(
            driver=job_base.driver,
            time_sleep=time_sleep,
            scroll_step=scroll_step,
            percentage=percentage,
            return_percentage=return_percentage,
            max_return=max_return,
            max_attempts=max_attempts
        )


def perform_additional_scroll(driver: WebDriver) -> None:
    """
    Performs an additional dynamic scroll with predefined parameters.

    Args:
        driver (WebDriver): The Selenium driver instance.

    Returns:
        None
    """
    se.dynamic_scroll(
        driver=driver,
        time_sleep=0.4,
        scroll_step=1000,
        percentage=0.5,
        return_percentage=0.1,
        max_return=100,
        max_attempts=2
    )


def handle_update_all_products_metadata(job_base: JobBase, url: str) -> None:
    """
    Handles the products metadata update process, including loading the URL,
    dynamic scrolling, and saving the page source.

    Args:
        job_base (JobBase): The page object containing configuration and state.
        driver (WebDriver): The Selenium driver instance.
        url (str): The URL to load.

    Returns:
        None
    """
    message("update_all_products_metadata")
    ref: str = generate_hash(url)
    file_name: str = f"{job_base.products_path}/{ref}.txt"
    driver: WebDriver = job_base.driver
    
    time.sleep(1)
    se.load_url(driver, url)
    
    se.dynamic_scroll(
        driver=driver,
        time_sleep=0.5,
        scroll_step=500,
        percentage=0.5,
        return_percentage=0.1,
        max_return=100,
        max_attempts=2
    )

    _, page_text = se.get_page_source(driver)
    save_page_text(file_name, page_text)


def save_page_text(file_name: str, content: str) -> None:
    """
    Saves the page text to a specified file.

    Args:
        file_name (str): The path to the file where content will be saved.
        content (str): The content to write to the file.

    Returns:
        None
    """
    try:
        with open(file_name, 'w') as file:
            file.write(content)
        message(f"File '{file_name}' created successfully.")
    except IOError as e:
        message(f"Failed to write to file '{file_name}': {e}")


def extract_data(job_base: JobBase, soup: BeautifulSoup) -> None:
    """
    Extracts product data from the provided soup object and updates the DataFrame.

    Args:
        job_base (JobBase): The job_base object containing configuration and state.
        soup (BeautifulSoup): The BeautifulSoup object containing the page's HTML content.

    Returns:
        None
    """
    message("executing extract_data")
    df_products_temp: pd.DataFrame = create_or_read_df(
        job_base.path_extract_temp, job_base.extract_dataframe_columns
    )
    
    size_products_temp: int = len(df_products_temp)
    items: List = job_base.page.get_items(soup)
    job_base.page.crawler_n_products_in_index = len(items)
    message(f"crawler_n_products_in_index = {job_base.page.crawler_n_products_in_index}")

    if job_base.page.crawler_n_products_in_index == 0:
        handle_no_items_found(job_base)
        return

    message("valid crawler_n_products_in_index for extraction")
    df_products_temp = process_items(job_base, items, df_products_temp)
    finalize_extraction(job_base, df_products_temp, size_products_temp)


def handle_no_items_found(job_base: JobBase) -> None:
    """
    Handles the scenario when no items are found on the page.

    Args:
        job_base (JobBase): The page object containing configuration and state.

    Returns:
        None
    """
    index: int = job_base.page.crawler_index
    message(f"crawler_n_products_in_index: 0 - No products found on page number {index}")

    if index == 1:
        message(
            "ERROR crawler_n_products_in_index: 0 - No products found on the first page, "
            "validation of page extraction is necessary."
        )
        message("Terminating program with error.")
        exit(1)


def process_items(job_base: JobBase, items: List, df_products_temp: pd.DataFrame) -> pd.DataFrame:
    """
    Processes each item, extracts relevant data, and updates the temporary DataFrame.

    Args:
        job_base (JobBase): The page object containing configuration and state.
        items (List): The list of items to process.
        df_products_temp (pd.DataFrame): The temporary DataFrame to update.

    Returns:
        pd.DataFrame: The updated temporary DataFrame.
    """
    df: pd.DataFrame = pd.DataFrame(columns=job_base.extract_dataframe_columns)
    for item in items:
        data: Dict[str, Optional[str]] = extract_item_data(job_base, item)
        handle_category(job_base, data)
        message(data)

        if job_base.check_if_job_is_ready:
            check_if_job_is_ready(job_base, data)

        df_aux: pd.DataFrame = pd.DataFrame([data])
        df = pd.concat([df, df_aux], ignore_index=True)
        
    df = pd.concat([df_products_temp, df], ignore_index=True)
    return df

def extract_item_data(job_base: JobBase, item: BeautifulSoup) -> Dict[str, str]:
    """
    Extracts data from a single item.

    Args:
        job_base (JobBase): The page object containing configuration and state.
        item (BeautifulSoup): The item to extract data from.

    Returns:
        Dict[str, str]: A dictionary containing the extracted data.
    """
    product_url: Optional[str]
    title: Optional[str]
    price: Optional[str]
    image_url: Optional[str]
    product_url, title, price, image_url = job_base.page.get_item_elements(item)
    ref: str = generate_hash(product_url)
    message(f"Generated ref - {ref}")

    if price:
        price = clean_string_break_line(price)
    if title:
        title = clean_string_break_line(title)

    data: Dict[str, Any] = {
        'ref': ref,
        'product_url': product_url,
        'title': title,
        'price': price,
        'image_url': image_url,
        'ing_date': job_base.date_today
    }
    return data


def handle_category(job_base: JobBase, data: Dict[str, Any]) -> None:
    """
    Handles category assignment for a product based on existing data.

    Args:
        job_base (JobBase): The job_base object containing configuration and state.
        data (Dict[str, Any]): The data dictionary of the current product.

    Returns:
        None
    """
    category: Optional[str] = job_base.page.seed.get("category")
    if category:
        file_path: str = f"{job_base.products_path}/{data['ref']}_class.txt"
        file_content: Optional[str] = read_file(file_path)

        categories: list = []
        if file_content:
            categories: list = list(set(file_content.split(",")))
            
        categories.append(category)
        categories_unique: list = list(set(categories))
        categories_str: str = ",".join(categories_unique)

        save_file(categories_str, file_path)


def finalize_extraction(job_base: JobBase, df_products_temp: pd.DataFrame, size_products_temp: int) -> None:
    """
    Finalizes the data extraction by removing duplicates and saving the DataFrame.

    Args:
        job_base (JobBase): The page object containing configuration and state.
        df_products_temp (pd.DataFrame): The temporary DataFrame to finalize.
        size_products_temp (int): The initial size of the temporary DataFrame.

    Returns:
        None
    """
    df_products_temp = df_products_temp.drop_duplicates(subset='ref').reset_index(drop=True)

    if size_products_temp == len(df_products_temp):
        message("No change in dataframe")
        job_base.page.crawler_n_products_in_index = 0
        return

    df_products_temp.to_csv(job_base.path_extract_temp, index=False)
    message("df_products_temp saved")