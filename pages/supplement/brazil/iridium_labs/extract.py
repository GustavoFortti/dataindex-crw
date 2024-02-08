import re
from shared.selenium_service import initialize_selenium
from shared.extractor import map_tree, map_seed

from utils.general_functions import first_exec

def get_last_page_index(soup=None):
    return 1

def get_next_url(url, index):
    return url

def get_items(soup):
    items = []
    items_container = soup.find_all('div', class_='t4s-product-wrapper')
    for item in items_container:
        if (not re.search("cdn.shopify.com", str(item))):
            items.append(item)
    return items

def get_product_link(soup, map_type):
    if (map_type == "seed"):
        product_link_element = soup.find('a', class_='t4s-full-width-link')
        return "https://www.iridiumlabs.com.br" + product_link_element['href'] if product_link_element else None
    # map_tree
    return None

def get_title(soup, map_type):
    if (map_type == "seed"):
        title_element = soup.find('h3', class_='t4s-product-title')
        return title_element.get_text().strip() if title_element else None
    # map_tree
    return None

def get_price(soup, map_type):
    if map_type == "seed":
        price = None
        price_container = soup.find(class_="t4s-product-price")
        if price_container:
            price_element = price_container.find("ins") 
            price = price_element.text.strip() if price_element else None 
        return price
    return None

def get_link_imagem(soup, map_type):
    if (map_type == "seed"):
        image_element = soup.find(class_='t4s-product-main-img')
        image = "https:" + image_element['src'] if image_element else None
        return image
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
    "time_sleep_page": 3,
    "scroll_page": [{"time_sleep": 0.3, "size_height": 1000}, {"time_sleep": 0.3, "size_height": 100}],
    "return_text": False,
}

map_tree_conf = {
    "get_elements_tree": get_elements_tree,
    "time": 1,
    "scroll_page": [{"time_sleep": 0.2, "size_height": 500}],
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