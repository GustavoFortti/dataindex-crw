import time

import pandas as pd
from src.lib.utils.log import message

import src.lib.extract.selenium_service as se
from src.lib.utils.data_quality import status_tag
from src.lib.utils.dataframe import create_or_read_df
from src.lib.utils.text_functions import clean_string_break_line, generate_hash
from src.lib.utils.file_system import read_file, save_file

def crawler(page, url):
    message("exec crawler")
    if (("driver" not in page.conf.keys()) or (not page.conf["driver"])):
        message("initialize_selenium")
        page.conf["driver"] = se.initialize_selenium(page.conf)
    
    load_page(page, url)

def load_page(page, url):
    message("exec load_page")

    driver = page.conf["driver"]

    if (page.conf['products_update']):
        message("PRODUCTS_UPDATE")

        element_selector = None
        se.load_url(driver, url, element_selector)

        time_sleep = page.conf['dynamic_scroll']['time_sleep']
        scroll_step = page.conf['dynamic_scroll']['scroll_step']
        percentage = page.conf['dynamic_scroll']['percentage']
        return_percentage = page.conf['dynamic_scroll']['return_percentage']
        max_return = page.conf['dynamic_scroll']['max_return']
        max_attempts = page.conf['dynamic_scroll']['max_attempts']
        
        start_time_sleep = page.conf['dynamic_scroll']['start_time_sleep'] + 2
        message(str(start_time_sleep) + " seconds")
        time.sleep(start_time_sleep)

        if (page.conf['scroll_page']):
            se.dynamic_scroll(
                driver=driver,
                time_sleep=time_sleep,
                scroll_step=scroll_step,
                percentage=percentage,
                return_percentage=return_percentage,
                max_return=max_return,
                max_attempts=max_attempts
            )
            
        if (page.conf["status_job"]):
            se.dynamic_scroll(
                driver=driver,
                time_sleep=0.4,
                scroll_step=1000,
                percentage=0.5,
                return_percentage=0.1,
                max_return=100,
                max_attempts=2
            )

        soup, page_html = se.get_page_source(driver)
        
        page.conf["soup"] = soup
        
        extract_data(page, soup)

    if (page.conf['products_metadata_update']):
        message("PRODUCTS_METADATA_UPDATE")
        ref = generate_hash(url)
        data_path = page.conf['data_path']
        file_name = f"{data_path}/products/{ref}.txt"
        
        time.sleep(1)

        se.load_url(driver, url)
        se.dynamic_scroll(
            driver=driver,
            time_sleep=0.5,
            scroll_step=500,
            percentage=0.5,
            return_percentage=0.1,
            max_return=100,
            max_attempts=2
        )
        
        soup, page_text = se.get_page_source(driver)

        with open(file_name, 'w') as file:
            file.write(page_text)
            message(f"File '{file_name}' created successfully.")

def extract_data(page, soup):
    message("exec extract_data")
    path_products_extract_temp = page.conf['path_products_extract_temp']
    df_products_temp = create_or_read_df(path_products_extract_temp, page.conf['df_products'].columns)
    size_products_temp = len(df_products_temp)
    items = page.get_items(soup)
    size_items = len(items)
    message(f"size_items = {size_items}")
    page.conf['size_items'] = size_items

    if (size_items == 0):
        index = page.conf["index"]
        message(f"size_items: 0 - não foram encontrados produtos na pagina numero {index}")
        message(items)
        if (index == 1):
            message("ERRO size_items: 0 - não foram encontrados produtos na primeira pagina, necessario validar extração da pagina")
            message("Finalizando programa com erro")
            exit(1)
    
    message(f"size_items valido para extração")
    count_size_items = 0
    for item in items:
        message(f"INDEX: {abs(count_size_items)} item")
        
        product_url, title, price, image_url = page.get_item_elements(item)
        ref = generate_hash(product_url)
        message(f"generete ref - {ref}")

        if (price): price = clean_string_break_line(price)
        if (title): title = clean_string_break_line(title)

        data = {
            'ref': ref,
            'product_url': product_url,
            'title': title,
            'price': price,
            'image_url': image_url,
            'ing_date': page.conf['formatted_date']
        }

        category = page.conf['seed'].get("category", False)
        if (category):
            file_path = f"{page.conf['src_data_path']}/{page.conf['page_name']}/products/{ref}_class.txt"
            file_content = read_file(file_path)
            
            if (file_content):
                categorys = list(set(file_content.split(",")))
                categorys.append(category)
                categorys = str(list(set(categorys)))[1:-1]
            
            save_file(categorys, file_path)
        
        message(data)
        if (page.conf["status_job"]):
            status_tag(page, data)

        temp_df = pd.DataFrame([data])
        df_products_temp = pd.concat([df_products_temp, temp_df], ignore_index=True)
        df_products_temp.to_csv(path_products_extract_temp, index=False)
        
        count_size_items -= 1

    df_products_temp = df_products_temp.drop_duplicates(subset='ref').reset_index(drop=True)

    if (size_products_temp == len(df_products_temp)):
        message("No change in dataframe")
        page.conf['size_items'] = 0
        return

    df_products_temp.to_csv(path_products_extract_temp, index=False)
    message("df_products_temp saved")