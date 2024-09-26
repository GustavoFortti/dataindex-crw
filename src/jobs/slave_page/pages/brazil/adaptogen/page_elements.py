def get_items(conf, soup):
    items = soup.find_all('li', class_='product-type-simple')
    return items

def get_product_url(conf, soup):
    product_link_element = soup.find('a')
    return product_link_element['href'] if product_link_element else None

def get_title(conf, soup):
    title_element = soup.find('h2', class_='woocommerce-loop-product__title')
    return title_element.get_text().strip() if title_element else None

def get_price(conf, soup):
    price_container = soup.find(class_="a_vista")
    if (price_container):
        price_element = price_container.find('p')
        price = price_element.contents[0].strip()
    return price

def get_image_url(conf, soup):
    image_element = soup.find('img', class_='entered lazyloaded')
    return image_element['src'] if image_element else None