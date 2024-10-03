JOB_NAME = "max_titanium"
BRAND = "max titanium"
URL = "https://www.maxtitanium.com.br"
STATUS = True

PRODUCT_DEFINITION_TAG_MAP = [
    {'tag': None, 'path': 'body > div.render-container.render-route-store-product > div > div.vtex-store__template.bg-base > div > div > div > div:nth-child(5) > div > div:nth-child(2) > div:nth-child(6) > section > div > div > div > div:nth-child(1) > div > div > div > div > div:nth-child(2) > div > div > div > div > table > tbody'},
    {'tag': None, 'path': 'body > div.render-container.render-route-store-product > div > div.vtex-store__template.bg-base > div > div > div > div:nth-child(5) > div > div:nth-child(1) > div.vtex-flex-layout-0-x-flexRow.vtex-flex-layout-0-x-flexRow--breadcrumb'},
]

DYNAMIC_SCROLL = {
    "time_sleep": 0.5,
    "scroll_step": 500,
    "percentage": 0.07,
    "return_percentage": 0.3,
    "max_return": 4000,
    "max_attempts": 3
}