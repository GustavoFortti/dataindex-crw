def get_items(conf, soup):
    return soup.find_all('a', class_='cardprod text-decoration-none')

def get_product_url(conf, soup):
    import re
    if not isinstance(soup, str):
        html_content = str(soup)
    else:
        html_content = soup
    
    pattern = r'<a[^>]*class="[^"]*cardprod[^"]*text-decoration-none[^"]*"[^>]*href="([^"]+)"'
    
    match = re.search(pattern, html_content)
    
    if match:
        product_link_element = conf['url'] + match.group(1).strip() 
        return product_link_element
    return None

def get_title(conf, soup):
    title_element = soup.find('h3', class_='cardprod-nomeProduto-t1')
    return title_element.get_text().strip() if title_element else None

def get_price(conf, soup):
    price_element = soup.find('span', class_='cardprod-valor')
    if price_element:
        # Obtém apenas o texto direto dentro do span, ignorando elementos filhos
        price_text = ''.join(price_element.find_all(string=True, recursive=False)).strip()
        # Remove o símbolo "R$" e quaisquer espaços
        price_without_symbol = price_text.strip()
        return price_without_symbol
    return None

def get_image_url(conf, soup):
    image_element = soup.find('img')
    return image_element['src'] if image_element and image_element.has_attr('src') else None
