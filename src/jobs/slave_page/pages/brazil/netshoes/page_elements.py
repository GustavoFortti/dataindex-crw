def get_items(conf, soup):
    items = soup.find_all('li', class_='ui-search-layout__item')
    return items

def get_product_url(conf, soup):
    product_link_element = soup.find('a', class_='ui-search-link')
    product_link = product_link_element['href'] if product_link_element else None
    return product_link

def get_title(conf, soup):
    title_element = soup.find('h2', class_='ui-search-item__title')
    
    if title_element:
        link_element = title_element.find('a')
        if link_element:
            title = link_element.get_text().strip()
            return title
    
    return None

def get_price(conf, soup):
    # Encontra a parte inteira do preço
    fraction_element = soup.find('span', class_='andes-money-amount__fraction')
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
    image_element = soup.find('img', class_='ui-search-result-image__element')
    image_url = image_element['src'] if image_element else None
    return image_url