from config.env import LOCAL

import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import time

from utils.general_functions import check_urls_in_parallel, is_price

def initialize_selenium():
    options = webdriver.ChromeOptions()
    
    display = os.getenv('DISPLAY')
    print(f"DISPLAY{display}")

    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--enable-logging")
    options.add_argument("--v=1")

    ua = UserAgent()
    user_agent = ua.random
    options.add_argument(f'user-agent={user_agent}')

    service = Service(executable_path=f"{LOCAL}/packages/chromedriver")
    driver = webdriver.Chrome(service=service, options=options)
    
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    driver.maximize_window() 
    print(driver.execute_script("return navigator.userAgent;"))
   
    return driver

def get_html(driver, url, sleep=1, scroll_page=False, return_text=False, functions_to_check_load=False):
    print("get_html")
    print(f"url: {url}")
    print("")

    driver.get(url)
    driver.implicitly_wait(100)
    if (sleep != 0): 
        print("*" * sleep)
    time.sleep(sleep)

    page_html = driver.page_source
    soup = BeautifulSoup(page_html, 'html.parser')

    if (scroll_page):
        print(f"SCROLL_PAGE...")

        scroll_rule = [{"time_sleep": 0.5, "size_height": 1500},
                       {"time_sleep": 1, "size_height": 1000},
                       {"time_sleep": 1, "size_height": 500}, 
                       {"time_sleep": 2, "size_height": 500}]
        
        if (type(scroll_page) == list):
            scroll_rule = scroll_page

        for scroll in scroll_rule:
            
            load_page(driver, scroll["time_sleep"], scroll["size_height"])
    
            page_html = driver.page_source
            soup = BeautifulSoup(page_html, 'html.parser')

            if (functions_to_check_load):
                is_page_load = check_load_page(soup, functions_to_check_load)
                print(f"is_page_load {is_page_load}")

                if (is_page_load):
                    break
            else:
                break

    if (return_text): 
        return soup, page_html
    return soup

def check_load_page(soup, functions_to_check_load):
    print(f"check_load_page")

    get_items, get_elements_seed = functions_to_check_load
    
    try:
        items = get_items(soup)
        url_list = []

        print(f"items size: {len(items)}")
        for item in items:
            product_url, title, price, image_url = get_elements_seed(item)
            url_list.append(image_url)
            url_list.append(product_url)
            if (not is_price(price)): 
                print(f"ERROR: price error {price}")

        urls_exists = check_urls_in_parallel(url_list)
        if (not urls_exists): 
            print("ERROR: urls_exists")
            return False
        
        return True
    except:
        print("Erro nas tags")
        return False

def load_page(driver, time_sleep, size_height):
    total_height = driver.execute_script("return document.body.scrollHeight")
    previous_height = 0

    while True:
        # Rola para a próxima "fatia" da página
        next_height = previous_height + size_height
        driver.execute_script(f"window.scrollTo(0, {next_height});")
        time.sleep(time_sleep)  # Espera para o carregamento do conteúdo

        # Verifica a nova altura total da página
        new_total_height = driver.execute_script("return document.body.scrollHeight")

        if new_total_height > total_height:
            # Se a altura total da página aumentou, volta ao início da página e ajusta a altura total
            driver.execute_script("window.scrollTo(0, 0);")  # Volta ao início da página
            total_height = new_total_height  # Atualiza a altura total
            previous_height = 0  # Reseta a altura anterior para começar a rolagem novamente
            print("Page size increased. Returning to the top of the page.")
        else:
            # Se a altura total da página não mudou, atualiza a altura anterior e continua a rolagem
            if next_height >= total_height:
                break  # Sai do loop se alcançar o final da página
            previous_height = next_height

        print(f"Current scroll position: {next_height}/{total_height}")

def move_mouse_over_all_elements(driver):
    elements = driver.find_elements(By.XPATH, "//*")

    for element in elements:
        try:
            if element.is_displayed() and element.size['width'] > 0 and element.size['height'] > 0:
                ActionChains(driver).move_to_element(element).perform()
        except Exception as e:
            continue 