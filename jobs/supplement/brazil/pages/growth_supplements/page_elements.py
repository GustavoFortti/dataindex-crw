def get_items(conf, soup):
    items = soup.find_all('div', class_='vitrine-prod')
    return items

def get_product_url(conf, soup):
    product_link_element = soup.find('a', class_='cardprod-nomeProduto')
    if product_link_element and 'href' in product_link_element.attrs:
        return conf["url"] + product_link_element['href']
    return None

def get_title(conf, soup):
    title_element = soup.find('h3', class_='cardprod-nomeProduto-t1')
    return title_element.get_text().strip() if title_element else None

def get_price(conf, soup):
    price_element = soup.find('span', class_='cardprod-valor')
    if price_element:
        full_text = price_element.get_text().strip()
        price = full_text.split('\n')[0].strip()
        return price
    else:
        return None

def get_image_url(conf, soup):
    card_topo = soup.find('div', class_='cardProd-topo')
    if card_topo:
        image_element = card_topo.find('img')
        return image_element['src'] if image_element else None
    else:
        return None