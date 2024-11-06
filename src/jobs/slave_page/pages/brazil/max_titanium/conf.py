JOB_NAME = "max_titanium"
BRAND = "max titanium"
URL = "https://www.maxtitanium.com.br"
STATUS = True
product_url_affiliated = "?utm_source=mais&utm_medium=maisplataforma&utm_campaign=nutrifind"
DISCOUNT_PERCENT_CUPOM = "10%"
CUPOM_CODE = "MAX10NUTRIFIND10"
USER_AGENT = None

TAG_MAP_PREFERENCE = ["text"]

PRODUCT_DESCRIPTION_TAG_MAP = [
    {'tag': None, 'path': '#\\:S17\\:-container-wrapper'},
]

PRODUCT_NUTRICIONAL_TABLE_TAG_MAP = [
    {'tag': None, 'path': ''},
]

PRODUCT_DEFINITION_TAG_MAP = [
    {'tag': None, 'path': '#\\:S17\\:-container-wrapper'},
]

DYNAMIC_SCROLL = {
    "start_time_sleep": 1,
    "time_sleep": 0.5,
    "scroll_step": 500,
    "percentage": 0.07,
    "return_percentage": 0.3,
    "max_return": 4000,
    "max_attempts": 3
}