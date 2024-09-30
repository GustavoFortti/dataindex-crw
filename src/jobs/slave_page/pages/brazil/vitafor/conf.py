JOB_NAME = "vitafor"
BRAND = "vitafor"
URL = "https://www.vitafor.com.br"
STATUS = True

PRODUCT_DEFINITION_TAG_MAP = [
    {'tag': None, 'path': 'body > div.render-container.render-route-store-product > div > div.vtex-store__template.bg-base > div > div > div > div:nth-child(5) > div > div:nth-child(4) > div'},
]

DYNAMIC_SCROLL = {
    "time_sleep": 0.7,
    "scroll_step": 1500,
    "percentage": 0.07,
    "return_percentage": 0.1,
    "max_return": 2000,
    "max_attempts": 3
}