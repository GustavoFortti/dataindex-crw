def get_items(conf, soup):
    # Busca todos os itens no HTML com a classe especificada
    items = soup.find_all('div', class_='duxnutrition-search-result-3-x-galleryItem')
    return items

def get_product_url(conf, soup):
    # Busca o link do produto no HTML
    product_link_element = soup.find('a', class_='vtex-product-summary-2-x-clearLink')
    product_link = conf["url"] + product_link_element['href'] if product_link_element else None
    return product_link

def get_title(conf, soup):
    # Busca o título do produto no HTML
    title_element = soup.find('span', class_='vtex-product-summary-2-x-productBrand')
    title = title_element.get_text().strip() if title_element else None
    return title

def get_price(conf, soup):
    # Busca o preço do produto no HTML
    price = None
    price_element = soup.find('span', class_='vtex-store-components-3-x-sellingPriceValue')
    if price_element:
        price = price_element.get_text().strip()
    return price

def get_image_url(conf, soup):
    # Busca a URL da imagem do produto no HTML
    image_element = soup.find('img', class_='vtex-product-summary-2-x-imageNormal')
    if image_element and 'src' in image_element.attrs:
        return image_element['src']
    return None
