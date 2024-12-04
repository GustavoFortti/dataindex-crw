def get_items(soup):
    items = soup.find_all('li', class_='grid__item')
    return items

def get_product_url(soup, url):
    product_link_element = soup.find('a')
    return url + product_link_element['href'] if product_link_element else None

def get_title(soup):
    title_element = soup.find('h2')
    return title_element.get_text().strip() if title_element else None

def get_price(soup):
    price_container = soup.find(class_="price__container")
    if price_container:
        price_element = price_container.find('span', class_="price-item price-item--regular")
        price = price_element.get_text().strip() if price_element else None
        if price and price.lower().startswith("from"):
            price = price.replace("From", "").strip()
    return price

def get_image_url(soup):
    image_element = soup.find('img')
    return "https:" + image_element['src'] if image_element else None
