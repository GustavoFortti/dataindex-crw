JOB_NAME = "nutrata"
BRAND = "nutrata"
PRD = True

PRODUCT_DEFINITION_TAG = [
    {'tag': 'span', 'class': 'tagged_as'}, 
    {'tag': 'nav', 'class': 'woocommerce-breadcrumb'}, 
    {'tag': 'div', 'class': 'woocommerce-Tabs-panel woocommerce-Tabs-panel--description panel entry-content wc-tab'},
    {'tag': 'div', 'class': 'woocommerce-tabs et-clearfix et_element wc-tabs-wrapper type-accordion opened-all-tabs toggles-by-arrow loaded'}
]

DYNAMIC_SCROLL = {
    "time_sleep": 0.5,
    "scroll_step": 1000,
    "percentage": 0.07,
    "return_percentage": 0.3,
    "max_return": 4000,
    "max_attempts": 3
}