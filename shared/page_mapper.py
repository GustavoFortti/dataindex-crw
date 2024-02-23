import pandas as pd
from datetime import date

from utils.log import message
from shared.crawler import crawler
from utils.wordlist import BLACK_LIST
from utils.general_functions import (DATE_FORMAT,
                                    read_json,
                                    first_exec,
                                    create_or_read_df,
                                    delete_file,
                                    list_directory,
                                    download_images_in_parallel,
                                    find_in_text_with_word_list,
                                    create_directory_if_not_exists,
                                    is_price)

def run(conf, Job):
    conf["scroll_page"] = True
    conf["status_job"] = False
    conf["seed"] = False
    conf["tree"] = False

    if (conf['option'] == "init"):
        message("init")
        first_exec(conf["data_path"])

        conf["seed"] = True
        conf["tree"] = False
        job = Job(conf)
        seed(job)

        conf["seed"] = False
        conf["tree"] = True
        job = Job(conf)
        tree_update(job)

    elif (conf['option'] == "update_products"):
        message("update_products")
        conf["seed"] = True
        job = Job(conf)
        seed(job)
    elif (conf['option'] == "update_pages"):
        message("update_pages")
        conf["tree"] = True
        job = Job(conf)
        tree_update(job)
    elif (conf['option'] == "extract_new_pages"):
        message("extract_new_pages")
        conf["tree"] = True
        job = Job(conf)
        tree_create(job)
    elif (conf['option'] == "status_job"):
        message("status_job")
        conf["scroll_page"] = False
        conf["seed"] = True
        conf['status_job'] = True
        job = Job(conf)
        seed(job)

def seed(job):
    seed_path = job.conf['seed_path'] + "/seed.json"
    seeds = read_json(seed_path)
    
    columns = ["ref", "title" ,"price" ,"image_url", "product_url", "ing_date"]
    path_origin = f"{job.conf['data_path']}/origin.csv"
    job.conf['path_origin'] = path_origin
    path_tree_temp = f"{job.conf['data_path']}/tree_temp.csv"
    delete_file(path_tree_temp)
    job.conf['path_tree_temp'] = path_tree_temp
    df_tree = create_or_read_df(path_origin, columns)

    data_atual = date.today()
    job.conf['formatted_date'] = data_atual.strftime(DATE_FORMAT)
    job.conf['df_tree'] = df_tree

    job.conf["size_items"] = 0
    for value, seed in enumerate(seeds):
        message(f"seed: {seed}")
        message(f"index seed: {value} / {len(seeds)}")
        while True:
            url = job.get_url(seed['url'])
            index = job.conf["index"]
            message(f"index url: {index}")
            message(f"url: {url}")
            
            crawler(job, url)

            if ((job.conf["size_items"] == 0) | (not index)):
                message(f"break size_items = 0")
                break
        job.reset_index()
    
    message(f"read file: {path_tree_temp}")
    df_tree_temp = pd.read_csv(path_tree_temp)
    df_tree_temp = df_tree_temp.drop_duplicates(subset='ref').reset_index(drop=True)
    df_tree_temp = df_tree_temp.dropna(subset=['price'])

    df_tree_temp = df_tree_temp[~df_tree_temp['title'].apply(lambda x: find_in_text_with_word_list(x, BLACK_LIST))]
    df_tree_temp = df_tree_temp[df_tree_temp['price'].apply(lambda x: is_price(x))]

    path_tree_droped = f"{job.conf['data_path']}/tree_droped.csv"
    delete_file(path_tree_droped)
    message(f"read file: {path_tree_droped}")
    df_tree_droped = pd.read_csv(path_tree_temp)
    df_tree_droped = df_tree_temp[~df_tree_temp['ref'].isin(df_tree_droped['ref'].values)]
    df_tree_droped.to_csv(path_tree_droped, index=False)

    create_directory_if_not_exists(job.conf['data_path'] + "/img_tmp")
    download_images_in_parallel(df_tree_temp["image_url"].values, job.conf['data_path'] + "/img_tmp/", df_tree_temp["ref"].values)
    
    message(f"write origin: {path_origin}")
    df_tree_temp.to_csv(path_origin, index=False)

def tree_update(job):
    message("tree_update")
    path_origin = f"{job.conf['data_path']}/origin.csv"
    job.conf['path_origin'] = path_origin
    df_origin = pd.read_csv(path_origin)
    create_directory_if_not_exists(job.conf['data_path'] + "/products")

    urls = df_origin['product_url'].values
    for value, url in enumerate(urls):
        size_urls = len(urls) - 1
        message(f"seed: {url}")
        message(f"index: {value} / {size_urls}")
        crawler(job, url)

def tree_create(job):
    message("tree_create")
    path_origin = f"{job.conf['data_path']}/origin.csv"
    job.conf['path_origin'] = path_origin
    df_origin = pd.read_csv(path_origin)

    pagas_path = job.conf['data_path'] + "/products"
    all_pages = [i for i in list_directory(pagas_path)]
    refs = [f"{i}.txt" for i in df_origin['ref'].values]
    pages_to_create = [i.replace(".txt", "") for i in refs if i not in all_pages]
    df_origin = df_origin[df_origin["ref"].isin(pages_to_create)]

    print(pages_to_create)

    create_directory_if_not_exists(job.conf['data_path'] + "/products")

    urls = df_origin['product_url'].values
    for value, url in enumerate(urls):
        size_urls = len(urls) - 1
        message(f"seed: {url}")
        message(f"index: {value} / {size_urls}")
        crawler(job, url)