import time
from typing import Any, Optional, Tuple, Dict

import pandas as pd
from src.lib.utils.log import message
import src.lib.extract.selenium_service as se
from src.lib.utils.data_quality import status_tag
from src.lib.utils.dataframe import create_or_read_df
from src.lib.utils.text_functions import clean_string_break_line, generate_hash
from src.lib.utils.file_system import read_file, save_file


def crawler(page: Dict, url: str) -> None:
    """
    Initiates the crawling process for a given page and URL.

    Args:
        page (Dict): The page object containing configuration and state.
        url (str): The URL to crawl.

    Returns:
        None
    """
    message("Executing crawler")
    if not is_driver_initialized(page):
        initialize_driver(page)
    load_page(page, url)


def is_driver_initialized(page: Dict) -> bool:
    """
    Checks if the Selenium driver is initialized in the page configuration.

    Args:
        page (Dict): The page object containing configuration and state.

    Returns:
        bool: True if driver is initialized, False otherwise.
    """
    driver_initialized: bool = "driver" in page.conf and bool(page.conf["driver"])
    if not driver_initialized:
        message("Driver not initialized.")
    return driver_initialized


def initialize_driver(page: Dict) -> None:
    """
    Initializes the Selenium driver and updates the page configuration.

    Args:
        page (Dict): The page object containing configuration and state.

    Returns:
        None
    """
    message("Initializing Selenium")
    page.conf["driver"] = se.initialize_selenium(page.conf)


def load_page(page: Dict, url: str) -> None:
    """
    Loads the specified URL using the configured Selenium driver and performs necessary updates.

    Args:
        page (Dict): The page object containing configuration and state.
        url (str): The URL to load.

    Returns:
        None
    """
    message("Executing load_page")
    driver: Any = page.conf["driver"]

    if page.conf.get('products_update', False):
        handle_products_update(page, driver, url)

    if page.conf.get('products_metadata_update', False):
        handle_products_metadata_update(page, driver, url)


def handle_products_update(page: Dict, driver: Any, url: str) -> None:
    """
    Handles the products update process, including loading the URL, dynamic scrolling,
    and data extraction.

    Args:
        page (Dict): The page object containing configuration and state.
        driver (Any): The Selenium driver instance.
        url (str): The URL to load.

    Returns:
        None
    """
    message("PRODUCTS_UPDATE")
    element_selector: Optional[str] = None
    se.load_url(driver, url, element_selector)

    dynamic_scroll_config: Dict[str, Any] = page.conf.get('dynamic_scroll', {})
    apply_dynamic_scroll(page, driver, dynamic_scroll_config)

    if page.conf.get("status_job", False):
        perform_additional_scroll(page, driver)

    soup, _ = se.get_page_source(driver)
    page.conf["soup"] = soup
    extract_data(page, soup)


def apply_dynamic_scroll(page: Dict, driver: Any, config: Dict[str, Any]) -> None:
    """
    Applies dynamic scrolling based on the provided configuration.

    Args:
        page (Dict): The page object containing configuration and state.
        driver (Any): The Selenium driver instance.
        config (Dict[str, Any]): Configuration parameters for dynamic scrolling.

    Returns:
        None
    """
    time_sleep: float = config.get('time_sleep', 1.0)
    scroll_step: int = config.get('scroll_step', 500)
    percentage: float = config.get('percentage', 0.5)
    return_percentage: float = config.get('return_percentage', 0.1)
    max_return: int = config.get('max_return', 100)
    max_attempts: int = config.get('max_attempts', 2)

    start_time_sleep: float = config.get('start_time_sleep', 0) + 2
    message(f"{start_time_sleep} seconds")
    time.sleep(start_time_sleep)

    if page.conf.get('scroll_page', False):
        se.dynamic_scroll(
            driver=driver,
            time_sleep=time_sleep,
            scroll_step=scroll_step,
            percentage=percentage,
            return_percentage=return_percentage,
            max_return=max_return,
            max_attempts=max_attempts
        )


def perform_additional_scroll(page: Dict, driver: Any) -> None:
    """
    Performs an additional dynamic scroll with predefined parameters.

    Args:
        page (Dict): The page object containing configuration and state.
        driver (Any): The Selenium driver instance.

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


def handle_products_metadata_update(page: Dict, driver: Any, url: str) -> None:
    """
    Handles the products metadata update process, including loading the URL,
    dynamic scrolling, and saving the page source.

    Args:
        page (Dict): The page object containing configuration and state.
        driver (Any): The Selenium driver instance.
        url (str): The URL to load.

    Returns:
        None
    """
    message("PRODUCTS_METADATA_UPDATE")
    ref: str = generate_hash(url)
    data_path: str = page.conf.get('data_path', '')
    file_name: str = f"{data_path}/products/{ref}.txt"

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


def extract_data(page: Dict, soup: Any) -> None:
    """
    Extracts product data from the provided soup object and updates the DataFrame.

    Args:
        page (Dict): The page object containing configuration and state.
        soup (Any): The BeautifulSoup object containing the page's HTML content.

    Returns:
        None
    """
    message("Executing extract_data")
    path_products_extract_temp: str = page.conf.get('path_products_extract_temp', '')
    df_products_temp: pd.DataFrame = create_or_read_df(
        path_products_extract_temp, page.conf['df_products'].columns
    )
    size_products_temp: int = len(df_products_temp)
    items: Any = page.get_items(soup)
    size_items: int = len(items)
    message(f"size_items = {size_items}")
    page.conf['size_items'] = size_items

    if size_items == 0:
        handle_no_items_found(page)
        return

    message("Valid size_items for extraction")
    process_items(page, items, df_products_temp)
    finalize_extraction(page, df_products_temp, size_products_temp)


def handle_no_items_found(page: Dict) -> None:
    """
    Handles the scenario when no items are found on the page.

    Args:
        page (Dict): The page object containing configuration and state.

    Returns:
        None
    """
    index: int = page.conf.get("index", 0)
    message(f"size_items: 0 - No products found on page number {index}")
    message(page.get_items(None))  # Assuming get_items can handle None

    if index == 1:
        message(
            "ERROR size_items: 0 - No products found on the first page, "
            "validation of page extraction is necessary."
        )
        message("Terminating program with error.")
        exit(1)


def process_items(page: Dict, items: Any, df_products_temp: pd.DataFrame) -> None:
    """
    Processes each item, extracts relevant data, and updates the temporary DataFrame.

    Args:
        page (Dict): The page object containing configuration and state.
        items (Any): The list of items to process.
        df_products_temp (pd.DataFrame): The temporary DataFrame to update.

    Returns:
        None
    """
    count_size_items: int = 0
    for item in items:
        message(f"INDEX: {abs(count_size_items)} item")
        data: Dict[str, Any] = extract_item_data(page, item)
        handle_category(page, data)
        message(data)

        if page.conf.get("status_job", False):
            status_tag(page, data)

        temp_df: pd.DataFrame = pd.DataFrame([data])
        df_products_temp = pd.concat([df_products_temp, temp_df], ignore_index=True)
        df_products_temp.to_csv(page.conf.get('path_products_extract_temp', ''), index=False)

        count_size_items -= 1


def extract_item_data(page: Dict, item: Any) -> Dict[str, Any]:
    """
    Extracts data from a single item.

    Args:
        page (Dict): The page object containing configuration and state.
        item (Any): The item to extract data from.

    Returns:
        Dict[str, Any]: A dictionary containing the extracted data.
    """
    product_url: str
    title: Optional[str]
    price: Optional[str]
    image_url: str
    product_url, title, price, image_url = page.get_item_elements(item)
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
        'ing_date': page.conf.get('formatted_date', '')
    }
    return data


def handle_category(page: Dict, data: Dict[str, Any]) -> None:
    """
    Handles category assignment for a product based on existing data.

    Args:
        page (Dict): The page object containing configuration and state.
        data (Dict[str, Any]): The data dictionary of the current product.

    Returns:
        None
    """
    category: Optional[str] = page.conf['seed'].get("category")
    if category:
        file_path: str = f"{page.conf.get('src_data_path', '')}/{page.conf.get('page_name', '')}/products/{data['ref']}_class.txt"
        file_content: Optional[str] = read_file(file_path)

        if file_content:
            categories: list = list(set(file_content.split(",")))
            categories.append(category)
            categories_unique: list = list(set(categories))
            categories_str: str = ",".join(categories_unique)

        save_file(categories_str, file_path)


def finalize_extraction(page: Dict, df_products_temp: pd.DataFrame, size_products_temp: int) -> None:
    """
    Finalizes the data extraction by removing duplicates and saving the DataFrame.

    Args:
        page (Dict): The page object containing configuration and state.
        df_products_temp (pd.DataFrame): The temporary DataFrame to finalize.
        size_products_temp (int): The initial size of the temporary DataFrame.

    Returns:
        None
    """
    df_products_temp = df_products_temp.drop_duplicates(subset='ref').reset_index(drop=True)

    if size_products_temp == len(df_products_temp):
        message("No change in dataframe")
        page.conf['size_items'] = 0
        return

    df_products_temp.to_csv(page.conf.get('path_products_extract_temp', ''), index=False)
    message("df_products_temp saved")