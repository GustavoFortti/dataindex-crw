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
        items = soup.find_all('div', class_='box-item')
        return items

    def get_product_url(self, soup):

        product_link_element = soup.find('a', class_='product-image')
        product_link =  product_link_element['href'] if product_link_element else None
        return product_link

    def get_title(self, soup):
        title_element = soup.find('a')
        if title_element and 'title' in title_element.attrs:
            title = title_element['title'].strip()
        else:
            title = None
        return title

    def get_price(self, soup):
        price_element = soup.find('span', class_='best-price')
        price = price_element.get_text().strip() if price_element else None
        return price

    def get_image_url(self, soup):
        image_container = soup.find('div', class_='__bs-img-show _lazy-box has--lazyload is--lazyloaded')
        link_imagem = None
        if image_container:
            image_element = image_container.find('img')
            link_imagem = image_element['src'] if image_element else None
        return link_imagem

    def get_elements_seed(self, soup):
        product_link =self. get_product_url(soup)
        title = self.get_title(soup)
        price = self.get_price(soup)
        link_imagem = self.get_image_url(soup)

        return product_link, title, price, link_imagem

def extract(conf):
    run_page_mapper(conf, Job)