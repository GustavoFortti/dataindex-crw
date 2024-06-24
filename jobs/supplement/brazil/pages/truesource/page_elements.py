def get_items(conf, soup):
    items = soup.find_all('div', class_='w-full lg:max-w-[260px]')
    return items

def get_product_url(conf, soup):
    product_link_element = soup.find('a', class_='flex items-center justify-center relative h-full bg-ice')
    product_url = conf["url"] + product_link_element['href'] if product_link_element else None
    return product_url

def get_title(conf, soup):
    title_element = soup.find('h3', class_='text-dark text-sm text-ellipsis font-bold line-clamp-2 h-10')
    title = title_element.get_text(strip=True) if title_element else None
    return title

def get_price(conf, soup):
    price_element = soup.find('div', class_='text-dark text-xs lg:text-sm')
    price = price_element.get_text(strip=True) if price_element else None
    return price

def get_image_url(conf, soup):
    image_element = soup.find('img')
    image_url = image_element['src'] if image_element else None
    return image_url