def get_items(conf, soup):
    items = soup.find_all('li', class_='product collection-product-list')
    return items

def get_product_url(conf, soup):
    product_link_element = soup.find('a', class_='card-link')
    product_link = conf["url"] + product_link_element['href'] if product_link_element else None
    
    return product_link

def get_title(conf, soup):
    title_element = soup.find('a', class_='card-title center link-underline card-title-ellipsis')
    title = title_element.get_text().strip() if title_element else None
    return title

def get_price(conf, soup):
    def format_price(price_text):
        # Remove espaços em branco, símbolos de moeda e pontos de separador de milhar
        cleaned_price = price_text.strip().replace("R$", "").replace(".", "").replace(",", ".")
        
        try:
            # Converte o texto do preço em um número float
            price_float = float(cleaned_price)
            # Formata o número de volta para o padrão brasileiro (R$ X.XXX,XX)
            formatted_price = f"R$ {price_float:,.2f}".replace(".", ",")
            return formatted_price
        except ValueError:
            return None

    # Busca pela classe de preço em promoção (sale)
    price_sale_span = soup.find('span', class_='price-item--sale')
    if price_sale_span:
        price_text = price_sale_span.get_text()
        return format_price(price_text)

    # Se não encontrar promoção, busca pelo preço regular
    price_regular_span = soup.find('span', class_='price-item--regular')
    if price_regular_span:
        price_text = price_regular_span.get_text()
        return format_price(price_text)
    
    return None

def get_image_url(conf, soup):
    div_container = soup.find('div', class_='card-product__wrapper')

    if div_container:
        image_element = div_container.find('img')
        if image_element and 'data-srcset' in image_element.attrs:
            srcset = image_element['data-srcset']
            images = srcset.split(",")
            
            middle_image = images[len(images) // 2].split(" ")[0].strip()
            image_url = "https:" + middle_image if middle_image.startswith("//") else middle_image
            return image_url
    return None
