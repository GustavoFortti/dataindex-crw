from shared.selenium_service import initialize_selenium
from shared.extractor_functions import map_tree, map_seed

def get_last_page_index(soup=None):
    return 10

def get_next_url(url, index):
    return url + str(index)

def get_items(soup):
    items = soup.find_all('div', class_='vtex-search-result-3-x-galleryItem')
    return items

def get_product_link(soup, map_type):
    if (map_type == "seed"):
        product_link_element = soup.find('a', class_='vtex-product-summary-2-x-clearLink')
        return "https://www.blackskullusa.com.br" + product_link_element['href'] if product_link_element else None
    # map_tree
    return None

def get_title(soup, map_type):
    if (map_type == "seed"):
        title_element = soup.find('span', class_='vtex-product-summary-2-x-brandName')
        return title_element.get_text().strip() if title_element else None
    # map_tree
    return None

def get_price(soup, map_type):
    if map_type == "seed":
        price = None
        price_element = soup.find("span", class_="vtex-product-price-1-x-sellingPriceValue")
        if price_element:
            currency_code = price_element.find("span", class_="vtex-product-price-1-x-currencyCode").get_text(strip=True)
            currency_integer = price_element.find("span", class_="vtex-product-price-1-x-currencyInteger").get_text(strip=True)
            currency_decimal = price_element.find("span", class_="vtex-product-price-1-x-currencyDecimal").get_text(strip=True)
            currency_fraction = price_element.find("span", class_="vtex-product-price-1-x-currencyFraction").get_text(strip=True)

            price = f"{currency_code} {currency_integer}{currency_decimal}{currency_fraction}"
        return price
    return None

def get_link_imagem(soup, map_type):
    if (map_type == "seed"):
        image_element = soup.find('img', class_='vtex-product-summary-2-x-imageNormal')
        return image_element['src'] if image_element else None
    # map_tree
    return None

def get_elements_tree(soup):
    title = get_title(soup, "tree")
    price = get_price(soup, "tree")
    link_imagem = get_link_imagem(soup, "tree")

    return title, price, link_imagem

def get_elements_seed(soup):
    product_link = get_product_link(soup, "seed")
    title = get_title(soup, "seed")
    price = get_price(soup, "seed")
    link_imagem = get_link_imagem(soup, "seed")

    return product_link, title, price, link_imagem

map_seed_conf = {
    "get_items": get_items,
    "get_last_page_index": get_last_page_index,
    "get_elements_seed": get_elements_seed,
    "get_next_url": get_next_url,
    "time": 8,
    "scroll_page": True,
    "return_text": False,
}

map_tree_conf = {
    "get_elements_tree": get_elements_tree,
    "time": 3,
    "scroll_page": True,
    "return_text": True,
}

def extract(conf):
    global CONF
    CONF = conf
    option = CONF["option"]

    driver = initialize_selenium()

    if (option == "init"):
        print("MAP FUNCTION: map_seed")
        map_seed(driver, CONF["data_path"], map_seed_conf)

        print("MAP FUNCTION: map_tree")
        map_tree(driver, CONF["data_path"], map_tree_conf)
    elif (option == "update_products"):
        print("MAP FUNCTION: map_seed")
        map_seed(driver, CONF["data_path"], map_seed_conf, True)
    elif (option == "update_pages"):
        print("MAP FUNCTION: map_tree")
        map_tree(driver, CONF["data_path"], map_tree_conf)

    driver.quit()