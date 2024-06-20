from datetime import date

import pandas as pd

from lib.crawler import crawler
from utils.general_functions import (DATE_FORMAT,
                                     create_directory_if_not_exists,
                                     create_or_read_df,
                                     delete_directory_and_contents,
                                     delete_file, download_images_in_parallel,
                                     file_exists, find_in_text_with_wordlist,
                                     get_old_files_by_percent, is_price,
                                     list_directory, read_json)
from utils.log import message
from utils.wordlist import BLACK_LIST


def run(conf, Page):
    conf["scroll_page"] = True
    conf["status_job"] = False
    conf["seed"] = False
    conf["tree"] = False

    if (conf['option'] == "init"):
        message("init")
        first_exec(conf["data_path"])

        conf["seed"] = True
        conf["tree"] = False
        page = Page(conf)
        seed(page)

        conf["seed"] = False
        conf["tree"] = True
        page = Page(conf)
        tree_update(page)

    elif (conf['option'] == "update_products"):
        message("update_products")
        conf["seed"] = True
        page = Page(conf)
        seed(page)
    elif (conf['option'] == "update_pages"):
        message("update_pages")
        conf["tree"] = True
        page = Page(conf)
        tree_update(page)
    elif (conf['option'] == "update_old_pages"):
        message("update_pages")
        conf["tree"] = True
        page = Page(conf)
        tree_update_old_pages(page)
    elif (conf['option'] == "create_pages"):
        message("create_pages")
        conf["tree"] = True
        page = Page(conf)
        tree_create(page)
    elif (conf['option'] == "status_job"):
        message("status_job")
        conf["scroll_page"] = False
        conf["seed"] = True
        conf['status_job'] = True
        page = Page(conf)
        seed(page)

def seed(page):
    seed_path = page.conf['seed_path'] + "/seed.json"
    seeds = read_json(seed_path)
    
    columns = ["ref", "title" ,"price" ,"image_url", "product_url", "ing_date"]
    path_origin = f"{page.conf['data_path']}/origin.csv"
    page.conf['path_origin'] = path_origin
    path_tree_temp = f"{page.conf['data_path']}/tree_temp.csv"
    delete_file(path_tree_temp)
    page.conf['path_tree_temp'] = path_tree_temp
    df_tree = create_or_read_df(path_origin, columns)

    data_atual = date.today()
    page.conf['formatted_date'] = data_atual.strftime(DATE_FORMAT)
    page.conf['df_tree'] = df_tree

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
                message(f"break size_items = 0")
                break
        page.reset_index()
    
    message(f"read file: {path_tree_temp}")
    df_tree_temp = pd.read_csv(path_tree_temp)
    df_tree_temp = df_tree_temp.drop_duplicates(subset='ref').reset_index(drop=True)
    df_tree_temp = df_tree_temp.dropna(subset=['price'])

    df_tree_temp = df_tree_temp[~df_tree_temp['title'].apply(lambda x: find_in_text_with_wordlist(x, BLACK_LIST))]
    df_tree_temp = df_tree_temp[df_tree_temp['price'].apply(lambda x: is_price(x))]

    path_tree_droped = f"{page.conf['data_path']}/tree_droped.csv"
    delete_file(path_tree_droped)
    message(f"read file: {path_tree_droped}")
    df_tree_droped = pd.read_csv(path_tree_temp)
    df_tree_droped = df_tree_temp[~df_tree_temp['ref'].isin(df_tree_droped['ref'].values)]
    df_tree_droped.to_csv(path_tree_droped, index=False)

    create_directory_if_not_exists(page.conf['data_path'] + "/img_tmp")
    download_images_in_parallel(df_tree_temp["image_url"].values, page.conf['data_path'] + "/img_tmp/", df_tree_temp["ref"].values)
    
    message(f"write origin: {path_origin}")
    df_tree_temp.to_csv(path_origin, index=False)

def tree_update(page):
    message("tree_update")
    path_origin = f"{page.conf['data_path']}/origin.csv"
    page.conf['path_origin'] = path_origin
    df_origin = pd.read_csv(path_origin)
    create_directory_if_not_exists(page.conf['data_path'] + "/products")

    urls = df_origin['product_url'].values
    for value, url in enumerate(urls):
        size_urls = len(urls) - 1
        message(f"seed: {url}")
        message(f"index: {value} / {size_urls}")
        crawler(page, url)

def tree_update_old_pages(page):
    message("update_old_pages")
    path_origin = f"{page.conf['data_path']}/origin.csv"
    page.conf['path_origin'] = path_origin
    df_origin = pd.read_csv(path_origin)

    pagas_path = page.conf['data_path'] + "/products"
    old_files = get_old_files_by_percent(pagas_path, True, 15)
    refs = [i.replace(".txt", "") for i in old_files]

    df_origin = df_origin[df_origin['ref'].isin(refs)]

    refs_to_delete = list(set(refs) - set(df_origin['ref']))
    if (refs_to_delete != []):
        for ref in refs_to_delete:
            delete_file(f"{pagas_path}/{ref}.txt")

    create_directory_if_not_exists(page.conf['data_path'] + "/products")

    urls = df_origin['product_url'].values
    for value, url in enumerate(urls):
        size_urls = len(urls) - 1
        message(f"seed: {url}")
        message(f"index: {value} / {size_urls}")
        crawler(page, url)

def tree_create(page):
    message("tree_create")
    path_origin = f"{page.conf['data_path']}/origin.csv"
    page.conf['path_origin'] = path_origin
    df_origin = pd.read_csv(path_origin)

    pagas_path = page.conf['data_path'] + "/products"
    all_pages = [i for i in list_directory(pagas_path)]
    refs = [f"{i}.txt" for i in df_origin['ref'].values]
    pages_to_create = [i.replace(".txt", "") for i in refs if i not in all_pages]
    df_origin = df_origin[df_origin["ref"].isin(pages_to_create)]

    print(pages_to_create)

    create_directory_if_not_exists(page.conf['data_path'] + "/products")

    urls = df_origin['product_url'].values
    for value, url in enumerate(urls):
        size_urls = len(urls) - 1
        message(f"seed: {url}")
        message(f"index: {value} / {size_urls}")
        crawler(page, url)
        
def first_exec(data_path):
    origin = file_exists(data_path, "origin.csv")
    tree = file_exists(data_path, "tree.csv")
    img_tmp = file_exists(data_path, "img_tmp")
    products = file_exists(data_path, "products")
    
    if (origin & tree & img_tmp & products):
        exit(0)

    if (origin or tree or img_tmp or products):
        delete_file(f"{data_path}/origin.csv")
        delete_file(f"{data_path}/tree.csv")
        delete_directory_and_contents(f"{data_path}/img_tmp")
        delete_directory_and_contents(f"{data_path}/products")

    message("First execution")