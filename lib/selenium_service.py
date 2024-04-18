import os
import time

from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config.env import LOCAL
from utils.log import message


def initialize_selenium():
    options = webdriver.ChromeOptions()
    
    display = os.getenv('DISPLAY')
    message(f"DISPLAY{display}")

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
    message(driver.execute_script("return navigator.userAgent;"))
   
    return driver

def load_url(driver, url, element_selector=None, timeout=30):
    driver.get(url)
    driver.implicitly_wait(100)
    if element_selector:
        try:
            element_present = EC.presence_of_element_located((By.CSS_SELECTOR, element_selector))
            WebDriverWait(driver, timeout).until(element_present)
        except TimeoutException:
            message(f"Timed out waiting for element {element_selector} to be present")

def get_page_source(driver, retry_delay=5):
    try:
        message("Tentando obter o page_source da página atual...")
        page_html = driver.page_source
        soup = BeautifulSoup(page_html, 'html.parser')
        return soup, page_html  # Retorna o objeto BeautifulSoup se o page_source for obtido com sucesso
    except WebDriverException as e:
        message(f"Erro ao obter o page_source: {e}. Tentando recarregar após {retry_delay} segundos...")
        time.sleep(retry_delay)  # Espera antes de tentar novamente
        try:
            driver.refresh()  # Tentativa de recarregar a página atual
            page_html = driver.page_source
            soup = BeautifulSoup(page_html, 'html.parser')
            return soup, page_html  # Retorna o objeto BeautifulSoup se a página for recarregada com sucesso na segunda tentativa
        except WebDriverException as e:
            message(f"Erro ao recarregar a página: {e}. Abortando...")
            return None  # Retorna None se falhar novamente
   
def dynamic_scroll(driver, time_sleep=0.7, scroll_step=1000, percentage=0.06, return_percentage=0.3, max_return=4000, max_attempts=3):
    total_height = driver.execute_script("return document.body.scrollHeight")
    scroll_increment = min(total_height * percentage, scroll_step)
    last_scrolled_height = 0
    attempt_count = 0  # Contador para rastrear tentativas sem mudança na posição de rolagem

    while True:
        driver.execute_script(f"window.scrollBy(0, {scroll_increment});")
        time.sleep(time_sleep)  # Espera para o carregamento do conteúdo

        scrolled_height = driver.execute_script("return window.pageYOffset;")
        message(f"Current scroll position: {scrolled_height}/{total_height}")  # Mostra a posição atual e o tamanho máximo

        if scrolled_height == last_scrolled_height:
            attempt_count += 1  # Incrementa o contador se a posição de rolagem não mudou
            if attempt_count >= max_attempts:
                message("Scroll position unchanged for consecutive attempts. Ending scroll.")
                break  # Sai do loop se a posição de rolagem permanecer a mesma por várias tentativas
        else:
            attempt_count = 0  # Reseta o contador se a posição de rolagem mudar

        last_scrolled_height = scrolled_height  # Atualiza a última posição de rolagem registrada

        new_total_height = driver.execute_script("return document.body.scrollHeight")
        if new_total_height > total_height:
            # Ajusta a altura total e o incremento de rolagem se o tamanho da página aumentou
            total_height = new_total_height
            scroll_increment = min(total_height * percentage, scroll_step)

            # Calcula a distância de retorno e ajusta a posição da rolagem
            return_distance = min(scrolled_height * return_percentage, max_return)
            new_scroll_position = max(scrolled_height - return_distance, 0)
            driver.execute_script(f"window.scrollTo(0, {new_scroll_position});")
            message(f"Page size increased to {total_height}. Returning to position {new_scroll_position} due to size increase.")

        if scrolled_height + scroll_increment >= total_height:
            break  # Sai do loop se alcançar ou ultrapassar o fundo da página

def move_mouse_over_all_elements(driver):
    elements = driver.find_elements(By.XPATH, "//*")

    for element in elements:
        try:
            if element.is_displayed() and element.size['width'] > 0 and element.size['height'] > 0:
                ActionChains(driver).move_to_element(element).perform()
        except Exception as e:
            continue 