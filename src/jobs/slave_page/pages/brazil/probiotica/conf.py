JOB_NAME = "probiotica"
BRAND = "probiotica"
URL = "https://www.probiotica.com.br"
STATUS = True
product_url_affiliated = None
DISCOUNT_PERCENT_CUPOM = "10%"
CUPOM_CODE = "PRO10NUTRIFIND10"
USER_AGENT = None

TAG_MAP_PREFERENCE = ["text"]

PRODUCT_DESCRIPTION_TAG_MAP = [
    {'tag': None, 'path': 'body > div.render-container.render-route-store-product > div > div.vtex-store__template.bg-base > div > div > div > div:nth-child(4) > div > div:nth-child(2) > div:nth-child(2) > section > div > div > div > div:nth-child(13) > div > div > div.pr10.items-stretch.vtex-flex-layout-0-x-stretchChildrenWidth.flex'},
]

PRODUCT_NUTRICIONAL_TABLE_TAG_MAP = [
    {'tag': None, 'path': ''},
]

PRODUCT_DEFINITION_TAG_MAP = [
    {'tag': None, 'path': 'body > div.render-container.render-route-store-product > div > div.vtex-store__template.bg-base > div > div > div > div:nth-child(4) > div > div:nth-child(2) > div:nth-child(2) > section > div > div > div > div:nth-child(1) > div > div'},
]

DYNAMIC_SCROLL = {
    "start_time_sleep": 1,
    "time_sleep": 1,
    "scroll_step": 1000,
    "percentage": 0.07,
    "return_percentage": 0.3,
    "max_return": 4000,
    "max_attempts": 3
}