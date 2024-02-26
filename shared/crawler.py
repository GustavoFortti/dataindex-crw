import time
import pandas as pd
import asyncio
from pyppeteer import launch

import shared.selenium_service as se 
from shared.data_quality import status_tag
from utils.log import message
from utils.general_functions import (generate_hash,
                                     create_or_read_df,
                                     clean_string_break_line)

def crawler(job, url):
    message("exec crawler")
    if (("driver" not in job.conf.keys()) or (not job.conf["driver"])):
        message("initialize_selenium")
        if (job.conf['seed']):
            job.conf["driver"] = se.initialize_selenium()
    
    load_page(job, url)

def load_page(job, url):
    message("exec load_page")

    driver = None

    if (job.conf['seed']):
        message("seed")
        message("3 seconds")
        time.sleep(3)

        driver = job.conf["driver"]

        element_selector = None
        se.load_url(driver, url, element_selector)

        time_sleep = job.conf['dynamic_scroll']['time_sleep']
        scroll_step = job.conf['dynamic_scroll']['scroll_step']
        percentage = job.conf['dynamic_scroll']['percentage']
        return_percentage = job.conf['dynamic_scroll']['return_percentage']
        max_return = job.conf['dynamic_scroll']['max_return']
        max_attempts = job.conf['dynamic_scroll']['max_attempts']

        if (job.conf['scroll_page']):
            se.dynamic_scroll(driver, time_sleep=time_sleep,
                                        scroll_step=scroll_step,
                                        percentage=percentage, 
                                        return_percentage=return_percentage, 
                                        max_return=max_return, 
                                        max_attempts=max_attempts)
            
        if (job.conf["status_job"]):
            se.dynamic_scroll(driver, time_sleep=0.4, scroll_step=1000, percentage=0.5, return_percentage=0.1, max_return=100, max_attempts=2)

        soup, page_html = se.get_page_source(driver)
        
        extract_data(job, soup)

    if (job.conf['tree']):
        message("tree")
        ref = generate_hash(url)
        data_path = job.conf['data_path']
        file_name = f"{data_path}/products/{ref}.txt"
        
        time.sleep(1)
        if (("driver" not in job.conf.keys()) or (not job.conf["driver"])):
            driver = se.initialize_selenium()

        se.load_url(driver, url)
        se.dynamic_scroll(driver, time_sleep=0.5, scroll_step=1000, percentage=0.5, return_percentage=0.1, max_return=100, max_attempts=2)
        soup, page_text = se.get_page_source(driver)

        with open(file_name, 'w') as file:
            file.write(page_text)
            message(f"File '{file_name}' created successfully.")

async def get_page_text(url, retries=3, delay=1):
    attempt = 0
    while attempt < retries:
        browser = None
        page = None
        try:
            browser = await launch()
            page = await browser.newPage()
            await page.goto(url, {'timeout': 30000})
            await page.waitForSelector('body', {'timeout': 30000})
            page_content = await page.content()
            return page_content
        except Exception as e:
            message(f"Erro ao tentar acessar {url}: {e}")
            attempt += 1
            await asyncio.sleep(delay)
            delay *= 2
        finally:
            if page:
                try:
                    await page.goto('about:blank')
                except Exception as e:
                    message(f"Erro ao navegar para about:blank: {e}")
                try:
                    await page.close()
                except Exception as e:
                    message(f"Erro ao fechar a página: {e}")
            if browser:
                try:
                    await browser.close()
                except Exception as e:
                    message(f"Erro ao fechar o navegador: {e}")

    message(f"Não foi possível acessar {url} após {retries} tentativas.")
    return None

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