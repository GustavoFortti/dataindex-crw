def get_items(conf, soup):
    # Atualizando para capturar os itens com a classe 'product-card'
    items = soup.find_all('article', class_='product-card')
    return items

def get_product_url(conf, item):
    # Buscando o link do produto dentro da tag 'a'
    product_link_element = item.find('a', class_='product-card__link')
    return conf["url"] + product_link_element['href'] if product_link_element else None

def get_title(conf, item):
    # Extraindo o título do produto
    title_element = item.find('h3', class_='product-card__title')
    return title_element.get_text().strip() if title_element else None

def get_price(conf, item):
    # Extraindo o preço do produto
    price_element = item.find("span", class_="product-card__priceper")
    if price_element:
        return price_element.get_text(strip=True)
    return None

def get_image_url(conf, item):
    # Extraindo a URL da imagem do produto
    image_element = item.find('img', class_='product-card__img')
    return image_element['src'] if image_element else None