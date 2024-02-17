from shared.page_mapper import run as run_page_mapper

class Job():
    def __init__(self, conf) -> None:
        self.conf = conf
        conf["index"] = None

    def get_url(self, url):
        return url
    
    def reset_index(self):
        self.conf["index"] = None

    def get_items(self, soup):
        items = soup.find_all('div', class_='product-grid-item')
        return items

    def get_product_url(self, soup):
        product_link_element = soup.find('a', class_='product__media__holder')
        product_link = "https://www.boldsnacks.com.br" + product_link_element['href'] if product_link_element else None
        return product_link

    def get_title(self, soup):
        title_element = soup.find('a', class_='product-grid-item__title')
        title = title_element.get_text().strip() if title_element else None
        return title

    def get_price(self, soup):
        price_element = soup.find('a', class_='product-grid-item__price price')
        if price_element:
            price_span = price_element.find('span', class_='product-grid-item__price__new')
            if price_span:
                return price_span.get_text().strip()
            else:
                return price_element.get_text().strip()

    def get_image_url(self, soup):
        image_container = soup.find('picture')
        link_imagem = None
        if image_container:
            image_element = image_container.find('source')
            link_imagem = image_element['srcset'].split(" ")[3] if image_element else None
            link_imagem = ("https:" + link_imagem if link_imagem[:2] == "//" else link_imagem)
        return link_imagem

    def get_elements_seed(self, soup):
        product_link =self. get_product_url(soup)
        title = self.get_title(soup)
        price = self.get_price(soup)
        link_imagem = self.get_image_url(soup)

        return product_link, title, price, link_imagem

def extract(conf):
    run_page_mapper(conf, Job)