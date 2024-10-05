JOB_NAME = "puravida"
BRAND = "puravida"
URL = "https://www.puravida.com.br"
STATUS = True
USER_AGENT = None

PRODUCT_DESCRIPTION_TAG_MAP = [
    {'tag': None, 'path': ''},
]

PRODUCT_NUTRICIONAL_TABLE_TAG_MAP = [
    {'tag': None, 'path': ''},
]

PRODUCT_DEFINITION_TAG_MAP = [
    {'tag': None, 'path': '#product-content > div:nth-child(2) > div'},
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