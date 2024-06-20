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
        items_container =  soup.find_all('li', class_='span3')
        items = [item for item in items_container if ((not item.has_attr('aria-hidden') or 
                                                        item['aria-hidden'] != 'true') & 
                                                        (item.find('strong', class_='preco-promocional') is not None))]
        return items

    def get_product_url(self, soup):
        product_link_element = soup.find('a', class_='produto-sobrepor')
        product_link =  product_link_element['href'] if product_link_element else None
        return product_link

    def get_title(self, soup):
        title_element = soup.find('a', class_='nome-produto')
        title = title_element.get_text().strip() if title_element else None
        return title

    def get_price(self, soup):
        price_element = soup.find('strong', class_='preco-promocional')
        price = price_element.get_text().strip() if price_element else None
        return price

    def get_image_url(self, soup):
        image_element = soup.find('img', class_='imagem-principal')
        link_imagem = image_element['src'] if image_element else None
        return link_imagem

    def get_item_elements(self, soup):
        product_link = self.get_product_url(soup)
        title = self.get_title(soup)
        price = self.get_price(soup)
        link_imagem = self.get_image_url(soup)

        return product_link, title, price, link_imagem

def extract(conf):
    run_page_mapper(conf, Job)