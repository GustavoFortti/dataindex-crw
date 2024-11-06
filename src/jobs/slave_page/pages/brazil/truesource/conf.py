JOB_NAME = "truesource"
BRAND = "truesource"
URL = "https://www.truesource.com.br"
STATUS = True
product_url_affiliated = None
DISCOUNT_PERCENT_CUPOM = None
CUPOM_CODE = None
USER_AGENT = None

TAG_MAP_PREFERENCE = ["text"]

PRODUCT_DESCRIPTION_TAG_MAP = [
    {'tag': None, 'path': '#\\32 642033340-0 > div > div:nth-child(2)'},
]

PRODUCT_NUTRICIONAL_TABLE_TAG_MAP = [
    {'tag': None, 'path': ''},
]

PRODUCT_DEFINITION_TAG_MAP = [
    {'tag': None, 'path': '#\\39 21277609-0 > div > div:nth-child(2)'}
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