def get_items(conf, soup):
    items = soup.find_all('div', class_='item-with-sidebar')
    return items

def get_product_url(conf, soup):
    product_link_container = soup.find('div', class_='item-image')
    product_link_element = product_link_container.find('a') if product_link_container else None
    product_link = product_link_element['href'] if product_link_element else None
    return product_link

def get_title(conf, soup):
    title_element = soup.find('div', class_='js-item-name')
    title = title_element.get_text().strip() if title_element else None
    return title

def get_price(conf, soup):
    price_element = soup.find('span', class_='js-price-display')
    price = price_element.get_text().strip() if price_element else None
    return price

def get_image_url(conf, soup):
    link_imagem = None
    image_container = soup.find('div', class_='item-image')
    image_element = image_container.find('img') if image_container else None
    
    try:
        link_imagem = "https:" + image_element.get('srcset').split(' ')[0] if image_element else None
    except:
        pass
        
    try:
        link_imagem = "https:" + image_element.get('data-srcset').split(' ')[0] if image_element else None
    except:
        pass
    
    return link_imagem