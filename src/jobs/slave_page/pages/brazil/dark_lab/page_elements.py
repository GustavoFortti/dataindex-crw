def get_items(conf, soup):
    # Captura todos os produtos na página que tenham um 'data-product-id' válido
    items = soup.find_all('div', class_='js-item-product')
    # Filtra apenas os itens que possuem um 'data-product-id' válido (não vazio)
    available_items = [item for item in items if item.get('data-product-id')]
    return available_items

def get_product_url(conf, item):
    # Captura a URL do produto dentro do item
    product_link_element = item.find('a', {'title': True})
    product_link = product_link_element['href'] if product_link_element else None
    return product_link

def get_title(conf, item):
    # Captura o título do produto
    title_element = item.find('div', class_='js-item-name')
    title = title_element.get_text().strip() if title_element else None
    return title

def get_price(conf, item):
    # Captura o preço do produto
    price_element = item.find('span', class_='js-price-display')
    price = price_element.get_text().strip() if price_element else None
    return price

def get_image_url(conf, item):
    # Captura a URL da imagem do produto
    image_container = item.find('div', class_='item-image')
    image_element = image_container.find('img') if image_container else None

    link_imagem = None
    if image_element:
        if image_element.has_attr('data-srcset'):
            link_imagem = "https:" + image_element['data-srcset'].split(' ')[0]
        elif image_element.has_attr('srcset'):
            link_imagem = "https:" + image_element['srcset'].split(' ')[0]
        elif image_element.has_attr('src'):
            link_imagem = "https:" + image_element['src']

    return link_imagem
