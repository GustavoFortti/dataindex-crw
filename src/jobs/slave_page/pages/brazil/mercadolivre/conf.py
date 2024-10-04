JOB_NAME = "mercadolivre"
BRAND = "mercado livre"
URL = "https://lista.mercadolivre.com.br/"
STATUS = True
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:115.0) Gecko/20100101 Firefox/115.0"

PRODUCT_DESCRIPTION_TAG_MAP = [
    {'tag': None, 'path': ''},
]

PRODUCT_NUTRICIONAL_TABLE_TAG_MAP = [
    {'tag': None, 'path': ''},
]

PRODUCT_DEFINITION_TAG_MAP = [
    {'tag': None, 'path': '#description'},
]

DYNAMIC_SCROLL = {
    "start_time_sleep": 1,
    "time_sleep": 0.7,
    "scroll_step": 1200,
    "percentage": 0.07,
    "return_percentage": 0.2,
    "max_return": 2000,
    "max_attempts": 3
}