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
        items = soup.find_all('div', class_='product-card')
        return items

    def get_product_url(self, soup):
        product_element = soup.find('figure', class_='area-photo').find('a', href=True)
        product_link = product_element['href'] if product_element else None
        return product_link


    def get_title(self, soup):
        title_element = soup.find('div', class_='area-text').find('h3')
        title = title_element.get_text().strip() if title_element else None
        return title

    def get_price(self, soup):
        # Tenta encontrar o elemento 'div' com a classe 'off-sale'
        off_sale_div = soup.find('div', class_='off-sale')
        
        # Se o elemento for encontrado, procura por 'p' com a classe 'price-current'
        if off_sale_div:
            price_element = off_sale_div.find('p', class_='price-current')
            
            # Se o elemento de preço for encontrado, retorna o texto
            if price_element:
                price = price_element.get_text().strip()
                return price

    def get_image_url(self, soup):
        image_element = soup.find('figure', class_='area-photo').find('img', src=True)
        image_link = image_element['src'] if image_element else None
        return image_link

    def get_elements_seed(self, soup):
        product_link = self. get_product_url(soup)
        title = self.get_title(soup)
        price = self.get_price(soup)
        link_imagem = self.get_image_url(soup)

        return product_link, title, price, link_imagem

def extract(conf):
    run_page_mapper(conf, Job)