JOB_NAME = "dark_lab"
BRAND = "dark lab"
URL = "https://darklabsuplementos.com.br"
STATUS = True

PRODUCT_DEFINITION_TAG_MAP = [
    {'tag': None, 'path': '#single-product > div > div:nth-child(2) > div > div.px-3'},
]

DYNAMIC_SCROLL = {
    "time_sleep": 0.5,
    "scroll_step": 1000,
    "percentage": 0.07,
    "return_percentage": 0.3,
    "max_return": 4000,
    "max_attempts": 3
}