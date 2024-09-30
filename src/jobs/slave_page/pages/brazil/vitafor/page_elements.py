def get_items(conf, soup):
    items = soup.find_all('section', class_='vtex-product-summary-2-x-container')
    return items

def get_product_url(conf, soup):
    product_element = soup.find(class_='vtex-product-summary-2-x-clearLink')
    product_link = conf["url"] + product_element['href'] if product_element else None
    return product_link

def get_title(conf, soup):
    title_element = soup.find('h3', class_='vtex-product-summary-2-x-productNameContainer')
    title = title_element.get_text().strip() if title_element else None
    return title

def get_price(conf, soup):
    # Encontra o contêiner que contém o preço
    price_container = soup.find('span', class_='vitafor-store-theme-9-x-customPrice')
    
    if price_container:
        # Captura o texto do preço e remove espaços extras
        price = price_container.get_text(strip=True)
        return price
    else:
        return None


def get_image_url(conf, soup):
    image_element = soup.find('img', class_='vtex-product-summary-2-x-imageNormal')
    image_link = image_element['src'] if image_element else None
    return image_link