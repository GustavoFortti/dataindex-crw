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
    price = None
    price_element = soup.find("span", class_="vtex-product-price-1-x-sellingPriceValue")
    if price_element:
        currency_code = price_element.find("span", class_="vtex-product-price-1-x-currencyCode").get_text(strip=True)
        currency_integer = price_element.find("span", class_="vtex-product-price-1-x-currencyInteger").get_text(strip=True)
        currency_decimal = price_element.find("span", class_="vtex-product-price-1-x-currencyDecimal").get_text(strip=True)
        currency_fraction = price_element.find("span", class_="vtex-product-price-1-x-currencyFraction").get_text(strip=True)

        price = f"{currency_code} {currency_integer}{currency_decimal}{currency_fraction}"
    return price

def get_image_url(conf, soup):
    image_element = soup.find('img', class_='vtex-product-summary-2-x-imageNormal')
    return image_element['src'] if image_element else None