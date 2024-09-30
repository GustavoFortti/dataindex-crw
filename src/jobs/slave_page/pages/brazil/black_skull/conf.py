JOB_NAME = "black_skull"
BRAND = "black skull"
URL = "https://www.blackskullusa.com.br"
STATUS = True

PRODUCT_DEFINITION_TAG_MAP = [
    {'tag': None, 'path': 'body > div.render-container.render-route-store-product > div > div.vtex-store__template.bg-base > div > div > div > div:nth-child(3) > div > div:nth-child(1) > div.vtex-tab-layout-0-x-container > div.vtex-tab-layout-0-x-contentContainer.w-100'}    
]

DYNAMIC_SCROLL = {
    "time_sleep": 0.5,
    "scroll_step": 1000,
    "percentage": 0.07,
    "return_percentage": 0.3,
    "max_return": 4000,
    "max_attempts": 3
}