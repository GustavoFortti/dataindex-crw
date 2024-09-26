def get_items(conf, soup):
    items_container =  soup.find_all('div', class_='content-product')
    items = [item for item in items_container if ((item.find('span', class_='woocommerce-Price-amount') is not None))]
    return items

def get_product_url(conf, soup):
    product_link_element = soup.find('a', class_='product-content-image')
    product_link = product_link_element['href'] if product_link_element else None
    return product_link

def get_title(conf, soup):
    title_element = soup.find('h2', class_='product-title')
    title = title_element.get_text().strip() if title_element else None
    return title

def get_price(conf, soup):
    price_element = soup.find('span', class_='woocommerce-Price-amount')
    price = price_element.get_text().strip() if price_element else None
    return price

def get_image_url(conf, soup):
    image_container = soup.find('a', class_='product-content-image')
    link_imagem = None
    if image_container:
        image_element = image_container.find('img')
        link_imagem = image_element['src'] if image_element else None
    return link_imagem