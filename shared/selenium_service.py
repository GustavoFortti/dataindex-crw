from config.env import LOCAL

import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import time

def initialize_selenium():
    options = webdriver.ChromeOptions()
    
    display = os.getenv('DISPLAY')
    print(f"DISPLAY{display}")

    options.add_argument("--start-maximized")
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
    driver.minimize_window()
    
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    print(driver.execute_script("return navigator.userAgent;"))
    return driver

def get_html(driver, url, sleep=1, scroll_page=False, return_text=False):
    try:
        
        driver.get(url)
        driver.implicitly_wait(100)
        if (sleep != 0): print("*" * sleep)
        time.sleep(sleep)

        if (scroll_page):
            prox_altura = 0
            total_altura = driver.execute_script("return document.body.scrollHeight")

            while (total_altura > prox_altura):
                prox_altura += 500
                atual_altura = prox_altura - 500
                driver.execute_script(f"window.scrollTo({atual_altura}, {prox_altura});")
                print(f"{prox_altura}/{total_altura}")
                time.sleep(0.4)
        
        page_html = driver.page_source
        soup = BeautifulSoup(page_html, 'html.parser')
        
        if (return_text): return soup, page_html
        return soup
    except Exception as e:
        print(f"Ocorreu um erro: {str(e)}")