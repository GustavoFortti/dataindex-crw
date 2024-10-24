def get_items(conf, soup):
    items = soup.find_all('li', class_='ui-search-layout__item')
    return items

def get_product_url(conf, soup):
    import re
    
    # Atualiza para buscar o link de todas as estruturas
    product_link_element = soup.find('a', href=re.compile(r'^https://www\.mercadolivre\.com\.br/'))
    if not product_link_element:
        product_link_element = soup.find('a', href=re.compile(r'^https://produto\.mercadolivre\.com\.br/'))
    
    if product_link_element and product_link_element.get('href'):
        return product_link_element['href'].strip()
    
    return None

def get_title(conf, soup):
    # Atualiza para buscar o título em todas as estruturas
    title_element = soup.find('h2', class_='ui-search-item__title')
    if not title_element:
        title_element = soup.find('h2', class_='poly-component__title')
    if not title_element:
        title_element = soup.find('h2', class_='ui-search-item__group__element')
    
    if title_element:
        link_element = title_element.find('a')
        if link_element:
            title = link_element.get_text().strip()
            return title
        else:
            # Caso o link esteja diretamente no h2
            title = title_element.get_text().strip()
            return title
    
    return None

def get_price(conf, soup):
    # Atualiza para buscar o preço em todas as estruturas
    # Encontra a parte inteira do preço
    fraction_element = soup.find('span', class_='andes-money-amount__fraction')
    if not fraction_element:
        fraction_element = soup.find('span', class_='poly-price__current').find('span', class_='andes-money-amount__fraction')
    if not fraction_element:
        fraction_element = soup.find('div', class_='ui-search-price__second-line').find('span', class_='andes-money-amount__fraction')
    fraction_text = fraction_element.get_text().strip() if fraction_element else None
    
    # Encontra os centavos do preço
    cents_element = soup.find('span', class_='andes-money-amount__cents')
    cents_text = cents_element.get_text().strip() if cents_element else None
    
    if fraction_text and cents_text:
        price = f"R$ {fraction_text},{cents_text}"
    elif fraction_text:
        price = fraction_text
    else:
        price = None
    
    return price

def get_image_url(conf, soup):
    # Atualiza para buscar a imagem em todas as estruturas
    image_element = soup.find('img', class_='ui-search-result-image__element')
    if not image_element:
        image_element = soup.find('img', class_='poly-component__picture')
    if not image_element:
        image_element = soup.find('img', class_='ui-search-result__image')
    
    image_url = image_element['src'] if image_element else None
    return image_url