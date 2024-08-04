def get_items(conf, soup):
    items = soup.find_all('div', class_='vtex-search-result-3-x-galleryItem')
    return items

def get_product_url(conf, soup):
    product_link_element = soup.find('a', class_='vtex-product-summary-2-x-clearLink')
    product_link = conf["url"] + product_link_element['href'] if product_link_element else None
    return product_link


def get_title(conf, soup):
    title_element = soup.find('span', class_='vtex-product-summary-2-x-productBrand')
    title = title_element.get_text().strip() if title_element else None
    return title

def get_price(conf, soup):
    price = None
    price_element = soup.find('span', class_='vtex-product-price-1-x-sellingPriceValue vtex-product-price-1-x-sellingPriceValue--summary')
    if price_element:
        currency_container = price_element.find('span', class_='vtex-product-price-1-x-currencyContainer')
        if currency_container:
            price = ''.join([elem.text for elem in currency_container.find_all('span')])
            price = price.replace('\xa0', ' ').strip()
    return price

def get_image_url(conf, soup):
    image_div = soup.find('div', class_='duxnutrition-product-0-x-imageStackContainer')
    if image_div:
        image_element = image_div.find('img', class_='duxnutrition-product-0-x-imageNormal')
        if image_element and 'src' in image_element.attrs:
            return image_element['src']
    return None