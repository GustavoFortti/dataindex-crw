JOB_NAME = "boldsnacks"
BRAND = "boldsnacks"
URL = "https://www.boldsnacks.com.br/"
STATUS = True

PRODUCT_DEFINITION_TAG = [
    {'tag': 'div', 'class': 'productView-desc halo-text-format'},
]

DYNAMIC_SCROLL = {
    "time_sleep": 0.5,
    "scroll_step": 1000,
    "percentage": 0.07,
    "return_percentage": 0.3,
    "max_return": 4000,
    "max_attempts": 3
}