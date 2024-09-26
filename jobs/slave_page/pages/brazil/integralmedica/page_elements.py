def get_items(conf, soup):
    items = soup.find_all('div', class_='vtex-search-result-3-x-galleryItem vtex-search-result-3-x-galleryItem--normal vtex-search-result-3-x-galleryItem--grid pa4')
    return items

def get_product_url(conf, soup):
    product_link_element = soup.find('a', class_='vtex-product-summary-2-x-clearLink vtex-product-summary-2-x-clearLink--default h-100 flex flex-column')
    product_link = conf["url"] + product_link_element['href'] if product_link_element else None
    return product_link

def get_title(conf, soup):
    title_element = soup.find('span', class_='vtex-product-summary-2-x-productBrand vtex-product-summary-2-x-brandName t-body')
    title = title_element.get_text().strip() if title_element else None
    return title

def get_price(conf, soup):
    price_element = soup.find('span', class_='vtex-product-price-1-x-sellingPriceValue vtex-product-price-1-x-sellingPriceValue--shelfDefault')
    price = price_element.get_text().strip() if price_element else None
    return price

def get_image_url(conf, soup):
    image_element = soup.find('img', class_='vtex-product-summary-2-x-imageNormal vtex-product-summary-2-x-image vtex-product-summary-2-x-image--shelfDefault')
    link_imagem = image_element['src'] if image_element else None
    return link_imagem
