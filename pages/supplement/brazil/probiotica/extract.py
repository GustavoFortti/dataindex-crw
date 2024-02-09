from shared.selenium_service import initialize_selenium
from shared.extractor import map_tree, map_seed

from utils.general_functions import first_exec

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
        product_link =  "https://www.probiotica.com.br" +  product_link_element['href'] if product_link_element else None
        return product_link
    # map_tree
    return None

def get_title(soup, map_type):
    if (map_type == "seed"):
        title_element = soup.find('h2', class_='vtex-product-summary-2-x-productNameContainer')
        if title_element:
            span_element = title_element.find('span', class_='vtex-product-summary-2-x-productBrand')
            title = span_element.text.strip() if span_element else None
        else:
            title = None
        return title
    # map_tree
    title_element = soup.find('h1', class_='vtex-store-components-3-x-productNameContainer')
    if title_element:
        title_spans = title_element.find_all('span', class_='vtex-store-components-3-x-productBrand')
        title = ' '.join(span.text for span in title_spans).strip()
    else:
        title = None

    return title

def get_price(soup, map_type):
    if (map_type == "seed"):
        price = None
        price_element = soup.find('span', class_='vtex-product-price-1-x-sellingPriceValue')
        if price_element:
            currency_container = price_element.find('span', class_='vtex-product-price-1-x-currencyContainer')
            if currency_container:
                price = ''.join([elem.text for elem in currency_container.find_all('span')])
                price = price.replace('\xa0', ' ').strip()
        return price
    # map_tree
    return None

def get_link_imagem(soup, map_type):
    if (map_type == "seed"):
        image_element = soup.find('img', class_='vtex-product-summary-2-x-imageNormal vtex-product-summary-2-x-image')
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
        map_seed(driver, map_seed_conf, True, ["preco", "link_imagem"])
    elif (option == "update_pages"):
        print("MAP FUNCTION: map_tree")
        map_tree(driver, map_tree_conf)
    elif (option == "status_job"):
        print("STATUS_JOB - MAP FUNCTION: map_seed")
        map_seed_conf["scroll_page"] = False
        map_seed(driver, map_seed_conf)

    driver.quit()