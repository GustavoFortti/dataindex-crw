JOB_NAME = "mercadolivre"
BRAND = "mercado livre"
URL = "https://lista.mercadolivre.com.br/"
STATUS = False
product_url_affiliated = None
DISCOUNT_PERCENT_CUPOM = None
CUPOM_CODE = None
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:115.0) Gecko/20100101 Firefox/115.0"

TAG_MAP_PREFERENCE = ["text"]

PRODUCT_DESCRIPTION_TAG_MAP = [
    {'tag': None, 'path': '#ui-pdp-main-container > div.ui-pdp-container__col.col-3.ui-pdp-container--column-center.pb-16 > div > div:nth-child(7) > div > div'},
]

PRODUCT_NUTRICIONAL_TABLE_TAG_MAP = [
    {'tag': None, 'path': ''},
]

PRODUCT_DEFINITION_TAG_MAP = [
    {'tag': None, 'path': '#ui-pdp-main-container > div.ui-pdp-container__col.col-3.ui-pdp-container--column-center.pb-16 > div > div:nth-child(7) > div > div'},
    {'tag': None, 'path': '#description'},
]

DYNAMIC_SCROLL = {
    "start_time_sleep": 1,
    "time_sleep": 0.5,
    "scroll_step": 1500,
    "percentage": 0.07,
    "return_percentage": 0.2,
    "max_return": 2000,
    "max_attempts": 3
}