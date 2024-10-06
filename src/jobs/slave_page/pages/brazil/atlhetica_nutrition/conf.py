JOB_NAME = "atlhetica_nutrition"
BRAND = "atlhetica nutrition"
URL = "https://www.atlheticanutrition.com.br"
STATUS = True
USER_AGENT = None

PRODUCT_DESCRIPTION_TAG_MAP = [
    {'tag': None, 'path': ''},
]

PRODUCT_NUTRICIONAL_TABLE_TAG_MAP = [
    {'tag': None, 'path': 'body > div.render-container.render-route-store-product > div > div.vtex-store__template.bg-base > div > div > div > div:nth-child(3) > div > div:nth-child(3) > div > div > div > div > div > div > div > div > div > div > div.pr6.items-stretch.vtex-flex-layout-0-x-stretchChildrenWidth.flex > div > div:nth-child(1) > div'},
]

PRODUCT_DEFINITION_TAG_MAP = [
    {'tag': None, 'path': 'body > div.render-container.render-route-store-product > div > div.vtex-store__template.bg-base > div > div > div > div:nth-child(3) > div > div:nth-child(1) > div > section > div > div > div > div'}
]

DYNAMIC_SCROLL = {
    "start_time_sleep": 1,
    "time_sleep": 0.8,
    "scroll_step": 500,
    "percentage": 0.07,
    "return_percentage": 0.3,
    "max_return": 4000,
    "max_attempts": 3
}