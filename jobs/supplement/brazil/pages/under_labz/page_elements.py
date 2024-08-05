def get_items(conf, soup):
    items = soup.find_all('li', class_='collection-product-card')
    return items

def get_product_url(conf, soup):
    product_link_element = soup.find('a')
    return conf["url"] + product_link_element['href'] if product_link_element else None

def get_title(conf, soup):
    title_element = soup.find('h3', class_='card__title')
    return title_element.get_text().strip() if title_element else None

def get_price(conf, soup):
    price_element = soup.find('span', class_='price-item price-item--sale')
    return price_element.get_text().strip() if price_element else None

def get_image_url(conf, soup):
    image_element = soup.find('img', class_='motion-reduce media--first')
    return "https:" + image_element['src'] if image_element else None