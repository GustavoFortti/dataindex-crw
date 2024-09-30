import importlib

class Page():
    def __init__(self, conf) -> None:
        self.conf = conf
        
        self.conf["index"] = None
        page_type = self.conf["page_type"]
        country = self.conf["country"]
        page_name = self.conf["page_name"]
        
        page_elements_str = f"src.jobs.slave_page.pages.{country}.{page_name}.page_elements"
        self.page_elements = importlib.import_module(page_elements_str)
        page_url_str = f"src.jobs.slave_page.pages.{country}.{page_name}.page_url"
        self.page_url = importlib.import_module(page_url_str)
        
    def get_url(self, url):
        return self.page_url.get_url(self.conf, url)
    
    def reset_index(self):
        self.conf["index"] = None
        
    def get_items(self, soup):
        return self.page_elements.get_items(self.conf, soup)
    
    def get_element(self, el_name, get_function, soup):
        try:
            el = get_function(self.conf, soup)
            return el
        except Exception as e:
            raise ValueError(f"Error obtaining {el_name}: {e}")

    def get_item_elements(self, soup):
        product_url = self.get_element(
            "product_url",
            self.page_elements.get_product_url,
            soup
        )

        title = self.get_element(
            "title",
            self.page_elements.get_title,
            soup
        )

        price = self.get_element(
            "price",
            self.page_elements.get_price,
            soup
        )

        image_url = self.get_element(
            "image_url",
            self.page_elements.get_image_url,
            soup
        )

        return product_url, title, price, image_url

    def check_element(self, el, el_name) -> None:
        if not isinstance(el, str):
            raise ValueError(f"Invalid type detected at el_name {el_name}: {el} is not a string.")
            