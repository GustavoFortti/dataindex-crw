def get_items(conf, soup):
    items_container = soup.find_all('div', class_='product-card')
    items = [item for item in items_container if item.find('div', class_='product-price-sale') is not None]
    return items

def get_product_url(conf, soup):
    product_link_element = soup.find('a', href=True)
    product_link = product_link_element['href'] if product_link_element else None
    return product_link

def get_title(conf, soup):
    title_element = soup.find('p', class_='product-title')
    title = title_element.get_text().strip() if title_element else None
    return title

def get_price(conf, soup):
    price_element = soup.find('div', class_='product-price-sale')
    price = price_element.get_text().strip() if price_element else None
    return price

def get_image_url(conf, soup):
    import re
    image_container = soup.find('div', class_='product-image')
    link_imagem = None
    if image_container:
        style_attr = image_container.get('style', '')
        match = re.search(r'url\("([^"]+)"\)', style_attr)
        link_imagem = match.group(1) if match else None
    return link_imagem