JOB_NAME = "iridium_labs"
BRAND = "iridium labs"
URL = "https://www.iridiumlabs.com.br"
STATUS = True

PRODUCT_DEFINITION_TAG = [
    {'tag': 'div', 'class': 't4s-product__description t4s-rte'}
]

DYNAMIC_SCROLL = {
    "time_sleep": 0.5,
    "scroll_step": 1000,
    "percentage": 0.07,
    "return_percentage": 0.3,
    "max_return": 4000,
    "max_attempts": 3
}