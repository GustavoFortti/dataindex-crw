JOB_NAME = "darkness"
BRAND = "darkness"
URL = "https://www.darkness.com.br"
STATUS = True
PRODUCT_URL_AFFILIATED = None
DISCOUNT_PERCENT_CUPOM = None
CUPOM_CODE = None
USER_AGENT = None

TAG_MAP_PREFERENCE = ["text"]

PRODUCT_DESCRIPTION_TAG_MAP = [
    {'tag': None, 'path': 'body > div.render-container.render-route-store-product > div > div.vtex-store__template.bg-base > div > div > div > div:nth-child(3) > div > div > div > div > div:nth-child(6)'},
]

PRODUCT_IMAGES_TAG_MAP = [
    {'tag': None, 'path': ''},
]

PRODUCT_DEFINITION_TAG_MAP = [
    {'tag': 'section', 'class': 'product-information'}, 
    {'tag': 'div', 'class': '__bs-nutri-table-container'}, 
    {'tag': 'div', 'class': 'col-md-6'},
    {'tag': 'div', 'class': '__bs-evora-list-text'}, 
    {'tag': 'div', 'id': 'descricao'},
    {'tag': 'div', 'id': 'sugestoes'},
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