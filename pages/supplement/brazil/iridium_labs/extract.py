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
        final_price = None
        price_container = soup.find(class_="t4s-product-price")
        
        if price_container:
            # Verifica se existe um desconto
            discount_price_element = price_container.find("ins")
            if discount_price_element:
                final_price = discount_price_element.text.strip()
            else:
                # Se não houver desconto, procura pela tag span com classe t4s-price__sale
                sale_price_element = price_container.find("span", class_="t4s-price__sale")
                if sale_price_element:
                    # Extrai todos os preços usando expressão regular
                    prices = re.findall(r"\d+,\d+", sale_price_element.text)
                    # Converte os preços para float e seleciona o menor
                    prices = [float(price.replace(',', '.')) for price in prices]
                    final_price = f"R$ {min(prices):.2f}".replace('.', ',')
                else:
                    # Se não houver intervalo de preços, pega o preço padrão
                    standard_price_element = price_container.text.strip()
                    if standard_price_element:
                        final_price = standard_price_element
        
        return final_price
    return None

def get_link_imagem(soup, map_type):
    if map_type == "seed":
        image_element = soup.find(class_='t4s-product-main-img')
        if (image_element and 'srcset' in image_element.attrs):
            srcset = image_element['srcset']
            image_urls = [img.strip() for img in srcset.split(',')]
            highest_res_image = image_urls[-1].split(' ')[0]
            image_link = "https:" + highest_res_image
            return image_link
        elif (image_element and 'src' in image_element.attrs):
            image_link = "https:" + image_element['src']
            return image_link
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
        map_seed(driver, map_seed_conf, True)
    elif (option == "update_pages"):
        print("MAP FUNCTION: map_tree")
        map_tree(driver, map_tree_conf)
    elif (option == "status_job"):
        print("STATUS_JOB - MAP FUNCTION: map_seed")
        map_seed_conf["scroll_page"] = False
        map_seed(driver, map_seed_conf)

    driver.quit()