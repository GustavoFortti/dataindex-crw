from typing import Any, Dict, List, Optional, Tuple, Union
import importlib

from bs4 import BeautifulSoup
from src.lib.utils.file_system import read_json
from src.lib.wordlist.wordlist import WORDLIST
from src.lib.wordlist.wordlist_flavor import WORDLIST_FLAVOR
from src.lib.wordlist.wordlist_format import WORDLIST_FORMAT


class Page:
    """
    Represents a web page with various configurations and methods for processing page content.

    Attributes:
        url (str): The base URL of the page.
        brand (str): The brand associated with the page.
        page_production_status (bool): Indicates if the page is in production.
        seeds (Optional[List[Dict[str, str]]]): List of seed data.
        seed (Optional[Dict[str, str]]): Current seed data.
        html_scroll_page (bool): Flag indicating if the page requires scrolling.
        wordlist (Dict[str, str]): Wordlist for processing.
        wordlist_flavor (Dict[str, str]): Flavor wordlist.
        wordlist_format (Dict[str, str]): Format wordlist.
        crawler_driver_user_agent (str): User agent for the crawler driver.
        crawler_index (Optional[int]): Index for crawler pagination.
        crawler_n_products_in_index (int): Number of products in the current index.
        affiliate_url (str): Affiliate URL.
        affiliate_coupon_discount_percentage (float): Affiliate coupon discount percentage.
        affiliate_coupon (str): Affiliate coupon code.
        html_metadata_type (List[str]): Types of HTML metadata.
        html_description_path (List[Dict[str, str]]): Paths to HTML descriptions.
        html_images_list (List[Dict[str, str]]): List of HTML image paths.
        html_remove_first_image_from_list (bool): Flag to remove the first image from the list.
        html_dynamic_scroll (Dict[str, Union[float, int]]): Configuration for dynamic scrolling.
        page_url (Any): Module handling URL generation.
        page_elements (Any): Module handling element extraction.
    """

    def __init__(
        self,
        name: str,
        url: str,
        brand: str,
        page_production_status: bool,
        crawler_driver_user_agent: str,
        affiliate_url: str,
        affiliate_coupon_discount_percentage: float,
        affiliate_coupon: str,
        html_metadata_type: List[str],
        html_description_path: List[Dict[str, str]],
        html_images_list: List[Dict[str, str]],
        html_remove_first_image_from_list: bool,
        html_dynamic_scroll: Dict[str, Union[float, int]],
    ) -> None:
        """
        Initializes the Page object with the provided configuration.

        Args:
            url (str): The base URL of the page.
            brand (str): The brand associated with the page.
            page_production_status (bool): Indicates if the page is in production.
            crawler_driver_user_agent (str): User agent for the crawler driver.
            affiliate_url (str): Affiliate URL.
            affiliate_coupon_discount_percentage (float): Affiliate coupon discount percentage.
            affiliate_coupon (str): Affiliate coupon code.
            html_metadata_type (List[str]): Types of HTML metadata.
            html_description_path (List[Dict[str, str]]): Paths to HTML descriptions.
            html_images_list (List[Dict[str, str]]): List of HTML image paths.
            html_remove_first_image_from_list (bool): Flag to remove the first image from the list.
            html_dynamic_scroll (Dict[str, Union[float, int]]): Configuration for dynamic scrolling.
        """
        # Page configuration
        self.name: str = name
        self.url: str = url
        self.brand: str = brand
        self.page_production_status: bool = page_production_status
        self.seeds: Optional[List[Dict[str, str]]] = None
        self.seed: Optional[Dict[str, str]] = None

        # Wordlist configuration
        self.wordlist: Dict[str, str] = WORDLIST
        self.wordlist_flavor: Dict[str, str] = WORDLIST_FLAVOR
        self.wordlist_format: Dict[str, str] = WORDLIST_FORMAT

        # Crawler configuration
        self.crawler_driver_user_agent: str = crawler_driver_user_agent
        self.crawler_index: Optional[int] = None
        self.crawler_n_products_in_index: int = 0

        # Affiliate configuration
        self.affiliate_url: str = affiliate_url
        self.affiliate_coupon_discount_percentage: float = affiliate_coupon_discount_percentage
        self.affiliate_coupon: str = affiliate_coupon

        # HTML configuration
        self.html_scroll_page: bool = True
        self.html_metadata_type: List[str] = html_metadata_type
        self.html_description_path: List[Dict[str, str]] = html_description_path
        self.html_images_list: List[Dict[str, str]] = html_images_list
        self.html_remove_first_image_from_list: bool = html_remove_first_image_from_list
        self.html_dynamic_scroll: Dict[str, Union[float, int]] = html_dynamic_scroll

        # Placeholder for page functions
        self.page_url: Optional[Any] = None
        self.page_elements: Optional[Any] = None

    def get_url(self) -> str:
        """
        Generates the next URL to crawl based on the current index and seed.

        Returns:
            str: The generated URL.
        """
        if not self.page_url:
            raise ValueError("Page URL module is not set. Call 'set_page_functions' first.")

        generated_url: str
        generated_url, self.crawler_index = self.page_url.get_url(
            self.url, self.crawler_index, self.seed
        )
        return generated_url

    def reset_index(self) -> None:
        """
        Resets the crawler index to None.
        """
        self.crawler_index = None

    def get_items(self, soup: BeautifulSoup) -> Any:
        """
        Retrieves items from the page content using the page elements module.

        Args:
            soup (BeautifulSoup): Parsed HTML content.

        Returns:
            Any: Items extracted from the page.

        Raises:
            ValueError: If the page elements module is not set.
        """
        if not self.page_elements:
            raise ValueError("Page elements module is not set. Call 'set_page_functions' first.")

        return self.page_elements.get_items(soup)

    def get_item_elements(self, soup: BeautifulSoup) -> Tuple[str, str, str, str]:
        """
        Retrieves the product URL, title, price, and image URL from the page content.

        Args:
            soup (BeautifulSoup): Parsed HTML content.

        Returns:
            Tuple[str, str, str, str]: A tuple containing product_url, title, price, and image_url.

        Raises:
            Exception: If any of the elements cannot be extracted.
        """
        try:
            product_url: str = self.page_elements.get_product_url(soup, self.url)
        except Exception as e:
            raise Exception(f"Error extracting 'product_url': {e}")

        try:
            title: str = self.page_elements.get_title(soup)
        except Exception as e:
            raise Exception(f"Error extracting 'title': {e}")

        try:
            price: str = self.page_elements.get_price(soup)
        except Exception as e:
            raise Exception(f"Error extracting 'price': {e}")

        try:
            image_url: str = self.page_elements.get_image_url(soup)
        except Exception as e:
            raise Exception(f"Error extracting 'image_url': {e}")

        return product_url, title, price, image_url

    def check_element(self, element: Any, element_name: str) -> None:
        """
        Checks if the provided element is a string.

        Args:
            element (Any): The element to check.
            element_name (str): The name of the element.

        Raises:
            ValueError: If the element is not a string.
        """
        if not isinstance(element, str):
            raise ValueError(
                f"Invalid type detected for element '{element_name}': Expected string, got {type(element).__name__}."
            )

    def set_seeds(self, file_path: str) -> None:
        """
        Reads seed data from a JSON file and sets it to the seeds attribute.

        Args:
            file_path (str): Path to the JSON file containing seed data.
        """
        seeds: List[Dict[str, str]] = read_json(file_path)
        self.seeds = seeds

    def set_page_functions(self, path_page_elements: str, path_page_url: str) -> None:
        """
        Imports and sets the page elements and page URL modules.

        Args:
            path_page_elements (str): Module path for page elements.
            path_page_url (str): Module path for page URL.
        """
        self.page_elements = importlib.import_module(path_page_elements)
        self.page_url = importlib.import_module(path_page_url)
