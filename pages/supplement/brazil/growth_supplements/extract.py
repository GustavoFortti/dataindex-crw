from shared.selenium_service import initialize_selenium
from shared.extractor import map_tree, map_seed

def get_last_page_index(soup=None):
    try:
        last_page_elemt = soup.find('button', class_='ultima')
        onclick_value = last_page_elemt['onclick'].split('/')[-1:][0][:-1]
        last_page_num = int(onclick_value)
    except:
        last_page_num = 2

    return last_page_num

def get_next_url(url, index):
    return url + str(index)

def get_items(soup):
    items = soup.find_all('div', class_='vitrine-prod')
    return items

def get_product_link(soup, map_type):
    if (map_type == "seed"):
        product_link_element = soup.find('a', class_='vitrine-nomeProduto')
        return product_link_element['href'] if product_link_element else None
    # map_tree
    return None

def get_title(soup, map_type):
    if (map_type == "seed"):
        title_element = soup.find('a', class_='vitrine-nomeProduto')
        return title_element.get_text().strip() if title_element else None
    # map_tree
    return None

def get_price(soup, map_type):
    if (map_type == "seed"):
        price_element = soup.find('span', class_='vitrine-valor')
        return price_element.get_text().strip() if price_element else None
    # map_tree
    return None

def get_link_imagem(soup, map_type):
    if (map_type == "seed"):
        image_element = soup.find('img', class_='lazy')
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
    "time": 5,
    "scroll_page": False,
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