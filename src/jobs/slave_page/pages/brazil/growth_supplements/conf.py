JOB_NAME = "growth_supplements"
BRAND = "growth supplements"
URL = "https://www.gsuplementos.com.br"
STATUS = True

PRODUCT_DEFINITION_TAG_MAP = [
    {'tag': None, 'path': '#breadcrumb'},
]

DYNAMIC_SCROLL = {
    "time_sleep": 0.5,
    "scroll_step": 1000,
    "percentage": 0.07,
    "return_percentage": 0.3,
    "max_return": 4000,
    "max_attempts": 3
}