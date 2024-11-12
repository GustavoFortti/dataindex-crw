JOB_NAME = "vitafor"
BRAND = "vitafor"
URL = "https://www.vitafor.com.br"
STATUS = True
PRODUCT_URL_AFFILIATED = None
DISCOUNT_PERCENT_CUPOM = None
CUPOM_CODE = None
USER_AGENT = None

TAG_MAP_PREFERENCE = ["text"]

PRODUCT_DESCRIPTION_TAG_MAP = [
    {'tag': None, 'path': 'body > div.render-container.render-route-store-product > div > div.vtex-store__template.bg-base > div > div > div > div:nth-child(5) > div > div:nth-child(4) > div > section > div > div > div > div.vitafor-store-theme-9-x-description'},
]

PRODUCT_NUTRICIONAL_TABLE_TAG_MAP = [
    {'tag': None, 'path': ''},
]

PRODUCT_DEFINITION_TAG_MAP = [
    {'tag': None, 'path': 'body > div.render-container.render-route-store-product > div > div.vtex-store__template.bg-base > div > div > div > div:nth-child(5) > div > div:nth-child(4) > div'},
]

DYNAMIC_SCROLL = {
    "start_time_sleep": 1,
    "time_sleep": 0.7,
    "scroll_step": 1500,
    "percentage": 0.07,
    "return_percentage": 0.1,
    "max_return": 2000,
    "max_attempts": 3
}