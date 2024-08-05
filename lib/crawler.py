import asyncio
import time

import pandas as pd
from pyppeteer import launch

import lib.selenium_service as se
from lib.data_quality import status_tag
from utils.general_functions import (clean_string_break_line,
                                     create_or_read_df, generate_hash)
from utils.log import message

def crawler(page, url):
    message("exec crawler")
    if (("driver" not in page.conf.keys()) or (not page.conf["driver"])):
        message("initialize_selenium")
        if (page.conf['seed']):
            page.conf["driver"] = se.initialize_selenium()
    
    load_page(page, url)

def load_page(page, url):
    message("exec load_page")

    driver = None

    if (page.conf['seed']):
        message("seed")
        message("3 seconds")
        time.sleep(3)

        driver = page.conf["driver"]

        element_selector = None
        se.load_url(driver, url, element_selector)

        time_sleep = page.conf['dynamic_scroll']['time_sleep']
        scroll_step = page.conf['dynamic_scroll']['scroll_step']
        percentage = page.conf['dynamic_scroll']['percentage']
        return_percentage = page.conf['dynamic_scroll']['return_percentage']
        max_return = page.conf['dynamic_scroll']['max_return']
        max_attempts = page.conf['dynamic_scroll']['max_attempts']

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
            se.dynamic_scroll(driver,
                time_sleep=0.4,
                scroll_step=1000,
                percentage=0.5,
                return_percentage=0.1,
                max_return=100,
                max_attempts=2
            )

        soup, page_html = se.get_page_source(driver)
        
        extract_data(page, soup)

    if (page.conf['tree']):
        message("tree")
        ref = generate_hash(url)
        data_path = page.conf['data_path']
        file_name = f"{data_path}/products/{ref}.txt"
        
        time.sleep(1)
        if (("driver" not in page.conf.keys()) or (not page.conf["driver"])):
            driver = se.initialize_selenium()

        se.load_url(driver, url)
        se.dynamic_scroll(driver, time_sleep=0.5, scroll_step=500, percentage=0.5, return_percentage=0.1, max_return=100, max_attempts=2)
        soup, page_text = se.get_page_source(driver)

        with open(file_name, 'w') as file:
            file.write(page_text)
            message(f"File '{file_name}' created successfully.")

async def get_page_text(url, retries=3, delay=1):
    attempt = 0
    while attempt < retries:
        browser = None
        page_html = None
        try:
            browser = await launch()
            page_html = await browser.newPage()
            await page_html.goto(url, {'timeout': 30000})
            await page_html.waitForSelector('body', {'timeout': 30000})
            page_content = await page_html.content()
            return page_content
        except Exception as e:
            message(f"Erro ao tentar acessar {url}: {e}")
            attempt += 1
            await asyncio.sleep(delay)
            delay *= 2
        finally:
            if page_html:
                try:
                    await page_html.goto('about:blank')
                except Exception as e:
                    message(f"Erro ao navegar para about:blank: {e}")
                try:
                    await page_html.close()
                except Exception as e:
                    message(f"Erro ao fechar a página: {e}")
            if browser:
                try:
                    await browser.close()
                except Exception as e:
                    message(f"Erro ao fechar o navegador: {e}")

    message(f"Não foi possível acessar {url} após {retries} tentativas.")
    return None

def extract_data(page, soup):
    message("exec extract_data")
    path_tree_temp = page.conf['path_tree_temp']
    df_tree_temp = create_or_read_df(path_tree_temp, page.conf['df_tree'].columns)
    size_tree_temp = len(df_tree_temp)
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
    
    message(f"size_items valido")
    count_size_items = 0
    for item in items:
        message(f"size_items {count_size_items}")
        
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

        message(data)
        if (page.conf["status_job"]):
            status_tag(data)

        temp_df = pd.DataFrame([data])
        df_tree_temp = pd.concat([df_tree_temp, temp_df], ignore_index=True)
        df_tree_temp.to_csv(path_tree_temp, index=False)
        
        count_size_items -= 1

    df_tree_temp = df_tree_temp.drop_duplicates(subset='ref').reset_index(drop=True)

    if (size_tree_temp == len(df_tree_temp)):
        message("No change in dataframe")
        page.conf['size_items'] = 0
        return

    df_tree_temp.to_csv(path_tree_temp, index=False)
    message("df_tree_temp saved")