def get_items(conf, soup):
    items_container =  soup.find_all('li', class_='span3')
    items = [item for item in items_container if ((not item.has_attr('aria-hidden') or 
                                                    item['aria-hidden'] != 'true') & 
                                                    (item.find('strong', class_='preco-promocional') is not None))]
    return items

def get_product_url(conf, soup):
    product_link_element = soup.find('a', class_='produto-sobrepor')
    product_link =  product_link_element['href'] if product_link_element else None
    return product_link

def get_title(conf, soup):
    title_element = soup.find('a', class_='nome-produto')
    title = title_element.get_text().strip() if title_element else None
    return title

def get_price(conf, soup):
    price_element = soup.find('strong', class_='preco-promocional')
    price = price_element.get_text().strip() if price_element else None
    return price

def get_image_url(conf, soup):
    image_element = soup.find('img', class_='imagem-principal')
    link_imagem = image_element['src'] if image_element else None
    return link_imagem