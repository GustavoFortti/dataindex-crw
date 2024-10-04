JOB_NAME = "ifood"
BRAND = "ifood"
URL = "https://ifood.com.br/"
STATUS = False

PRODUCT_DEFINITION_TAG_MAP = [
    {'tag': None, 'path': ''},
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