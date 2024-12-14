import os
import re
import subprocess
import time
from typing import Optional, Tuple

from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from src.jobs.job_manager import JobBase
from src.lib.utils.log import message


def initialize_selenium(job_base: JobBase) -> WebDriver:
    """
    Initializes and returns a Selenium WebDriver with specified options.

    Args:
        job_base (JobBase): An object containing driver and page configurations.

    Returns:
        WebDriver: An instance of Selenium WebDriver.
    """
    options: Options = webdriver.ChromeOptions()

    display: Optional[str] = os.getenv('DISPLAY')
    message(f"display - {display}")

    # General Chrome options
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--enable-logging")
    options.add_argument("--v=1")
    options.add_argument("--remote-allow-origins=*")
    options.add_argument("disable-infobars")

    # Headless mode configurations
    if job_base.driver_use_headless:
        options.add_argument("--headless=new")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--window-size=1280,720")

    options.binary_location = "/usr/bin/google-chrome"

    # User agent configuration
    user_agent: str = (
        job_base.page.crawler_driver_user_agent
        if job_base.page.crawler_driver_user_agent
        else get_desktop_user_agent()
    )
    options.add_argument(f'user-agent={user_agent}')

    # Initialize WebDriver
    try:
        chrome_version = get_chrome_version()
        driver_version: str = chrome_version
        chrome_service: Service = Service(
            ChromeDriverManager(driver_version=driver_version).install()
        )
        driver: WebDriver = webdriver.Chrome(service=chrome_service, options=options)
    except Exception as e:
        message(f"Error initializing WebDriver: {e}")
        raise e

    # Hide WebDriver property to avoid detection
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    driver.maximize_window()
    message(driver.execute_script("return navigator.userAgent;"))

    return driver


def get_desktop_user_agent() -> str:
    """
    Generates a random desktop user agent string.

    Returns:
        str: A user agent string for a desktop browser.
    """
    ua: UserAgent = UserAgent()
    user_agent: str = ua.random

    # Ensure the user agent is for a desktop browser
    while 'Mobile' in user_agent or 'Android' in user_agent or 'iPhone' in user_agent:
        user_agent = ua.random

    return user_agent


def load_url(
    driver: WebDriver,
    url: str,
    element_selector: Optional[str] = None,
    timeout: int = 30,
    reload_timeout: int = 30,
    max_retries: int = 3
) -> None:
    """
    Loads a URL using the provided WebDriver, waits for the page to load, and retries if needed.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        url (str): The URL to load.
        element_selector (Optional[str]): CSS selector for an element to wait for.
        timeout (int): Time to wait for the element in seconds.
        reload_timeout (int): Time to wait for the page load check in seconds.
        max_retries (int): Maximum number of reload attempts.

    Raises:
        TimeoutException: If the page does not load or the element does not appear within the time limit.
    """
    retries = 0
    while retries < max_retries:
        try:
            # Definir o tempo máximo para o carregamento da página
            driver.set_page_load_timeout(reload_timeout)
            message(f"Carregando a URL: {url} (Tentativa {retries + 1}/{max_retries})")
            driver.get(url)
            # Esperar até que a página esteja completamente carregada
            WebDriverWait(driver, reload_timeout).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            # Verificar se o elemento especificado está presente
            if element_selector:
                element_present = EC.presence_of_element_located((By.CSS_SELECTOR, element_selector))
                WebDriverWait(driver, timeout).until(element_present)
            message(f"Página carregada com sucesso na tentativa {retries + 1}.")
            return  # Página carregada com sucesso
        except TimeoutException:
            message(f"Retry {retries + 1}/{max_retries}: Página não carregou em {reload_timeout} segundos, recarregando...")
            retries += 1
            try:
                # Opcional: Parar o carregamento atual da página
                driver.execute_script("window.stop();")
            except WebDriverException as e:
                message(f"Erro ao parar o carregamento da página: {e}")
            time.sleep(1)  # Pequeno intervalo antes de tentar novamente
        except WebDriverException as e:
            message(f"WebDriverException ocorreu: {e}. Recarregando a página...")
            retries += 1
            time.sleep(1)

    # Se todas as tentativas falharem, lançar exceção
    raise TimeoutException(f"Falha ao carregar a página {url} após {max_retries} tentativas.")


def get_page_source(
    driver: WebDriver,
    retry_delay: int = 5
) -> Optional[Tuple[BeautifulSoup, str]]:
    """
    Retrieves the page source from the current page in the WebDriver.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        retry_delay (int): Delay before retrying in seconds.

    Returns:
        Optional[Tuple[BeautifulSoup, str]]: A tuple containing the BeautifulSoup object and page HTML, or None if failed.
    """
    try:
        message("Attempting to retrieve the current page...")
        page_html: str = driver.page_source
        soup: BeautifulSoup = BeautifulSoup(page_html, 'html.parser')
        return soup, page_html
    except WebDriverException as e:
        message(f"Error retrieving page source: {e}. Retrying after {retry_delay} seconds...")
        time.sleep(retry_delay)
        try:
            driver.refresh()
            page_html = driver.page_source
            soup = BeautifulSoup(page_html, 'html.parser')
            return soup, page_html
        except WebDriverException as e:
            message(f"Error reloading the page: {e}. Aborting...")
            return None


def dynamic_scroll(
    driver: WebDriver,
    time_sleep: float = 0.7,
    scroll_step: int = 1000,
    percentage: float = 0.06,
    return_percentage: float = 0.3,
    max_return: int = 4000,
    max_attempts: int = 3
) -> None:
    """
    Dynamically scrolls through the page to load all content.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        time_sleep (float): Sleep time between scrolls in seconds.
        scroll_step (int): Maximum pixels to scroll each time.
        percentage (float): Percentage of the page to scroll each time.
        return_percentage (float): Percentage of scrolled height to return when page height increases.
        max_return (int): Maximum pixels to scroll back.
        max_attempts (int): Max attempts when scroll position doesn't change before exiting.
    """
    total_height: int = driver.execute_script("return document.body.scrollHeight")
    scroll_increment: float = min(total_height * percentage, scroll_step)
    last_scrolled_height: int = 0
    attempt_count: int = 0
    max_scroll_reached: int = 0  # Rastreia a altura máxima alcançada

    # Obter um elemento visível para mover o mouse
    try:
        body_element = driver.find_element(By.TAG_NAME, "body")
    except:
        message("Elemento 'body' não encontrado. Abortando scroll.")
        return

    action = ActionChains(driver)

    while True:
        # Realiza o scroll para baixo
        driver.execute_script(f"window.scrollBy(0, {scroll_increment});")
        time.sleep(time_sleep)

        # Obtém a posição atual do scroll e a nova altura total da página
        scrolled_height: int = driver.execute_script("return window.pageYOffset;")
        new_total_height: int = driver.execute_script("return document.body.scrollHeight")

        message(f"Current scroll position: {scrolled_height}/{new_total_height}")

        # Move o mouse para o elemento 'body' para evitar detecção
        action.move_to_element(body_element).perform()

        # Atualiza a altura total se a página aumentou
        if new_total_height > total_height:
            message(f"Page height increased from {total_height} to {new_total_height}.")
            total_height = new_total_height
            scroll_increment = min(total_height * percentage, scroll_step)

            # Atualiza a altura máxima alcançada
            if scrolled_height > max_scroll_reached:
                max_scroll_reached = scrolled_height

            # Calcula a nova posição de scroll para evitar ficar preso
            return_distance: float = min(scrolled_height * return_percentage, max_return)
            new_scroll_position: float = max(scrolled_height - return_distance, 0)
            driver.execute_script(f"window.scrollTo(0, {new_scroll_position});")
            message(f"Returning to position {new_scroll_position} due to page height increase.")

            # Atualiza a altura máxima alcançada após o retorno
            max_scroll_reached = max(max_scroll_reached, new_scroll_position)

        # Verifica se o scroll avançou
        if scrolled_height > last_scrolled_height:
            message("Scroll avançou. Resetando contador de tentativas.")
            attempt_count = 0
            last_scrolled_height = scrolled_height
            max_scroll_reached = max(max_scroll_reached, scrolled_height)
        else:
            attempt_count += 1
            message(f"Scroll não avançou. Tentativa {attempt_count}/{max_attempts}.")
            if attempt_count >= max_attempts:
                message("Scroll não avançou após tentativas máximas. Finalizando scroll.")
                break

        # Condição de término: se o scroll atingiu ou ultrapassou a altura total da página
        if scrolled_height + scroll_increment >= total_height:
            message("Atingiu o final da página. Finalizando scroll.")
            break


def get_chrome_version() -> str:
    """
    Retrieves the version of Google Chrome installed on the system.

    This function runs a shell command to get the version of Google Chrome and extracts the version
    number using a regular expression. If the version cannot be determined, it defaults to returning "latest".

    Returns:
        str: The version number of Google Chrome, or "latest" if an error occurs.
    """
    try:
        version_output: str = subprocess.check_output(['google-chrome', '--version']).decode('utf-8')
        version_match: Optional[re.Match] = re.search(r'(\d+\.\d+\.\d+\.\d+)', version_output)
        if version_match:
            return version_match.group(1)
    except Exception as error:
        message(f"Error retrieving Chrome version: {error}")
    return "latest"