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
        items = soup.find_all('div', class_='vtex-search-result-3-x-galleryItem')
        return items

    def get_product_url(self, soup):
        product_link_element = soup.find('a', class_='vtex-product-summary-2-x-clearLink')
        product_link = "https://www.duxnutrition.com" + product_link_element['href'] if product_link_element else None
        return product_link


    def get_title(self, soup):
        title_element = soup.find('span', class_='vtex-product-summary-2-x-productBrand')
        title = title_element.get_text().strip() if title_element else None
        return title

    def get_price(self, soup):
        price = None
        price_element = soup.find('span', class_='vtex-product-price-1-x-sellingPriceValue vtex-product-price-1-x-sellingPriceValue--summary')
        if price_element:
            currency_container = price_element.find('span', class_='vtex-product-price-1-x-currencyContainer')
            if currency_container:
                price = ''.join([elem.text for elem in currency_container.find_all('span')])
                price = price.replace('\xa0', ' ').strip()
        return price

    def get_image_url(self, soup):
        image_container = soup.find('div', class_='vtex-product-summary-2-x-imageContainer')
        link_imagem = None
        if image_container:
            image_element = image_container.find('img')
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