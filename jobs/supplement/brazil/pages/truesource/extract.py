from lib.page_mapper import run as run_page_mapper

class Job():
    def __init__(self, conf) -> None:
        self.conf = conf
        conf["index"] = None
        
    def get_url(self, url):
        return url
    
    def reset_index(self):
        self.conf["index"] = None

    def get_items(self, soup):
        items = soup.find_all('div', class_='gap-x-3.5 gap-y-6 grid grid-cols-2 lg:grid-cols-4 items-center')
        if (self.conf["status_job"]):
            self.validate_strings(items)
        return items

    def get_product_url(self, item):
        product_link_element = item.find('a', class_='flex items-center justify-center relative h-full bg-ice')
        product_url = self.conf["url"] + product_link_element['href'] if product_link_element else None
        return product_url

    def get_title(self, item):
        title_element = item.find('h3', class_='text-dark text-sm text-ellipsis font-bold line-clamp-2 h-10')
        title = title_element.get_text(strip=True) if title_element else None
        return title

    def get_price(self, item):
        price_element = item.find('div', class_='text-dark text-xs lg:text-sm')
        price = price_element.get_text(strip=True) if price_element else None
        return price

    def get_image_url(self, item):
        image_element = item.find('img')
        image_url = image_element['src'] if image_element else None
        return image_url

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