JOB_NAME = "integralmedica"
BRAND = "integralmedica"
URL = "https://www.integralmedica.com.br"
STATUS = True

PRODUCT_DEFINITION_TAG_MAP = [
    {'tag': None, 'path': 'body > div.render-container.render-route-store-product > div > div.vtex-store__template.bg-base > div > div > div > div:nth-child(3) > div > div > div > div > div:nth-child(3) > div > div > div:nth-child(3) > div'},
]

USER_AGENT = None

DYNAMIC_SCROLL = {
    "start_time_sleep": 1,
    "time_sleep": 0.5,
    "scroll_step": 1000,
    "percentage": 0.07,
    "return_percentage": 0.3,
    "max_return": 4000,
    "max_attempts": 3
}