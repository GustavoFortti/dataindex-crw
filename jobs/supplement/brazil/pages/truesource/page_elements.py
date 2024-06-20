def get_items(conf, soup):
    items = soup.find_all('div', class_='gap-x-3.5 gap-y-6 grid grid-cols-2 lg:grid-cols-4 items-center')
    return items

def get_product_url(conf, item):
    product_link_element = item.find('a', class_='flex items-center justify-center relative h-full bg-ice')
    product_url = conf["url"] + product_link_element['href'] if product_link_element else None
    return product_url

def get_title(conf, item):
    title_element = item.find('h3', class_='text-dark text-sm text-ellipsis font-bold line-clamp-2 h-10')
    title = title_element.get_text(strip=True) if title_element else None
    return title

def get_price(conf, item):
    price_element = item.find('div', class_='text-dark text-xs lg:text-sm')
    price = price_element.get_text(strip=True) if price_element else None
    return price

def get_image_url(conf, item):
    image_element = item.find('img')
    image_url = image_element['src'] if image_element else None
    return image_url