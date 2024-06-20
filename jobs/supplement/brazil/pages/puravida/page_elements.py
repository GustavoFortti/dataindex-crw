def get_items(conf, soup):
    items = soup.find_all('div', class_='spot-product-info px-4 pt-4')
    return items

def get_product_url(conf, soup):
    # Procura pelo elemento 'a' com a classe 'spot-product-link'
    product_link_element = soup.find('a', class_='spot-product-link')
    # Concatena a URL base com o atributo 'href' do elemento de link, se encontrado
    product_link = conf["url"] + product_link_element['href'] if product_link_element else None
    return product_link

def get_title(conf, soup):
    # Procura pelo elemento h3 com o id 'novo-titulo' para obter o título
    title_element = soup.find('h3', id='novo-titulo')
    # Extrai o texto e remove espaços em branco desnecessários, se o elemento for encontrado
    title = title_element.text.strip() if title_element else None
    return title


def get_price(conf, soup):
    price = None
    # Procura pela classe que contém o preço
    price_element = soup.find('span', class_='precoPor')
    if price_element:
        # Captura o valor principal do preço
        main_price = price_element.get_text(strip=True)
        
        # Procura por elementos <sup> que contêm a parte fracionária do preço
        sup_elements = price_element.find_all('sup')
        fractional_price = ''.join([elem.text for elem in sup_elements])

        # Concatena o valor principal com a parte fracionária
        price = f'{main_price}{fractional_price}'.strip()

    return price

def get_image_url(conf, soup):
    # Procura pelo primeiro elemento 'img' dentro de um 'div' com a classe 'spot-image'
    image_container = soup.find('div', class_='spot-image')
    image_element = image_container.find('img') if image_container else None
    
    # Extrai o atributo 'src' do elemento de imagem, se encontrado
    link_imagem = image_element['src'] if image_element else None
    return link_imagem