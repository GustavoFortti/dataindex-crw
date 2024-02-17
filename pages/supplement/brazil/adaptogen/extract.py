from shared.page_mapper import run as run_page_mapper

class Job():
    def __init__(self, conf) -> None:
        self.conf = conf
        conf["index"] = None

    def get_url(self, url):
        if (not self.conf["index"]):
            self.conf["index"] = 1
            return url + str(1)
        self.conf["index"] += 1
        return url + str(self.conf["index"])

    def reset_index(self):
        self.conf["index"] = None

    def get_items(self, soup):
        items = soup.find_all('li', class_='product-type-simple')
        return items

    def get_product_url(self, soup):
        product_link_element = soup.find('a')
        return product_link_element['href'] if product_link_element else None

    def get_title(self, soup):
        title_element = soup.find('h2', class_='woocommerce-loop-product__title')
        return title_element.get_text().strip() if title_element else None
    
    def get_price(self, soup):
        price_container = soup.find(class_="a_vista")
        if (price_container):
            price_element = price_container.find('p')
            price = price_element.contents[0].strip()
        return price

    def get_image_url(self, soup):
        image_element = soup.find('img', class_='entered lazyloaded')
        return image_element['src'] if image_element else None

    def get_elements_seed(self, soup):
        product_link =self. get_product_url(soup)
        title = self.get_title(soup)
        price = self.get_price(soup)
        link_imagem = self.get_image_url(soup)

        return product_link, title, price, link_imagem

def extract(conf):
    run_page_mapper(conf, Job)