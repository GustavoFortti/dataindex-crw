def get_items(conf, soup):
    items = soup.find_all('div', class_='item item-rounded item-product box-rounded p-0')
    return items

def get_product_url(conf, soup):
    product_link_container = soup.find('div', class_='position-relative')
    if (product_link_container):
        product_link_element = product_link_container.find('a')
        return product_link_element['href'] if product_link_element else None

def get_title(conf, soup):
    title_element = soup.find('div', class_='js-item-name item-name mb-3')
    return title_element.get_text().strip() if title_element else None

def get_price(conf, soup):
    price_element = soup.find("span", class_="js-price-display item-price")
    price = price_element.get_text() if price_element else None
    return price

def get_image_url(conf, soup):
    image_container = soup.find('div', class_='position-relative')
    if (image_container):
        image_element = soup.find('img')
        return "https:" + image_element['srcset'].split(" ")[0] if image_element else None
