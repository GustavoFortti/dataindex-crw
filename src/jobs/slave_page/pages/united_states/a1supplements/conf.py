JOB_NAME = "a1supplements"
BRAND = "a1supplements"
URL = "https://a1supplements.com"
STATUS = True
PRODUCT_URL_AFFILIATED = None
DISCOUNT_PERCENT_CUPOM = None
CUPOM_CODE = None
USER_AGENT = None

TAG_MAP_PREFERENCE = ["text", "image"]

PRODUCT_DESCRIPTION_TAG_MAP = [
    {'tag': None, 'path': '#tab-description'},
    {'tag': None, 'path': '#ProductInfo-template--22993487429938__main > div.product__description.rte.quick-add-hidden'},
    {'tag': None, 'path': '#MainProduct-template--22993487429938__main > div.product.product--large.product--left.product--thumbnail_slider.product--mobile-show.grid.grid--1-col.grid--2-col-tablet > div.grid__item.product__media-wrapper > div.MainAccordionSection.workOnlyDesktop'},
]

PRODUCT_IMAGES_TAG_MAP = [
    {'tag': None, 'remove_first': True, 'path': '#MainProduct-template--22993487429938__main > div.product.product--large.product--left.product--thumbnail_slider.product--mobile-show.grid.grid--1-col.grid--2-col-tablet > div.grid__item.product__media-wrapper > div.MainMEdiaWrapper > div.CustomThumbnailWrapper > div > div > div'},
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