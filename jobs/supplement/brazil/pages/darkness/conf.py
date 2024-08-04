JOB_NAME = "darkness"
BRAND = "darkness"
URL = "https://www.darkness.com.br"
STATUS = True

PRODUCT_DEFINITION_TAG = [
    {'tag': 'section', 'class': 'product-information'}, 
    {'tag': 'div', 'class': '__bs-nutri-table-container'}, 
    {'tag': 'div', 'class': 'col-md-6'},
    {'tag': 'div', 'class': '__bs-evora-list-text'}, 
    {'tag': 'div', 'id': 'descricao'},
    {'tag': 'div', 'id': 'sugestoes'},
]

DYNAMIC_SCROLL = {
    "time_sleep": 0.5,
    "scroll_step": 500,
    "percentage": 0.07,
    "return_percentage": 0.3,
    "max_return": 4000,
    "max_attempts": 3
}