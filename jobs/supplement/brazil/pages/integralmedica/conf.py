JOB_NAME = "integralmedica"
BRAND = "integralmedica"
URL = "https://www.integralmedica.com.br"
STATUS = True

PRODUCT_DEFINITION_TAG = [
    {'tag': 'div', 'class': 'vtex-flex-layout-0-x-flexRow vtex-flex-layout-0-x-flexRow--pdpProductInfo'},
    {'tag': 'div', 'class': 'integralmedica-store-components-0-x-doubleImageAndTopicsCardContainer'},
]

DYNAMIC_SCROLL = {
    "time_sleep": 0.5,
    "scroll_step": 1000,
    "percentage": 0.07,
    "return_percentage": 0.3,
    "max_return": 4000,
    "max_attempts": 3
}