JOB_NAME = "new_millen"
BRAND = "new millen"
URL = "https://loja.newmillen.com.br"
STATUS = True
PRODUCT_URL_AFFILIATED = None
DISCOUNT_PERCENT_CUPOM = None
CUPOM_CODE = None
USER_AGENT = None

TAG_MAP_PREFERENCE = ["text"]

PRODUCT_DESCRIPTION_TAG_MAP = [
    {'tag': None, 'path': '#product-description'},
]

PRODUCT_IMAGES_TAG_MAP = [
    {'tag': None, 'path': ''},
]

PRODUCT_DEFINITION_TAG_MAP = [
    {'tag': None, 'path': '#product-description'},
]

DYNAMIC_SCROLL = {
    "start_time_sleep": 1,
    "time_sleep": 0.5,
    "scroll_step": 1000,
    "percentage": 0.07,
    "return_percentage": 0.3,
    "max_return": 4000,
    "max_attempts": 3
}