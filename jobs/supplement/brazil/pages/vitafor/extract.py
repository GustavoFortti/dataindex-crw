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
        items = soup.find_all('section', class_='vtex-product-summary-2-x-container')
        return items

    def get_product_url(self, soup):
        product_element = soup.find(class_='vtex-product-summary-2-x-clearLink')
        product_link = "https://www.vitafor.com.br" + product_element['href'] if product_element else None
        return product_link

    def get_title(self, soup):
        title_element = soup.find('h3', class_='vtex-product-summary-2-x-productNameContainer')
        title = title_element.get_text().strip() if title_element else None
        return title

    def get_price(self, soup):
        price_container = soup.find('div', class_='vtex-product-summary-2-x-sellingPriceContainer')
        if price_container:
            currency_code = price_container.find('span', class_='vtex-product-summary-2-x-currencyCode').get_text(strip=True)
            currency_integer = price_container.find('span', class_='vtex-product-summary-2-x-currencyInteger').get_text(strip=True)
            currency_decimal = price_container.find('span', class_='vtex-product-summary-2-x-currencyDecimal').get_text(strip=True)
            currency_fraction = price_container.find('span', class_='vtex-product-summary-2-x-currencyFraction').get_text(strip=True)
            
            price = f"{currency_code} {currency_integer}{currency_decimal}{currency_fraction}"
            return price
        else:
            return None

    def get_image_url(self, soup):
        image_element = soup.find('img', class_='vtex-product-summary-2-x-imageNormal')
        image_link = image_element['src'] if image_element else None
        return image_link

    def get_item_elements(self, soup):
        product_link = self.get_product_url(soup)
        title = self.get_title(soup)
        price = self.get_price(soup)
        link_imagem = self.get_image_url(soup)

        return product_link, title, price, link_imagem

def extract(conf):
    run_page_mapper(conf, Job)