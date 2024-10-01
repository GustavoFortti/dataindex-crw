from datetime import date

import pandas as pd

from src.lib.extract.crawler import crawler
from src.lib.extract.page_elements import Page
from src.lib.utils.data_quality import is_price
from src.lib.utils.dataframe import create_or_read_df
from src.lib.utils.file_system import (DATE_FORMAT, create_directory_if_not_exists,
                                   delete_directory_and_contents, delete_file,
                                   get_old_files_by_percent, list_directory,
                                   read_json, save_images)
from src.lib.utils.log import message
from src.lib.utils.text_functions import find_in_text_with_wordlist
from src.lib.wordlist.wordlist import BLACK_LIST


def extract(conf: dict):
    message("EXTRACT")
    page = Page(conf)

    if (conf['exec_flag'] == "new_page"):
        message("initializing_new_page")
        delete_directory_and_contents(f"{conf["data_path"]}/*")

        conf["products_update"] = True
        products_update(page)

        conf["products_update"] = False
        conf["products_metadata_update"] = True
        page = Page(conf)
        products_metadata_update(page)
        
    if (conf['exec_flag'] == "products_update"):
        conf["products_update"] = True
        page = Page(conf)
        products_update(page)
    elif (conf['exec_flag'] == "products_metadata_update"):
        conf["products_metadata_update"] = True
        page = Page(conf)
        products_metadata_update(page)
    elif (conf['exec_flag'] == "products_metadata_update_old_pages"):
        conf["products_metadata_update"] = True
        page = Page(conf)
        products_metadata_update_old_pages(page)
    elif (conf['exec_flag'] == "products_metadata_create_pages_if_not_exist"):
        conf["products_metadata_update"] = True
        page = Page(conf)
        products_metadata_create_pages_if_not_exist(page)
    elif (conf['exec_flag'] == "status_job"):
        conf["scroll_page"] = False
        conf["products_update"] = True
        conf['status_job'] = True
        page = Page(conf)
        products_update(page)


def products_update(page):
    seed_path = page.conf['seed_path'] + "/seed.json"
    seeds = read_json(seed_path)
    
    page.conf['products_extract_csl'] = f"{page.conf['data_path']}/products_extract_csl.csv"
    page.conf['path_products_extract_temp'] = f"{page.conf['data_path']}/products_extract_temp.csv"
    delete_file(page.conf['path_products_extract_temp'])
    
    columns = ["ref", "title" ,"price" ,"image_url", "product_url", "ing_date"]
    df_products = create_or_read_df(page.conf['products_extract_csl'], columns)

    data_atual = date.today()
    page.conf['formatted_date'] = data_atual.strftime(DATE_FORMAT)
    page.conf['df_products'] = df_products

    page.conf["size_items"] = 0
    for value, seed in enumerate(seeds):
        message(f"seed: {seed}")
        message(f"index seed: {value} / {len(seeds)}")
        while True:
            url = page.get_url(seed['url'])
            index = page.conf["index"]
            message(f"index url: {index}")
            message(f"url: {url}")
            
            crawler(page, url)

            if ((page.conf["size_items"] == 0) | (not index)):
                message(f"size_items = {page.conf["size_items"]}")
                message(f"index = {index}")
                message("EXECUTANDO PROXIMA SEED - devido ao index ou size_items")
                break
        page.reset_index()
    
    message(f"read file: {page.conf['path_products_extract_temp']}")
    df_products_extract_temp = pd.read_csv(page.conf['path_products_extract_temp'])
    df_products_extract_temp = df_products_extract_temp.drop_duplicates(subset='ref').reset_index(drop=True)
    df_products_extract_temp = df_products_extract_temp.dropna(subset=['price'])

    df_products_extract_temp = df_products_extract_temp[~df_products_extract_temp['title'].apply(lambda x: find_in_text_with_wordlist(x, BLACK_LIST))]
    df_products_extract_temp = df_products_extract_temp[df_products_extract_temp['price'].apply(lambda x: is_price(x))]

    create_directory_if_not_exists(page.conf['data_path'] + "/img_tmp")
    save_images(df_products_extract_temp["image_url"].values, page.conf['data_path'] + "/img_tmp/", df_products_extract_temp["ref"].values)
    
    message(f"write origin: {page.conf['products_extract_csl']}")
    df_products_extract_temp.to_csv(page.conf['products_extract_csl'], index=False)


def products_metadata_update(page):
    message("products_metadata_update")
    page.conf['products_extract_csl'] = f"{page.conf['data_path']}/products_extract_csl.csv"
    df_products_extract_csl = pd.read_csv(page.conf['products_extract_csl'])

    urls = df_products_extract_csl['product_url'].values
    for value, url in enumerate(urls):
        size_urls = len(urls) - 1
        message(f"seed: {url}")
        message(f"index: {value} / {size_urls}")
        crawler(page, url)


def products_metadata_update_old_pages(page):
    message("PRODUCTS_METADATA_UPDATE_OLD_PAGES")
    products_extract_csl = f"{page.conf['data_path']}/products_extract_csl.csv"
    page.conf['products_extract_csl'] = products_extract_csl
    df_products_extract_csl = pd.read_csv(products_extract_csl)

    pagas_path = page.conf['data_path'] + "/products"
    old_files = get_old_files_by_percent(pagas_path, True, 5)
    refs = [i.replace(".txt", "") for i in old_files]

    df_products_extract_csl = df_products_extract_csl[df_products_extract_csl['ref'].isin(refs)]

    refs_to_delete = list(set(refs) - set(df_products_extract_csl['ref']))
    if (refs_to_delete != []):
        for ref in refs_to_delete:
            delete_file(f"{pagas_path}/{ref}.txt")

    create_directory_if_not_exists(page.conf['data_path'] + "/products")

    urls = df_products_extract_csl['product_url'].values
    for value, url in enumerate(urls):
        size_urls = len(urls) - 1
        message(f"seed: {url}")
        message(f"index: {value} / {size_urls}")
        crawler(page, url)


def products_metadata_update_old_pages_by_ref(conf: dict, Page: object, url: str):
    message("update_old_page by ref if page is with error in tags")
    conf["scroll_page"] = True
    conf["status_job"] = False
    conf["products_metadata_update"] = True
    conf["products_update"] = False
    
    page = Page(conf)
    message(f"seed: {url}")
    crawler(page, url)


def products_metadata_create_pages_if_not_exist(page):
    message("PRODUCTS_METADATA_CREATE_PAGES_IF_NOT_EXIST")
    products_extract_csl = f"{page.conf['data_path']}/products_extract_csl.csv"
    page.conf['products_extract_csl'] = products_extract_csl
    df_products_extract_csl = pd.read_csv(products_extract_csl)

    pagas_path = page.conf['data_path'] + "/products"
    all_pages = [i for i in list_directory(pagas_path)]
    refs = [f"{i}.txt" for i in df_products_extract_csl['ref'].values]
    pages_to_create = [i.replace(".txt", "") for i in refs if i not in all_pages]
    df_products_extract_csl = df_products_extract_csl[df_products_extract_csl["ref"].isin(pages_to_create)]

    message(f"pages_to_create -> {pages_to_create}")

    create_directory_if_not_exists(page.conf['data_path'] + "/products")

    urls = df_products_extract_csl['product_url'].values
    for value, url in enumerate(urls):
        size_urls = len(urls) - 1
        message(f"seed: {url}")
        message(f"index: {value} / {size_urls}")
        crawler(page, url)