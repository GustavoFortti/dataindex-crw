JOB_NAME = "oficialfarma"
BRAND = "oficialfarma"
URL = "https://www.oficialfarma.com.br/"
STATUS = False

PRODUCT_DEFINITION_TAG_MAP = [
    {'tag': None, 'path': '#maincontent > div.columns > div > div.product.attribute.description > div > div > div'},
]

DYNAMIC_SCROLL = {
    "time_sleep": 1.3,
    "scroll_step": 700,
    "percentage": 0.07,
    "return_percentage": 0.3,
    "max_return": 2000,
    "max_attempts": 3
}