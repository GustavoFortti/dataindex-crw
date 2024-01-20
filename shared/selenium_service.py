import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import time
import random

def initialize_selenium():
    options = webdriver.ChromeOptions()

    # Configurações para evitar detecção
    # options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    # Rotacionar User-Agent
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0 Safari/605.1.15',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'
    ]
    user_agent = random.choice(user_agents)
    options.add_argument(f'user-agent={user_agent}')

    service = Service(executable_path="./.env/chromedriver")
    driver = webdriver.Chrome(service=service, options=options)

    # Modificar a propriedade 'navigator.webdriver'
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    # Verificar o User-Agent atual
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