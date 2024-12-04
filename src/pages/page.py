from typing import Dict, List, Union
import importlib
from src.lib.utils.file_system import read_json
from src.lib.wordlist.wordlist import WORDLIST
from src.lib.wordlist.wordlist_flavor import WORDLIST_FLAVOR
from src.lib.wordlist.wordlist_format import WORDLIST_FORMAT


class Page():
    def __init__(
        self,
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
        
        # page config
        self.url: str = url
        self.page_production_status: bool = page_production_status
        self.brand: str = brand
        self.seeds: List[Dict[str, str]] = None
        self.seed: Dict[str, str] = None
        
        # Outros atributos
        self.scroll_page: bool = True
        self.wordlist: Dict[str, str] = WORDLIST
        self.wordlist_flavor: Dict[str, str] = WORDLIST_FLAVOR
        self.wordlist_format: Dict[str, str] = WORDLIST_FORMAT
        
        # crawler config
        self.crawler_driver_user_agent: str = crawler_driver_user_agent
        self.crawler_index: int = None
        self.crawler_n_products_in_index: int = 0
        
        # affilited config
        self.affiliate_url: str = affiliate_url
        self.affiliate_coupon_discount_percentage: float = affiliate_coupon_discount_percentage
        self.affiliate_coupon: str = affiliate_coupon

        # html config
        self.html_metadata_type: List[str] = html_metadata_type
        self.html_description_path: List[Dict[str, str]] = html_description_path
        self.html_images_list: List[Dict[str, str]] = html_images_list
        self.html_remove_first_image_from_list: bool = html_remove_first_image_from_list
        self.html_dynamic_scroll: Dict[str, Union[float, int]] = html_dynamic_scroll
        
    def get_url(self) -> str:
        generated_url, self.crawler_index = self.page_url.get_url(self.url, self.crawler_index, self.seed)
        return generated_url
    
    def reset_index(self) -> None:
        self.crawler_index = None
        
    def get_items(self, soup):
        return self.page_elements.get_items(self.conf, soup)
    
    def get_element(self, el_name, get_function, soup):
        try:
            el = get_function(self.conf, soup)
            return el
        except Exception as e:
            raise ValueError(f"Error obtaining {el_name}: {e}")

    def get_item_elements(self, soup):
        try:
            product_url = self.get_element(
                "product_url",
                self.page_elements.get_product_url,
                soup
            )
        except Exception as e:
            raise Exception(f"Erro ao extrair 'product_url': {str(e)}")

        try:
            title = self.get_element(
                "title",
                self.page_elements.get_title,
                soup
            )
        except Exception as e:
            raise Exception(f"Erro ao extrair 'title': {str(e)}")

        try:
            price = self.get_element(
                "price",
                self.page_elements.get_price,
                soup
            )
        except Exception as e:
            raise Exception(f"Erro ao extrair 'price': {str(e)}")

        try:
            image_url = self.get_element(
                "image_url",
                self.page_elements.get_image_url,
                soup
            )
        except Exception as e:
            raise Exception(f"Erro ao extrair 'image_url': {str(e)}")
            
        return product_url, title, price, image_url

    def check_element(self, el, el_name) -> None:
        if not isinstance(el, str):
            raise ValueError(f"Invalid type detected at el_name {el_name}: {el} is not a string.")
        
    def set_seeds(self, file_path) -> None:
        seeds = read_json(file_path)
        self.seeds = seeds
        
    def set_page_functions(self, path_page_elements, path_page_url) -> None:
        # self.page_elements = importlib.import_module(path_page_elements)
        self.page_url = importlib.import_module(path_page_url)