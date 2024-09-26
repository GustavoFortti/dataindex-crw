def get_items(conf, soup):
    items = soup.find_all('div', class_='vtex-search-result-3-x-galleryItem')
    return items

def get_product_url(conf, soup):
    product_link_element = soup.find('a', class_='vtex-product-summary-2-x-clearLink')
    return conf["url"] + product_link_element['href'] if product_link_element else None

def get_title(conf, soup):
    title_element = soup.find('span', class_='vtex-product-summary-2-x-brandName')
    return title_element.get_text().strip() if title_element else None

def get_price(conf, soup):
    # Busca pelo elemento que contém o preço de venda não riscado
    selling_price_element = soup.find(class_="vtex-store-components-3-x-sellingPriceValue")
    if not selling_price_element:
        # Se não encontrar o preço de venda, tenta buscar por qualquer preço disponível
        selling_price_element = soup.find(class_="vtex-product-summary-2-x-currencyContainer")

    if selling_price_element:
        # Captura as diferentes partes do preço
        currency_code = selling_price_element.find(class_="vtex-product-summary-2-x-currencyCode").get_text(strip=True)
        currency_integer = selling_price_element.find(class_="vtex-product-summary-2-x-currencyInteger").get_text(strip=True)
        currency_decimal = selling_price_element.find(class_="vtex-product-summary-2-x-currencyDecimal").get_text(strip=True)
        currency_fraction = selling_price_element.find(class_="vtex-product-summary-2-x-currencyFraction").get_text(strip=True)

        # Constrói o preço formatado corretamente
        price = f"{currency_code} {currency_integer}{currency_decimal}{currency_fraction}"
        return price

    # Retorna None se nenhum preço for encontrado
    return None

def get_image_url(conf, soup):
    image_element = soup.find('img', class_='vtex-product-summary-2-x-imageNormal')
    return image_element['src'] if image_element else None