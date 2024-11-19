JOB_NAME = "oficialfarma"
BRAND = "oficial farma"
URL = "https://www.oficialfarma.com.br/"
STATUS = False
USER_AGENT = None

TAG_MAP_PREFERENCE = ["text"]

PRODUCT_DESCRIPTION_TAG_MAP = [
    {'tag': None, 'path': '#maincontent > div.columns > div > div.product.attribute.description'},
]

PRODUCT_IMAGES_TAG_MAP = [
    {'tag': None, 'path': ''},
]

PRODUCT_DEFINITION_TAG_MAP = [
    {'tag': None, 'path': '#maincontent > div.columns > div > div.product.attribute.description > div > div > div'},
]

DYNAMIC_SCROLL = {
    "start_time_sleep": 1,
    "time_sleep": 1.3,
    "scroll_step": 700,
    "percentage": 0.07,
    "return_percentage": 0.3,
    "max_return": 2000,
    "max_attempts": 3
}