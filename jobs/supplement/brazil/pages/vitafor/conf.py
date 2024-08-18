JOB_NAME = "vitafor"
BRAND = "vitafor"
URL = "https://www.vitafor.com.br"
STATUS = True

PRODUCT_DEFINITION_TAG_MAP = [
    {'tag': 'p', 'class': 'vitafor-store-theme-9-x-productPageShortDescription'},
    {'tag': 'div', 'class': 'vitafor-store-theme-9-x-description'}
]

DYNAMIC_SCROLL = {
    "time_sleep": 1.5,
    "scroll_step": 1000,
    "percentage": 0.07,
    "return_percentage": 0.3,
    "max_return": 4000,
    "max_attempts": 3
}