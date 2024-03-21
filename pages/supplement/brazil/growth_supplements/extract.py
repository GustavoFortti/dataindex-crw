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
        items = soup.find_all('div', class_='vitrine-prod')
        return items

    def get_product_url(self, soup):
        product_link_element = soup.find('a', class_='cardprod-nomeProduto')
        return product_link_element['href'] if product_link_element else None

    def get_title(self, soup):
        title_element = soup.find('h3', class_='cardprod-nomeProduto-t1')
        return title_element.get_text().strip() if title_element else None

    def get_price(self, soup):
        price_element = soup.find('span', class_='cardprod-valor')
        if price_element:
            full_text = price_element.get_text().strip()
            price = full_text.split('\n')[0].strip()
            return price
        else:
            return None

    def get_image_url(self, soup):
        card_topo = soup.find('div', class_='cardProd-topo')
        if card_topo:
            image_element = card_topo.find('img')
            return image_element['src'] if image_element else None
        else:
            return None

    def get_elements_seed(self, soup):
        product_link =self. get_product_url(soup)
        title = self.get_title(soup)
        price = self.get_price(soup)
        link_imagem = self.get_image_url(soup)

        return product_link, title, price, link_imagem

def extract(conf):
    run_page_mapper(conf, Job)