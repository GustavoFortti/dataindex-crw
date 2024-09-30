def get_items(conf, soup):
    # Procura por todos os itens de produtos na página
    items = soup.select('div[id^="product-new-spot-item-"]')
    return items

def get_product_url(conf, soup):
    import re
    # Converte o objeto soup para string, se necessário
    if not isinstance(soup, str):
        html_content = str(soup)
    else:
        html_content = soup
    
    # Expressão regular para encontrar o href dentro da tag <a> com a classe 'spot-product-info'
    pattern = r'<a[^>]*class="[^"]*spot-product-info[^"]*"[^>]*href="([^"]+)"'
    
    # Buscar a primeira correspondência do padrão
    match = re.search(pattern, html_content)
    
    if match:
        product_url = match.group(1)  # Captura a URL relativa
        return conf["url"] + product_url.strip()  # Constrói a URL absoluta
    
    return None

def get_title(conf, soup):
    # Procura pelo elemento 'p' com a classe 'product-name' para obter o título
    title_element = soup.find('p', class_='product-name')
    # Extrai o texto e remove espaços em branco desnecessários, se o elemento for encontrado
    title = title_element.text.strip() if title_element else None
    return title

def get_price(conf, soup):
    import re
    
    # Procura pela div que contém o preço
    price_element = soup.find('div', class_='product-price')
    
    if price_element:
        price_text = price_element.get_text(strip=True)
        # Usa regex para capturar o valor numérico após 'R$'
        match = re.search(r'R\$\s*([\d.,]+)', price_text)
        if match:
            price = match.group(1)
            return "R$" + price
    # Alternativamente, usa regex para encontrar o preço no texto do contêiner
    text = soup.get_text()
    match = re.search(r'R\$\s*([\d.,]+)', text)
    if match:
        price = match.group(1)
        return "R$" + price
    return None

def get_image_url(conf, soup):
    # Procura pelo primeiro elemento 'img' dentro de um 'picture' associado ao produto
    image_container = soup.find('picture')
    image_element = image_container.find('img') if image_container else None
    
    # Extrai o atributo 'src' do elemento de imagem, se encontrado
    link_imagem = image_element['src'] if image_element else None
    return link_imagem