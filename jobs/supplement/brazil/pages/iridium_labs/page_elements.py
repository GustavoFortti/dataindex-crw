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
                # Converte os preços para float e seleciona o menor
                prices = [float(price.replace(',', '.')) for price in prices]
                final_price = f"R$ {min(prices):.2f}".replace('.', ',')
            else:
                # Se não houver intervalo de preços, pega o preço padrão
                standard_price_element = price_container.text.strip()
                if standard_price_element:
                    final_price = standard_price_element
    
    return final_price

def get_image_url(conf, soup):
    image_element = soup.find(class_='t4s-product-main-img')
    if (image_element and 'srcset' in image_element.attrs):
        srcset = image_element['srcset']
        image_urls = [img.strip() for img in srcset.split(',')]
        highest_res_image = image_urls[-1].split(' ')[0]
        image_link = "https:" + highest_res_image
        return image_link
    elif (image_element and 'src' in image_element.attrs):
        image_link = "https:" + image_element['src']
        return image_link