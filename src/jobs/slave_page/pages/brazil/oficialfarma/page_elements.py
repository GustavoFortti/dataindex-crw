def get_items(conf, soup):
    items = soup.find_all('li', class_='item product product-item')
    return items

def get_product_url(conf, soup):
    product_link_element = soup.find('a', class_='product-item-link')
    product_link = product_link_element['href'] if product_link_element else None
    return product_link

def get_title(conf, soup):
    title_element = soup.find('strong', class_='product name product-item-name').find('a')
    title = title_element.get_text().strip() if title_element else None
    return title

def get_price(conf, soup):
    price_element = soup.find('span', class_='price-wrapper')
    price_text = price_element.get_text().strip() if price_element else None
    return price_text

def get_image_url(conf, soup):
    image_element = soup.find('img', class_='product-image-photo')
    image_url = image_element['src'] if image_element else None
    return image_url