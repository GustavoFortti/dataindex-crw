JOB_NAME = "adaptogen"
BRAND = "adaptogen"
URL = "https://adaptogen.com.br"
STATUS = True
PRODUCT_URL_AFFILIATED = None
DISCOUNT_PERCENT_CUPOM = "10%"
CUPOM_CODE = "ADAPNUTRIFIND10"
USER_AGENT = None

TAG_MAP_PREFERENCE = ["text"]

PRODUCT_DESCRIPTION_TAG_MAP = [
    {'tag': None, 'path': '#tab-beneficios'},
    {'tag': None, 'path': '#tab-tabela_nutricional'},
    {'tag': None, 'path': '#tab-description'},
]

PRODUCT_IMAGES_TAG_MAP = [
    {'tag': None, 'path': ''},
]

PRODUCT_DEFINITION_TAG_MAP = [
    {'tag': None, 'path': '#tab-description'}
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