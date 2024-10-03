def get_items(conf, soup):
    import re
    items = []
    items_container = soup.find_all('div', class_='t4s-product-wrapper')
    for item in items_container:
        if (not re.search("cdn.shopify.com", str(item))):
            items.append(item)
    return items

def get_product_url(conf, soup):
    product_link_element = soup.find('a', class_='t4s-full-width-link')
    return conf["url"] + product_link_element['href'] if product_link_element else None

def get_title(conf, soup):
    title_element = soup.find('h3', class_='t4s-product-title')
    return title_element.get_text().strip() if title_element else None

def get_price(conf, soup):
    import re
    final_price = None
    price_container = soup.find(class_="t4s-product-price")
    
    if price_container:
        # Verifica se existe um desconto
        discount_price_element = price_container.find("ins")
        if discount_price_element:
            final_price = discount_price_element.text.strip()
        else:
            # Se não houver desconto, procura pela tag span com classe t4s-price__sale
            sale_price_element = price_container.find("span", class_="t4s-price__sale")
            if sale_price_element:
                # Extrai todos os preços usando expressão regular
                prices = re.findall(r"\d+,\d+", sale_price_element.text)
                # Converte os preços para float e seleciona o maior
                prices = [float(price.replace(',', '.')) for price in prices]
                final_price = f"R$ {max(prices):.2f}".replace('.', ',')
            else:
                # Se não houver intervalo de preços, pega o preço padrão
                standard_price_element = price_container.text.strip()
                if standard_price_element:
                    # Verifica se há mais de um preço no preço padrão
                    prices = re.findall(r"\d+,\d+", standard_price_element)
                    if prices:
                        prices = [float(price.replace(',', '.')) for price in prices]
                        final_price = f"R$ {max(prices):.2f}".replace('.', ',')
                    else:
                        final_price = standard_price_element
    
    return final_price

def get_image_url(conf, soup):
    import re
    image_element = soup.find(class_='t4s-product-main-img')

    if image_element:
        # Extrai a URL base da imagem do 'data-src'
        if 'data-src' in image_element.attrs:
            base_image_url = "https:" + image_element['data-src']
            # Extrai os tamanhos do atributo 'data-widths'
            if 'data-widths' in image_element.attrs:
                widths = image_element['data-widths']
                
                # Converte a string dos tamanhos em uma lista de inteiros
                width_list = [int(width) for width in re.findall(r'\d+', widths)]
                
                # Seleciona o maior tamanho da lista
                max_width = max(width_list)
                
                # Constrói a URL final com o maior tamanho disponível
                final_image_url = re.sub(r'width=\d+', f'width={max_width}', base_image_url)
                
                return final_image_url
        # Caso não tenha 'data-src', verifica o atributo 'src'
        elif 'src' in image_element.attrs and not image_element['src'].startswith('data:image'):
            image_link = "https:" + image_element['src']
            return image_link

    return None  # Retorna None se não encontrar a imagem
