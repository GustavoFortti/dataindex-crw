JOB_NAME = "probiotica"
BRAND = "probiotica"
URL = "https://www.probiotica.com.br"
STATUS = True

PRODUCT_DEFINITION_TAG_MAP = [
    {'tag': None, 'path': 'body > div.render-container.render-route-store-product > div > div.vtex-store__template.bg-base > div > div > div > div:nth-child(4) > div > div:nth-child(2) > div:nth-child(2) > section > div > div > div > div:nth-child(1) > div > div'},
]

DYNAMIC_SCROLL = {
    "time_sleep": 1,
    "scroll_step": 1000,
    "percentage": 0.07,
    "return_percentage": 0.3,
    "max_return": 4000,
    "max_attempts": 3
}