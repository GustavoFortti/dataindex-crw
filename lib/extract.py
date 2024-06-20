import importlib
from lib.page_mapper import run as run_page_mapper

class Job():
    def __init__(self, conf) -> None:
        self.conf = conf
        
        self.conf["index"] = None
        page_type = self.conf["page_type"]
        country = self.conf["country"]
        page_name = self.conf["page_name"]
        
        page_elements_str = f"jobs.{page_type}.{country}.pages.{page_name}.page_elements"
        self.page_elements = importlib.import_module(page_elements_str)
        page_url_str = f"jobs.{page_type}.{country}.pages.{page_name}.page_url"
        self.page_url = importlib.import_module(page_url_str)
        
    def get_url(self, url):
        return self.page_url.get_url(self.conf, url)
    
    def reset_index(self):
        self.conf["index"] = None
        
    def get_items(self, soup):
        return self.page_elements.get_items(self.conf, soup)

    def get_product_url(self, soup):
        return self.page_elements.get_product_url(self.conf, soup)

    def get_title(self, soup):
        return self.page_elements.get_title(self.conf, soup)

    def get_price(self, soup):
        return self.page_elements.get_price(self.conf, soup)

    def get_image_url(self, soup):
        return self.page_elements.get_image_url(self.conf, soup)

    def get_item_elements(self, soup):
        product_link = self.get_product_url(soup)
        title = self.get_title(soup)
        price = self.get_price(soup)
        link_imagem = self.get_image_url(soup)
        
        if (self.conf["status_job"]):
            self.validate_strings(product_link, title, price, link_imagem)

        return product_link, title, price, link_imagem

    def validate_strings(self, *args) -> None:
        for index, arg in enumerate(args):
            if not isinstance(arg, str):
                raise ValueError(f"Invalid type detected at index {index}: {arg} is not a string.")

            
def extract(conf):
    run_page_mapper(conf, Job)