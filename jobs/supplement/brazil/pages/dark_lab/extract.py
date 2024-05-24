from lib.page_mapper import run as run_page_mapper

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
        items = soup.find_all('div', class_='item-with-sidebar')
        return items

    def get_product_url(self, soup):
        product_link_container = soup.find('div', class_='item-image')
        product_link_element = product_link_container.find('a') if product_link_container else None
        product_link = product_link_element['href'] if product_link_element else None
        return product_link

    def get_title(self, soup):
        title_element = soup.find('div', class_='js-item-name')
        title = title_element.get_text().strip() if title_element else None
        return title

    def get_price(self, soup):
        price_element = soup.find('span', class_='js-price-display')
        price = price_element.get_text().strip() if price_element else None
        return price

    def get_image_url(self, soup):
        link_imagem = None
        image_container = soup.find('div', class_='item-image')
        image_element = image_container.find('img') if image_container else None
        
        try:
            link_imagem = "https:" + image_element.get('srcset').split(' ')[0] if image_element else None
        except:
            pass
            
        try:
            link_imagem = "https:" + image_element.get('data-srcset').split(' ')[0] if image_element else None
        except:
            pass
        
        return link_imagem

    def get_elements_seed(self, soup):
        product_link = self. get_product_url(soup)
        title = self.get_title(soup)
        price = self.get_price(soup)
        link_imagem = self.get_image_url(soup)

        return product_link, title, price, link_imagem

def extract(conf):
    run_page_mapper(conf, Job)