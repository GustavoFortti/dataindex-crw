from shared.selenium_service import initialize_selenium
from shared.extractor_functions import map_tree, map_seed

def get_last_page_index(soup=None):
    return 1

def get_next_url(url, index):
    return url

def get_items(soup):
    items = soup.find_all('div', class_='box-item')

    return items

def get_product_link(soup, map_type):
    if (map_type == "seed"):
        product_link_element = soup.find('a', class_='product-image')
        product_link =  product_link_element['href'] if product_link_element else None
        return product_link
    # map_tree
    return None

def get_title(soup, map_type):
    if (map_type == "seed"):
        title_element = soup.find('p', class_='product-name')
        title = title_element.get_text().strip() if title_element else None
        return title
    # map_tree
    return None

def get_price(soup, map_type):
    if (map_type == "seed"):
        price_element = soup.find('span', class_='best-price')
        price = price_element.get_text().strip() if price_element else None
        return price
    # map_tree
    return None

def get_link_imagem(soup, map_type):
    if (map_type == "seed"):
        image_container = soup.find('div', class_='_lazy-box has--lazyload is--lazyloaded')
        link_imagem = None
        if image_container:
            image_element = image_container.find('img')
            link_imagem = image_element['src'] if image_element else None
        return link_imagem
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