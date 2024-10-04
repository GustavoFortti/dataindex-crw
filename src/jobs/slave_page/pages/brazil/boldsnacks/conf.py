JOB_NAME = "boldsnacks"
BRAND = "bold snacks"
URL = "https://www.boldsnacks.com.br/"
STATUS = True

PRODUCT_DEFINITION_TAG_MAP = [
    {'tag': None, 'path': '#ProductSection-template--17547208458430__main > div.productView-container.container > div > div.productView-top > div.halo-productView-right.productView-details.clearfix > div'},
]

USER_AGENT = None

DYNAMIC_SCROLL = {
    "start_time_sleep": 1,
    "time_sleep": 0.5,
    "scroll_step": 1000,
    "percentage": 0.07,
    "return_percentage": 0.3,
    "max_return": 4000,
    "max_attempts": 3
}