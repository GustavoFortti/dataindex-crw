import pandas as pd

from utils.log import message
from shared.data_quality import status_tag
import shared.selenium_service as se 
from utils.general_functions import (generate_hash,
                                     create_or_read_df,
                                     clean_string_break_line)

def crawler(job, url):
    message("exec crawler")
    if (("driver" not in job.conf.keys()) or (not job.conf["driver"])):
        message("initialize_selenium")
        job.conf["driver"] = se.initialize_selenium()
    
    driver = job.conf["driver"]

    element_selector = None
    se.load_url(driver, url, element_selector)
    load_page(driver, job, url)

def load_page(driver, job, url):
    message("exec load_page")

    if (job.conf['scroll_page']):
        se.dynamic_scroll(driver)

    soup, page_html = se.get_page_source(driver)
    if (job.conf['seed']):
        extract_data(job, soup)

    if (job.conf['tree']):
        ref = generate_hash(url)
        data_path = job.conf['data_path']
        file_name = f"{data_path}/products/{ref}.txt"
        with open(file_name, 'w') as file:
            file.write(page_html)
            message(f"File '{file_name}' created successfully.")

def extract_data(job, soup):
    message("exec extract_data")
    path_tree_temp = job.conf['path_tree_temp']
    df_tree_temp = create_or_read_df(path_tree_temp, job.conf['df_tree'].columns)
    size_tree_temp = len(df_tree_temp)
    items = job.get_items(soup)
    size_items = len(items)
    job.conf['size_items'] = size_items

    if (size_items == 0):
        message("size_items: 0")
        return

    for item in items:
        
        product_url, title, price, image_url = job.get_elements_seed(item)
        ref = generate_hash(product_url)

        if (price): price = clean_string_break_line(price)
        if (title): title = clean_string_break_line(title)

        data = {
            'ref': ref,
            'product_url': product_url,
            'title': title,
            'price': price,
            'image_url': image_url,
            'ing_date': job.conf['formatted_date']
        }

        if (job.conf["status_job"]):
            status_tag(data)

        message(data)
        temp_df = pd.DataFrame([data])
        df_tree_temp = pd.concat([df_tree_temp, temp_df], ignore_index=True)
        df_tree_temp.to_csv(path_tree_temp, index=False)

    df_tree_temp = df_tree_temp.drop_duplicates(subset='ref').reset_index(drop=True)

    if (size_tree_temp == len(df_tree_temp)):
        message("No change in dataframe")
        job.conf['size_items'] = 0
        return

    df_tree_temp.to_csv(path_tree_temp, index=False)
    message("df_tree_temp saved")