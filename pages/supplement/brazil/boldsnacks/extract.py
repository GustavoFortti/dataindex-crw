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
        items = soup.find_all('div', class_='product-item')
        return items

    def get_product_url(self, soup):
        product_link_element = soup.find('a', class_='card-title link-underline card-title-ellipsis')
        product_link = "https://www.boldsnacks.com.br" + product_link_element['href'] if product_link_element else None
        return product_link

    def get_title(self, soup):
        title_element = soup.find('a', class_='card-title link-underline card-title-ellipsis')
        title = title_element.get_text().strip() if title_element else None
        return title

    def get_price(self, soup):
        def format_price(price_text):
            cleaned_price = price_text.strip()
            if "," in cleaned_price:
                return None
            else:
                return cleaned_price + ",00"

        price_sale_span = soup.find('span', class_='price-item--sale')
        if price_sale_span:
            price_text = price_sale_span.get_text()
            return format_price(price_text)

        price_regular_span = soup.find('span', class_='price-item--regular')
        if price_regular_span:
            price_text = price_regular_span.get_text()
            return format_price(price_text)
        
        return None

    def get_image_url(self, soup):
        div_container = soup.find('div', class_='card-product__wrapper')
    
        if div_container:
            image_element = div_container.find('img')
            if image_element and 'data-srcset' in image_element.attrs:
                srcset = image_element['data-srcset']
                images = srcset.split(",")
                
                middle_image = images[len(images) // 2].split(" ")[0].strip()
                image_url = "https:" + middle_image if middle_image.startswith("//") else middle_image
                return image_url
        return None

    def get_elements_seed(self, soup):
        product_link =self. get_product_url(soup)
        title = self.get_title(soup)
        price = self.get_price(soup)
        link_imagem = self.get_image_url(soup)

        return product_link, title, price, link_imagem

def extract(conf):
    run_page_mapper(conf, Job)