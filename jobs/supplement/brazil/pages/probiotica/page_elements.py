def get_items(conf, soup):
    items = soup.find_all('div', class_='vtex-search-result-3-x-galleryItem')
    return items

def get_product_url(conf, soup):
    product_link_element = soup.find('a', class_='vtex-product-summary-2-x-clearLink')
    product_link = conf["url"] + product_link_element['href'] if product_link_element else None
    return product_link

def get_title(conf, soup):
    title_element = soup.find('h2', class_='vtex-product-summary-2-x-productNameContainer')
    if title_element:
        span_element = title_element.find('span', class_='vtex-product-summary-2-x-productBrand')
        title = span_element.text.strip() if span_element else None
    else:
        title = None
    return title

def get_price(conf, soup):
    price = None
    price_element = soup.find('span', class_='vtex-product-price-1-x-sellingPriceValue')
    if price_element:
        currency_container = price_element.find('span', class_='vtex-product-price-1-x-currencyContainer')
        if currency_container:
            price = ''.join([elem.text for elem in currency_container.find_all('span')])
            price = price.replace('\xa0', ' ').strip()
    return price

def get_image_url(conf, soup):
    image_element = soup.find('img', class_='vtex-product-summary-2-x-imageNormal vtex-product-summary-2-x-image')
    link_imagem = image_element['src'] if image_element else None
    return link_imagem