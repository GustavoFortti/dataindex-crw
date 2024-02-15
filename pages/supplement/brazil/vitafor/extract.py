import re
from shared.selenium_service import initialize_selenium
from shared.extractor import map_tree, map_seed

from utils.general_functions import first_exec

def get_last_page_index(soup=None):
    return 40

def get_next_url(url, index):
    return url

def get_items(soup):
    items = soup.find_all('article', class_='vtex-product-summary-2-x-element')
    print(items[0])
    exit(0)
    return items

def get_product_url(soup, map_type):
    if (map_type == "seed"):
        # Tentativa de encontrar um elemento de link envolvendo o título ou a imagem, se houver
        product_element = soup.find('a', class_='vtex-product-summary-2-x-clearLink')
        product_link = product_element['href'] if product_element else None
        return product_link
    # map_tree
    return None

def get_title(soup, map_type):
    if (map_type == "seed"):
        title_element = soup.find('h3', class_='vtex-product-summary-2-x-productNameContainer')
        title = title_element.get_text().strip() if title_element else None
        return title
    # map_tree
    return None

def get_price(soup, map_type):
    if (map_type == "seed"):
        price_element = soup.find('div', class_='vtex-product-summary-2-x-sellingPrice')
        price = price_element.get_text().strip() if price_element else None
        return price
    # map_tree
    return None

def get_image_url(soup, map_type):
    if (map_type == "seed"):
        image_element = soup.find('img', class_='vtex-product-summary-2-x-imageNormal')
        image_link = image_element['src'] if image_element else None
        return image_link
    # map_tree
    return None

def get_elements_tree(soup):
    title = get_title(soup, "tree")
    price = get_price(soup, "tree")
    link_imagem = get_image_url(soup, "tree")

    return title, price, link_imagem

def get_elements_seed(soup):
    product_link = get_product_url(soup, "seed")
    title = get_title(soup, "seed")
    price = get_price(soup, "seed")
    link_imagem = get_image_url(soup, "seed")

    return product_link, title, price, link_imagem

map_seed_conf = {
    "get_items": get_items,
    "get_last_page_index": get_last_page_index,
    "get_elements_seed": get_elements_seed,
    "get_next_url": get_next_url,
    "time_sleep_page": 3,
    "scroll_page": True,
    "return_text": False,
}

map_tree_conf = {
    "get_elements_tree": get_elements_tree,
    "time_sleep_page": 1,
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
        first_exec(conf["data_path"])
        
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
    elif (option == "status_job"):
        print("STATUS_JOB - MAP FUNCTION: map_seed")
        map_seed_conf["scroll_page"] = False
        map_seed(driver, map_seed_conf)

    driver.quit()