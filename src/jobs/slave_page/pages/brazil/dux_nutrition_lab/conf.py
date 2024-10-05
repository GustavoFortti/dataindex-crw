JOB_NAME = "dux_nutrition_lab"
BRAND = "dux nutrition lab"
URL = "https://www.duxnutrition.com"
STATUS = True
USER_AGENT = None

PRODUCT_DESCRIPTION_TAG_MAP = [
    {'tag': None, 'path': ''},
]

PRODUCT_NUTRICIONAL_TABLE_TAG_MAP = [
    {'tag': None, 'path': ''},
]

PRODUCT_DEFINITION_TAG_MAP = [
    {'tag': None, 'path': '#ProductDescriptionAccordion > div.vtex-flex-layout-0-x-flexRow.vtex-flex-layout-0-x-flexRow--productDescriptionAccordion.vtex-flex-layout-0-x-flexRow--container.vtex-flex-layout-0-x-flexRow--block > section > div'},
]

DYNAMIC_SCROLL = {
    "start_time_sleep": 1,
    "time_sleep": 1,
    "scroll_step": 1000,
    "percentage": 0.07,
    "return_percentage": 0.3,
    "max_return": 4000,
    "max_attempts": 3
}