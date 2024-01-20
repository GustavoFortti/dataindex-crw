from shared.selenium_service import initialize_selenium
from shared.extractor_functions import map_tree, map_seed

def get_last_page_index(soup=None):
    return 1

def get_next_url(url, index):
    return url

def get_items(soup):
    items = soup.find_all('div', class_='product-grid-item')

    return items

def get_product_link(soup, map_type):
    if (map_type == "seed"):
        product_link_element = soup.find('a', class_='product__media__holder')
        product_link = "https://www.boldsnacks.com.br" + product_link_element['href'] if product_link_element else None
        return product_link
    # map_tree
    return None

def get_title(soup, map_type):
    if (map_type == "seed"):
        title_element = soup.find('a', class_='product-grid-item__title')
        title = title_element.get_text().strip() if title_element else None
        return title
    # map_tree
    return None

def get_price(soup, map_type):
    if map_type == "seed":
        price_element = soup.find('a', class_='product-grid-item__price price')
        if price_element:
            price_span = price_element.find('span', class_='product-grid-item__price__new')
            if price_span:
                return price_span.get_text().strip()
            else:
                return price_element.get_text().strip()
    # map_tree
    return None

def get_link_imagem(soup, map_type):
    if (map_type == "seed"):
        image_container = soup.find('picture')
        link_imagem = None
        if image_container:
            image_element = image_container.find('source')
            link_imagem = image_element['srcset'].split(" ")[3] if image_element else None
            link_imagem = ("https:" + link_imagem if link_imagem[:2] == "//" else link_imagem)
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
    "time": 3,
    "scroll_page": True,
    "return_text": False,
}

map_tree_conf = {
    "get_elements_tree": get_elements_tree,
    "time": 1,
    "scroll_page": True,
    "return_text": True,
}

def extract(conf):
    option = conf["option"]

    map_seed_conf["option"] = conf["option"]
    map_seed_conf["data_path"] = conf["data_path"]
    map_seed_conf["seed_path"] = conf["seed_path"]

    map_tree_conf["option"] = conf["option"]
    map_tree_conf["data_path"] = conf["data_path"]

    driver = initialize_selenium()

    if (option == "init"):
        print("MAP FUNCTION: map_seed")
        map_seed(driver, map_seed_conf)

        print("MAP FUNCTION: map_tree")
        map_tree(driver, map_tree_conf)
    elif (option == "update_products"):
        print("MAP FUNCTION: map_seed")
        map_seed(driver, map_seed_conf, True)
    elif (option == "update_pages"):
        print("MAP FUNCTION: map_tree")
        map_tree(driver, map_tree_conf)
    elif (option == "test_tag"):
        print("MAP FUNCTION: map_seed")
        map_seed_conf["scroll_page"] = False
        map_seed(driver, map_seed_conf)

    driver.quit()