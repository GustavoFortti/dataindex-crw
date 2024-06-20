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
        items = soup.find_all('div', class_='vtex-search-result-3-x-galleryItem')
        return items

    def get_product_url(self, item):
        product_link_element = item.find('a', class_='vtex-product-summary-2-x-clearLink')
        return "https://www.darkness.com.br" + product_link_element['href'] if product_link_element else None

    def get_title(self, item):
        title_element = item.find('span', class_='vtex-product-summary-2-x-brandName')
        return title_element.get_text().strip() if title_element else None

    def get_price(self, item):
        price_element = item.find("span", class_="vtex-product-price-1-x-sellingPriceValue")
        if price_element:
            currency_code = price_element.find("span", class_="vtex-product-price-1-x-currencyCode").get_text(strip=True)
            currency_integer = price_element.find("span", class_="vtex-product-price-1-x-currencyInteger").get_text(strip=True)
            currency_decimal = price_element.find("span", class_="vtex-product-price-1-x-currencyDecimal").get_text(strip=True)
            currency_fraction = price_element.find("span", class_="vtex-product-price-1-x-currencyFraction").get_text(strip=True)
            price = f"{currency_code} {currency_integer}{currency_decimal}{currency_fraction}"
            return price
        return None

    def get_image_url(self, item):
        image_element = item.find('img', class_='vtex-product-summary-2-x-imageNormal')
        return image_element['src'] if image_element else None

    def get_item_elements(self, soup):
        product_link = self.get_product_url(soup)
        title = self.get_title(soup)
        price = self.get_price(soup)
        link_imagem = self.get_image_url(soup)

        return product_link, title, price, link_imagem

def extract(conf):
    run_page_mapper(conf, Job)