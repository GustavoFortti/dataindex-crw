JOB_NAME = "iridium_labs"
BRAND = "iridium labs"
URL = "https://www.iridiumlabs.com.br"
STATUS = True
DISCOUNT_PERCENT_CUPOM = None
CUPOM_CODE = None
USER_AGENT = None

TAG_MAP_PREFERENCE = ["text"]

PRODUCT_DESCRIPTION_TAG_MAP = [
    {'tag': None, 'path': '#ProductInfo-template--template--14719947636839__main__main > div.t4s-product__description.t4s-rte'},
]

PRODUCT_NUTRICIONAL_TABLE_TAG_MAP = [
    {'tag': None, 'path': ''},
]

PRODUCT_DEFINITION_TAG_MAP = [
    {'tag': None, 'path': '#shopify-section-template--14719947636839__main > div > div > div > div > div.t4s-col-md-6.t4s-col-12.t4s-col-item.t4s-product__info-wrapper.t4s-pr'},
]

DYNAMIC_SCROLL = {
    "start_time_sleep": 1,
    "time_sleep": 0.5,
    "scroll_step": 1000,
    "percentage": 0.07,
    "return_percentage": 0.3,
    "max_return": 4000,
    "max_attempts": 3
}